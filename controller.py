import pygame
from bluepy import btle

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

# MAC address of the BLE device you want to connect to
DEVICE_MAC_ADDRESS = "28:26:a1:5b:89:0d"

# UUID of the characteristic you want to read from the BLE device
SERVICE_UUID = "0000ae00-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "0000ae01-0000-1000-8000-00805f9b34fb"

# Commands
cmd_idle = bytes.fromhex("5a00080008a5")
cmd_fwd = bytes.fromhex("5a01080009a5")
cmd_back = bytes.fromhex("5a0208000aa5")
cmd_right = bytes.fromhex("5a08080010a5")
cmd_left = bytes.fromhex("5a0408000ca5")
cmd_spd = bytes.fromhex("")

# Used for command
direction = "idle"

# Define your own delegate class
class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        # Handle notification data here
        print("Received notification:", data)


def main():
    # Connect to the BLE device
    device = btle.Peripheral(DEVICE_MAC_ADDRESS)
    
    service = device.getServiceByUUID(btle.UUID(SERVICE_UUID))
    characteristic = service.getCharacteristics(btle.UUID(CHARACTERISTIC_UUID))[0]

    # Set up notification handler
    device.setDelegate(MyDelegate())
    

    init_cmd = bytes.fromhex("5af38b1d7f768919a5")
    characteristic.write(init_cmd)

    # Wait for notifications with a timeout of 3 seconds
    if device.waitForNotifications(3.0):
        print("Received the expected notification.")
    else:
        print("Timed out waiting for notification.")

    try:
        
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
            #buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())
            
            if tick%5000 == 0:
                # Print the state of axes and buttons
                print("Axes:", axes)
                #print("Buttons:", buttons)
        

                # Get the state of the joystick axes
                axes = [round(joystick.get_axis(i), 2) for i in range(joystick.get_numaxes())]

                # Interpret joystick direction
                left_x_axis = axes[0]
                right_x_axis = axes[2]
                y_axis = axes[1]

                direction = "idle"

                if y_axis < -0.8:
                    direction = "fwd"
                elif y_axis > 0.8:
                    direction = "back"

                if left_x_axis < -0.8 or right_x_axis < -0.8:
                    direction = "left"
                elif left_x_axis > 0.8 or right_x_axis > 0.8:
                    direction = "right"

                if direction:
                    print("Moving", direction)
                else:
                    print("Not moving")

                command = convert_input_to_command(direction)
                # Write to the characteristic
                characteristic.write(command, withResponse=False)

            tick += 1

            #user_input = input("Enter a command to send to BLE device 'idle', 'fwd', 'back', 'right', 'left' (or type 'exit' to quit)\n")
            #if user_input.lower() == 'exit':
            #    print("Exiting the program...")
            #    break
            #else:
            #print("Sending '" + direction + "' command to device.")
            

    finally:
        # Disconnect from the BLE device
        device.disconnect()

def convert_input_to_command(user_input):
    # Map user input to corresponding command
    if user_input.lower() == 'idle':
        return cmd_idle
    elif user_input.lower() == 'fwd':
        return cmd_fwd
    elif user_input.lower() == 'back':
        return cmd_back
    elif user_input.lower() == 'right':
        return cmd_right
    elif user_input.lower() == 'left':
        return cmd_left
    elif user_input.lower() == 'spd':
        return cmd_spd
    else:
        print("invalid input")
        # Assuming user input is a hex string
        return cmd_idle
    
if __name__ == "__main__":
    main()

