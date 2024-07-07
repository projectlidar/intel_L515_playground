import cv2 as cv
import time
from datetime import datetime
''' code that get the video from host's cam and view and capture.



'''
a = cv.VideoCapture(1)
if not a.isOpened():
    print("Cannot open camera")
    exit()

cap_count = 1
RELATIVE_PATH = "opencv_practice/captured/"
current_timestamp = time.time()

# 타임스탬프를 datetime 객체로 변환
dt_object = datetime.fromtimestamp(current_timestamp)
print(dt_object)

while True:
    ret, frame = a.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    cv.imshow('frame', frame)
    if cv.waitKey(10) == ord('c'):
        current_timestamp = time.time()
        dt_object = datetime.fromtimestamp(current_timestamp)
        dt_object = str(dt_object) \
            .replace(':', '')\
            .replace('-', '')\
            .replace(' ', '')[:-4]
        dt_object = dt_object.replace('.', '')
        # dt_object = list(dt_object)[:-3]
        # dt_object = str(dt_object)
        img_captured = cv.imwrite(
            f'{RELATIVE_PATH}captured_{dt_object}_{cap_count}.jpg', frame)
        print(f"captured!{cap_count}")
        cap_count += 1
    if cv.waitKey(10) == ord('q'):
        break
a.release
cv.destroyAllWindows()
