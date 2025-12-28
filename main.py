import pygame
import numpy as np
from random import choice
from typing import Sequence

pygame.init()
clock = pygame.time.Clock()
FPS = 60

class Obstacles:
    def __init__(self, attribute: Sequence[int | float]) -> None:
        self.attribute = np.array(attribute, dtype = np.float64)

# Size
WIDTH, HEIGHT = 800, 400

# Color
BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)

LAND = HEIGHT // 2
DINSOUR_WIDTH = 30
DINOSOUR_HEIGHT = 60
dinosour =np.array([100, LAND - DINOSOUR_HEIGHT, DINSOUR_WIDTH, DINOSOUR_HEIGHT], dtype= np.float64)

START_POINT = (0, LAND)
END_POINT = (800, LAND)
MAX_JUMP = 7
jump_vel = MAX_JUMP
m = 1

OBSTACLE_WIDTH = [30, 40, 50, 60, 70]
OBSTACLE_HEIGHT = 30
# obstacle = np.array([800 - dinosour[0], LAND - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT], dtype= np.float64)
obstacles = []

speed = 10
obs_increment = 1000
obs_count = 0

GRAVITY = 0.2

running = True
is_jump = False

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

def create_obs():
    obstacle = Obstacles([1000, LAND - OBSTACLE_HEIGHT, choice(OBSTACLE_WIDTH), OBSTACLE_HEIGHT])
    obstacles.append(obstacle)

def draw_obs(obs: Obstacles):
    pygame.draw.rect(WINDOW, RED, obs) # type: ignore

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
        dinosour[1] -= F
        jump_vel -= 0.5
        if jump_vel < 0:
            m = -1

        # if jump_vel == MIN_JUMP:
        if dinosour[1] + DINOSOUR_HEIGHT >= LAND:
            is_jump = False

            jump_vel = MAX_JUMP
            m = 1

    obs_count += clock.tick(FPS)
    if obs_count > obs_increment:
        create_obs()
        obs_increment = max(300, obs_increment - 5)
        obs_count = 0
        speed += 0.2

    for obs in obstacles:
        obs.attribute[0] -= speed

    for obs in obstacles:
        if obs.attribute[0] + obs.attribute[3] < 0:
            obstacles.remove(obs)
    # Check the current position of the object
    # print(dinosour)

    # Check the number of obstacle 
    print(obstacles)

    WINDOW.fill(BLACK)
    pygame.display.set_caption("Dinosour Game")
    pygame.draw.rect(WINDOW, RED, dinosour) # type: ignore

    for obs in obstacles:
        draw_obs(obs.attribute)

    pygame.draw.line(WINDOW, WHITE, START_POINT, END_POINT, width= 3)

    pygame.display.flip()

pygame.quit()
