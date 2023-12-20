import cv2
import numpy as np
import time

# * img import and resize for easier review
img_import = cv2.imread(
    "opencv_practice\img\CMS00750.JPG", cv2.IMREAD_COLOR)
img_import = cv2.resize(img_import, dsize=(0, 0), fx=0.3,
                        fy=0.3, interpolation=cv2.INTER_AREA)

print(img_import.shape)
print(img_import.size)
# px = img_import[600, 900]
n = img_import.shape[0]
m = img_import.shape[1]
# print(n, m)

x_rng = 1000
y_rng = 1300
x_shift = (n - x_rng)//2
y_shift = (m - y_rng)//2

ini_time = time.time()
for i in range(x_shift, (x_shift+x_rng)):
    for j in range(y_shift, (y_shift+y_rng)):
        img_import[i, j] = [img_import[i, j, 2],
                            img_import[i, j, 1], img_import[i, j, 0]]
print(time.time()-ini_time)


# * visualization
cv2.imshow("img_import", img_import)
cv2.waitKey(0)
cv2.destroyWindow
gray = cv2.cvtColor(img_import, cv2.COLOR_BGR2GRAY)
cv2.imshow("img_import", gray)
cv2.waitKey(0)
# TODO 오픈cv 연습해야됨!
# ! 이새끼 아무것도 안하고 있음!
