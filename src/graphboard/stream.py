from typing import Callable
import numpy as np


class Stream:

    def __init__(self, get_data: Callable[[],np.array]):
        pass

    def main_callback(self) -> np.array:
        return np.zeros(100)