from typing import Iterator, Tuple

from src.coord import Coord

import pygame

# Define colour constants
_BLACK = (0, 0, 0)
_WHITE = (255, 255, 255)
_BLUE = (0, 0, 255)
_YELLOW = (255, 255, 0)
_GREEN = (0, 255, 0)
_DARK_GREEN = (0, 128, 0)


class GameView:
    def __init__(self, width: int, height: int, game_cols: int, game_rows: int, grid_weight: int = 2, border_size: int = 10):
        """Initialise the GameView window.

        Args:
            width: the width of the window in pixels.
            height: the height of the window in pixels.
            game_cols: the number of columns in the snake game.
            game_rows: the number of rows in the snake game.
            grid_weight: the thickness of the grid in pixels.
            border_size: the border around the grid in pixels.
        """
        assert width > 0, "Must have a positive window width."
        assert height > 0, "Must have a positive window height."
        self._width = width
        self._height = height
        self._size = (width, height)

        self._rows = game_rows
        self._cols = game_cols
        self._grid_weight = grid_weight

        # Now we calculate what the grid size should be:
        max_grid_width = self._width - 2 * border_size
        max_box_width = max_grid_width // self._cols
        max_grid_height = self._height - 2 * border_size
        max_box_height = max_grid_height // (self._rows + 1)  # Add a dummy row to display the score.
        self._grid_size = min(max_box_height, max_box_width)

        # And now what the actual grid border will be:
        actual_grid_width = self._grid_size * self._cols
        actual_grid_height = self._grid_size * (self._rows + 1)
        self._side_border = (self._width - actual_grid_width) // 2
        self._top_border = (self._height - actual_grid_height) // 2 + self._grid_size  # Blank dummy row for score.

        self._screen = pygame.display.set_mode(self._size)
        self._screen.fill(_BLACK)

        self._font = pygame.font.SysFont("monospace", size=self._grid_size // 2)

    def _coord_to_square_top_left(self, coord: Coord) -> Tuple[int, int]:
        x = self._side_border + coord.x * self._grid_size
        y = self._top_border + (self._rows - coord.y - 1) * self._grid_size
        return x, y

    def update_view(self, snake_pos: Iterator[Coord], apple_pos: Coord, score: int):
        self._screen.fill(_BLACK)
        self._draw_snake(snake_pos)
        self._draw_apple(apple_pos)
        self._draw_score(score)
        self._draw_grid()
        pygame.display.flip()

    def game_over(self):
        self._draw_grid(color=_YELLOW)
        pygame.display.flip()

    def _draw_snake(self, snake_pos: Iterator[Coord]):
        color = _GREEN
        for coord in snake_pos:
            x, y = self._coord_to_square_top_left(coord)
            rect = pygame.Rect(x, y, self._grid_size, self._grid_size)
            pygame.draw.rect(self._screen, color, rect)
            color = _DARK_GREEN

    def _draw_apple(self, apple_pos: Coord):
        x, y = self._coord_to_square_top_left(apple_pos)
        red = (255, 0, 0)
        rect = pygame.Rect(x, y, self._grid_size, self._grid_size)
        pygame.draw.rect(self._screen, red, rect)

    def _draw_score(self, score: int):
        antialias = True
        label = self._font.render(str(score), antialias, _WHITE)
        x = self._width // 2
        y = self._top_border // 2 - self._grid_size // 2
        top_middle = (x, y)
        self._screen.blit(label, top_middle)

    def _draw_grid(self, color=_BLUE) -> None:
        for i in range(self._rows):
            for j in range(self._cols):
                x = j * self._grid_size + self._side_border
                y = i * self._grid_size + self._top_border
                rect = pygame.Rect(x, y, self._grid_size, self._grid_size)
                pygame.draw.rect(self._screen, color, rect, width=self._grid_weight)


if __name__ == "__main__":
    pygame.init()
    gv = GameView(600, 800, 10, 10, grid_weight=2)
    snake_pos = iter([Coord(0, 0), Coord(1, 0), Coord(1, 1), Coord(1, 2)])
    apple_pos = Coord(2, 2)
    gv.update_view(snake_pos, apple_pos, 3)
    pygame.time.wait(5000)



