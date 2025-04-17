import time
import pygame
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio
from adafruit_motor import servo

# Initialize I2C and PCA9685
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50

min_pulse = 560  # in microseconds
max_pulse = 2440  # in microseconds

# Define mechanical constraints
HIP_MIN = 23
HIP_MAX = 197
KNEE_MIN = 21
KNEE_MAX = 118

# Create servo objects on channels 0 and 1
servo1 = servo.Servo(pca.channels[0], min_pulse=min_pulse, max_pulse=max_pulse, actuation_range=270)
servo2 = servo.Servo(pca.channels[1], min_pulse=min_pulse, max_pulse=max_pulse, actuation_range=270)

# Set both servos to 20 degrees at start
servo1_angle = 90
servo2_angle = 105
servo1.angle = servo1_angle
servo2.angle = servo2_angle
time.sleep(0.5)  # Small delay to allow servos to move

# Initialize pygame for controller input
pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Using controller: {joystick.get_name()}")

deadzone = 0.1
increment_speed = 3  # Adjust for how fast you want the angle to change

try:
    while True:
        pygame.event.pump()

        left_y = -joystick.get_axis(1)  # Invert to make up = positive
        right_y = -joystick.get_axis(4)

        # Only update angle if outside deadzone
        if abs(left_y) > deadzone:
            servo1_angle += left_y * increment_speed
        if abs(right_y) > deadzone:
            servo2_angle += right_y * increment_speed

        # Clamp angles
        servo1_angle = max(HIP_MIN, min(HIP_MAX, servo1_angle))
        servo2_angle = max(KNEE_MIN, min(KNEE_MAX, servo2_angle))

        # Update servo angles
        servo1.angle = servo1_angle
        servo2.angle = servo2_angle

        print(f"Servo 1: {int(servo1_angle)}°   |   Servo 2: {int(servo2_angle)}°")
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Exiting program.")
finally:
    pca.deinit()
    pygame.quit()

