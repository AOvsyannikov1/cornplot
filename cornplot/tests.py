import numpy as np
from .core import plt


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

    plt.window(1)
    plt.plot(X, Y1, name="Sin x")
    plt.plot(X, Y2, name="Cos x")
    plt.plot(X, Y3, name="Gauss")
    plt.plot(X, Y4, name="Sigmoid")

    plt.window(2)
    plt.subplot(2, 3, 1, link_plots=True)
    plt.plot(X, Y1, name="Sin x")

    plt.subplot(2, 3, 2, link_plots=True)
    plt.plot(X, Y2, name="Cos x")

    plt.subplot(2, 3, 3, link_plots=True)
    plt.plot(X, Y3, name="Гауссоида")

    plt.subplot(2, 3, 4, link_plots=True)
    plt.plot(X, Y4, name="Логистическая кривая")

    plt.subplot(2, 3, 5)
    plt.plot(X, Y5, name="1 / sqrt(1 + x^2)")

    plt.subplot(2, 3, 6, link_plots=True)
    plt.plot(X, Y6, name="Сигмоида")

    plt.window(3)
    plt.subplot(6, 1, 1, link_plots=True)
    plt.plot(X, Y1, name="Sin x")

    plt.subplot(6, 1, 2, link_plots=True)
    plt.plot(X, Y2, name="Cos x")

    plt.subplot(6, 1, 3, link_plots=True)
    plt.plot(X, Y3, name="Гауссоида")

    plt.subplot(6, 1, 4, link_plots=True)
    plt.plot(X, Y4, name="Логистическая кривая")

    plt.subplot(6, 1, 5, link_plots=True)
    plt.plot(X, Y5, name="1 / sqrt(1 + x^2)")

    plt.subplot(6, 1, 6, link_plots=True)
    plt.plot(X, Y6, name="Сигмоида")
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

    plt.window(1)
    plt.subplot(2, 2, 1, link_plots=True)
    plt.plot(X, Y1, name="Sin x")

    plt.subplot(2, 2, 3, link_plots=True)
    plt.plot(X, Y2, name="Cos x")

    plt.subplot(2, 1, 2, link_plots=True)
    plt.plot(X, Y3, name="Гауссоида")

    plt.window(2)
    plt.subplot(1, 3, 1, link_plots=True)
    plt.plot(X, Y5, name="1 / sqrt(1 + x^2)")

    plt.subplot(2, 3, 3, link_plots=True)
    plt.plot(X, Y1, name="Sin x")

    plt.subplot(2, 3, 4, link_plots=True)
    plt.plot(X, Y4, name="Сигмоида 1")

    plt.subplot(1, 3, 3, link_plots=True)
    plt.plot(X, Y6, name="Сигмоида 2")
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

    plt.subplot(3, 3, 1, axes=True)
    plt.plot(X, Y, name="Спираль")

    plt.subplot(3, 3, 2, axes=True)
    plt.plot(X1, Y1, name="Сердце")

    plt.subplot(3, 3, 3, axes=True)
    plt.plot(X2, Y2, name="Дельтоида")

    plt.subplot(3, 3, 4, axes=True)
    plt.plot(X3, Y3, name="Астроида")

    plt.subplot(3, 3, 5, axes=True)
    plt.plot(X4, Y4, name="Гипоциклоида")

    plt.subplot(3, 3, 6, axes=True)
    plt.plot(X5, Y5, name="Кардиоида")

    plt.subplot(3, 3, 7, axes=True)
    plt.plot(X6, Y6, name="Нефроида")

    plt.subplot(3, 3, 8, axes=True)
    plt.plot(X7, Y7, name="Эпициклоида")

    plt.subplot(3, 3, 9)
    plt.plot(X8, Y8, name="Бабочка")
    plt.show()


def show_demo_plots_4():
    X = np.arange(-10, 10, 1)
    Y = np.exp(0.2 * X)
    Y1 = -np.exp(0.2 * X)
    plt.plot(X, Y, name="Гистограмма", axes=True)
    plt.plot(X, Y1, name="Гистограмма1", axes=True)
    plt.show()


def show_demo_plots_5():
    X = np.arange(0, 0.04, 1e-5)
    Y = 220 * np.sqrt(2) * np.sin(314 * X)

    plt.plot(X, Y, name="Переменный ток")
    plt.show()


def show_demo_plots_6():
    X = np.random.beta(a=2, b=5, size=100000)

    plt.hist(X, bins=25, name="Бета-распределение")
    plt.show()


def show_demo_pie_chart():
    perc = (78, 21, 1)
    cats = ("Азот", "Кислород", "Прочие газы")
    descrs = ("АЗОТ АЗОТ ЕГО ДОФИГА АЗОТ ОН НЕ ДЫШИТСЯ АЗОТ АЗООООООООООООООТ",
              "кислород любимый кислород что ж ты такой классный аааааааааа",
              "а прочие газы тут углекислый газ лох но им растения дышат")

    X = np.arange(-10, 10, 0.005)
    Y1 = np.sin(X)
    Y2 = np.cos(X)
    plt.subplot(2, 2, 1, link_plots=True)
    plt.plot(X, Y1, name="Sin x")

    plt.subplot(2, 2, 2, link_plots=True)
    plt.plot(X, Y2, name="Cos x")

    plt.subplot(2, 2, 3, pie_chart=True)
    plt.pie_chart(perc, cats, descrs)

    plt.subplot(2, 2, 4)
    X = np.random.beta(a=2, b=1.5, size=10000)
    plt.hist(X, bins=25, name="Нормальное распределение", color='heatmap')
    plt.show()

