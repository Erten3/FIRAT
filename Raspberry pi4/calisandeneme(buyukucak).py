from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, Battery, LocationGlobal, Attitude
from pymavlink import mavutil
import socket
from math import sin, cos, sqrt, atan2, radians
import math
import time
import argparse
import cv2
import numpy as np
import imutils
from threading import Thread
import socket
from struct import pack

class WebcamVideoStream:
    def __init__(self, src=0, name="WebcamVideoStream"):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the thread name
        self.name = name

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True

def imageprcssng():
    cx = 0
    f = time.time
    my_image = stream.read()

    my_image = cv2.resize(my_image, (400, 400))
    my_image = my_image[1:400, 0:400]
    #out.write(my_image)
    #cv2.imshow("ham my_image", my_image)
    hsv = cv2.cvtColor(my_image, cv2.COLOR_BGR2HSV)
    my_mask = cv2.inRange(hsv, minimumm, maximumm)
    my_mask = cv2.medianBlur(my_mask, 15)
    kernel = np.ones((10, 10), np.uint8)
    dilation = cv2.dilate(my_mask, kernel, iterations=4)
    cnts = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        cv2.drawContours(my_image, [c], -1, (0, 255, 0), 2)
        x, y, w, h = cv2.boundingRect(c)
        M = cv2.moments(c)
        if M["m00"] == 0:
            M["m00"] = 1
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        frame = cv2.circle(my_image, (cx, cy), 5, (0, 255, 0), -1)

        print("cx:", cx)
        #cv2.imwrite("my_image.jpg", my_image)

        s = time.time()
        #cv2.imwrite("framemy_image.jpg", frame)
        cv2.waitKey(0)

    return cx

a = 0
minimumm = np.array([158, 103, 55])
maximumm = np.array([180, 255, 255])


stream = WebcamVideoStream(src=0).start()


'''
fnames = [
    'my_image.jpg',
    'framemy_image.jpg'
]
'''
def main():
    while (1):
        a = imageprcssng()


if __name__ == '__main__':
    main()
