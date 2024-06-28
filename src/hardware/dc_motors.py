
import RPi.GPIO as GPIO
import time
import random 
#
# # Set GPIO mode (BCM or BOARD)
GPIO.setmode(GPIO.BCM)
#
# # Define GPIO pins for motor control
# # Motor 1
IN1_PIN = 17  # Input 1 of Motor 1
IN2_PIN = 25  # Input 2 of Motor 1
EN1_PIN = 27  # Enable pin of Motor 1
# # Motor 2
IN3_PIN = 22  # Input 1 of Motor 2
IN4_PIN = 23  # Input 2 of Motor 2
EN2_PIN = 24  # Enable pin of Motor 2

# # Set up GPIO pins for motor control
GPIO.setup(IN1_PIN, GPIO.OUT)
GPIO.setup(IN2_PIN, GPIO.OUT)
GPIO.setup(EN1_PIN, GPIO.OUT)
GPIO.setup(IN3_PIN, GPIO.OUT)
GPIO.setup(IN4_PIN, GPIO.OUT)
GPIO.setup(EN2_PIN, GPIO.OUT)

# # Set up PWM for motor speed control
motor1_pwm = GPIO.PWM(EN1_PIN, 100)  # Frequency = 100 Hz
motor2_pwm = GPIO.PWM(EN2_PIN, 100)
#
# # Start PWM with 0% duty cycle (motors off)
motor1_pwm.start(0)
motor2_pwm.start(0)


class Dc_motor():

    def __init__(self):
        self.duty_cycle = 50
        motor1_pwm.start( self.duty_cycle)
        motor2_pwm.start( self.duty_cycle)
        GPIO.output(IN1_PIN, GPIO.LOW)
        GPIO.output(IN2_PIN, GPIO.LOW)
        GPIO.output(IN3_PIN, GPIO.LOW)
        GPIO.output(IN4_PIN, GPIO.LOW)
       
 
    def set_speed(self,speed):
        motor1_pwm.start( min(max(speed,0),100))
        motor2_pwm.start( min(max(speed,0),100)) 
    
  
    def step_left(self,speed,delay=1):
        self.set_speed(speed)
        GPIO.output(IN1_PIN, GPIO.LOW)
        GPIO.output(IN2_PIN, GPIO.HIGH)
        GPIO.output(IN3_PIN, GPIO.HIGH)
        GPIO.output(IN4_PIN, GPIO.LOW)
        time.sleep(delay)
        
        self.stop()

    def step_right(self,speed,delay=0.5):
        self.set_speed(speed)
        GPIO.output(IN1_PIN, GPIO.HIGH)
        GPIO.output(IN2_PIN, GPIO.LOW)
        GPIO.output(IN3_PIN, GPIO.LOW)
        GPIO.output(IN4_PIN, GPIO.HIGH)
        time.sleep(delay)
    
        self.stop()
    def step_back(self,speed,delay=0.5):
        self.set_speed(speed)
        GPIO.output(IN1_PIN, GPIO.HIGH)
        GPIO.output(IN2_PIN, GPIO.LOW)
        GPIO.output(IN3_PIN, GPIO.HIGH)
        GPIO.output(IN4_PIN, GPIO.LOW)
        time.sleep(delay)
        self.stop()         

    def move_forward(self,speed,delay=1):
        print("moving forawarf")
        self.set_speed(speed)
        GPIO.output(IN1_PIN, GPIO.LOW)
        GPIO.output(IN2_PIN, GPIO.HIGH)
        GPIO.output(IN3_PIN, GPIO.LOW)
        GPIO.output(IN4_PIN, GPIO.HIGH)
        time.sleep(delay)
        print("done")
    
        self.stop()
 
    def move_backward(self,speed,delay=1):
        self.set_speed(speed)
        GPIO.output(IN1_PIN, GPIO.HIGH)
        GPIO.output(IN2_PIN, GPIO.LOW)
        GPIO.output(IN3_PIN, GPIO.HIGH)
        GPIO.output(IN4_PIN, GPIO.LOW)
        time.sleep(delay)
    
        self.stop()
 
    def movment_decoder(self,current_movment):
        data = current_movment.split('-')
        
        direction =data[0]
        speed_value =int(data[1])
        delay_value=float(data[2])
 
        
        if direction=="f":
            
            self.move_forward(speed=speed_value,delay=delay_value)
            print("moving forward")
        elif direction=="b":
           
             self.move_backward(speed=speed_value,delay=delay_value)
             print("moving backward")


            
        elif direction=="sl":
           
             self.step_left(speed=speed_value,delay=delay_value)

        elif direction=="sr":
           
             self.step_right(speed=speed_value,delay=delay_value)
     

        elif direction=="s":
           
             self.stop ()
        else:
           raise TypeError("wronge data decoding in movment_decoder method")
 
    def stop(self):
        GPIO.output(IN1_PIN, GPIO.LOW)
        GPIO.output(IN2_PIN, GPIO.LOW)
        GPIO.output(IN3_PIN, GPIO.LOW)
        GPIO.output(IN4_PIN, GPIO.LOW)


 

if __name__ == "__main__":
    # hall_readings()

    dc =Dc_motor()

    try:
        while True:
            dc.move_forward(speed=100,delay=1)
            time.sleep(1)
            dc.move_backward(speed=100,delay=1)
            time.sleep(1)
            dc.step_right(speed=100,delay=2)
            time.sleep(1)
            dc.move_forward(speed=100)
            time.sleep(1)

            dc.step_left(speed=100,delay=1)

            time.sleep(1)
            dc.stop()
            # stop()  # Stop motors
            # time.sleep(1)  # Pause for 1 second
 
    except KeyboardInterrupt:
        # Clean up GPIO on exit
        dc.stop()
        # motor1_pwm.stop()
        # motor2_pwm.stop()
        GPIO.cleanup()
 