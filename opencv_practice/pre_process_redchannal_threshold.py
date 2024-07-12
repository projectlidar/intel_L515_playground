import numpy as np
import time
from function_tool import MathTool as math
import cv2 as cv

FILE_PATH = "opencv_practice\captured\Snipaste_2024-07-05_14-24-43.png"
# FILE_PATH = "opencv_practice\captured\maximun_distance_2024071218210875_2.jpg"
MAX_VALUE = 255

'''the global variable for make red dot's contour '''
# # 빨강영역이 HSV에서 ㅈ같이 분할되는 문제를 해결하기 위해 범위를 둘로 나눴다.
# MIN_RED_THRESHOLD_1 = np.array([0, 85, 80])  # [H,S,V]
# MAX_RED_THRESHOLD_1 = np.array([10, 255, 255])  # [H,S,V]
# MIN_RED_THRESHOLD_2 = np.array([165, 85, 80])  # [H,S,V]
# MAX_RED_THRESHOLD_2 = np.array([180, 255, 255])  # [H,S,V]
MASK_THRESHOLD = np.array([[[0, 85, 80], [10, 255, 255]],
                          [[165, 85, 80], [180, 255, 255]]])  # [[[MAX1],[MIN1]],[[MAX2],[MIN2]]]
# 문제가 진자 ㅈㄴ 많다. 피사체 표면 색 조금만 달라도 안되고 (특히 흰표면) 거리 멀어도 못잡음 시발.
MIN_AREA = 4  # 최소 dot 크기, 약 160cm 거리에서 최소 5px
MAX_AREA = 30  # 최대 dot 크기, 약 15cm 거리에서 최대 23px (약간의 shear 있음)
''''''


class PreProcess():
    def __init__(self, filePath, maxValue) -> None:
        self._FILE_PATH = filePath
        # RGB 아니고 BGR임 주의.
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

    def mask_maker(self, lower, upper, min_area, max_area):
        _img = cv.cvtColor(self.img_import, cv.COLOR_BGR2HSV)  # HSV로 변환
        _mask = cv.inRange(_img, lower, upper)  # lower와 upper를 범위로 갖는 마스크 생성
        # _contour, _ = cv.findContours(_mask, cv.RETR_EXTERNAL)
        return _mask

    def mask_kluster(self):
        n, m, o = np.shape(MASK_THRESHOLD)
        _mask = self.mask_maker(
            np.array([0, 0, 0]), np.array([0, 0, 0]), 0, 0)
        _mask -= _mask
        for i in range(n):
            _mask += self.mask_maker(
                MASK_THRESHOLD[i, 0], MASK_THRESHOLD[i, 1], MIN_AREA, MAX_AREA)
        return _mask

    def contour_maker(self, mask):
        contour, _ = cv.findContours(
            mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        return contour


a = PreProcess(FILE_PATH, MAX_VALUE)
print(a.contour_maker(a.mask_kluster()))
# a.single_channel_contrast_generator(1)
# a.multi_channel_contrast_generator(channel=[2])

# while (True):
#     cv.imshow("img_import", a.mask_kluster())
#     if cv.waitKey(10) == ord('q'):
#         break

# cv.destroyAllWindows()

# def multi_channel_contrast_generator(self, channel: list, curve_div=5):
#     self.img_import = np.moveaxis(self.img_import, source=2, destination=0)
#     for k in list(channel):
#         for i in range(self.n):
#             for j in range(self.m):
#                 self.img_import[k, i, j] = math.sigmoid(
#                     x=((self.img_import[k, i, j] / MAX_VALUE)*2 - 1), a=curve_div) * MAX_VALUE
#     self.img_import = np.moveaxis(self.img_import, source=0, destination=2)
