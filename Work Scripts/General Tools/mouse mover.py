import pyautogui
import time
import random

# Define the range for mouse movement (in pixels)
# You can adjust these values to control the extent of movement
x_range = 10  # Horizontal movement range
y_range = 10  # Vertical movement range

# Define the time interval between mouse movements (in seconds)
interval = 5  # Adjust this value for the desired time interval

try:
    while True:
        # Generate random offsets for mouse movement within the defined range
        x_offset = random.randint(-x_range, x_range)
        y_offset = random.randint(-y_range, y_range)

        # Get the current mouse position
        current_x, current_y = pyautogui.position()

        # Calculate the new mouse position
        new_x = current_x + x_offset
        new_y = current_y + y_offset

        # Move the mouse to the new position
        pyautogui.moveTo(new_x, new_y, duration=0.25)

        # Wait for the specified interval before the next movement
        time.sleep(interval)

except KeyboardInterrupt:
    print("Mouse movement script terminated.")
