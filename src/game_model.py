from typing import Deque, Iterator
from random import randrange
from collections import deque

from src.coord import Coord
from src.direction import Direction

_DIRECTION_TO_DELTA = {
    Direction.UP: Coord(x=0, y=1),
    Direction.DOWN: Coord(x=0, y=-1),
    Direction.LEFT: Coord(x=-1, y=0),
    Direction.RIGHT: Coord(x=1, y=0),
}


class GameModel:

    __slots__ = ["_height", "_width", "_score", "_snake_state", "_alive", "_apple_position"]

    def __init__(self, width: int, height: int):
        assert height >= 3, "The board must be at least 3 units high!"
        assert width >= 2, "The board must be at least 2 units wide!"

        self._height = height
        self._width = width

        # Set member variables to stop Pip complaining. They all get overwritten in reset_state.
        self._score = 0
        self._snake_state: Deque[Coord] = deque()
        self._alive = True
        self._apple_position = Coord(0, 0)

        self.reset_state()

    def reset_state(self):
        """Initialises:
            _snake_state,
            _snake_length,
            _alive,
        """
        self._score = 0
        snake_head_pos = Coord(self._width // 2, self._height // 2)
        snake_body_pos = Coord(snake_head_pos.x, snake_head_pos.y - 1)
        self._snake_state = deque([snake_body_pos, snake_head_pos])
        self._alive = True
        self._new_apple_position()

    @property
    def snake_state(self) -> Iterator[Coord]:
        return iter(self._snake_state)

    @property
    def score(self) -> int:
        return self._score

    @property
    def apple_position(self) -> Coord:
        return self._apple_position

    @property
    def alive(self) -> bool:
        return self._alive

    def update(self, movement: Direction) -> None:
        """Update the state based on the movement given by delta.

        Args:
            movement: the direction that the snake head should move in this update.
        """
        # Easy out if the game is already over.
        if not self._alive:
            return

        # Find the possible next move:
        delta = _DIRECTION_TO_DELTA[movement]
        snake_head = self._snake_state[0]
        proposed_new_head = snake_head + delta

        # Check if it has gone outside the board:
        x_still_valid = (0 <= proposed_new_head.x < self._width)
        y_still_valid = (0 <= proposed_new_head.y < self._height)
        if not x_still_valid or not y_still_valid:
            self._alive = False
            return

        # Check if it has hit itself:
        # COMMENT: DOUBLE ENDED QUEUES AND NEGATIVE INDEXES. PYTHON IS CRAZY.
        current_tail = self._snake_state[-1]
        if proposed_new_head in self._snake_state and proposed_new_head != current_tail:
            self._alive = False
            return

        # If we reach this point, the proposed new head is valid. So we append it to the body.
        self._snake_state.appendleft(proposed_new_head)
        if proposed_new_head == self._apple_position:
            self._score += 1
            self._new_apple_position()
        else:
            self._snake_state.pop()

    def _new_apple_position(self) -> None:
        """Uniformly sample a new apple position through rejection sampling."""
        while True:
            x = randrange(0, self._width)
            y = randrange(0, self._height)
            proposed_pos = Coord(x, y)
            if proposed_pos not in self._snake_state:
                self._apple_position = proposed_pos
                return


if __name__ == "__main__":
    import doctest
    doctest.testmod()
