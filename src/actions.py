import time

import pyttsx3
# from API_functionalities import get_joke, get_ip
from multiprocessing import Queue, Process, Value, Array, Manager, Event, get_context

from hardware import servo ,dc_motors
# ,screen
from hardware import ultrasonic
import os
import utills 
import random

from errors import AyyashError
# from hardware import  screen ,servo,ultrasonic,dc_motors
# from src.main import firebase
import API_functionalities


motors = dc_motors.Dc_motor()



def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 115)
    engine.setProperty('voice', "com.apple.eloquence.en-US.Grandma")

    print("ASSISTANT -> " + text)
    try:
        print("before saying")
        engine.say(text)
        print("after saying 1")
        engine.runAndWait()
        print("after saying 2")
        time.sleep(2)
        print("done")
    except (KeyboardInterrupt, RuntimeError) as e:
        print("Error occurred:", e)
        return
    

def query_indexing(query):
    try :
        if query is None:
            print("Query is None, cannot proceed with indexing")
            return
        elif "IP" and "address"  in query:
            print("getting ip address")
            text= API_functionalities.get_ip()
            speak(text)

        if "tired" in query:
            speak("you broke you broke haaaaaaaaa")
        else:


            None
        return
    
           
    except AyyashError as e:
        print (e) 


def queue_receiver(queue,current_action):
    try: 
        while queue.__sizeof__()!=0:
            # print(current)
            current_action.clear()
            current_action.update(queue.get())
            print("current_action")
            print(current_action)
            time.sleep(0.5)
    except AyyashError as e:
        print (e)

    

# checking the ultrasonic sensor
def ultrasonic_controller(event2,stop_event):
    try:
        while  not stop_event.is_set():
            if ultrasonic.is_about_to_fall():
                event2.set()

            else:
                event2.clear()

            time.sleep(0.1)
        return 
    except AyyashError as e:
        print(e)


# checking the servo sensor
def servo_controller(fall_event, wake_event,stop_event,current_action):
    try:
        while  not stop_event.is_set():
            if fall_event.is_set():
                servo.set_angle(0.1)
                time.sleep(0.5)
                servo.set_angle(-0.5)

                print("servo move down ")
            if wake_event.is_set():
                servo.set_angle(-0.5)
                time.sleep(0.3)
                servo.set_angle(-0.0)
                time.sleep(0.2)
                servo.set_angle(-0.5)  

                wake_event.clear()
                print("servo move wake ")
            else:
        
                if "servo" in  current_action:
                    for angel in current_action["servo"]:
                        servo.set_angle( angel)
                        time.sleep(0.3)

            time.sleep(0.1)

        return
    except AyyashError as e:
        print(e)


def screen_controller(fall_event, wake_event,stop_event,current_action):

    try: 
        while not stop_event.is_set():
            if fall_event.is_set():
                print("scary expression")

            if wake_event.is_set():
                print("wake_exresssion")

                # screen.show_behavior("wake4")
                print("wake_exresssion")
                time.sleep(2)

            else:
                # screen.show_behavior("normal")
                pass
            time.sleep(0.5)
        return 
    except KeyboardInterrupt:

        screen.kill_win()
    except AyyashError as e:
        print (e)

# checking the ultrasonic sensor
def motor_controller(fall_event, wake_event,stop_event,current_action):
    try: 
        global motors
        while not stop_event.is_set() :
            if fall_event.is_set():
                print("motor move back")
                motors.step_back(delay=0.5 ,speed=100)
                time.sleep(2)
            
            if wake_event.is_set():
                motors.step_left(speed=40,delay=0.2) 
                motors.step_right(speed=40,delay=0.2) 

                time.sleep(1)
                # print("motor move wake")

            else:
                if "dc_motors" in current_action:
                    print("queue motors")
                
                    for movments in current_action["dc_motors"]:
                        print("movments") 
                        print(movments)
                        motors.movment_decoder(movments)     
                        time.sleep(0.1) 
            time.sleep(0.1)
        return
    except AyyashError as e :
        print(e)


# checking the ultrasonic sensor
def sound_controller(fall_event, wake_event,stop_event,current_action):
    sounds={
    "scary":os.listdir(utills.root_path+"Data/sounds/"+"scary"),
    "cry":os.listdir(utills.root_path+"Data/sounds/"+"cry"),
    "alarm":os.listdir(utills.root_path+"Data/sounds/"+"alarm"),
    "happy":os.listdir(utills.root_path+"Data/sounds/"+"happy"),
    "ok":os.listdir(utills.root_path+"Data/sounds/"+"ok"),
    "wake_up":os.listdir(utills.root_path+"Data/sounds/"+"wake_up"),
    }

    try:
        while  not stop_event.is_set():
            try :
                if fall_event.is_set():
                    os.system("aplay"+" "+ os.path.join(utills.root_path, "Data/sounds","scary",sounds['scary'][random.randint(0,len( sounds["scary"] ))]))

                    # os.system("aplay" +" "+ utills.root_path+"Data/sounds/"+"scary/"+ sounds["scary"][ random.randint(0,len( sounds["scary"]))])
                    time.sleep(1)
                    print("scary sound")

                if wake_event.is_set():
                    os.system("aplay"+" "+ os.path.join(utills.root_path, "Data/sounds","wake_up",sounds['wake_up'][random.randint(0,len( sounds["wake_up"] ))]))

                    # os.system("aplay" +" "+ utills.root_path+"Data/sounds/"+"wake_up/"+  sounds["wake_up"][random.randint(0,len( sounds["wake_up"] ))])

                    print("wake_sound")
                    time.sleep(2)

                else:
                    if "sound" in current_action :
                        # os.system("aplay"+" "+ os.path.join(utills.root_path, "Data/sounds", current_action["sound"], random.choice(sounds[current_action["sound"]])))
                        os.system("aplay"+" "+ os.path.join(utills.root_path, "Data/sounds",current_action["sound"],random.choice(sounds[current_action["sound"]])))

    
                        print("wake_sound")
                        print("random expression ")
                        time.sleep(0.5)
                time.sleep(0.1)
            except  Exception as e:
                print(e)
                
        return
    except AyyashError as e:
        print(e)
  