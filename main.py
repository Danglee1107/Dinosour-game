import pygame

pygame.init()


# Size
WIDTH, HEIGHT = 800, 800


# Color
BLACK = (0,0,0)


running = True
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))


# game loop
while running:

# for loop through the event queue  
    for event in pygame.event.get():
    
        # Check for QUIT event      
        if event.type == pygame.QUIT:
            running = False

WINDOW.fill(BLACK)
pygame.display.set_caption("Dinosour Game")
pygame.display.flip()
