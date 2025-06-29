import pygame
import sys

pygame.init()

ANCHO = 800
ALTO = 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Plataformas")

BLACK = (0, 0, 0)

imagen_personaje_idle = pygame.image.load("img/Cats/P1/cat.png")
imagen_personaje_idle = pygame.transform.scale(imagen_personaje_idle, (50, 50))

imagen_personaje_running1 = pygame.image.load("img/Cats/P1/cat_running1.png")
imagen_personaje_running1 = pygame.transform.scale(imagen_personaje_running1, (50, 50))

imagen_personaje_running2 = pygame.image.load("img/Cats/P1/cat_running2.png")
imagen_personaje_running2 = pygame.transform.scale(imagen_personaje_running2, (50, 50))

player_pos = [100, 500]
player_speed = 5
gravity = 0.5
player_velocity_y = 0
ground_level = 500
jump_strength = -15
can_double_jump = False

is_flipping = False
flip_duration = 20
flip_timer = 0

facing_right = True

running_animation_frames = [imagen_personaje_running1, imagen_personaje_running2]
current_frame = 0
animation_speed = 5
animation_counter = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
        facing_right = False
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
        facing_right = True

    if keys[pygame.K_UP]:
        if player_pos[1] == ground_level:
            player_velocity_y = jump_strength
            can_double_jump = True
        elif can_double_jump:
            player_velocity_y = jump_strength
            can_double_jump = False
            is_flipping = True
            flip_timer = flip_duration

    player_velocity_y += gravity
    player_pos[1] += player_velocity_y

    if player_pos[1] >= ground_level:
        player_pos[1] = ground_level
        player_velocity_y = 0
        can_double_jump = False
        is_flipping = False

    if is_flipping:
        flip_timer -= 1
        if flip_timer <= 0:
            is_flipping = False

    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        if player_pos[1] == ground_level:
            animation_counter += 1
            if animation_counter >= animation_speed:
                current_frame = (current_frame + 1) % len(running_animation_frames)
                animation_counter = 0

    screen.fill(BLACK)

    if player_pos[1] < ground_level:
        if facing_right:
            screen.blit(imagen_personaje_idle, (player_pos[0], player_pos[1]))
        else:
            flipped_image = pygame.transform.flip(imagen_personaje_idle, True, False)
            screen.blit(flipped_image, (player_pos[0], player_pos[1]))
    else:
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            if facing_right:
                screen.blit(running_animation_frames[current_frame], (player_pos[0], player_pos[1]))
            else:
                flipped_image = pygame.transform.flip(running_animation_frames[current_frame], True, False)
                screen.blit(flipped_image, (player_pos[0], player_pos[1]))
        else:
            if facing_right:
                screen.blit(imagen_personaje_idle, (player_pos[0], player_pos[1]))
            else:
                flipped_image = pygame.transform.flip(imagen_personaje_idle, True, False)
                screen.blit(flipped_image, (player_pos[0], player_pos[1]))

    pygame.display.flip()
    pygame.time.Clock().tick(60)
