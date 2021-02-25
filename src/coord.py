from typing import NamedTuple


class Coord(NamedTuple):
    """Coordinate class

    Example usage:
    >>> a = Coord(3, 2)
    >>> delta = Coord(0, 1)
    >>> a + delta
    Coord(x=3, y=3)
    """
    x: int
    y: int

    def __add__(self, other) -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
