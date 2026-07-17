import numpy as np
from random import uniform
from .console_plotter import _plotter as plt
from .utils import UPPER_INDEXES


class SecondOrderLink:

    def __init__(self, t1, t2, dt, y0=0, v0=0):
        self.dt = dt
        self.T1 = t1
        self.T2 = t2

        self.v = v0
        self.y = y0

    def dv(self, x_in, v, y):
        return (1 * x_in - (self.T1 + self.T2) * v - y) / (self.T1 * self.T2)

    def process(self, x_in):
        self.v += self.dv(x_in, self.v, self.y) * self.dt
        self.y += self.v * self.dt

        return self.y
    

class RealDiffLink:

    def __init__(self, kd, td, dt):
        self.T = td
        self.diff_output = 0
        self.prev_input = 0
        self.Kd = kd
        self.dt = dt

    def deriv_process(self, x_in, dt=0.0):
        if dt > 0:
            self.dt = dt

        deriv = (x_in - self.prev_input) / self.dt
        self.prev_input = x_in
        self.diff_output += (self.Kd * deriv - self.diff_output) / self.T * self.dt
        return self.diff_output


class PID(RealDiffLink):

    def __init__(self, kp, ki, kd, td, dt):
        super().__init__(kd, td, dt)
        self.Kp = kp
        self.Ki = ki
        self.dt = dt
        self.integral = 0

    def control(self, target, value, dt=0.0):
        if dt > 0:
            self.dt = dt
        e = target - value
        self.integral += e * self.dt
        derivative = self.deriv_process(e)
        return self.Kp * e + self.Ki * self.integral + derivative

    def reset(self):
        self.diff_output = 0
        self.integral = 0


def show_demo_plots_1(dark=False):
    X = np.arange(-10, 10, 0.005)
    Y1 = np.sin(X)
    Y2 = np.cos(X)
    sigma = 2
    m = 0
    Y3 = (1 / np.sqrt(sigma * 2 * np.pi) * np.exp(-(X - m) ** 2 / (2 * sigma ** 2)))
    Y4 = (1 / (1 + np.exp(-X)))
    Y5 = (1 / np.sqrt(1 + X ** 2))
    Y6 = np.tanh(X)

    plt.set_dark(dark)
    plt.window(1, x=50, y=50)
    plt.plot(X, Y1, plot_label="Sin x", axes=True)
    plt.plot(X, Y2, plot_label="Cos x", axes=True)
    plt.plot(X, Y3, plot_label="Gauss", axes=True)
    plt.plot(X, Y4, plot_label="Sigmoid", axes=True)

    plt.window(2, x=200, y=100)
    plt.subplot(2, 3, 1)
    plt.set_font("Times new roman", 14)
    plt.plot(X, Y1, plot_label="Sin x")

    plt.subplot(2, 3, 2)
    plt.plot(X, Y2, plot_label="Cos x")

    plt.subplot(2, 3, 3)
    plt.plot(X, Y3, plot_label="Гауссоида")

    plt.subplot(2, 3, 4)
    plt.plot(X, Y4, plot_label="Логистическая кривая")

    plt.subplot(2, 3, 5)
    plt.plot(X, Y5, plot_label=f"1 / sqrt(1 + x{UPPER_INDEXES[2]})")

    plt.subplot(2, 3, 6)
    plt.plot(X, Y6, plot_label="Сигмоида")

    plt.window(3, x=500, y=200)
    plt.subplot(6, 1, 1)
    plt.plot(X, Y1, plot_label="Sin x", draw_x=False)

    plt.subplot(6, 1, 2)
    plt.plot(X, Y2, plot_label="Cos x", draw_x=False)

    plt.subplot(6, 1, 3)
    plt.plot(X, Y3, plot_label="Гауссоида", draw_x=False)

    plt.subplot(6, 1, 4)
    plt.plot(X, Y4, plot_label="Логистическая кривая", draw_x=False)

    plt.subplot(6, 1, 5)
    plt.plot(X, Y5, plot_label=f"1 / sqrt(1 + x{UPPER_INDEXES[2]})", draw_x=False)

    plt.subplot(6, 1, 6)
    plt.plot(X, Y6, plot_label="Сигмоида")
    plt.show()


