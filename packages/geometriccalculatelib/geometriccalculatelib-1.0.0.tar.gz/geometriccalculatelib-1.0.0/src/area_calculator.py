import math

from abc import ABC, abstractmethod


class Figure(ABC):
    """
    Абстрактный базовый класс для геометрических фигур.

    Абстрактные методы:
        area(): Абстрактный метод, который должен быть реализован в подклассах.
    """

    @abstractmethod
    def area(self):
        pass


class Circle(Figure):
    """
       Класс представляющий круг.

       Атрибуты:
           r (float): Радиус круга.

       Методы:
           area(): Возвращает площадь круга.
           __str__(): Возвращает строковое представление круга.
       """

    def __init__(self, r):
        if r <= 0:
            raise ValueError("Radius cannot be negative")
        self.r = r

    def area(self):
        return math.pi * self.r ** 2

    def __str__(self):
        return f"Circle with radius: {self.r}"


class Triangle(Figure):
    """
       Класс, представляющий треугольник.

       Атрибуты:
           a, b, c (float): Длины сторон треугольника.

       Методы:
           area(): Возвращает площадь треугольника.
           __str__(): Возвращает строковое представление треугольника.
       """

    def __init__(self, a, b, c):
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("Side lengths must be positive numbers")
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def __str__(self):
        return f"Triangle with sides: {self.a, self.b, self.c}"


class TriangleType:
    """
        Класс предоставляющий методы для определения типа(вида) треугольника.

        Методы:
            is_right_triangle(triangle): Проверяет, является ли треугольник прямоугольным.

        """

    @staticmethod
    def is_right_triangle(triangle):
        return triangle.a ** 2 + triangle.b ** 2 == triangle.c ** 2


class FigureArea:
    """
        Класс для вычисления площади фигуры.

        Атрибуты:
            figure (Figure): Экземпляр геометрической фигуры.

        Методы:
            calc_area(): Вычисляет площадь фигуры с использованием метода area() фигуры.
        """

    def __init__(self, figure):
        self.figure = figure

    def calc_area(self):
        return self.figure.area()

    def __str__(self):
        return f"{self.figure}"
