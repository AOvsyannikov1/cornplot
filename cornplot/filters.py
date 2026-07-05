from statistics import median


class MovingAverageFilter:
    __slots__ = "__buffer", "__order", "__current_index", "__sum"
    def __init__(self, order):
        self.__buffer = [0] * order
        self.__order = order
        self.__current_index = 0
        self.__sum = 0

    def filter_data(self, data):
        self.__current_index += 1
        if self.__current_index >= self.__order:
            self.__current_index = 0
        self.__sum -= self.__buffer[self.__current_index]
        self.__sum += data
        self.__buffer[self.__current_index] = data
        return self.__sum / self.__order


class MedianFilter:
    __slots__ = "__buffer", "__order", "__current_index",
    def __init__(self, order):
        self.__buffer = [0] * order
        self.__order = order
        self.__current_index = 0

    def filter_data(self, data):
        self.__buffer[self.__current_index] = data
        self.__current_index += 1
        if self.__current_index >= self.__order:
            self.__current_index = 0
        return median(self.__buffer)


class ExponentialFilter:
    __slots__ = "__k", "__prev_val", "__is_first"

    def __init__(self, k):
        self.__k = k
        self.__prev_val = 0
        self.__is_first = True

    def filter_data(self, data):
        if self.__is_first:
            self.__is_first = False
            self.__prev_val = data
            return data

        y = self.__k * data + (1 - self.__k) * self.__prev_val
        self.__prev_val = y
        return self.__prev_val