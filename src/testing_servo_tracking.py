import face_tracking
from hardware import servo,dc_motors
from multiprocessing import Queue, Process, Array, Event 
import utills
import time

dc=dc_motors.Dc_motor()
def assign_face_cordanaite(face_detection_event,arr,stop_event):
    while  not (stop_event.is_set()) :
        x,y,w=face_tracking.get_tracking_points()
     
        if x is not None:
            face_detection_event.set()
            arr[0]= x
            arr[1]=y
            arr[2]=w
    
        else: 
            face_detection_event.clear()
        time.sleep(0.5)

 
    
        


def servo_controller(face_detection_event,arr,stop_event, ):
    while not stop_event.is_set():
   
        if face_detection_event.is_set():
            print("face_detected")

            tolerance=utills.map_range(arr[2],50,300,60,150)
            tolerance=  abs(tolerance-150 + 60)
            print("tolerance {} ".format(tolerance))
            print(arr[1])
            if not utills.is_close(arr[1],200,tolerance):

                

                angle = utills.map_range(arr[1],5,300,-1.0,1.0)
                angle=max(min(angle,1.0), -1.0)
         
                print("angle"+str(angle))
                servo.set_angle(angle)
    

           
        time.sleep(2)
        

         
 

def motors_tracking(face_detection_event,arr,stop_event):
    global dc
    while not stop_event.is_set():
 
        if face_detection_event.is_set():
            
            if utills.is_close(arr[0],250,50):
                if arr[0] < 200:
                    dc.step_left(speed=utills.map_range(arr[0],0,450,15,50),delay=utills.map_range(arr[0],0,450,0.2,0.5))
                else:
                    dc.step_right(speed=utills.map_range(arr[0],0,450,15,50),delay=utills.map_range(arr[0],0,450,0.2,0.5))
        
        time.sleep(1)
        
    

    

     


if __name__=="__main__":
    try:

        while True:

            x,y,w=face_tracking.get_tracking_points()
      
            if y is not None:

                if not utills.is_close(x,200,50):

                    if x<200:
                       dc.step_right(20,delay=0.3)
                    else:
                        dc.step_left(20,delay=0.3)
 

                # if  not utills.is_close(y,200,50):
                #     current_angle=servo.get_angle()
                #     print(current_angle)

                #     if  y<130:
                #         current_angle-=0.1  

                #     else:
                #         current_angle+=0.1
                         
                #     servo.set_angle(max(min(current_angle ,1.0),-1.0))
            time.sleep(0.05)
        
        




            
                
        
            









        # arr=Array('d',3)
        # face_detection_event = Event()
        # stop_event=Event()
        # tracking_process = Process(target=assign_face_cordanaite, args=(face_detection_event,arr,stop_event))
        # servo_process = Process(target=servo_controller, args=(face_detection_event,arr,stop_event))
        # motors_process = Process(target=motors_tracking, args=(face_detection_event,arr,stop_event))

       
        # tracking_process.start()
        # servo_process.start()
        # motors_process.start()

        # tracking_process.join()
        # servo_process.join()
        # motors_process.join()
 
    except KeyboardInterrupt :
        servo.stop()
        face_tracking.kill_all()
        # stop_event.set()
        # tracking_process.terminate()
        # servo_process.terminate()
 
    
  
            
        
   