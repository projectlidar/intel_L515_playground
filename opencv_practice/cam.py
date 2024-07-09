import cv2 as cv
import time
import math as m
from datetime import datetime
''' code that get the video from host's cam and view and capture.



'''
a = cv.VideoCapture(1)
if not a.isOpened():
    print("Cannot open camera")
    exit()

cap_count = 1
RELATIVE_PATH = "opencv_practice/captured/"  # 캡쳐파일이 저장될 위치 [상대경로]
current_timestamp = time.time()

# 타임스탬프를 datetime 객체로 변환
dt_object = datetime.fromtimestamp(current_timestamp)
print(dt_object)

''' 
'''
while True:
    ret, frame = a.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    cv.imshow('frame', frame)
    if cv.waitKey(10) == ord('c'):
        # time stamp 기준점 찍기
        current_timestamp = time.time()
        dt_object = datetime.fromtimestamp(current_timestamp)
        # window os의 파일작명 기준을 지키기 위한 염병 & 보기싫은 timestamp 소숫점 버리기
        dt_object = str(dt_object) \
            .replace(':', '')\
            .replace('-', '')\
            .replace(' ', '')[:-4]
        dt_object = dt_object.replace('.', '')
        # dt_object = list(dt_object)[:-3]
        # dt_object = str(dt_object)

        # 캡처파일 저장
        img_captured = cv.imwrite(
            f'{RELATIVE_PATH}captured_{dt_object}_{cap_count}.jpg', frame)
        # print captured number and elipsed time
        print(
            f"captured!{cap_count}, elipsed time : {(m.floor((time.time() - current_timestamp)*100000))/100}ms")
        cap_count += 1
    if cv.waitKey(10) == ord('q'):
        break
a.release
cv.destroyAllWindows()
