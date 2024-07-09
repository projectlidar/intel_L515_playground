import numpy as np
import time
from function_tool import MathTool as math
import cv2 as cv

FILE_PATH = "opencv_practice\captured\captured_20240707202125.771463_1.jpg"
MAX_VALUE = 255

img_import = cv.imread(FILE_PATH, cv.IMREAD_COLOR)  # BGR이다, 까먹지 말자.

print(np.shape(img_import))
try:
    if (np.shape(img_import == None)):
        raise NameError
except:
    # print("파일이 없습니다.")
    pass

# a = img_import
# a = np.array(a)
# print(a)
# print(np.shape(a))

# b = np.moveaxis(a, source=2, destination=0)
# print(b)
# print(np.shape(b))

n, m, c = np.shape(img_import)
img_import = np.moveaxis(img_import, source=2, destination=0)
for i in range(n):
    for j in range(m):
        img_import[2, i, j] = math.sigmoid(
            x=((img_import[2, i, j] / MAX_VALUE)*2 - 1), a=5) * MAX_VALUE
img_import = np.moveaxis(img_import, source=0, destination=2)
print(np.shape(img_import))

while (True):
    cv.imshow("img_import", img_import)
    if cv.waitKey(10) == ord('q'):
        break

cv.destroyAllWindows()
