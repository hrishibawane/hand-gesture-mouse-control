import cv2
import numpy as np
from keras.models import load_model
from PIL import Image
from skimage import transform

model = load_model('model2_50_0.87.h5')
classes = '0 1 2 3 4 5 6 7 8 9 unknown'.split()

def load_img(image):
    np_img = np.array(image).astype('float32')
    np_img = transform.resize(np_img, (100, 72, 3))
    np_img = np.expand_dims(np_img, axis=0)
    return np_img

def hdet(frame, min_YCrCb, max_YCrCb):
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Convert frame to YCrCb
    imgYCrCb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)

    # Find region with skin tone in YCrCb image
    skinRegion = cv2.inRange(imgYCrCb, min_YCrCb, max_YCrCb)

    # Do contour detection on skin region
    contours, hierarchy = cv2.findContours(
        skinRegion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cx, cy, cw, ch = 0, 0, 0, 0
    cat = '1'
    for i, c in enumerate(contours):

        area = cv2.contourArea(c)

        if area > 1000:
            cnt = max(contours, key=lambda x: cv2.contourArea(x))
            hull = cv2.convexHull(cnt, returnPoints=False)
            defects = cv2.convexityDefects(cnt, hull)

            # Create rectangle around contours
            cx, cy, cw, ch = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (cx, cy), (cx+cw, cy+ch), (255, 255, 0), 2)
            topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
            cv2.circle(frame, topmost, 10, [54, 38, 227], -1)

            ix, iy, iw, ih = cx, cy, cw, ch
            ix = cx-10 if cx-10>=0 else 0
            iw = cw+10 if cw+10<640 else 640
            iy = cy-10 if cy-10>=0 else 0
            ih = ch+10 if ch+10<480 else 480
            # print(ix, iw, iy, ih)

            image = gray[iy:iy+ih, ix:ix+iw]
            np_img = load_img(image)
            pred = model.predict(np_img)
            cat = classes[np.argmax(pred)]
            cv2.imwrite('ok.jpg', image)

    mx, my = cx*3, cy*2.25

    return mx, my, cat