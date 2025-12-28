import pygame
import numpy as np

pygame.init()
clock = pygame.time.Clock()
FPS = 60

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
# MIN_JUMP = - (MAX_JUMP + 1)
jump_vel = MAX_JUMP
m = 1

GRAVITY = 0.2

running = True
is_jump = False

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

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
    print(dinosour)
    WINDOW.fill(BLACK)
    pygame.display.set_caption("Dinosour Game")
    pygame.draw.rect(WINDOW, RED, dinosour) # type: ignore
    pygame.draw.line(WINDOW, WHITE, START_POINT, END_POINT, width= 3)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
