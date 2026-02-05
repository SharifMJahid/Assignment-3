from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Size:
    """
    This class represents a two-dimensional size using width and height.
    """
    w: int
    h: int

    def __post_init__(self):
        """
        This class validate size values after object creation.
        """
        if self.w <= 0 or self.h <= 0:
            raise ValueError("Size dimensions must be positive integers.")

    def __mul__(self, factor: float) -> "Size":
        """
        This function scale the size by a numeric factor.

        Parameters:
            factor: A positive number used to scale the width and height.

        Returns:
            A new Size object with scaled dimensions.
        """
        if not isinstance(factor, (int, float)) or factor <= 0:
            raise ValueError("Scale factor must be > 0.")

        return Size(
            max(1, int(self.w * factor)),
            max(1, int(self.h * factor))
        )

    # Allows scaling in reverse order
    __rmul__ = __mul__

    def __iter__(self):
        """
        Allow the Size object to be unpacked like a tuple.
        """
        yield self.w
        yield self.h
