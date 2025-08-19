

class AxleSlider:

    def __init__(self):
        self.__mouse_on = False
        self.__x = -1
        self.__y = -1
        self.__w = -1
        self.__h = -1
        self.__pressed = False
        self.__x0 = -1
        self.__length = 0.2

    def set_mouse_on(self, on: bool):
        self.__mouse_on = on

    @property
    def x(self):
        return self.__x
    
    @x.setter
    def x(self, x):
        self.__x = x

    @property
    def x0(self):
        return self.__x0
    
    @x0.setter
    def x0(self, x):
        self.__x0 = x
    
    @property
    def y(self):
        return self.__y
    
    @y.setter
    def y(self, y):
        self.__y = y
    
    @property
    def w(self):
        return self.__w
    
    @w.setter
    def w(self, w):
        self.__w = w
    
    @property
    def h(self):
        return self.__h
    
    @h.setter
    def h(self, h):
        self.__h = h
    
    @property
    def length(self):
        return self.__length

    def mouse_on(self):
        return self.__mouse_on
    
    def press(self):
        self.__pressed = True

    def release(self):
        self.__pressed = False
    
    def is_pressed(self):
        return self.__pressed
    
    def set_initial_x(self, x0):
        self.__x0 = x0