import numpy as np
from .console_plotter import _plotter as plt
from .utils import UPPER_INDEXES


def show_demo_plots_1():
    X = np.arange(-10, 10, 0.005)
    Y1 = np.sin(X)
    Y2 = np.cos(X)
    sigma = 2
    m = 0
    Y3 = (1 / np.sqrt(sigma * 2 * np.pi) * np.exp(-(X - m) ** 2 / (2 * sigma ** 2)))
    Y4 = (1 / (1 + np.exp(-X)))
    Y5 = (1 / np.sqrt(1 + X ** 2))
    Y6 = np.tanh(X)

    plt.window(1, x=50, y=50)
    plt.plot(X, Y1, plot_label="Sin x")
    plt.plot(X, Y2, plot_label="Cos x")
    plt.plot(X, Y3, plot_label="Gauss")
    plt.plot(X, Y4, plot_label="Sigmoid")

    plt.window(2, x=200, y=100)
    plt.subplot(2, 3, 1)
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


def show_demo_plots_2():
    X = np.arange(-10, 10, 0.005)
    Y1 = np.sin(X)
    Y2 = np.cos(X)
    sigma = 2
    m = 0
    Y3 = (1 / np.sqrt(sigma * 2 * np.pi) * np.exp(-(X - m) ** 2 / (2 * sigma ** 2)))
    Y4 = (1 / (1 + np.exp(-X)))
    Y5 = (1 / np.sqrt(1 + X ** 2))
    Y6 = np.tanh(X)
    plt.set_dark(True)
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


def show_demo_plots_3():
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


def show_demo_plots_4():
    X = np.arange(0, 0.04, 1e-5)
    Y = 220 * np.sqrt(2) * np.sin(314 * X)

    plt.plot(X, Y, plot_label="Переменный ток")
    plt.show()


def show_demo_histogram():
    X = np.random.beta(a=2, b=5, size=100000)

    plt.window(1)
    plt.histogram(X, name="Бета-распределение", probabilities=True)
    plt.set_dark()
    plt.window(2)
    X = np.random.chisquare(df=10, size=100000)
    
    plt.histogram(X, name=f"Распределение χ{UPPER_INDEXES[2]} (k = 10)", probabilities=True, color="#73C991")
    plt.show()


def show_demo_bar_chart():
    months = ("Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек")
    temperatures = {
                    "Москва": [-6.2, -5.9, -0.7, 6.9, 13.6, 17.3, 19.7, 17.6, 11.9, 5.8, -0.5, -4.4],
                    "Сочи": [6.3, 6.5, 8.6, 12.3, 16.6, 20.9, 23.7, 24.3, 20.5, 16.2, 11.4, 8.3],
                    "Оймякон": [-46, -42.2, -35.2, -15.1, -0.2, 12.2, 14.1, 9.7, -0.2, -20.3, -36.7, -45.8]
                    }
    plt.window(1)
    plt.bar_chart(months, temperatures, y_label="T, °C", legend_loc='left')

    plt.set_dark()
    plt.window(2)
    plt.bar_chart(months, temperatures, y_label="T, °C", legend_loc='left')
    plt.show()


def show_demo_animation():
    import time
    from .plot_updater import PlotUpdater

    class Update(PlotUpdater):
        def update_plot(self):
            t = time.monotonic()
            plt.add_point_to_animated_plot("Sin", t, 100000*np.sin(t))
            plt.add_point_to_animated_plot("Cos", t, 100000*np.cos(t))
            plt.add_point_to_animated_plot("SinSin", t, np.sin(2 * t))
            plt.add_point_to_animated_plot("CosCos", t, np.cos(2 * t))


    class Update1(PlotUpdater):
        def update_plot(self):
            t = time.monotonic()
            plt.add_point_to_animated_plot("sinsinsin", t, np.sin(t) + 0.3 * np.cos(3.5 * t))

    plt.window(1, name="Sin, cos")
    plt.subplot(2, 1, 1)
    plt.animated_plot("Sin")
    plt.animated_plot("Cos")
    plt.subplot(2, 1, 2)
    plt.animated_plot("SinSin")
    plt.animated_plot("CosCos")
    plt.add_plot_updater(Update())

    plt.set_dark(True)
    plt.window(2, name="Sinsin", x=500, y=200)
    plt.animated_plot("sinsinsin")
    updater = Update1()
    updater.set_delay_ms(10)
    plt.add_plot_updater(updater)
    plt.show()


def show_demo_pie_chart():
    perc = (78, 21, 1)
    cats = ("Азот", "Кислород", "Прочие газы")
    descrs = ("АЗОТ АЗОТ ЕГО ДОФИГА АЗОТ ОН НЕ ДЫШИТСЯ АЗОТ АЗООООООООООООООТ",
              "кислород любимый кислород что ж ты такой классный аааааааааа",
              "а прочие газы тут углекислый газ лох но им растения дышат")

    plt.pie_chart(perc, cats, descrs)
    plt.show()


def show_demo_polar_plot():
    for i in range(2):
        plt.set_dark(i == 1)
        plt.window(i + 1, "", w=900, h=800)

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

