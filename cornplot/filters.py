import numpy as np


class MovingAverageFilter:
    def __init__(self, order):
        self.buffer = [0] * order
        self.order = order
        self.current_index = 0
        self.sum = 0

    def filter_data(self, data):
        self.current_index += 1
        if self.current_index >= self.order:
            self.current_index = 0
        self.sum -= self.buffer[self.current_index]
        self.sum += data
        self.buffer[self.current_index] = data
        return self.sum / self.order


class MedianFilter:
    def __init__(self, order):
        self.buffer = [0] * order
        self.order = order
        self.current_index = 0

    def filter_data(self, data):
        self.buffer[self.current_index] = data
        self.current_index += 1
        if self.current_index >= self.order:
            self.current_index = 0
        return np.median(self.buffer)


class ExponentialFilter:
    def __init__(self, k):
        self.k = k
        self.prev_val = 0
        self.is_first = True

    def filter_data(self, data):
        if self.is_first:
            self.is_first = False
            self.prev_val = data
            return data

        self.prev_val += self.k * (data - self.prev_val)
        return self.prev_val