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
