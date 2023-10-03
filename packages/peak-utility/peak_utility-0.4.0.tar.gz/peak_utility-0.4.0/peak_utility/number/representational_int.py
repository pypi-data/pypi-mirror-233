from typing import Self


class RepresentationalInt(int):
    """
    A class for integers that are for representational use only,
    i.e. no arithmetic operations can be performed on them, but comparisons can.
    Can only be initialised with another int or str representation of it.

    """

    def __new__(cls, value: int | str) -> Self:
        if not str(int(value)) == str(value):
            raise ValueError(f"{cls.__name__} must represent an integer value")

        return super().__new__(cls, value)

    def __add__(self, other: int) -> int:
        raise TypeError(f"Instances of {self.__class__.__name__} cannot be added")

    def __sub__(self, other: int) -> int:
        raise TypeError(f"Instances of {self.__class__.__name__} cannot be subtracted")

    def __matmul__(self, other: int) -> int:
        raise TypeError(f"Instances of {self.__class__.__name__} cannot be multiplied")

    def __mul__(self, other: int) -> int:
        raise TypeError(f"Instances of {self.__class__.__name__} cannot be multiplied")

    def __floordiv__(self, other: int) -> int:
        raise TypeError(f"Instances of {self.__class__.__name__} cannot be divided")

    def __truediv__(self, other: int) -> float:
        raise TypeError(f"Instances of {self.__class__.__name__} cannot be divided")

    def __mod__(self, other: int) -> int:
        raise TypeError(f"Instances of {self.__class__.__name__} cannot be divided")

    def __divmod__(self, other: int) -> tuple[int, int]:
        raise TypeError(f"Instances of {self.__class__.__name__} cannot be divided")

    def __pow__(self, other: int) -> int:  # type: ignore
        raise TypeError(
            f"Instances of {self.__class__.__name__} cannot be raised to a power"
        )
