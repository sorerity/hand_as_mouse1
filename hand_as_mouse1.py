import cv2
import mediapipe
import pyautogui

capture_hands = mediapipe.solutions.hands.Hands()
drawing_option = mediapipe.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

camera = cv2.VideoCapture(0)

finger_resting_positions = {'middle': None, 'index': None, 'ring': None, 'thumb_finger': None}
key_press_states = {'W': False, 'A': False, 'D': False, 'Space': False}

index_finger1 = index_finger2 = thumb_tip1 = thumb_tip2 = 0

if not camera.isOpened():
    print("Error: Camera could not be opened.")
    exit()

def calculate_hand_center(hand_landmarks_list, image_width, image_height):
    hand_center_x = sum([landmark.x for landmark in hand_landmarks_list]) / len(hand_landmarks_list)
    hand_center_y = sum([landmark.y for landmark in hand_landmarks_list]) / len(hand_landmarks_list)

    center_pixel_x = int(hand_center_x * image_width)
    center_pixel_y = int(hand_center_y * image_height)

    return center_pixel_x, center_pixel_y

while True:
    ret,image = camera.read()
    if not ret or image is None:
        print("Error, could not read image from the camera.")
        break

    image = cv2.resize(image, (640, 480))

    image_height, image_width, _ = image.shape
    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output_hands = capture_hands.process(rgb_image)
    all_hands = output_hands.multi_hand_landmarks

    if all_hands:
        for index, hand in enumerate(all_hands):
            drawing_option.draw_landmarks(image, hand)
            one_hand_landmarks = hand.landmark

            hand_label = output_hands.multi_handedness[index].classification[0].label

            if hand_label == "Left":
                finger_positions = {
                    'middle_finger': int(one_hand_landmarks[12].y * image_height),
                    'index_finger': int(one_hand_landmarks[8].y * image_height),
                    'ring_finger': int(one_hand_landmarks[16].y * image_height),
                    'thumb_finger': int(one_hand_landmarks[4].y * image_height),
                }
                
            hand_center_x, hand_center_y = calculate_hand_center(one_hand_landmarks, image_width, image_height)
            cv2.circle(image, (hand_center_x, hand_center_y), 10, (255, 0, 0), -1)

            for id, lm in enumerate(one_hand_landmarks):
                current_pixel1 = int(lm.x * image_width)
                current_pixel2 = int(lm.y * image_height)
                if id == 8:
                    mouse_x = int(screen_width / image_width * current_pixel1 )
                    mouse_y = int(screen_height / image_height * current_pixel2 )
                    cv2.circle(image,(current_pixel1,current_pixel2),10,(0,255,255), -1)
                    pyautogui.moveTo(hand_center_x * screen_width / image_width, hand_center_y * screen_height / image_height)
                    index_finger1 = current_pixel1
                    index_finger2 = current_pixel2
                if id == 4:
                    thumb_tip1 = current_pixel1
                    thumb_tip2 = current_pixel2
                    cv2.circle(image,(current_pixel1,current_pixel2),10,(0,255,255))

        distance = ((thumb_tip1 - index_finger1) ** 2 + (thumb_tip2 - index_finger2) ** 2) ** 0.5
        print(distance)

        if distance < 40:
            pyautogui.click()
    
    image = cv2.resize(image, (1280, 720))
    cv2.imshow("Hand Movement Video Capture",image)
    key = cv2.waitKey(100)
    if key == 27:
        break

camera.release()
cv2.destroyAllWindows()