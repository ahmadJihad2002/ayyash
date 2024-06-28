import subprocess
subprocess.run(["sudo", "pigpiod"])

from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
import time
factory = PiGPIOFactory()

current_angle=0.0

servo = Servo(12,initial_value=current_angle ,min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)


def set_angle(value):
    global current_angle
    servo.value=value
    current_angle=value

def get_angle():
    global current_angle
    return current_angle

# Function to move servo to a specific angle quickly
def move_servo_to_angle(servo, angle):
    # Convert angle to a value between -1 (min) and 1 (max)
    servo_value = (angle / 90) - 1
    servo.value = servo_value

def stop():
     servo.detach() 
    

if __name__ == "__main__":
    try:
        while True:
            print("Moving to 0 degrees (min position)")
            move_servo_to_angle(servo, 0)  # Move to 0 degrees
            time.sleep(0.5)  # Short delay to observe movement

            print("Moving to 90 degrees (mid position)")
            move_servo_to_angle(servo, 90)  # Move to 90 degrees
            time.sleep(0.5)  # Short delay to observe movement

            print("Moving to 180 degrees (max position)")
            move_servo_to_angle(servo, 180)  # Move to 180 degrees
            time.sleep(0.5)  
    except KeyboardInterrupt:
        servo.detach()  # Release the servo
        print("Program terminated by user")
        sleep(0.001)
 