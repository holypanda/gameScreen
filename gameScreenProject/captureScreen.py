import numpy as np
from PIL import ImageGrab
import cv2
import time
from directKeys import PressKey, ReleaseKey, W, A, S, D



def roi(img, vertices):  # region of interest
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

def draw_lines(img, lines):
    try:
        for line in lines:
            coords = line[0]
            cv2.line(img, (coords[0], coords[1]), (coords[2], coords[3]), [255,255,255], 3)
    except:
        pass
def process_image(original_image):
    process_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    process_img = cv2.Canny(process_img, threshold1=200, threshold2=300)
    vertices = np.array([[10, 500], [10, 300], [300, 200], [500, 200], [800, 300], [800, 500]])
    process_img = roi(process_img, [vertices])
    process_img = cv2.GaussianBlur(process_img,(5,5),0)

    lines = cv2.HoughLinesP(process_img, 1, np.pi/180, 180, np.array([]), 100, 5)
    draw_lines(process_img, lines)


    return process_img


# for i in list(range(4))[::-1]:
#     print(i+1)
#     time.sleep(1)

last_time = time.time()
while True:
    screen = np.array(ImageGrab.grab(bbox=(0, 0, 960, 600)))  # capture screen
    new_screen = process_image(screen)

    # print("down")
    # PressKey(W)
    # time.sleep(3)
    # ReleaseKey(W)


    cv2.imshow('window', new_screen)  # play the screen
    cv2.imshow('window2', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))  # play the screen

    print("%s FPS" % (int(1 / (time.time() - last_time))))

    last_time = time.time()

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