def show_demo_plots_2(dark=False):
    X = np.arange(-10, 10, 0.005)
    Y1 = np.sin(X)
    Y2 = np.cos(X)
    sigma = 2
    m = 0
    Y3 = (1 / np.sqrt(sigma * 2 * np.pi) * np.exp(-(X - m) ** 2 / (2 * sigma ** 2)))
    Y4 = (1 / (1 + np.exp(-X)))
    Y5 = (1 / np.sqrt(1 + X ** 2))
    Y6 = np.tanh(X)
    plt.set_dark(dark)
    plt.window(1)
    plt.subplot(2, 2, 1)
    plt.plot(X, Y1, plot_label="Sin x")

    plt.subplot(2, 2, 3)
    plt.plot(X, Y2, plot_label="Cos x")

    plt.subplot(2, 1, 2)
    plt.plot(X, Y3, plot_label="Гауссоида")

    plt.window(2)
    plt.subplot(1, 3, 1)
    plt.plot(X, Y5, plot_label="1 / sqrt(1 + x^2)")

    plt.subplot(2, 3, 3)
    plt.plot(X, Y1, plot_label="Sin x")

    plt.subplot(2, 3, 4)
    plt.plot(X, Y4, plot_label="Сигмоида 1")

    plt.subplot(1, 3, 3)
    plt.plot(X, Y6, plot_label="Сигмоида 2")
    plt.show()


def show_demo_plots_3(dark=False):
    t = np.arange(0, 6 * np.pi, 0.005)
    X = np.exp(-0.2 * t) * np.sin(t)
    Y = np.exp(-0.2 * t) * np.cos(t)

    t = np.arange(0, 2 * np.pi, 0.005)
    X1 = 16 * np.sin(t) ** 3
    Y1 = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)

    X2 = 2 * np.cos(t) + np.cos(2 * t)
    Y2 = 2 * np.sin(t) - np.sin(2 * t)

    X3 = 2 * np.sin(t) ** 3
    Y3 = 2 * np.cos(t) ** 3

    X4 = 20 * (np.cos(t) + np.cos(5 * t) / 5)
    Y4 = 20 * (np.sin(t) - np.sin(5 * t) / 5)

    X5 = (1 + np.cos(t)) * np.cos(t)
    Y5 = (1 + np.cos(t)) * np.sin(t)

    X6 = 6 * np.cos(t) - 4 * np.cos(t) ** 3
    Y6 = 4 * np.sin(t) ** 3

    X7 = 8 * (np.cos(t) - np.cos(4 * t) / 4)
    Y7 = 8 * (np.sin(t) - np.sin(4 * t) / 4)

    t = np.arange(0, 12 * np.pi, 0.005)
    X8 = np.sin(t) * (np.exp(np.cos(t)) - 2 * np.cos(4 * t) + np.sin(t / 12) ** 5)
    Y8 = np.cos(t) * (np.exp(np.cos(t)) - 2 * np.cos(4 * t) + np.sin(t / 12) ** 5)
    
    plt.set_dark(dark)
    plt.subplot(3, 3, 1)
    plt.plot(X, Y, plot_label="Спираль", link_plots=False)

    plt.subplot(3, 3, 2)
    plt.plot(X1, Y1, plot_label="Сердце", link_plots=False)

    plt.subplot(3, 3, 3)
    plt.plot(X2, Y2, plot_label="Дельтоида", link_plots=False)

    plt.subplot(3, 3, 4)
    plt.plot(X3, Y3, plot_label="Астроида", link_plots=False)

    plt.subplot(3, 3, 5)
    plt.plot(X4, Y4, plot_label="Гипоциклоида", link_plots=False)

    plt.subplot(3, 3, 6)
    plt.plot(X5, Y5, plot_label="Кардиоида", link_plots=False)

    plt.subplot(3, 3, 7)
    plt.plot(X6, Y6, plot_label="Нефроида", link_plots=False)

    plt.subplot(3, 3, 8)
    plt.plot(X7, Y7, plot_label="Эпициклоида", link_plots=False)

    plt.subplot(3, 3, 9)
    plt.plot(X8, Y8, plot_label="Бабочка", link_plots=False)
    plt.show()


def show_demo_plots_4(dark=False):
    X = np.arange(0, 0.04, 1e-5)
    Y = 220 * np.sqrt(2) * np.sin(314 * X)

    plt.set_dark(dark)
    plt.plot(X, Y, plot_label="Переменный ток")
    plt.show()


def show_demo_plots_5(dark=False):
    X = np.arange(-2, 2, 0.0011)
    X1 = np.arange(0.5, 2, 0.001)

    plt.set_dark(dark)
    plt.plot(X, 1 / X, plot_label="", axes=True)
    plt.plot(X1, 1 / X1 + 10, plot_label="", axes=True)
    plt.auxiliary_line("10")
    plt.auxiliary_line("-1*x+8")
    plt.auxiliary_line("-x+12")
    plt.show()


def show_demo_plots_6(dark=False):
    X = np.arange(-3.14, 3.14, 0.01)
    Y1 = np.sin(X)
    Y2 = np.cos(X)

    plt.set_dark(dark)
    plt.fill_between(X, Y1, Y2, plot_label="Sin and Cos")
    plt.show()


