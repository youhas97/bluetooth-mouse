import pygame
import asyncio
from bleak import BleakClient

# BLE Device address
address = "28:26:a1:5b:89:0d"

# Service id for BLE Device
service_id = "0000ae01-0000-1000-8000-00805f9b34fb"

# Initialize pygame
pygame.init()

# Initialize the joystick
pygame.joystick.init()

# Check for available joysticks
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("No joystick detected.")
    pygame.quit()
    exit()

# Connect to the first joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

print("Initialized joystick:", joystick.get_name())

tick = 0
# Main loop
while True:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of the joystick axes
    axes = [joystick.get_axis(i) for i in range(joystick.get_numaxes())]

    # Get the state of the joystick buttons
    buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]

    if tick%50000 == 0:
        # Print the state of axes and buttons
        print("Axes:", axes)
        #print("Buttons:", buttons)
 

        # Get the state of the joystick axes
        axes = [round(joystick.get_axis(i), 2) for i in range(joystick.get_numaxes())]

        # Interpret joystick direction
        x_axis = axes[0]
        y_axis = axes[1]
        direction = ""

        if y_axis < -0.8:
            direction += "Up"
        elif y_axis > 0.8:
            direction += "Down"

        if x_axis < -0.8:
            direction += "Left"
        elif x_axis > 0.8:
            direction += "Right"

        if direction:
            print("Joystick Direction:", direction)
        else:
            print("idle")

    tick += 1

    # Information to GPT: Add logic here for the joystick logic. print which direction the joystick is pointed.

# Quit pygame
pygame.quit()
        