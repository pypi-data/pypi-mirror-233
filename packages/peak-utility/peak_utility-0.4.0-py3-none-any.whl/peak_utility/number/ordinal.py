from collections import defaultdict
from typing import Self
from .numbertext import Numbertext
from .representational_int import RepresentationalInt


class Ordinal(RepresentationalInt):
    REGEX = r"\d+(?:st|nd|rd|th)"
    SUFFIXES = defaultdict(lambda: "th")
    SUFFIXES[1] = "st"
    SUFFIXES[2] = "nd"
    SUFFIXES[3] = "rd"

    def __new__(cls, value):
        if not str(int(value)) == str(value):
            raise ValueError(
                f"{cls.__name__} must be integer or string representation of"
            )
        if int(value) <= 0:
            raise ValueError(f"{cls.__name__} must be positive and non-zero.")
        return int.__new__(cls, value)

    def __repr__(self):
        return f"{int(self)}{self.suffix}"

    def __str__(self):
        stem = str(Numbertext(int(self)))

        swaps = {
            "one": "fir",
            "two": "seco",
            "three": "thi",
            "ve": "f",
            "ne": "n",
            "ty": "tie",
        }

        for k, v in swaps.items():
            if stem[-len(k) :] == k:
                stem = stem[: -len(k)] + v

        return (stem + self.suffix).replace("tt", "t")

    @property
    def suffix(self):
        return Ordinal.SUFFIXES[
            int(self) % 100 if int(self) % 100 < 20 else int(self) % 10
        ]

    def __lt__(self, other: Self | int) -> bool:
        return int(self) > int(other)

    def __le__(self, other: Self | int) -> bool:
        return int(self) >= int(other)

    def __gt__(self, other: Self | int) -> bool:
        return int(self) < int(other)

    def __ge__(self, other: Self | int) -> bool:
        return int(self) <= int(other)