def show_demo_histogram(dark=False):
    X = np.random.beta(a=2, b=5, size=100000)

    plt.set_dark(dark)
    plt.window(1)
    plt.histogram(X, hist_label="Бета-распределение", probabilities=True)
    plt.window(2)
    X = np.random.chisquare(df=10, size=100000)
    
    plt.histogram(X, hist_label=f"Распределение χ{UPPER_INDEXES[2]} (k = 10)", probabilities=True, color="#73C991")
    plt.show()


def show_demo_bar_chart(dark=False):
    months = ("Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек")
    temperatures = {
                    "Москва": [-6.2, -5.9, -0.7, 6.9, 13.6, 17.3, 19.7, 17.6, 11.9, 5.8, -0.5, -4.4],
                    "Сочи": [6.3, 6.5, 8.6, 12.3, 16.6, 20.9, 23.7, 24.3, 20.5, 16.2, 11.4, 8.3],
                    "Оймякон": [-46, -42.2, -35.2, -15.1, -0.2, 12.2, 14.1, 9.7, -0.2, -20.3, -36.7, -45.8]
                    }
    plt.set_dark(dark)
    plt.bar_chart(months, temperatures, y_label="T, °C", legend_loc='left')
    plt.show()


def show_demo_animation(dark=False):
    import time
    from .plot_updater import PlotUpdater

    class Update(PlotUpdater):
        def __init__(self):
            super().__init__()
            self.link = SecondOrderLink(0.7, 1.1, 0.025)
            self.controller = PID(5, 2, 0.2, 1, 0.025)
            self.t = time.monotonic()
            self.target = 1

        def update_plot(self):
            t = time.monotonic()
            plt.add_point_to_animated_plot("Sin", t, 100000*(np.sin(t) * np.sin(t / 10)))
            plt.add_point_to_animated_plot("Cos", t, 100000*np.cos(t))

            if t - self.t >= 10:
                self.target = uniform(-1, 1)
                self.t = t

            u = self.controller.control(self.target, self.link.y)
            y = self.link.process(u)
            plt.add_point_to_animated_plot("Second order link", t, y)
            plt.add_point_to_animated_plot("Target", t, self.target)


    class Update1(PlotUpdater):
        def update_plot(self):
            t = time.monotonic()
            plt.add_point_to_animated_plot("sinsinsin", t, np.sin(t) + 0.3 * np.cos(3.5 * t))

    plt.set_dark(dark)
    plt.window(1, name="Sin, cos")
    plt.subplot(2, 1, 1)
    plt.animated_plot("Sin", x_size=30)
    plt.animated_plot("Cos", x_size=30)
    plt.subplot(2, 1, 2)
    plt.animated_plot("Second order link", x_size=30)
    plt.animated_plot("Target", x_size=30)
    plt.add_plot_updater(Update())

    plt.window(2, name="Sinsin", x=500, y=200)
    plt.animated_plot("sinsinsin", x_size=30, real_time=True)
    updater = Update1()
    updater.set_delay_ms(25)
    plt.add_plot_updater(updater)
    plt.show()


def show_demo_pie_chart(dark=False):
    perc = (78, 21, 1)
    cats = ("Азот", "Кислород", "Прочие газы")
    descrs = ("АЗОТ АЗОТ ЕГО ДОФИГА АЗОТ ОН НЕ ДЫШИТСЯ АЗОТ АЗООООООООООООООТ",
              "кислород любимый кислород что ж ты такой классный аааааааааа",
              "а прочие газы тут углекислый газ лох но им растения дышат")
    plt.set_dark(dark)
    plt.pie_chart(perc, cats, descrs)
    plt.show()


def show_demo_polar_plot(dark=False):
    plt.set_dark(dark)
    plt.window(1, "", w=900, h=800)

    plt.subplot(2, 2, 1)
    angles = np.arange(0, 2 * np.pi, np.pi / 1000)
    amplitudes = np.exp(-angles) + np.sin(2 * angles)
    plt.polar_plot(amplitudes, angles, color='red')

    plt.subplot(2, 2, 2)
    angles = np.arange(0, 8 * np.pi, np.pi / 1000)
    amplitudes = 2 * angles
    plt.polar_plot(amplitudes, angles)

    plt.subplot(2, 2, 3)
    angles = np.arange(0, 2 * np.pi, np.pi / 1000)
    amplitudes = np.sin(6 * angles)
    plt.polar_plot(amplitudes, angles, color='purple')

    plt.subplot(2, 2, 4)
    angles = np.arange(0, 8 * np.pi, np.pi / 1000)
    amplitudes = np.sin(3/4 * angles)
    plt.polar_plot(amplitudes, angles, color='green')
    plt.show()

