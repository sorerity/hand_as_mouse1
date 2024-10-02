import cv2
import mediapipe
import pyautogui
capture_hands = mediapipe.solutions.hands.Hands()
drawing_option = mediapipe.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
camera = cv2.VideoCapture(0)
index_finger1 = index_finger2 = thumb_tip1 = thumb_tip2 = 0

if not camera.isOpened():
    print("Error: Camera could not be opened.")
    exit()

while True:
    ret,image = camera.read()
    if not ret or image is None:
        print("Error, could not read image from the camera.")
        break

    image_height, image_width, _= image.shape
    image = cv2.flip(image,1)
    rgb_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    output_hands = capture_hands.process(rgb_image)
    all_hands = output_hands.multi_hand_landmarks

    if all_hands:
        for hand in all_hands:
            drawing_option.draw_landmarks(image,hand)
            one_hand_landmarks = hand.landmark
            for id, lm in enumerate(one_hand_landmarks):
                current_pixel1 = int(lm.x * image_width)
                current_pixel2 = int(lm.y * image_height)
                if id == 8:
                    mouse_x = int(screen_width / image_width * current_pixel1 )
                    mouse_y = int(screen_height / image_height * current_pixel2 )
                    cv2.circle(image,(current_pixel1,current_pixel2),10,(0,255,255))
                    pyautogui.moveTo(mouse_x,mouse_y)
                    index_finger1 = current_pixel1
                    index_finger2 = current_pixel2
                if id == 4:
                    thumb_tip1 = current_pixel1
                    thumb_tip2 = current_pixel2
                    cv2.circle(image,(current_pixel1,current_pixel2),10,(0,255,255))

        distance = ((thumb_tip1 - index_finger1) ** 2 + (thumb_tip2 - index_finger2) ** 2) ** 0.5
        print(distance)

        if(distance<40):
            pyautogui.click()
    
    cv2.imshow("Hand Movement Video Capture",image)
    key = cv2.waitKey(100)
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()