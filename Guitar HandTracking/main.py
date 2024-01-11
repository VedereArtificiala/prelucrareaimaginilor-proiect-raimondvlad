from cvzone.HandTrackingModule import HandDetector
import cv2
import keyboard
import rotate_and_crop
from imageModule import Image
import grid_detection

def recognition(fingers, image):
    index = fingers[0]
    middle = fingers[1]
    ring = fingers[2]
    print(fingers)
    print("Degetul mijlociu: ", middle)
    print("Degetul inelar: ", ring)

    imgAux = Image(img=image)
    cropping = rotate_and_crop.crop_image(imgAux)
    rotated = rotate_and_crop.rotate_picture(cropping)
    points1, string, image = grid_detection.string_detection(rotated)
    points2, image = grid_detection.fret_detection(rotated)

    # Em
    if middle[0] <= points2[1] and middle[1] >= points1[2]:
        if ring[1] <= middle[1] and middle[1] >= points1[3] or middle[1] >= points1[4]:
            print("Acordul Em sau Mi minor realizat")
    print("Gata")

cap = cv2.VideoCapture(0)

detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

fingerList = []

while True:
    success, img = cap.read()

    hands, img = detector.findHands(img, draw=False, flipType=True)

    if hands:
        hand1 = hands[0]  # Get the first hand detected
        lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
        bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
        center1 = hand1['center']  # Center coordinates of the first hand
        handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")

        fingers1 = detector.fingersUp(hand1)
        # print(f'H1 = {fingers1.count(1)}', end=" ")  # Print the count of fingers that are up

        #length, info, img = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img, color=(255, 0, 255), scale=10)
        fingerList.append(lmList1[8][0:2])
        fingerList.append(lmList1[12][0:2])
        fingerList.append(lmList1[16][0:2])
        # Check if a second hand is detected
        '''if len(hands) == 2:
            # Information for the second hand
            hand2 = hands[1]
            lmList2 = hand2["lmList"]
            bbox2 = hand2["bbox"]
            center2 = hand2['center']
            handType2 = hand2["type"]

            # Count the number of fingers up for the second hand
            fingers2 = detector.fingersUp(hand2)
            print(f'H2 = {fingers2.count(1)}', end=" ")

            # Calculate distance between the index fingers of both hands and draw it on the image
            length, info, img = detector.findDistance(lmList1[8][0:2], lmList2[8][0:2], img, color=(255, 0, 0),
                                                      scale=10)

        print(" ")  # New line for better readability of the printed output'''

    # Display the image in a window
    cv2.imshow("Image", img)
    if keyboard.is_pressed("space"):
        #cv2.imwrite("Test_images/output2.jpg", img)
        break


    # Keep the window open and update it for each frame; wait for 1 millisecond between frames
    cv2.waitKey(1)
recognition(fingerList, img)