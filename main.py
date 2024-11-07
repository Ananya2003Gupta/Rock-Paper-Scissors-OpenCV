import cv2
import time
import cvzone
import random
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

flag = 1
detector = HandDetector(maxHands=1)
timer = 0
stateResult = False
startGame = False
scores = [0, 0] #[AI Score, Player Score]

while flag:
    imgBG = cv2.imread("assets\BG.png")
    success, img = cap.read()
    imgScaled = cv2.resize(img, (0,0), None, 0.916, 0.916)
    imgScaled = imgScaled[ :, 58:506]
    hands, img = detector.findHands(imgScaled)
    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (760, 516), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)
        
        if timer > 3:
            stateResult = True
            timer = 0
            if hands:
                hand = hands[0]
                fingers = detector.fingersUp(hand)
                if fingers == [0,0,0,0,0]:
                    playerMove = 1
                elif fingers == [1,1,1,1,1]:
                    playerMove = 2
                elif fingers == [0,1,1,0,0]:
                    playerMove = 3
                else:
                    playerMove = None

                randomNumber = random.randint(1,3)
                imgAI = cv2.imread(f"assets/{randomNumber}.png", cv2.IMREAD_UNCHANGED)
                imgBG = cvzone.overlayPNG(imgBG, imgAI, (158, 316))
                
                # Player Wins
                if((playerMove == 1 and randomNumber == 3) or (playerMove == 2 and randomNumber == 1) or (playerMove == 3 and randomNumber == 2)):
                    scores[1] += 1
                # AI Wins
                elif ((playerMove == 1 and randomNumber == 2) or (playerMove == 2 and randomNumber == 3) or (playerMove == 3 and randomNumber == 1)):
                    scores[0] += 1

    imgBG[318:758, 988:1436] = imgScaled
    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (158, 316))

    cv2.putText(imgBG, str(scores[0]), (515, 296), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5) # AI Score
    cv2.putText(imgBG, str(scores[1]), (1350, 298), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5) # Player Score
    cv2.imshow("BG", imgBG)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False
    
    if key == ord('q'):
        flag = 0