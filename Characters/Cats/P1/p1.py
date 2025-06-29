import pygame
import random

class PlayerOne:
    def __init__(self):
        self.i_idle = pygame.image.load("img/Cats/P1/cat.png")
        self.i_idle = pygame.transform.scale(self.i_idle, (80, 80))

        self.i_run1 = pygame.image.load("img/Cats/P1/cat_running1.png")
        self.i_run1 = pygame.transform.scale(self.i_run1, (80, 80))

        self.i_run2 = pygame.image.load("img/Cats/P1/cat_running2.png")
        self.i_run2 = pygame.transform.scale(self.i_run2, (80, 80))

        self.s_run = pygame.mixer.Sound("Sound/run-sound.mp3")
        self.s_jump = pygame.mixer.Sound("Sound/jump-sound.mp3")

        self.g_level = 400
        self.pos = [100, self.g_level - 80]
        self.spd = 12
        self.gravity = 0.4
        self.vel_y = 0
        self.jump_rng = (-18, -16)
        self.can_jump = True
        self.jump_count = 0

        self.f_ok = False
        self.f_time = 30
        self.f_angle = 0
        self.f_dir = 1

        self.f_right = True
        self.anim_frames = [self.i_run1, self.i_run2]
        self.anim_idx = 0
        self.anim_spd = 5
        self.anim_cnt = 0
        self.is_idle = True

    def play_run(self, run):
        if run:
            if not self.s_run.get_num_channels():
                self.s_run.play(-1)
        else:
            self.s_run.stop()

    def play_jump(self, jump):
        if jump:
            self.s_jump.play()

    def mover(self, keys):
        running = False
        jumping = False
        on_ground = self.pos[1] == self.g_level

        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.pos[0] -= self.spd
            self.f_right = False
            running = True
            self.is_idle = False

        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.pos[0] += self.spd
            self.f_right = True
            running = True
            self.is_idle = False

        else:
            self.is_idle = True

        if keys[pygame.K_UP] and self.can_jump:
            self.vel_y = random.uniform(*self.jump_rng)
            self.can_jump = False
            self.jump_count += 1
            jumping = True
            self.is_idle = False
            if self.jump_count % 2 == 0:
                self.f_ok = True
                self.f_time = 30
                self.f_angle = 0
                self.f_dir = 1 if self.f_right else -1

        self.play_run(running and on_ground)
        self.play_jump(jumping)

        self.vel_y += self.gravity
        self.pos[1] += self.vel_y
        if self.pos[1] >= self.g_level:
            self.pos[1] = self.g_level
            self.vel_y = 0
            self.can_jump = True
            self.f_ok = False

        if self.f_ok:
            self.f_time -= 1
            self.f_angle += 12 * self.f_dir
            if self.f_time <= 0:
                self.f_ok = False
                self.f_angle = 0

        if running and on_ground:
            self.anim_cnt += 1
            if self.anim_cnt >= self.anim_spd:
                self.anim_idx = (self.anim_idx + 1) % len(self.anim_frames)
                self.anim_cnt = 0

    def draw(self, screen, screen_x=None):
        if screen_x is None:
            screen_x = self.pos[0]

        if self.f_ok:
            rotated = pygame.transform.rotate(self.i_idle, self.f_angle)
            rect = rotated.get_rect(center=(screen_x + 40, self.pos[1] + 40))
            screen.blit(rotated, rect.topleft)

        elif not self.is_idle and self.pos[1] == self.g_level:
            self.anim_cnt += 1
            if self.anim_cnt >= self.anim_spd:
                self.anim_cnt = 0
                self.anim_idx = (self.anim_idx + 1) % len(self.anim_frames)

            frame = self.anim_frames[self.anim_idx]
            if not self.f_right:
                frame = pygame.transform.flip(frame, True, False)
            screen.blit(frame, (screen_x, self.pos[1]))

        else:
            idle_image = self.i_idle
            if not self.f_right:
                idle_image = pygame.transform.flip(self.i_idle, True, False)
            screen.blit(idle_image, (screen_x, self.pos[1]))