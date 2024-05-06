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


def main():
    # Connect to the BLE device
    device = btle.Peripheral(DEVICE_MAC_ADDRESS)
    
    service = device.getServiceByUUID(btle.UUID(SERVICE_UUID))
    characteristic = service.getCharacteristics(btle.UUID(CHARACTERISTIC_UUID))[0]

    init_cmd = bytes.fromhex("5af38b1d7f768919a5")
    characteristic.write(init_cmd)

    try:
        tick = 0
        # Main loop
        while True:
            if tick%50000 == 0:
                # user_input = input("Enter a command to send to BLE device 'idle', 'fwd', 'back', 'right', 'left' (or type 'exit' to quit)\n")
                # if user_input.lower() == 'exit':
                #     print("Exiting the program...")
                #     break
                # else:
                #     command = convert_input_to_command(user_input)
                #     # Write to the characteristic
                #     characteristic.write(command, withResponse=False)
                #     print("Sending '" + user_input + "' command to device.")

                    
                characteristic.write(cmd_fwd, withResponse=False)
            tick += 1
            

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

