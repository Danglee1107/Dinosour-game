from dataclasses import dataclass


@dataclass(frozen= True)
class Config:
    FPS = 120

    # Window size
    WIDTH = 1200
    HEIGHT = 600

    GROUND_Y = HEIGHT // 2
    GROUND_START = (0,GROUND_Y)
    GROUND_END = (WIDTH,GROUND_Y)

@dataclass()
class JumpConfig:
    # properties
    MAX_JUMP_HEIGHT = 5
    GRAVITY = 0.2
    jump_velocity = MAX_JUMP_HEIGHT
    mass = 1


@dataclass(frozen= True)
class Color:
    # Color
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    ORANGE = (255,165,0)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)


@dataclass(frozen= True)
class Player:
    # Dino
    DINOSOUR_WIDTH = 30
    DINOSOUR_HEIGHT = 50
# dinosour = pygame.Rect(100, LAND - DINOSOUR_HEIGHT, DINOSOUR_WIDTH, DINOSOUR_HEIGHT)


@dataclass(frozen= True)
class Cactus:
    # Cactus (obstacles)
    OBSTACLE_WIDTH = [30, 40, 50, 60, 70]
    OBSTACLE_HEIGHT = [40, 50, 60]
    OBSTACLE_SPEED_INCREMENT = 0.2


@dataclass(frozen= True)
class Birds:
    # Birds (obstacles)
    BIRD_WIDTH = 30
    BIRD_HEIGHT = 30
    BIRDS_ALTITUDES= [3,40,60]


@dataclass(frozen= True)
class Clouds:
    # Clouds (decorative objects)
    CLOUD_WIDTH = 30
    CLOUD_HEIGHT = 20
    CLOUD_SPEED = 1
    CLOUD_SPAWN_INTERVAL = 1000 # ms
    CLOUD_ALTITUDES = [h for h in range(10, 125, 10)]


@dataclass()
class GameFlags:
    # Bools
    running = True
    is_jump = False
    is_touch = False
    down_button_held = False
    disable_jump = False

