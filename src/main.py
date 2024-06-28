import time
from multiprocessing import Event, Process,Queue,Manager
import config
import actions
import wake_word_detection
from  expressions_generator import Behavior 
# import firebase_calls
import speech_recognizer as sr


def chat(text):
    # parameters
    max_len = 20
    while True:
        return ""

ultrasonic_process = None
servo_process = None
sound_process = None
motor_process = None
screen_process = None
wake_word_process = None
controller_process = None
queue_manager_process=None
queue_receiver_process=None

def record():
   text = sr.recognize.record(period=7)
   return text

def listen_audio(wake_event):
    response = record()
    print("response")
    print(response)


    actions.query_indexing(response)
    time.sleep(1)
    wake_event.clear()

def listen_wake_word(wake_event, stop_event):
    wake_word = wake_word_detection.WakeWord()
    while not stop_event.is_set():
        if wake_word.listing():
            print('Wake word detected')
            wake_event.set()
            listen_audio(wake_event)
            time.sleep(1)

            # Re-initiate the wake-word detection module
            wake_word.__init__()
            print("Reinitialize the wake word engine")
        
        print("Inside the wake word engine loop")
        time.sleep(1)

def queue_manager(q):
    behavior= Behavior()
    # exprisions generator 
    while True :
        if behavior.start() != None: 
    
            q.put(  behavior.start())
            time.sleep(5)
        time.sleep(1)



def expression_controller(wake_event, stop_event):
    global queue_manager_process
    global queue_receiver_process
    global ultrasonic_process
    global servo_process
    global sound_process
    global motor_process
    global screen_process
 
    with Manager() as manager:
        q= Queue()
        fall_event = Event()

        current_action = manager.dict()

        queue_manager_process = Process(target=queue_manager, args=(q,))
        queue_receiver_process = Process(target=actions.queue_receiver, args=(q,current_action))

        ultrasonic_process = Process(target=actions.ultrasonic_controller, args=(fall_event, stop_event))
        servo_process = Process(target=actions.servo_controller, args=(fall_event, wake_event, stop_event,current_action))
        sound_process = Process(target=actions.sound_controller, args=(fall_event, wake_event, stop_event,current_action))
        motor_process = Process(target=actions.motor_controller, args=(fall_event, wake_event, stop_event,current_action))
        screen_process = Process(target=actions.screen_controller, args=(fall_event, wake_event, stop_event,current_action))

        queue_manager_process.start()
        queue_receiver_process.start()

        ultrasonic_process.start()
        servo_process.start()
        sound_process.start()
        motor_process.start()
        screen_process.start()

        queue_manager_process.join()
        queue_receiver_process.join()

        motor_process.join()
        sound_process.join()
        servo_process.join()
        ultrasonic_process.join()
        screen_process.join()
    
if __name__ == "__main__":


    wake_event = Event()
    stop_event = Event()
    
    try:
        wake_word_process = Process(target=listen_wake_word, args=(wake_event, stop_event))
        controller_process = Process(target=expression_controller, args=(wake_event, stop_event))

        wake_word_process.start()
        controller_process.start()

        wake_word_process.join()
        controller_process.join()
     
    except KeyboardInterrupt:
        print("Terminating due to KeyboardInterrupt")
        stop_event.set()
        time.sleep(1)
   
    finally:
        processes = [ultrasonic_process, servo_process, sound_process, motor_process,
                      screen_process, wake_word_process, controller_process,queue_manager_process, queue_receiver_process]
        for p in processes:
            if p is not None:
                p.terminate()
                time.sleep(0.001)
       
        print("All processes terminated")



 
   