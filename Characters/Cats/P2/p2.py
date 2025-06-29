import pygame
import sys
import random

pygame.init()
w = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Juego")
r = (255, 255, 0)

i_idle = pygame.image.load("img/Cats/P2/cat.png")
i_idle = pygame.transform.scale(i_idle, (80, 80))
i_run1 = pygame.image.load("img/Cats/P2/cat_running1.png")
i_run1 = pygame.transform.scale(i_run1, (80, 80))
i_run2 = pygame.image.load("img/Cats/P2/cat_running2.png")
i_run2 = pygame.transform.scale(i_run2, (80, 80))

pygame.mixer.init()
s_run = pygame.mixer.Sound("Sound/run-sound.mp3")
s_jump = pygame.mixer.Sound("Sound/jump-sound.mp3")

p_pos = [100, 500]
p_spd = 8
g = 0.5
v_y = 0
g_lvl = 500
j_rng = (-20, -18)
j_ok = True
j_cnt = 0

f_ok = False
f_time = 30
f_angle = 0
f_dir = 1

f_right = True

anim_frames = [i_run1, i_run2]
anim_idx = 0
anim_spd = 5
anim_cnt = 0

def play_run(run):
    if run:
        if not pygame.mixer.get_busy():
            s_run.play(-1)
    else:
        s_run.stop()

def play_jump(jump):
    if jump:
        s_jump.play()

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    k = pygame.key.get_pressed()
    running = False
    jumping = False

    if k[pygame.K_LEFT] or k[pygame.K_RIGHT]:
        if k[pygame.K_LEFT]:
            p_pos[0] -= p_spd
            f_right = False
        if k[pygame.K_RIGHT]:
            p_pos[0] += p_spd
            f_right = True
        running = True

    play_run(running and p_pos[1] == g_lvl)

    if k[pygame.K_UP] and j_ok:
        v_y = random.uniform(*j_rng)
        j_ok = False
        j_cnt += 1
        jumping = True
        if j_cnt % 2 == 0:
            f_ok = True
            f_time = 30
            f_angle = 0
            f_dir = 1 if f_right else -1

    play_jump(jumping)

    v_y += g
    p_pos[1] += v_y

    if p_pos[1] >= g_lvl:
        p_pos[1] = g_lvl
        v_y = 0
        j_ok = True
        f_ok = False

    if f_ok:
        f_time -= 1
        f_angle += 12 * f_dir
        if f_time <= 0:
            f_ok = False
            f_angle = 0

    if k[pygame.K_LEFT] or k[pygame.K_RIGHT]:
        if p_pos[1] == g_lvl:
            anim_cnt += 1
            if anim_cnt >= anim_spd:
                anim_idx = (anim_idx + 1) % len(anim_frames)
                anim_cnt = 0

    w.fill(r)

    if p_pos[1] < g_lvl:
        if f_ok:
            rot = pygame.transform.rotate(i_run2, f_angle)
            rect = rot.get_rect(center=(p_pos[0] + 40, p_pos[1] + 40))
            w.blit(rot, rect.topleft)
        else:
            if f_right:
                w.blit(i_idle, (p_pos[0], p_pos[1]))
            else:
                flip = pygame.transform.flip(i_idle, True, False)
                w.blit(flip, (p_pos[0], p_pos[1]))
    else:
        if k[pygame.K_LEFT] or k[pygame.K_RIGHT]:
            if f_right:
                w.blit(anim_frames[anim_idx], (p_pos[0], p_pos[1]))
            else:
                flip = pygame.transform.flip(anim_frames[anim_idx], True, False)
                w.blit(flip, (p_pos[0], p_pos[1]))
        else:
            if f_right:
                w.blit(i_idle, (p_pos[0], p_pos[1]))
            else:
                flip = pygame.transform.flip(i_idle, True, False)
                w.blit(flip, (p_pos[0], p_pos[1]))

    pygame.display.flip()
    pygame.time.Clock().tick(60)
