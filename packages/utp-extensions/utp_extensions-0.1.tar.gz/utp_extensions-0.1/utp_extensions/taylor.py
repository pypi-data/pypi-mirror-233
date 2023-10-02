from scipy.misc import derivative
import math


class TaylorSeries:
    def __init__(self, function: type(lambda x: x), order: int, center: int = 0):
        """
        Класс реализующий функционал ряда Тейлора
        :param function: - функция, для которой мы ищем ряд тейлора
        :param order: - порядок ряда тейлора
        :param center: - точка, в окресности которой происходит поиск ряда Тейлора
        """
        self.center = center
        self.f = function
        self.order = order
        self.d_pts = order * 2
        self.coefficients = []

        if self.d_pts % 2 == 0:
            self.d_pts += 1

        self.__find_coefficients()

    def __find_coefficients(self):
        """
        Метод, который вычисляет коэфициэнты
        :return:
        """
        for i in range(0, self.order + 1):
            self.coefficients.append(
                round(derivative(self.f, self.center, n=i, order=self.d_pts) / math.factorial(i), 5))

    def get_coefficients(self) -> list:
        """
        Метод возвращает коэфициэнты В ОБРАТНОМ ПОРЯДКЕ
        :return: Список коэфициэнтов
        """
        return self.coefficients

    def count_polynom(self, x: float) -> float:
        """
        Метод, считающий значение полинома
        :param x: - значение x
        :return: - значение y
        """
        end_value = 0
        for i in range(self.order + 1):
            end_value += self.coefficients[i] * ((x - self.center) ** i)
        return end_value

    def __str__(self):
        eqn_string = ""
        for i in range(self.order + 1):
            if self.coefficients[i] != 0:
                eqn_string += str(self.coefficients[i]) + ("(x-{})^{}".format(self.center, i) if i > 0 else "") + " + "
        eqn_string = eqn_string[:-3] if eqn_string.endswith(" + ") else eqn_string
        return eqn_string
