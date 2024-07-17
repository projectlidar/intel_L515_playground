''' every needed function are here

    NOTE:
        - math.py 대신 import 해서 쓸 수 있도록 고안함.
        해서, math.py에는 있는데 여기에는 없는 함수가 필요한 경우, 걍 여기에 추가하자. \n
        e.g. 어 ㅅㅂ m.floor()가 없네>?\n
        바로 def floor(self, x):\n
                return math.floor(x) 못참지 ㅋㅋㅋ
        
'''

import numpy as np


class MathTool(np):
    def __init__(self) -> None:
        pass

    def sigmoid(x, a) -> float:
        return (1/(1 + np.exp(-1*a*x)))

    def normal(self, sigma, mu) -> float:
        pass

    def gaussian(self, x, mean, sigma) -> float:
        return (1 / (np.sqrt(2 * np.pi) * sigma**2)) * np.exp(-(x-mean**2) / (2 * sigma**2))

    def ceil(self, x):
        return np.ceil(x)

    def floor(x):
        return np.floor(x)

    def distance_calc(d_rel: float, h_rel: float, d_f: float, theta_laser: float, theta_2: float, n: float) -> tuple:
        '''calculate object distance use "eq.of straight line" when know the angle of lens to sensor.
            Args:
                - d_rel[m] : relative distance (x-axis) between center of sensor to center of laser.[m]
                - h_rel[m] : relative distance (y-axis) between center of sensor to center of laser.[m]
                - d_f[m] : distance with center of lens to center of sensor.
                - theta_laser[rad] : relative angle of lasor about vertical normal line. [rad]
                - theta_2[rad] : relative angle of refracted light about lens's optical axis. [rad]
                    when n=1, you can input incident light's angle instead of refracted one.
                - n : relative refraction rate of lens about atmosphere(STP, for 653nm).

        '''
        if (n == 1):
            theta_1 = theta_2
        else:
            theta_1 = np.arcsin(n * np.sin(theta_2))
        x = ((-1 * d_f) + (d_rel*np.cot)) / (() + ())

        return (x, y)
