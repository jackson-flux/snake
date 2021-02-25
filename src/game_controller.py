from typing import NoReturn
import sys

import pygame

from src.game_model import GameModel
from src.game_view import GameView
from src.direction import Direction


def game_loop(game_model: GameModel, game_view: GameView, delay: int = 10000) -> NoReturn:
    key_to_action = {pygame.K_LEFT: Direction.LEFT, pygame.K_RIGHT: Direction.RIGHT, pygame.K_UP: Direction.UP, pygame.K_DOWN: Direction.DOWN}
    next_action = Direction.UP
    while True:

        # Handle user input:
        # COMMENT: DOES PYGAME.EVENT GET RESET AFTER YOU ACCESS IT?
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # COMMENT: I ASSUME THIS IS WHERE THE "USER OVERLOAD" ISSUE STEMS FROM - THE PYGAME EVENT LIST IS ADDED TO WHILE WE'RE IN THIS LOOP?
                # FEELS LIKE IF 'EVENTS' IS A LIST, THIS SHOULD BE PREPARED FOR THERE TO BE MULTIPLE NEXT ACTIONS HERE
                next_action = key_to_action[event.key]

        # Update game model:
        game_model.update(next_action)

        # Update game view:
        game_view.update_view(game_model.snake_state, game_model.apple_position, game_model.score)

        # Deal with game over:
        if not game_model.alive:
            game_view.game_over()
            time_delay = 3000
            pygame.time.wait(time_delay)
            game_model.reset_state()
            # Update game view:
            game_view.update_view(game_model.snake_state, game_model.apple_position, game_model.score)

        # Wait to make the game easier:
        time_delay = delay // (10 + game_model.score)
        pygame.time.wait(time_delay)


if __name__ == "__main__":
    pygame.init()

    game_rows = 10
    game_cols = 10
    game_height = 600
    game_width = 800

    game_model = GameModel(width=game_cols, height=game_rows)
    game_view = GameView(width=game_width, height=game_height, game_cols=game_cols, game_rows=game_rows)

    game_loop(game_model, game_view)
