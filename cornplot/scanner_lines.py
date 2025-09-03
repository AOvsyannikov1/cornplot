class VerticalLine:

    def __init__(self):
        self.__x = 0.0
        self.__selected = False
        self.__visible = False

    def set_x_coord(self, x: float):
        self.__x = x

    def x(self):
        return self.__x
    
    def show(self):
        self.__visible = True

    def hide(self):
        self.__visible = False

    def is_visible(self):
        return self.__visible
    
    def is_selected(self):
        return self.__selected
    
    def select(self, val: bool):
        self.__selected = val


class VerticalLineList(list[VerticalLine]):

    def __init__(self, n):
        for _ in range(n):
            self.append(VerticalLine())

        self.last_line = 0
        self.nearest_line = -1

    def get_nearest_line(self) -> VerticalLine:
        return self[self.nearest_line]
    
    def line_under_mouse(self):
        return self.nearest_line >= 0

    def line_count(self):
        res = 0
        for l in self:
            if l.is_visible():
                res += 1
        return res
    
    def any_selected(self):
        return any(l.is_selected() and l.is_visible() for l in self)
    
    def select_line(self):
        ...

    def add_line(self, coord):
        for l in self:
            if not l.is_visible():
                l.show()
                l.set_x_coord(coord)
                break
