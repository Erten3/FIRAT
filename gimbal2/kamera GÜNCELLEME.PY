import cv2
import serial
import time

# Load the Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the video capture and serial connection
vid = cv2.VideoCapture(0)
ArduinoSerial = serial.Serial('com3', 9600, timeout=0.1)
time.sleep(1)

# Define the desired width and height for resizing
desired_width = 640
desired_height = 480

while vid.isOpened():
    ret, frame = vid.read()
    if not ret:
        break

    # Resize the frame
    frame = cv2.resize(frame, (desired_width, desired_height))

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 6)
    konum = "N/A"  # Default value if no face is detected

    for x, y, w, h in faces:
        konum = 'X{0:d}Y{1:d}'.format((x + w // 2), (y + h // 2))
        ArduinoSerial.write(konum.encode('utf-8'))
        cv2.circle(frame, (x + w // 2, y + h // 2), 2, (255, 0, 0), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

    # Display additional information
    cv2.putText(frame, 'FURKAN ERTEN', (370, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, str(konum), (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.rectangle(frame, (desired_width // 2 - 30, desired_height // 2 - 30), (desired_width // 2 + 30, desired_height // 2 + 30), (255, 255, 255), 3)

    # Show the frame
    cv2.imshow('img', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release resources
vid.release()
cv2.destroyAllWindows()
q