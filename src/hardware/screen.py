import logging
import os
import time
import turtle
import sys
import copy
# print("current working directory")
# print(os.getcwd())
# sys.path.append('cd ..')
# print("current working directory")
# print(os.getcwd())
import random 
root_path="/home/admin/Documents/ayyash/"

screenHeight = 1.0
screenWidth = 1.0

wn = turtle.Screen()
wn.setup(screenWidth, screenHeight)
wn.title("ayyash")
wn.bgcolor("black")
wn.tracer(0)
wn.delay(0)

turtle.penup()

# reg all frames into turtle before displaying it
path = root_path +"Data/behavior/"
behaviors = os.listdir(path)
print(behaviors)

faces= {}
expressions_faces={}
for behavior in behaviors:
    if behavior != ".DS_Store":
        expressions=os.listdir(os.path.join(path,behavior))
        if expressions != ".DS_Store":  
                filtered_list= []
                print(expressions)
                for expression in expressions:
                    if expression != ".DS_Store": 
                        print(expression)
                        frames = os.listdir(os.path.join(path,behavior,expression))
                        sorted_frames=sorted(frames, key=lambda x: int(x.split('.')[0]))
                        for frame in sorted_frames:
                            print(frame) 
                            wn.register_shape(os.path.join(path,behavior, expression, frame))
                        
                        #putting in buffring array 
                        faces.update({behavior+'/'+expression:sorted_frames})
                        filtered_list.append(expression)
                expressions_faces.update({behavior:filtered_list})                   



def kill_win():
    wn.kill_win()

def show(expression):
    frames = os.listdir(path + expression)
    sorted_frame = sorted(frames, key=lambda x: int(x.split('.')[0]))
    print(sorted_frame)
    wn.delay(0)
    while True:
        for frame in sorted_frame:
            turtle.shape(os.path.join(path, expression, frame))
            wn.update()
            # time.sleep(0.001)
        
        time.sleep(0.5)
        # image = Image.open('Blink-0/' + str(i) + '.png')

        # win.blit(image, (0, 0))
        # pygame.display.update()

def show_behavior(behavior):
    length =len(expressions_faces[behavior])
    buffer_exprissons=copy.deepcopy(expressions_faces[behavior])
    # buffer_exprissons=set(expressions_faces[behavior])
    print (length)

    # refresh_speed = random.uniform(0.007,0.0071)
    refresh_speed =  0.007

    while True:
        if len(buffer_exprissons)== 0 :
             buffer_exprissons=copy.deepcopy(expressions_faces[behavior])
        expression= random.choice(buffer_exprissons)
        buffer_exprissons.remove(expression)
        
        for frame in  faces[behavior+'/'+expression]:
            print ("displaying")
            print (expression)
            turtle.shape(os.path.join(path, behavior,expression, frame))
            wn.update()
            time.sleep(refresh_speed)
        time.sleep(0.5)
        # refresh_speed = random.uniform(0.007,0.0071)
    
        


if __name__ == "__main__":
    # show("Wake UP")
    show_behavior("blink")
