"""
Main game loop for 'Aventuras Peluditas' (Fluffy Adventures).

This script initializes the game window, sets up the game environment, and manages 
the primary game loop. It handles:
- Pygame initialization
- Screen setup
- Menu screen with start button
- Level and player creation
- Game event processing
- Level scrolling with camera system
- Drawing game elements (clouds, floor, grass, houses, trees)
- Player movement and rendering

The game uses a side-scrolling mechanic with camera following the player.

Dependencies:
- pygame
- sys
- random
- Custom modules: Characters.Cats.P1.p1, Levels.L1, screens.menu
"""
import pygame
import sys
from Characters.Cats.P1.p1 import PlayerOne
from Levels.L1 import Level
from screens.menu import Menu
import random

pygame.init()

favicon = pygame.image.load("img/Logo/favicon.png")
pygame.display.set_icon(favicon)

W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Aventuras Peluditas")

WHITE = (255, 255, 255)
BG_COLOR = (173, 216, 230)

player = PlayerOne()
level = Level(1, "Fácil", BG_COLOR)
menu = Menu(screen, W, H, BG_COLOR)

clouds_large_pos = [[random.randint(0, W), random.randint(50, 150)] for _ in range(len(level.clouds_large))]
clouds_small_pos = [[random.randint(0, W), random.randint(200, 300)] for _ in range(len(level.clouds_small))]

clock = pygame.time.Clock()
offset = 0
level_length = 2000
game_started = False

while True:
    if not game_started:
        menu.draw()
        if menu.handle_events():
            game_started = True
            continue
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.mover(keys)
        
        if hasattr(level, 'left_limit') and hasattr(level, 'right_limit'):
            if player.pos[0] < level.left_limit:
                player.pos[0] = level.left_limit
            elif player.pos[0] > level.right_limit:
                player.pos[0] = level.right_limit

        target_x = player.pos[0]
        offset = target_x - W//2
        offset = max(0, min(offset, level_length - W))

        player_screen_x = target_x - offset

        screen.fill(BG_COLOR)
        
        adjusted_clouds_large = [[x - offset, y] for x, y in clouds_large_pos]
        adjusted_clouds_small = [[x - offset, y] for x, y in clouds_small_pos]
        
        level.draw_clouds(screen, adjusted_clouds_large, adjusted_clouds_small)
        level.draw_floor(screen, offset)
        level.draw_grass(screen, offset)
        level.draw_houses(screen, offset)
        level.draw_trees(screen, offset)

        player.draw(screen, player_screen_x)

    pygame.display.flip()
    clock.tick(60)
