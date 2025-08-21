# CORNPLOT #
В библиотеке реализовано построение различных видов графиков, а также различные инструменты их анализа, такие как нахождение производной, интеграла,
преобразование Фурье и другие.
Библиотека основана на PyQt6, работает на Python 3.11+

## Демонстрационные примеры ##
	import cornplot as cp
	
	# Выберите один из примеров:
	cp.show_demo_plots_1()
	cp.show_demo_plots_2()
	cp.show_demo_plots_3()
	cp.show_demo_plots_4()
	cp.show_demo_plots_5()
	cp.show_demo_pie_chart()


----------


## Использование в составе окна PyQt ##

    from PyQt6 import QtCore, QtWidgets
    import cornplot as cp
    import numpy as np
    
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
          self.plt2.add_plot(X, Y1, name="SIN 1")
          self.plt2.add_plot(X, Y2, name="Косинус 1")
  
          self.plt1.move_to_group("1")
          self.plt2.move_to_group("1")
  
  
      def resizeEvent(self, a0):
          self.plt1.set_geometry(120, 50, self.width() - 200, self.height() // 4)
          self.plt2.set_geometry(120, self.plt1.y() + self.plt1.height() + 20, self.width() - 200, self.height() // 4)

	if __name__ == '__main__':
	    import sys
	    app = QtWidgets.QApplication(sys.argv)
	    ui = Window()
	    ui.show()
	    sys.exit(app.exec())



----------

## Построение статичных графиков ##

	import cornplot as cp
	import numpy as np
	
	X = np.arange(-20, 20, 0.001)
	Y1 = np.sin(X)
	Y2 = 0.4 * np.cos(3*X)
	Y3 = np.sin(2*X + 0.1) + np.sin(0.68*X - 0.2)
	
	cp.subplot(2, 1, 1)
	cp.plot(X, Y1, name="Sinus")
	cp.subplot(2, 1, 2)
	cp.plot(X, Y3)
	cp.show()

## Построение анимированных графиков ##

	import time
	
	import cornplot as cp
	import numpy as np
	
	
	class UpdateFig1(cp.PlotUpdater):
		"""Функция update_plot() вызывается в бесконечном цикле в отдельном потоке QThread."""
	    def update_plot(self):
	        t = time.monotonic()
	        cp.add_point_to_animated_plot("Sin", t, np.sin(t))
	        cp.add_point_to_animated_plot("Cos", t, np.cos(t))
	        cp.add_point_to_animated_plot("SinSin", t, np.sin(2 * t))
	        cp.add_point_to_animated_plot("CosCos", t, np.cos(2 * t))
	
	
	class UpdateFig2(cp.PlotUpdater):
		"""Период вызова по умолчанию 25 мс. Может быть изменён функцией set_delay_ms()"""
	    def update_plot(self):
	        t = time.monotonic()
	        cp.add_point_to_animated_plot("sinsinsin", t, np.sin(t) + 0.3 * np.cos(3.5 * t))
	
	
	cp.figure(1)
	cp.subplot(2, 1, 1)
	cp.animated_plot("Sin")
	cp.animated_plot("Cos")
	cp.subplot(2, 1, 2, link_subplots=False)
	cp.animated_plot("SinSin")
	cp.animated_plot("CosCos")
	cp.add_plot_updater(UpdateFig1())
	
	cp.figure(2)
	cp.animated_plot("sinsinsin")
	updater = UpdateFig2()
	updater.set_delay_ms(50)
	cp.add_plot_updater(updater)
	cp.show()