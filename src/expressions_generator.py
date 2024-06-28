from face_tracking import get_tracking_points

class Behavior :
    def __init__(self) :
        self._current_expression = {}

    

    def happy(self):
        self._current_expression= {"servo":[0.0,0.4],"sound": "ha.wav",
                                  "screen":"happy","dc_motors":None}
        
        return self._current_expression
    

    def start (self):

         self._current_expression= {"servo":[0.0,0.4],"sound": "wake1.wav",
                            "screen":"happy","dc_motors":["f-100-0.3","sr-40-0.3","sl-40-0.3","f-50-0.3","s-0-0"],}
     
         return self._current_expression

    def start (self):


        # self._current_expression= {"servo":[0.0,0.4],"sound": "wake1.wav",
        #                 "screen":"happy","dc_motors":["f-100-0.3","sr-40-0.3","sl-40-0.3","f-50-0.3","s-0-0"],}
        
        self._current_expression= {"servo":[0.0,0.4],"sound": "wake_up",
                        "screen":"happy","dc_motors":["sr-40-0.3","sl-40-0.3","s-0-0"],}
        


        
        return self._current_expression
        # return None
    def generate(self):
        
        return None
    
         

