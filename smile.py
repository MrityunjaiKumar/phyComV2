import cv2
import pyttsx3
from pyfirmata import Arduino, util
import time

# Setup Firmata and Arduino connection
board = Arduino('COM7')  # Replace with the correct port for your Arduino
it = util.Iterator(board)
it.start()

# Pin Setup for LED and Buzzer
led_pin = board.get_pin('d:6:o')  # LED pin (digital pin 2)
buzzer_pin = board.get_pin('d:11:o')  # Buzzer pin (digital pin 3)

# Load pre-trained classifiers for face and smile detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to speak out a message
def speak(message):
    engine.say(message)
    engine.runAndWait()

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame from the webcam
    ret, frame = cap.read()
    
    # Convert the image to grayscale (required for face and smile detection)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Region of interest (ROI) for smile detection
        roi_gray = gray[y:y + h, x:x + w]
        
        # Detect smiles within the face ROI
        smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
        
        if len(smiles) > 0:
            # Draw a rectangle around each smile
            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(frame, (x + sx, y + sy), (x + sx + sw, y + sy + sh), (0, 255, 0), 2)

            # Feedback for smile detected
            speak("You are smiling!")
            cv2.putText(frame, "Smile Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            
            # Turn on the LED on Arduino when a smile is detected
            led_pin.write(1)  # Turn on LED
            buzzer_pin.write(0)  # Ensure Buzzer is off when smile is detected
            
        else:
            # Feedback for no smile detected
            speak("No smile detected.")
            cv2.putText(frame, "No Smile Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            
            # Turn off the LED and turn on the buzzer when no smile is detected
            led_pin.write(0)  # Turn off LED
            buzzer_pin.write(1)  # Turn on Buzzer

    # Display the resulting frame
    cv2.imshow('Smile Detection with Arduino Feedback', frame)
    
    # Break the loop if the user presses the 'ESC' key
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()