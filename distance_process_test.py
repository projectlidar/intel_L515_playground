import numpy as np
import time
import math
import cv2 as cv

# 설정 변수들
FILE_PATH = "opencv_practice/captured/43.png"
MAX_VALUE = 255  # 이미지의 비트 수, 이미지가 고화질이라면 해당 값을 2**10으로 변경.

'''이미지로부터 신호를 구분짓는 1차 신호결정값. 신호 대 잡음비를 결정한다.'''
MASK_THRESHOLD = np.array([[[0, 16,  16], [10, 255, 255]],
                          [[165,  16,  16], [180, 255, 255]]])

MIN_AREA = 0.5**2  # 최소 dot 크기
MAX_AREA = 14**3  # 최대 dot 크기 (14**2 or 14**2)

# 삼각측량법에 기반한 거리 계산 함수


def calculate_distance(laser_sensor_distance, laser_angle_deg, reflected_angle_deg):
    # 각도를 라디안으로 변환
    laser_angle = math.radians(laser_angle_deg)
    reflected_angle = math.radians(reflected_angle_deg)

    # 삼각측량 계산: d = L / (tan(θ) + tan(φ))
    distance = laser_sensor_distance / \
        (math.tan(laser_angle) + math.tan(reflected_angle))
    return distance


class PreProcess():
    '''각 변수들을 초기값으로 설정한다'''

    def __init__(self, filePath, maxValue) -> None:
        self._FILE_PATH = filePath  # 이미지 불러오기
        self.img_import = cv.imread(self._FILE_PATH, cv.IMREAD_COLOR)
        '''예외처리 항'''
        try:
            if (np.shape(self.img_import == None)):
                raise NameError
        except:
            print(np.shape(self.img_import))
            pass
        ''''''
        self._MAX_VALUE = maxValue
        self.n, self.m, self.c = np.shape(self.img_import)
        self.t_tot = 0
        self.time_sig_fig = 10**3  # 수치들을 소숫점 셋째자리에서 절삭한다.


'''이미지로부터 신호를 구분하기 위한 1차 필터 생성함수'''

 def mask_maker(self, lower, upper, min_area, max_area):
      # 이미지의 색상환을 색도-채도-밝기 규칙으로 변환한다.
      _img = cv.cvtColor(self.img_import, cv.COLOR_BGR2HSV)
       _mask = cv.inRange(_img, lower, upper)
        return _mask
''''''

'''이미지로부터 신호를 구분하기 위한 1차 필터 적용 및 후처리 함수'''

 def mask_kluster(self):
      n, m, o = np.shape(MASK_THRESHOLD)
       _mask = self.mask_maker(np.array([0, 0, 0]), np.array(
           [0, 0, 0]), 0, 0)  # 생성한 1차 필터 호출
        _mask -= _mask  # 1차 필터 병합
        for i in range(n):
            _mask += self.mask_maker(MASK_THRESHOLD[i, 0],
                                     MASK_THRESHOLD[i, 1], MIN_AREA, MAX_AREA)  # 1차 필터 적용
        return _mask
''''''

