''' every needed function are here

    NOTE:
        - math.py 대신 import 해서 쓸 수 있도록 고안함.
        해서, math.py에는 있는데 여기에는 없는 함수가 필요한 경우, 걍 여기에 추가하자. \n
        e.g. 어 ㅅㅂ m.floor()가 없네>?\n
        바로 def floor(self, x):\n
                return math.floor(x) 못참지 ㅋㅋㅋ
        
'''

import numpy as np


class MathTool():
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

    def truncation(x, digit):
        return np.floor(x*(10**digit))/10**digit

    def csc(x):
        return 1/np.sin(x)

    def sec(x):
        return 1/np.cos(x)

    def cot(x):
        return 1/np.tan(x)

    def distance_calc_lin(self, d_rel: float, h_rel: float, d_f: float, theta_laser: float, pixel_pitch: float, peak: float, n: float) -> tuple:
        '''calculate object distance use "eq.of straight line" when know the angle of lens to sensor. \n
            Args:
                - d_rel[m] : relative distance (x-axis) between center of sensor to center of laser.[m]
                - h_rel[m] : relative distance (y-axis) between center of sensor to center of laser.[m]
                - d_f[m] : distance with center of lens to center of sensor.
                - theta_laser[rad] : relative angle of lasor about vertical normal line. [rad]
                - pixel_pitch[m] : distance between each pixel. [m]
                - peak[pixel] : relative number of pixel about center of sensor's pixel. [pixel] 
                - n[1] : relative refraction rate of lens about atmosphere(STP, for 653nm). [1]

            Returns : tuple, (x,y) is relative coordinate of object about center of sensor. [(m, m)]

            Notes: it can use only when...
                - sensor and lens's optic axis are orthogonal.
                - cartesian coord.
                - if you can assume a thin lens.(or optic path is pass through the center of the lens.)
                - light source's frequency is 653nm(He-Ne Lasor). \n
                or there is mono-frequency light source, and it's refraction rate is nearly 1 in atmosphere(STP).
                - there is no z-axis deviation. (sensor - lens - object point - light source are aligned in z-axis).
        '''
        d_img = pixel_pitch * peak
        theta_2 = self.cot(d_f/d_img)

        if (n == 1):
            theta_1 = theta_2
        else:
            theta_1 = np.arcsin(n * np.sin(theta_2))

        x = ((-1 * d_f) + (d_rel*self.cot(theta_laser))) / \
            ((self.cot(theta_1)) + (self.cot(theta_laser)))
        y = d_f + (x * self.cot(theta_1))

        return (x, y)

    def distance_calc_tri(self, d_rel: float, b: float, pixel_pitch: float, peak: float) -> float:
        '''calculate object distance use "triangle's similar ratio". \n
            Args: 
                - d_rel[m] : relative distance (x-axis) between center of sensor to center of laser.[m]
                - b[m] : the constant value at "thin lens eq.", it means image distance.[m] \n
                        It is highly recommended to use measurements relative to an arbitrary reference point.
                - pixel_pitch[m] : distance between each pixel [m]
                - peak[pixel] : relative number of pixel about center of sensor's pixel. [pixel]

            Returns: float, vertical distance of object [m]

            Notes: it can use only when...
                - there is no y-axis deviation between light source and lens (there are aligned in y-axis).
                - light source and sensor are orthogonal.
                - sensor and lens's optic axis are orthogonal.
                - cartesian coord.
                - if you can assume a thin lens.(or optic path is pass through the center of the lens.)
                - there is no z-axis deviation. (sensor - lens - object point - light source are aligned in z-axis).
        '''
        return (b*d_rel)/(peak*pixel_pitch)
