import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

# Initialize I2C bus and PCA9685 module
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c)
pca.frequency = 50

min_pulse = 560  # in microseconds
max_pulse = 2440  # in microseconds


# Create servo objects on channels 0 and 1 with a 270-degree range
servo1 = servo.Servo(pca.channels[0], actuation_range=270, min_pulse=min_pulse, max_pulse=max_pulse)
servo2 = servo.Servo(pca.channels[1], actuation_range=270, min_pulse=min_pulse, max_pulse=max_pulse)

try:
    while True:
        user_input = input("Enter angles for Servo1 and Servo2 (e.g., 50,180) or 'q' to quit: ")
        if user_input.lower() == 'q':
            print("Exiting program.")
            break
        try:
            angle1_str, angle2_str = user_input.split(',')
            angle1 = float(angle1_str.strip())
            angle2 = float(angle2_str.strip())
            if 0 <= angle1 <= 270 and 0 <= angle2 <= 270:
                servo1.angle = angle1
                servo2.angle = angle2
                print(f"Moved Servo1 to {angle1}° and Servo2 to {angle2}°.")
            else:
                print("Please enter angles between 0 and 270.")
        except ValueError:
            print("Invalid input format. Please enter two numbers separated by a comma.")
except KeyboardInterrupt:
    print("\nProgram interrupted by user.")
finally:
    pca.deinit()
