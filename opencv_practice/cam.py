import cv2 as cv
import time
''' code that get the video from host's cam and view and capture.



'''
a = cv.VideoCapture(1)
if not a.isOpened():
    print("Cannot open camera")
    exit()
cap_count = 1
while True:
    ret, frame = a.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    cv.imshow('frame', frame)
    if cv.waitKey(10) == ord('c'):
        img_captured = cv.imwrite('captured.jpg', frame)
        print(f"captured!{cap_count}")
        cap_count += 1
    if cv.waitKey(10) == ord('q'):
        break
a.release
cv.destroyAllWindows()
