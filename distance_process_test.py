import numpy as np
import time
import math  
import cv2 as cv

# 설정 변수들
FILE_PATH = "opencv_practice/captured/43.png"
MAX_VALUE = 255

MASK_THRESHOLD = np.array([[[0, 16,  16], [10, 255, 255]],
                          [[165,  16,  16], [180, 255, 255]]])

MIN_AREA = 0.5**2  # 최소 dot 크기
MAX_AREA = 14**3  # 최대 dot 크기 (14**2 or 14**2)

# 거리 계산 함수
def calculate_distance(laser_sensor_distance, laser_angle_deg, reflected_angle_deg):
    # 각도를 라디안으로 변환
    laser_angle = math.radians(laser_angle_deg)
    reflected_angle = math.radians(reflected_angle_deg)

    # 삼각측량 계산: d = L / (tan(θ) + tan(φ))
    distance = laser_sensor_distance / (math.tan(laser_angle) + math.tan(reflected_angle))
    return distance

class PreProcess():
    def __init__(self, filePath, maxValue) -> None:
        self._FILE_PATH = filePath
        self.img_import = cv.imread(self._FILE_PATH, cv.IMREAD_COLOR)
        try:
            if (np.shape(self.img_import == None)):
                raise NameError
        except:
            print(np.shape(self.img_import))
            pass
        self._MAX_VALUE = maxValue
        self.n, self.m, self.c = np.shape(self.img_import)
        self.t_tot = 0
        self.time_sig_fig = 1000

    def mask_maker(self, lower, upper, min_area, max_area):
        _img = cv.cvtColor(self.img_import, cv.COLOR_BGR2HSV)
        _mask = cv.inRange(_img, lower, upper)
        return _mask

    def mask_kluster(self):
        n, m, o = np.shape(MASK_THRESHOLD)
        _mask = self.mask_maker(np.array([0, 0, 0]), np.array([0, 0, 0]), 0, 0)
        _mask -= _mask
        for i in range(n):
            _mask += self.mask_maker(MASK_THRESHOLD[i, 0], MASK_THRESHOLD[i, 1], MIN_AREA, MAX_AREA)
        return _mask

    def contour_maker(self, mask):
        contour, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        return contour

    def contour_filter(self, contour, min_area=MIN_AREA, max_area=MAX_AREA):
        filtered_contour = [cnt for cnt in contour if (
            (cv.contourArea(cnt) > min_area) and (cv.contourArea(cnt) < max_area))]
        return filtered_contour

    def dot_shower(self, filtered_contour):
        dot_pos = []
        for i, dot in enumerate(filtered_contour):
            (x, y), radius = cv.minEnclosingCircle(dot)
            dot_pos.append([(x, y), radius])
            center = (int(x), int(y))
            radius = int(radius)
            cv.circle(self.img_import, center, radius, (0, 255, 0), 2)
            cv.putText(self.img_import, str(i + 1), center,
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return dot_pos

    # 점들의 위치를 바탕으로 거리를 계산하고 이미지에 표시하는 메서드
    def dot_pos_maker(self, filtered_contour, laser_sensor_distance=45.2, laser_angle_deg=43):  #석고상 측정을 위해 원래에서 나사 한칸 2.5만큼 이동함 원래 47.7 석고상은 45.2(laser sensor 간)
        significant_figure = 1000
        distances = []  # 거리 값을 저장할 리스트
        for i, dot in enumerate(filtered_contour):
            M = cv.moments(dot)
            if M["m00"] != 0:
                cX = (int((M["m10"] / M["m00"]) * significant_figure)) / significant_figure
                cY = (int((M["m01"] / M["m00"]) * significant_figure)) / significant_figure

                # 각도 계산 (cX에 따라 달라짐)
                reflected_angle_deg = (cX - 320) * 0.0618619  #초기 0.0929692에서 0.0618619 으로 변경했더니 음의 값에서도 

                # 반사 각도가 중앙(320)보다 왼쪽이면 음수로 처리
                if cX < 320:
                    reflected_angle_deg = -abs(reflected_angle_deg)

                # 거리 계산
                distance = calculate_distance(laser_sensor_distance, laser_angle_deg, reflected_angle_deg)

                distances.append(distance)
                # 터미널에 좌표와 거리 값 출력
                print(f"Red dot {i+1} coordinates: ({cX}, {cY}), Distance: {distance:.2f} cm")

                # 이미지에 각 점의 거리 표시
                text = f"{distance:.2f} cm"
                cv.putText(self.img_import, text, (int(cX), int(cY) - 10),
                           cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        return distances

    def time_keeper(self, t_ini, print_text):
        t_fin = time.time()
        elipsed_time = (int((t_fin - t_ini) * 1000 * self.time_sig_fig)) / self.time_sig_fig
        self.t_tot += elipsed_time
        print(f"{print_text}, elipsed time : {elipsed_time} ms")
        t_ini = time.time()
        return t_fin


# 메인 코드 실행
t_ini = time.time()
a = PreProcess(FILE_PATH, MAX_VALUE)
t_ini = a.time_keeper(t_ini=t_ini, print_text="load")

mask = a.mask_kluster()
t_ini = a.time_keeper(t_ini=t_ini, print_text="make mask")
filtered_contour = a.contour_filter(a.contour_maker(mask))
t_ini = a.time_keeper(t_ini=t_ini, print_text="make contour")
dot = a.dot_shower(filtered_contour)
t_ini = a.time_keeper(t_ini=t_ini, print_text="get dot")
print(dot)

# 모든 점들의 거리를 계산하여 출력하고, 이미지에 표시
distances = a.dot_pos_maker(filtered_contour)
t_ini = a.time_keeper(t_ini=t_ini, print_text="get dot pos")
print(distances)

while True:
    cv.imshow("img_import", a.img_import)
    cv.imshow("mask", mask)
    if cv.waitKey(10) == ord('q'):
        break

print(f"total elipsed time : {a.t_tot} ms")
print(f"total FPS : {1000/a.t_tot} fps")
