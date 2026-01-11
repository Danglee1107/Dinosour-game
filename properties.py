from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen= True)
class Config:
    FPS: int = 120

    # Window size
    WIDTH: int = 1200
    HEIGHT: int = 600

    GROUND_Y: int = HEIGHT // 2
    GROUND_START: Sequence[int] = (0,GROUND_Y)
    GROUND_END: Sequence[int] = (WIDTH,GROUND_Y)

@dataclass()
class JumpConfig:
    # properties
    MAX_JUMP_HEIGHT: int = 5
    GRAVITY: float = 0.2
    jump_velocity: float = MAX_JUMP_HEIGHT
    mass: int = 1


@dataclass(frozen= True)
class Color:
    # Color
    BLACK: Sequence[int] = (0,0,0)
    WHITE: Sequence[int] = (255,255,255)
    ORANGE: Sequence[int] = (255,165,0)
    RED: Sequence[int] = (255,0,0)
    GREEN: Sequence[int] = (0,255,0)
    BLUE: Sequence[int] = (0,0,255)


@dataclass(frozen= True)
class Player:
    # Dino
    DINOSOUR_WIDTH: int = 30
    DINOSOUR_HEIGHT: int = 50


@dataclass(frozen= True)
class Cactus:
    # Cactus (obstacles)
    OBSTACLE_WIDTH: Sequence[int] = [30, 40, 50, 60, 70]
    OBSTACLE_HEIGHT: Sequence[int] = [40, 50, 60]
    OBSTACLE_SPEED_INCREMENT: int|float = 0.2


@dataclass(frozen= True)
class Birds:
    # Birds (obstacles)
    BIRD_WIDTH: int = 30
    BIRD_HEIGHT: int = 30
    BIRDS_ALTITUDES: Sequence[int]= [3,40,60]


@dataclass(frozen= True)
class Clouds:
    # Clouds (decorative objects)
    CLOUD_WIDTH: int = 30
    CLOUD_HEIGHT: int = 20
    CLOUD_SPEED: int = 1
    CLOUD_SPAWN_INTERVAL: int = 1000 # ms
    CLOUD_ALTITUDES: Sequence[int] = [h for h in range(10, 125, 10)]


@dataclass()
class GameFlags:
    # Bools
    running: bool = True
    is_jump: bool= False
    is_touch: bool = False
    down_button_held: bool = False
    disable_jump: bool = False

