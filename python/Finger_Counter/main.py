import cv2
import mediapipe as mp
mpHand = mp.solutions.hands
hands = mpHand.Hands()
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    imgRgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(imgRgb)
    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        mp.solutions.drawing_utils.draw_landmarks(frame, hand, mpHand.HAND_CONNECTIONS)
        lmlist = []
        fingers = 0
        for id, lm in enumerate(hand.landmark):
            h, w, c = frame.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            lmlist.append([id, cx, cy])
        if len(lmlist) != 0:
            if lmlist[4][1] < lmlist[3][1]:
                fingers += 1
            if lmlist[8][2] < lmlist[7][2]:
                fingers += 1
            if lmlist[12][2] < lmlist[11][2]:
                fingers += 1
            if lmlist[16][2] < lmlist[15][2]:
                fingers += 1
            if lmlist[20][2] < lmlist[19][2]:
                fingers += 1
            cv2.putText(frame, str(fingers), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
