# Cornplot library #
В библиотеке реализовано построение различных видов графиков. Библиотека основана на PyQt6.

## Пример использования ##

    """ Создание простого окна PyQt и построение графиков в двух осях """
    from PyQt6 import QtCore, QtWidgets
    import cornplot as cp
    import numpy as np
    import time
    
    class Window(QtWidgets.QWidget):
  
      def __init__(self):
          super().__init__()
  
          self.setGeometry(100, 100, 1200, 1024)
  
          self.plt1 = cp.Dashboard(self, 100, 50, 1000, 300)
          self.plt2 = cp.Dashboard(self, 100, 400, 1000, 300)
  
          X = np.arange(-20, 20, 0.001)
          X1 = np.arange(-20, 20, 1)
          YY1 = 0.005 * X1 ** 2
          Y1 = np.sin(X)
          Y2 = 0.4 * np.cos(3*X)
          Y3 = np.sin(2*X + 0.1) + np.sin(0.68*X - 0.2)
  
          self.plt1.add_plot(X, Y1, name="SIN")
          self.plt1.add_plot(X, Y3, name="Косинус")
          self.plt1.add_plot(X1, YY1, name="Парабола")
          self.plt2.add_plot(X, Y1, name="SIN")
          self.plt2.add_plot(X, Y2, name="Косинус")
  
          self.plt1.move_to_group("1")
          self.plt2.move_to_group("1")
  
  
      def resizeEvent(self, a0):
          self.plt1.set_geometry(120, 50, self.width() - 200, self.height() // 4)
          self.plt2.set_geometry(120, self.plt1.y() + self.plt1.height() + 20, self.width() - 200, self.height() // 4)


----------
