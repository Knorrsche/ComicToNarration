import cv2
import numpy as np

THICKNESS = 2

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
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), THICKNESS)
    return image




def detect_speech_bubbles(
    image,
    bubble_thresh=220,
    min_area_ratio=0.005,
    max_area_ratio=0.05,
        min_circularity = 0.4,
    use_adaptive=False
):
    height, width = image.shape[:2]
    min_area = (width * height) * min_area_ratio
    max_area = (width * height) * max_area_ratio

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if use_adaptive:
        bin_img = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            15, 2
        )
        bin_img = cv2.bitwise_not(bin_img)
    else:
        _, bin_img = cv2.threshold(gray, bubble_thresh, 255, cv2.THRESH_BINARY)
        bin_img = cv2.bitwise_not(bin_img)

    contours, hierarchy = cv2.findContours(bin_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if min_area < area < max_area:
            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0:
                continue
            circularity = 4 * np.pi * area / (perimeter ** 2)
            if circularity >= min_circularity:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), THICKNESS)

    return image

