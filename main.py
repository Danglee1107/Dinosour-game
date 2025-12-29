import pygame
import numpy as np
from random import choice, randint
from typing import Sequence


pygame.init()
clock = pygame.time.Clock()
FPS = 60


# Size
WIDTH = 800
HEIGHT = 400
LAND = HEIGHT // 2


# Color
BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)
ORANGE = (255,165,0)


DINSOUR_WIDTH = 30
DINOSOUR_HEIGHT = 60
dinosour = pygame.Rect(100, LAND - DINOSOUR_HEIGHT, DINSOUR_WIDTH, DINOSOUR_HEIGHT)

START_POINT = (0, LAND)
END_POINT = (800, LAND)
MAX_JUMP = 7
jump_vel = MAX_JUMP
m = 1


OBSTACLE_WIDTH = [30, 40, 50, 60, 70]
OBSTACLE_HEIGHT = 30
obstacles = []

speed = 10
obs_increment = 1000
obs_count = 0


# Bools
running = True
is_jump = False
is_touch = False

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))


class Obstacles:
    def __init__(self, pos: Sequence[int | float],
                 size: Sequence[int | float]) -> None:

        self.pos= np.array(pos, dtype = np.float64)
        self.size= np.array(size, dtype = np.float64)

def create_obs():
    obstacle = Obstacles(pos=[randint(WIDTH, WIDTH + 500), LAND - OBSTACLE_HEIGHT],
                         size=[choice(OBSTACLE_WIDTH), OBSTACLE_HEIGHT])
    obstacles.append(obstacle)


def draw_obs(obs: Obstacles):
    pygame.draw.rect(WINDOW, ORANGE, [obs.pos, obs.size]) #type: ignore

# game loop
while running:

    # for loop through the event queue  
    for event in pygame.event.get():
        # Check for QUIT event      
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False  # exit the game when ESC is pressed

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        is_jump = True

    if is_jump:
        F = (1 / 2)*m*(jump_vel**2)
        dinosour.y -= F #type: ignore
        jump_vel -= 0.5
        if jump_vel < 0:
            m = -1

        # if jump_vel == MIN_JUMP:
        if dinosour.y + DINOSOUR_HEIGHT >= LAND:
            is_jump = False
            dinosour.y = LAND - DINOSOUR_HEIGHT

            jump_vel = MAX_JUMP
            m = 1

    obs_count += clock.tick(FPS)
    if obs_count > obs_increment:
        create_obs()
        obs_increment = max(300, obs_increment - 5)
        obs_count = 0
        speed += 0.2

    for obs in obstacles[:]:
        obs.pos[0] -= speed

        if obs.pos[0] + obs.size[0] < 0:
            obstacles.remove(obs)

        obs_rect = pygame.Rect(obs.pos,obs.size) # type: ignore
        if obs_rect.colliderect(dinosour):
            is_touch = True

    # Check the current position of the object
    # print(dinosour)

    # Check the number of obstacles
    # print(obstacles)


    WINDOW.fill(BLACK)
    pygame.display.set_caption("Dinosour Game")
    pygame.draw.rect(WINDOW, RED, dinosour) # type: ignore

    for obs in obstacles[:]:
        draw_obs(obs)

    pygame.draw.line(WINDOW, WHITE, START_POINT, END_POINT, width= 3)

    pygame.display.flip()

    if is_touch:
        print("GAME OVER")
        break


pygame.quit()
