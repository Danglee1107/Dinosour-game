import pygame
import numpy as np
from typing import Sequence


class Objects:
    def __init__(self, pos: Sequence[int | float],
                 size: Sequence[int | float], status: bool= False) -> None:

        self.pos= np.array(pos, dtype = np.float64)
        self.size= np.array(size, dtype = np.float64)
        self.status= status


def create_obj(obj_x: int|float, obj_y: int|float,
               obj_width: int|float, obj_height: int|float, status: bool= False) -> Objects:

    obj = Objects(pos=[obj_x, obj_y],
                  size= [obj_width, obj_height],
                  status= status)

    return obj


def draw_obj(window: pygame.Surface,
             color: Sequence[int],
             object: Objects) -> None:
    pygame.draw.rect(window, color, [object.pos, object.size]) #type: ignore


