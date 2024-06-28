
import time
import cv2

"""
x range 0"right" --- 450"left"

w range 300 -50

"""
# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize video capture from webcam (you can also use a video file)
cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH,  620)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

def get_tracking_points():
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        return None, None,None

    # Convert frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(10, 10))
    print(faces)
    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
 
         
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        print("Face detected at coordinates (x={}, y={},w={})".format(x, y,w))
        # print('Number of faces detected:', len(faces))

    # Display the resulting frame
    # cv2.imshow('Video', frame)


    if len(faces) != 0:
        face_center_x=faces[0][0]+faces[0][1] // 2
        face_center_y=faces[0][1]+faces[0][3] // 2
 

        return  faces[0][0], faces[0][1], faces[0][2]
    
    else:
        return None, None, None

def kill_all():
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        while True:
            get_tracking_points()
            # Exit loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        kill_all()
 