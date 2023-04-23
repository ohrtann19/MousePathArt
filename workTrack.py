

import keyboard

mouse_events = []


# mouse.hook(mouse_events.append)
# keyboard.start_recording()       #Starting the recording
import pygame
import pyautogui
import json
import time
import win32gui
import win32process
import psutil

pyautogui.PAUSE = 0.1
pyautogui.MINIMUM_DURATION = 0.1
pyautogui.MINIMUM_SLEEP = 0.1
pyautogui.FAILSAFE = False

# Set the color of the mouse trail
trail_color = (255, 255, 255)
process_names = set()

#track movements
while True:
    x, y = pyautogui.position()
    
    # Get the handle of the foreground window
    foreground_window_handle = win32gui.GetForegroundWindow()

    # Get the process ID of the application that created the foreground window
    if foreground_window_handle != 0:
        foreground_window_pid = win32process.GetWindowThreadProcessId(foreground_window_handle)[1]
        
        # Get the name of the executable file of the process
        foreground_process_name = psutil.Process(foreground_window_pid).name()
        process_names.add(foreground_process_name)
        # Set the color of the mouse trail based on the name of the foreground process
        # {'chrome.exe', 'explorer.exe', 'msedge.exe', 'Code.exe', 'cmd.exe'}
        # if foreground_process_name == "cmd.exe":
        #     trail_color = (255, 255, 255) # White for cmd
        # elif foreground_process_name == "Code.exe":
        #     trail_color = (255, 0, 0) # Red for notepad?
        # else:
        #     trail_color = (0, 255, 0) # Green for other applications
    position_str = [x,y, trail_color]
    mouse_events.append(position_str)

    if keyboard.is_pressed('esc'):
        print("Exiting the loop.")

        with open('mouse_events.json', 'w') as f:
            json.dump(mouse_events, f)
        break
    time.sleep(0.0001)

# draw path

actions = []
with open('mouse_events.json', 'r') as f:
    actions = json.load(f)

# Initialize Pygame
pygame.init()


# Set the thickness of the mouse trail
trail_thickness = 5

# Set the maximum length of the trail
max_trail_length = 100

# Set the display mode to full screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Fill the screen with black color
screen.fill((0, 0, 0))

# Update the screen
pygame.display.update()

game_pos = []
prev_pos = None
ctr = 0
prev_color = None
for action in actions:

    trail_color = action[2]

    pyautogui.moveTo(action[0], action[1])
    ctr+= 1
    actions.remove(action)

    mouse_x, mouse_y = action[0], action[1]
    screen_rect = screen.get_bounding_rect()
    if mouse_x >= screen_rect.left and mouse_x < screen_rect.right and mouse_y >= screen_rect.top and mouse_y < screen_rect.bottom:
        current_pos = (mouse_x, mouse_y)
        if prev_pos is None or abs(current_pos[0]-prev_pos[0]) >= 5 or abs(current_pos[1]-prev_pos[1]) >= 5:
            game_pos.append((action[0], action[1]))
            if len(game_pos) > 3: # max_trail_length #or (prev_color != trail_color):
                game_pos.pop(0)
            
            # Draw the trail on the screen
            if len(game_pos) >= 2:
                pygame.draw.lines(screen, trail_color, False, game_pos, trail_thickness)
                pygame.display.update()
                time.sleep(0.005)
    prev_color = trail_color
# Quit Pygame

# Take a screenshot of the current screen
screenshot = pygame.surfarray.array3d(pygame.display.get_surface())

# Save the screenshot to a file
pygame.image.save(pygame.surfarray.make_surface(screenshot), "finish_saving_to_github.png")
pygame.quit()