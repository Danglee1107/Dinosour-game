import pygame
import numpy as np
from random import choice, randint, getrandbits
from typing import Sequence


pygame.init()
clock = pygame.time.Clock()
FPS = 120


# Size
WIDTH = 1000
HEIGHT = 500
LAND = HEIGHT // 2


# Color
BLACK = (0,0,0)
WHITE = (255,255,255)
ORANGE = (255,165,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)


DINOSOUR_WIDTH = 30
DINOSOUR_HEIGHT = 50
dinosour = pygame.Rect(100, LAND - DINOSOUR_HEIGHT, DINOSOUR_WIDTH, DINOSOUR_HEIGHT)

START_POINT = (0, LAND)
END_POINT = (WIDTH, LAND)
MAX_JUMP = 5
GRAVITY = 0.2
jump_vel = MAX_JUMP
m = 1


OBSTACLE_WIDTH = [30, 40, 50, 60, 70]
OBSTACLE_HEIGHT = [40, 50, 60]
obstacles = []


obs_speed= 5
obs_increment = 1000
obs_count = 0


BIRD_WIDTH = 30
BIRD_HEIGHT = 30
h = [3,40,60]


CLOUD_WIDTH = 30
CLOUD_HEIGHT = 20
CLOUD_SPEED = 1
MAX_CLOUD = 3
CLOUD_SPAWN_INTERVAL = 1000 # ms
last_spawn= 0
cloud_h = [h for h in range(10, 125, 10)]
cloud_rect = pygame.Rect(randint(WIDTH, WIDTH + 500), choice(cloud_h), CLOUD_WIDTH, CLOUD_HEIGHT)
clouds: list = []


# Bools
running = True
is_jump = False
is_touch = False
down_button_held = False
disable_jump = False

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

class Clouds:
    def __init__(self, pos: Sequence[int | float],
                 size: Sequence[int | float]) -> None:

        self.pos= np.array(pos, dtype = np.float64)
        self.size= np.array(size, dtype = np.float64)

class Obstacles:
    def __init__(self, pos: Sequence[int | float],
                 size: Sequence[int | float], is_bird: bool= False) -> None:

        self.pos= np.array(pos, dtype = np.float64)
        self.size= np.array(size, dtype = np.float64)
        self.is_bird = is_bird

def create_obs():
    is_bird = bool(getrandbits(1)) # 1 for bird and 0 for cactus
    if is_bird:
        rand_height = choice(h)
        obstacle = Obstacles(pos=[randint(WIDTH, WIDTH + 500), LAND - BIRD_HEIGHT - rand_height],
                            size=[BIRD_WIDTH, BIRD_HEIGHT], is_bird= True)
    else:
        rand_height = choice(OBSTACLE_HEIGHT)
        obstacle = Obstacles(pos=[randint(WIDTH, WIDTH + 500), LAND - rand_height],
                            size=[choice(OBSTACLE_WIDTH),rand_height])
    obstacles.append(obstacle)

def create_cloud(num_cloud: int):
    for _ in range(num_cloud):
        cloud = Clouds(pos= [randint(WIDTH, WIDTH + 500), choice(cloud_h)],
                    size= [CLOUD_WIDTH, CLOUD_HEIGHT])

        clouds.append(cloud)

def draw_clouds(cloud: Clouds):
    pygame.draw.rect(WINDOW, BLUE, [cloud.pos, cloud.size]) #type: ignore

def draw_obs(obs: Obstacles):
    if obs.is_bird:
        pygame.draw.rect(WINDOW, GREEN, [obs.pos, obs.size]) #type: ignore
    else:
        pygame.draw.rect(WINDOW, ORANGE, [obs.pos, obs.size]) #type: ignore

# game loop
while running:
    current_time = pygame.time.get_ticks()

    # for loop through the event queue
    for event in pygame.event.get():
        # Check for QUIT event
        if event.type == pygame.QUIT:
            running = False

        # button pressed
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_DOWN:
                if not is_jump:
                    dinosour.w = DINOSOUR_HEIGHT
                    dinosour.h = DINOSOUR_WIDTH
                    dinosour.y = LAND - dinosour.h
                    disable_jump = True

                if not down_button_held:
                    down_button_held = True

        # button released
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_DOWN:
                dinosour.w = DINOSOUR_WIDTH
                dinosour.h = DINOSOUR_HEIGHT

                dinosour.y = LAND - dinosour.h
                disable_jump = False
                down_button_held = False

    # Hold button
    if down_button_held:
        if dinosour.y == LAND - DINOSOUR_HEIGHT:
            dinosour.w = DINOSOUR_HEIGHT
            dinosour.h = DINOSOUR_WIDTH
            dinosour.y = LAND - dinosour.h
            disable_jump = True

    keys = pygame.key.get_pressed()
    if not disable_jump:
        if keys[pygame.K_SPACE]:
            is_jump = True

        if is_jump:
            F = (1 / 2)*m*(jump_vel**2)
            dinosour.y -= F #type: ignore
            jump_vel -= GRAVITY if not down_button_held else GRAVITY *2

            if jump_vel < 0:
                m = -1

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
        obs_speed+= 0.2

    for obs in obstacles[:]:
        obs.pos[0] -=obs_speed

        if obs.pos[0] + obs.size[0] < 0:
            obstacles.remove(obs)

        obs_rect = pygame.Rect(obs.pos,obs.size) # type: ignore
        if obs_rect.colliderect(dinosour):
            is_touch = True

    # Check the current position of the object
    # print(dinosour)

    # Check the number of obstacles
    # print(obstacles)

    if current_time - last_spawn >= CLOUD_SPAWN_INTERVAL:
        # num_cloud = randint(1, MAX_CLOUD)
        create_cloud(num_cloud= 1)
        last_spawn = current_time

    for cloud in clouds[:]:
        cloud.pos[0] -= CLOUD_SPEED
        if cloud.pos[0] + cloud.size[0] < 0:
            clouds.remove(cloud)

    WINDOW.fill(BLACK)
    pygame.display.set_caption("Dinosour Game")

    for cloud in clouds[:]:
        draw_clouds(cloud)

    pygame.draw.rect(WINDOW, BLUE, cloud_rect)
    pygame.draw.rect(WINDOW, RED, dinosour) # type: ignore

    for obs in obstacles[:]:
        draw_obs(obs)

    pygame.draw.line(WINDOW, WHITE, START_POINT, END_POINT, width= 3)
    pygame.display.flip()

    if is_touch:
        print("GAME OVER")
        break


pygame.quit()
