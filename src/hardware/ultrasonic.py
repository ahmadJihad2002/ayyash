import RPi.GPIO as GPIO
import time

# Define GPIO pins for trigger and echo
trig_pin = 26
echo_pin = 21
maxTime = 0.04
# import RPi.GPIO as GPIO
# import time

# try:
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setwarnings(False)

#     TRIG = 26
#     ECHO = 21
#     maxTime = 0.04
#     GPIO.setup(TRIG,GPIO.OUT)
#     GPIO.setup(ECHO,GPIO.IN)

#     time_out=False
#     while True:

#         GPIO.output(TRIG,False)
#         time.sleep(0.01)
#         GPIO.output(TRIG,True)
#         time.sleep(0.00001)
#         GPIO.output(TRIG,False)

#         pulse_start = time.time()
#         timeout = pulse_start + maxTime
#         while GPIO.input(ECHO) == 0 and pulse_start < timeout:
#             pulse_start = time.time()

#         pulse_end = time.time()
#         timeout = pulse_end + maxTime
#         while GPIO.input(ECHO) == 1 and pulse_end < timeout:
#             pulse_end = time.time()

#         pulse_duration = pulse_end - pulse_start
#         distance = pulse_duration * 17000
#         distance = round(distance, 2)

#         print(distance)
# except:
#     GPIO.cleanup()

# Set up GPIO pins (BCM numbering)
GPIO.setmode(GPIO.BCM)
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

def get_distance():
    try:
        # Set trigger pin to LOW (default)
        GPIO.output(trig_pin, False)
        time.sleep(0.002)  # Wait for sensor to settle

        # Send a 10 microsecond high pulse to trigger
        GPIO.output(trig_pin, True)
        time.sleep(0.00001)  # Send pulse for 10 microseconds
        GPIO.output(trig_pin, False)

        # Start recording pulse duration (time for echo to return)
        pulse_start = time.time()
        while GPIO.input(echo_pin) == 0:
            pulse_start = time.time()  # Wait for echo pulse to start

        while GPIO.input(echo_pin) == 1:
            pulse_end = time.time()  # Wait for echo pulse to end

        # Calculate pulse duration (difference in start and end time)
        pulse_duration = pulse_end - pulse_start

        # Calculate distance (speed of sound * pulse duration / 2)
        distance = pulse_duration * 34300 / 2

        if distance == 0 or distance is None:
            return 1

        return distance

    except Exception as e:
        print(f"An error occurred in get_distance: {e}")
        return None

def is_about_to_fall() -> bool:
    try:
        distance = get_distance()
        print(f"Distance: {distance} cm")
        if distance is not None:
            if distance > 20:
                return True
            else:
                return False
    except Exception as e:
        print(f"An error occurred in is_about_to_fall: {e}")
        return False

if __name__ == "__main__":
    try:
        while True:
            if is_about_to_fall():
                print("I am falling!")
            else:
                print("All good.")
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
    except Exception as e:
        print(f"An error occurred in main loop: {e}")
        GPIO.cleanup()
