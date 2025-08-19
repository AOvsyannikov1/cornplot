class ColorGenerator:
    COLORS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
              "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

    def __init__(self):
        self.color_index = 0

    def get_color(self):
        ret = self.COLORS[self.color_index]
        self.color_index += 1
        if self.color_index >= len(self.COLORS):
            self.color_index = 0
        return ret

    def one_color_back(self):
        if self.color_index > 0:
            self.color_index -= 1

    def reset(self):
        self.color_index = 0
