import numpy as np
import time
from function_tool import MathTool as math
import cv2 as cv

# TODO 거리-위치 그라디언트 맵 생성 함수
# TODO 그라디언트 맵 필터 함수
# TODO 더 충실한 객채지향

# FILE_PATH = "opencv_practice\captured\Snipaste_2024-07-05_14-24-43.png" #default
# FILE_PATH = "opencv_practice\captured\maximun_distance_2024071218210875_2.jpg"
# FILE_PATH = "opencv_practice\captured\captured_2024081610185380_3.jpg"
FILE_PATH = "opencv_practice\captured\captured_2024082000201028_5.jpg"


MAX_VALUE = 255

'''the global variable for make red dot's contour '''
# # ? 빨강영역이 HSV에서 ㅈ같이 분할되는 문제를 해결하기 위해 범위를 둘로 나눴다.
# MIN_RED_THRESHOLD_1 = np.array([0, 85, 80])  # [H,S,V], 구간 1(a,b)의 a 즉, [MAX1]
# MAX_RED_THRESHOLD_1 = np.array([10, 255, 255])  # [H,S,V] 구간 1(a,b)의 b 즉, [MIN1]
# MIN_RED_THRESHOLD_2 = np.array([165, 85, 80])  # [H,S,V] 구간 2(a,b)의 a 즉, [MAX2]
# MAX_RED_THRESHOLD_2 = np.array([180, 255, 255])  # [H,S,V] 구간 2(a,b)의 b 즉, [MIN2]
MASK_THRESHOLD = np.array([[[0, 16,  16], [10, 255, 255]],
                          [[165,  16,  16], [180, 255, 255]]])  # [[[MAX1],[MIN1]],[[MAX2],[MIN2]]]
# 문제가 진자 ㅈㄴ 많다. 피사체 표면 색 조금만 달라도 안되고 (특히 흰표면) 거리 멀어도 못잡음
MIN_AREA = 0.5**2  # 최소 dot 크기, 약 160cm 거리에서 최소 5px [r^2]
MAX_AREA = 14**2  # 최대 dot 크기, 약 15cm 거리에서 최대 23px (약간의 shear 있음) [r^2]
''''''

'''The global veriable for making distance-displacement gradient map'''


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
        self.t_tot = 0
        self.time_sig_fig = 1000

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
        # // for k in list(channel):
        # //     '''under construction'''
        # //     # self.img_import = map(math.sigmoid, self.img_import[k])
        # //     ''''''
        # //     for i in range(self.n):
        # //         for j in range(self.m):
        # //             self.img_import[k, i, j] = math.sigmoid(
        # //                 x=((self.img_import[k, i, j] / MAX_VALUE)*2 - 1), a=curve_div) * MAX_VALUE
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
            mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # ! 왜 쓰는지 모름
        return contour

    def contour_shower(self, contour):
        temp_map = self.img_import
        x, y, c = np.shape(temp_map)
        temp_map = temp_map*0
        # for _ in contour:
        #     for i, j in list(_):
        #         temp_map[i, j] = [255, 255, 255]
        return temp_map

    def contour_filter(self, contour, min_area=MIN_AREA, max_area=MAX_AREA):
        # Filter contours based on area to remove noise
        filtered_contour = [cnt for cnt in contour if (
            (cv.contourArea(cnt) > min_area) and (cv.contourArea(cnt) < max_area))]
        return filtered_contour

    def dot_shower(self, filtered_contour):
        dot_pos = []
        for dot in filtered_contour:
            (x, y), radius = cv.minEnclosingCircle(dot)
            dot_pos.append([(x, y), radius])
            center = (int(x), int(y))
            radius = int(radius)
            cv.circle(self.img_import, center, radius, (0, 255, 0), 2)
        return (dot_pos)

    def dot_pos_maker(self, filtered_contour):
        significant_figure = 1000
        for i, dot in enumerate(filtered_contour):
            M = cv.moments(dot)  # ! 구조 이해 안했음!
            if M["m00"] != 0:
                cX = (int((M["m10"] / M["m00"])*significant_figure)
                      )/significant_figure
                cY = (int((M["m01"] / M["m00"])*significant_figure)
                      )/significant_figure
                print(f"Red dot {i+1} coordinates: ({cX}, {cY})")

    def time_keeper(self, t_ini, print_text):
        t_fin = time.time()
        elipsed_time = (int((t_fin - t_ini) * 1000 *
                        self.time_sig_fig))/self.time_sig_fig
        self.t_tot += elipsed_time
        print(f"{print_text}, elipsed time : {elipsed_time} ms")
        t_ini = time.time()
        return t_fin


t_ini = time.time()
a = PreProcess(FILE_PATH, MAX_VALUE)
t_ini = a.time_keeper(t_ini=t_ini, print_text="load")

''''''
# print(np.shape(a.contour_maker(a.mask_kluster())))
# print(a.contour_maker(a.mask_kluster()))
''''''
mask = a.mask_kluster()
t_ini = a.time_keeper(t_ini=t_ini, print_text="make mask")
filtered_contour = a.contour_filter(a.contour_maker(mask))
t_ini = a.time_keeper(t_ini=t_ini, print_text="make contour")
# print(filtered_contour)
dot = a.dot_shower(filtered_contour)
t_ini = a.time_keeper(t_ini=t_ini, print_text="get dot")
print(dot)
dot_pos = a.dot_pos_maker(filtered_contour)
t_ini = a.time_keeper(t_ini=t_ini, print_text="get dot pos")
print(dot_pos)


# a.single_channel_contrast_generator(1)
# a.multi_channel_contrast_generator(channel=[2])

while (True):
    cv.imshow("img_import", a.img_import)
    cv.imshow("mask", mask)
    # t_ini = a.time_keeper(t_ini=t_ini, print_text="drow screen")
    if cv.waitKey(10) == ord('q'):
        break

print(f"total elipsed time : {a.t_tot} ms")
print(f"total FPS : {1000/a.t_tot} fps")

# cv.destroyAllWindows()

# def multi_channel_contrast_generator(self, channel: list, curve_div=5):
#     self.img_import = np.moveaxis(self.img_import, source=2, destination=0)
#     for k in list(channel):
#         for i in range(self.n):
#             for j in range(self.m):
#                 self.img_import[k, i, j] = math.sigmoid(
#                     x=((self.img_import[k, i, j] / MAX_VALUE)*2 - 1), a=curve_div) * MAX_VALUE
#     self.img_import = np.moveaxis(self.img_import, source=0, destination=2)