'''이미지로부터 신호를 구분하기 위한 2차 필터 생성 및 적용 함수'''

 def contour_maker(self, mask):
      contour, _ = cv.findContours(
           mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 1차 필터를 지난 데이터에 2차 필터 적용
       return contour
''''''

'''이미지로부터 신호를 구분하기 위한 2차 필터 후처리 함수'''

 def contour_filter(self, contour, min_area=MIN_AREA, max_area=MAX_AREA):
      filtered_contour = [cnt for cnt in contour if (
           (cv.contourArea(cnt) > min_area) and (cv.contourArea(cnt) < max_area))]  # 2차 필터 후처리 후 제적용
       return filtered_contour
''''''

'''신호의 위치와 크기를 각각 계산하는 함수'''

 def dot_shower(self, filtered_contour):
      dot_pos = []  # 위치 및 크기 값을 저장할 리스트
       for i, dot in enumerate(filtered_contour):
            (x, y), radius = cv.minEnclosingCircle(dot)  # 각 점의 위치와 크기를 생성
            dot_pos.append([(x, y), radius])  # 생성된 데이터 저장
            center = (int(x), int(y))  # 위치 값 저장
            radius = int(radius)  # 크기 값 저장
            cv.circle(self.img_import, center, radius,
                      (0, 255, 0), 2)  # 이미지에 신호 위치 표시
            cv.putText(self.img_import, str(i + 1), center,
                       cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # 이미지에 신호 위치 표기
        return dot_pos
''''''

# 점들의 위치를 바탕으로 거리를 계산하고 이미지에 표시하는 함수
# 석고상 측정을 위해 원래에서 나사 한칸 2.5만큼 이동함 원래 47.7 석고상은 45.2(laser sensor 간)
def dot_pos_maker(self, filtered_contour, laser_sensor_distance=45.2, laser_angle_deg=43):
     significant_figure = 10*3  # 수치들을 소숫점 셋째자리에서 절삭
      distances = []  # 거리 값을 저장할 리스트
       for i, dot in enumerate(filtered_contour):
            M = cv.moments(dot)
            if M["m00"] != 0:
                cX = (int((M["m10"] / M["m00"]) *
                      significant_figure)) / significant_figure
                cY = (int((M["m01"] / M["m00"]) *
                      significant_figure)) / significant_figure

                # 각도 계산 (cX에 따라 달라짐)
                # 초기 0.0929692에서 0.0618619 으로 변경했더니 음의 값에서도
                reflected_angle_deg = (cX - 320) * 0.0618619

                # 반사 각도가 중앙(320)보다 왼쪽이면 음수로 처리
                if cX < 320:
                    reflected_angle_deg = -abs(reflected_angle_deg)

                # 거리 계산
                distance = calculate_distance(
                    laser_sensor_distance, laser_angle_deg, reflected_angle_deg)
                distances.append(distance)

                # 터미널에 좌표와 거리 값 출력
                print(
                    f"Red dot {i+1} coordinates: ({cX}, {cY}), Distance: {distance:.2f} cm")

                # 이미지에 각 점의 거리 표시
                text = f"{distance:.2f} cm"
                cv.putText(self.img_import, text, (int(cX), int(cY) - 10),
                           cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        return distances

'''각 함수별 동작속도 측정을 위한 함수'''

 def time_keeper(self, t_ini, print_text):
      t_fin = time.time()
       elipsed_time = (int((t_fin - t_ini) * 1000 *
                        self.time_sig_fig)) / self.time_sig_fig
        self.t_tot += elipsed_time
        print(f"{print_text}, elipsed time : {elipsed_time} ms")
        t_ini = time.time()
        return t_fin


# 메인 코드 실행
t_ini = time.time()  # 초기 시간[ms] 설정
a = PreProcess(FILE_PATH, MAX_VALUE)  # 거리측정함수를 생성한다.
# 설정한 초기 시간을 기준으로 각 함수 실행시간 기록 시작
t_ini = a.time_keeper(t_ini=t_ini, print_text="load")

'''이미지로부터 신호와 노이즈를 구분하는 함수 동작구문'''
mask = a.mask_kluster()
t_ini = a.time_keeper(t_ini=t_ini, print_text="make mask")
filtered_contour = a.contour_filter(a.contour_maker(mask))
t_ini = a.time_keeper(t_ini=t_ini, print_text="make contour")
''''''

dot = a.dot_shower(filtered_contour)  # 신호의 위치 출력
t_ini = a.time_keeper(t_ini=t_ini, print_text="get dot")
print(dot)

# 모든 점들의 거리를 계산하여 출력하고, 이미지에 표시
distances = a.dot_pos_maker(filtered_contour)
t_ini = a.time_keeper(t_ini=t_ini, print_text="get dot pos")
print(distances)

'''코드의 실행결과를 화면 주사율에 맞춰 gui로 뿌려주는 구문'''
while True:
    cv.imshow("img_import", a.img_import)
    cv.imshow("mask", mask)
    if cv.waitKey(10) == ord('q'):
        break
''''''

'''프로그램 종료 후 총 소요시간을 터미널에 출력'''
print(f"total elipsed time : {a.t_tot} ms")
print(f"total FPS : {1000/a.t_tot} fps")
