import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

# GPIO ayarları
servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Servo PWM ayarları
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz PWM frekansı
pwm.start(7.5)  # Orta pozisyon (7.5% duty cycle)

# Servo motor pozisyon fonksiyonu
def setServoAngle(angle):
    duty = angle / 18 + 2.5
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

# Kamera ayarları
cap = cv2.VideoCapture(0)
cap.set(3, 480)  # Genişlik
cap.set(4, 320)  # Yükseklik

_, frame = cap.read()
rows, cols, _ = frame.shape

x_medium = int(cols / 2)
center = int(cols / 2)
position = 90  # Başlangıç pozisyonu

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Kırmızı renk
    low_red = np.array([161, 155, 84])
    high_red = np.array([179, 255, 255])
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        x_medium = int((x + x + w) / 2)
        break
    
    cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)
    
    # Servo motoru hareket ettirme
    if x_medium < center - 30:
        position += 1
        if position > 180:
            position = 180
    elif x_medium > center + 30:
        position -= 1
        if position < 0:
            position = 0
    setServoAngle(position)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    
    if key == 27:  # ESC tuşuna basıldığında çık
        break
    
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
