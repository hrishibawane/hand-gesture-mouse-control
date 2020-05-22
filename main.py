import cv2
import numpy as np
import sys
import pyautogui as pai
from detect_hand import hdet

pai.FAILSAFE = False

scr_wid, scr_ht = pai.size()
print(scr_wid, scr_ht)

cap = cv2.VideoCapture(0)
# Constants for finding range of skin color in YCrCb
min_YCrCb = np.array([0, 130, 70], np.uint8)
max_YCrCb = np.array([255, 180, 130], np.uint8)

while True:
    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)
    mx, my, cat = hdet(frame, min_YCrCb, max_YCrCb)

    if mx==0 and my==0:
        sys.exit()

    # pai.moveTo(mx, my)
    if cat=='2':
        pai.click(mx, my)
    elif cat=='0':
        pai.dragTo(mx, my)
    else:
        pai.moveTo(mx, my)
        
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame', 640, 360)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

