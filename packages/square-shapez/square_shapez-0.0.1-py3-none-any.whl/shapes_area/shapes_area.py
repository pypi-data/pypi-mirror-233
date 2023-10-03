import math
from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def get_perimetr(self) -> float | int:
        pass

    @abstractmethod
    def get_area(self) -> float | int:
        pass


# class MultiSideShape(Shape):
#     def __init__(self, side_count: int, side_values: list[float | int]):
#         self.side_count: int = side_count
#         self.side_values: list[float | int] = side_values
#
#     @abstractmethod
#     def get_area(self) -> float | int:
#         pass


class Circle(Shape):
    def __init__(self, radius: float | int):
        self.radius: float | int = radius

    def get_perimetr(self) -> float | int:
        return 2 * math.pi * self.radius

    def get_area(self) -> float | int:
        return math.pi * self.radius ** 2


class Triangle(Shape):
    def __init__(self, a, b, c: float | int):
        self.a: float | int = a
        self.b: float | int = b
        self.c: float | int = c

    def get_perimetr(self) -> float | int:
        return self.a + self.b + self.c

    def get_area(self) -> float | int:
        p = self.get_perimetr() / 2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    def is_rectangular(self) -> bool:
        if self.a > self.b and self.a > self.c:
            return self.a ** 2 == self.b ** 2 + self.c ** 2
        if self.b > self.a and self.b > self.c:
            return self.b ** 2 == self.a ** 2 + self.c ** 2
        return self.c ** 2 == self.a ** 2 + self.b ** 2


def calculate_area(shape: Shape) -> float | int:
    return shape.get_area()
