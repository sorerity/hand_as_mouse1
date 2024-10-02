import cv2
import mediapipe
import pyautogui

camera = cv2.VideoCapture(0)
while True:
    ret,image = camera.read()
    cv2.imshow("Hand Movement Video Capture",image)
    key = cv2.waitKey(100)
    if key == 27:
        break