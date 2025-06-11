import cv2
import numpy as np


def detect_panels(image, blur_kernel=5, thresh_val=200, morph_kernel=5, min_size=50):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (blur_kernel, blur_kernel), 0)
    _, thresh = cv2.threshold(blur, thresh_val, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((morph_kernel, morph_kernel), np.uint8)
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > min_size and h > min_size:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return image


def detect_speech_bubbles(image, bubble_thresh=220, min_area=1000, max_area=10000, approx_factor=0.02):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, bin_img = cv2.threshold(gray, bubble_thresh, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(bin_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, approx_factor * cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(cnt)
        if min_area < area < max_area and len(approx) > 4:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return image
