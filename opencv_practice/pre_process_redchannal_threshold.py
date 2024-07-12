import numpy as np
import time
from function_tool import MathTool as math
import cv2 as cv

FILE_PATH = "opencv_practice\captured\Snipaste_2024-07-05_14-24-43.png"
MAX_VALUE = 255


class PreProcess():
    def __init__(self, filePath, maxValue) -> None:
        self._FILE_PATH = filePath
        # RGB 아니다, BGR이다. 까먹지 말자.
        self.img_import = cv.imread(self._FILE_PATH, cv.IMREAD_COLOR)
        # 예외처리항
        try:
            if (np.shape(self.img_import == None)):
                raise NameError  # 귀찮아서 NameError로 함. 새로 에러클래스 선언하는것이 정배이긴함.
        except:
            print(np.shape(self.img_import))  # debug
            # print("파일이 없습니다.") # debug
            pass
        self._MAX_VALUE = maxValue
        self.n, self.m, self.c = np.shape(self.img_import)

    def single_channel_contrast_generator(self, channel: int, curve_div=5):
        self.img_import = np.moveaxis(self.img_import, source=2, destination=0)
        for i in range(self.n):
            for j in range(self.m):
                self.img_import[channel, i, j] = math.sigmoid(
                    x=((self.img_import[channel, i, j] / MAX_VALUE)*2 - 1), a=curve_div) * MAX_VALUE
        self.img_import = np.moveaxis(self.img_import, source=0, destination=2)

    def multi_channel_contrast_generator(self, channel: list, curve_div=5):
        '''
        this function looks quite similler to single_channel_contrast_generator. \n
        the only thing that different is channel arg's type.

        Args: 
            - channel : put the channel's number that you want to change contrast with BGR rules, *Not RGB*
                i.e. channel = (0) will apply only Blue channel, and channel = (0,1,2) will apply all channel.
        '''
        current_timestamp = time.time()
        self.img_import = np.moveaxis(self.img_import, source=2, destination=0)
        # for k in list(channel):
        #     '''under construction'''
        #     # self.img_import = map(math.sigmoid, self.img_import[k])
        #     ''''''
        #     for i in range(self.n):
        #         for j in range(self.m):
        #             self.img_import[k, i, j] = math.sigmoid(
        #                 x=((self.img_import[k, i, j] / MAX_VALUE)*2 - 1), a=curve_div) * MAX_VALUE
        for k in channel:
            # 벡터화된 연산을 사용하여 시그모이드 적용
            self.img_import[k] = math.sigmoid(
                x=((self.img_import[k] / MAX_VALUE) * 2 - 1), a=curve_div) * MAX_VALUE
        self.img_import = np.moveaxis(self.img_import, source=0, destination=2)
        print(
            f"elipsed time : {(math.floor((time.time() - current_timestamp)*100000))/100}ms")


a = PreProcess(FILE_PATH, MAX_VALUE)
# a.single_channel_contrast_generator(1)
a.multi_channel_contrast_generator(channel=[0, 1, 2])
while (True):
    cv.imshow("img_import", a.img_import)
    if cv.waitKey(10) == ord('q'):
        break

cv.destroyAllWindows()

# def multi_channel_contrast_generator(self, channel: list, curve_div=5):
#     self.img_import = np.moveaxis(self.img_import, source=2, destination=0)
#     for k in list(channel):
#         for i in range(self.n):
#             for j in range(self.m):
#                 self.img_import[k, i, j] = math.sigmoid(
#                     x=((self.img_import[k, i, j] / MAX_VALUE)*2 - 1), a=curve_div) * MAX_VALUE
#     self.img_import = np.moveaxis(self.img_import, source=0, destination=2)
