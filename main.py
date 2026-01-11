# Import here
import pygame
from random import choice, choices, randint
from function import create_obj, draw_obj
from properties import (Config, Clouds, Player, GameFlags,
                        JumpConfig, Cactus, Color, Birds)


pygame.init()
clock = pygame.time.Clock()


dinosour = pygame.Rect(100,
                       Config.GROUND_Y- Player.DINOSOUR_HEIGHT,
                       Player.DINOSOUR_WIDTH,
                       Player.DINOSOUR_HEIGHT)


obstacles = []
obs_speed= 5
obs_increment = 1000
obs_count = 0


last_spawn= 0
clouds: list = []


WINDOW = pygame.display.set_mode(
    (Config.WIDTH, Config.HEIGHT),
    pygame.SCALED | pygame.DOUBLEBUF
)

def main() -> None:
    # modified global variables
    global obs_count
    global obs_increment
    global obs_speed
    global last_spawn

    # game loop
    while GameFlags.running:
        dt = clock.tick(Config.FPS) / 1000
        current_time = pygame.time.get_ticks()

        # for loop through the event queue
        for event in pygame.event.get():
            # Check for QUIT event
            if event.type == pygame.QUIT:
                GameFlags.running = False

            # button pressed
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DOWN:
                    if not GameFlags.is_jump:
                        dinosour.w = Player.DINOSOUR_HEIGHT
                        dinosour.h = Player.DINOSOUR_WIDTH
                        dinosour.y = Config.GROUND_Y - dinosour.h
                        GameFlags.disable_jump = True

                    if not GameFlags.down_button_held:
                        GameFlags.down_button_held = True

            # button released
            if event.type == pygame.KEYUP:

                if event.key == pygame.K_DOWN:
                    dinosour.w = Player.DINOSOUR_WIDTH
                    dinosour.h = Player.DINOSOUR_HEIGHT

                    dinosour.y = Config.GROUND_Y - dinosour.h
                    GameFlags.disable_jump = False
                    GameFlags.down_button_held = False

        # Hold button
        if GameFlags.down_button_held:
            if dinosour.y == Config.GROUND_Y - Player.DINOSOUR_HEIGHT:
                dinosour.w = Player.DINOSOUR_HEIGHT
                dinosour.h = Player.DINOSOUR_WIDTH
                dinosour.y = Config.GROUND_Y - dinosour.h
                GameFlags.disable_jump = True

        # Jump physics
        keys = pygame.key.get_pressed()
        if not GameFlags.disable_jump:
            if keys[pygame.K_SPACE]:
                GameFlags.is_jump = True

            if GameFlags.is_jump:
                F = (1 / 2)* JumpConfig.mass*( JumpConfig.jump_velocity**2)
                dinosour.y -= F #type: ignore
                JumpConfig.jump_velocity -= (JumpConfig.GRAVITY # type: ignore
                                             if not GameFlags.down_button_held
                                             else JumpConfig.GRAVITY *2)

                if JumpConfig.jump_velocity < 0:
                     JumpConfig.mass = -1

                if dinosour.y + Player.DINOSOUR_HEIGHT >= Config.GROUND_Y:
                    GameFlags.is_jump = False
                    dinosour.y = Config.GROUND_Y - Player.DINOSOUR_HEIGHT

                    JumpConfig.jump_velocity = JumpConfig.MAX_JUMP_HEIGHT
                    JumpConfig.mass = 1

        # Increase difficulty when go further
        obs_count += dt * 1000
        if obs_count > obs_increment:

            is_bird = bool(choices([1,0], weights= [0.3,0.7])[0]) # 1 for bird and 0 for cactus
            if is_bird:
                rand_height = choice(Birds.BIRDS_ALTITUDES)
                obs = create_obj(obj_x= randint(Config.WIDTH, Config.WIDTH + 500),
                                obj_y= Config.GROUND_Y - Birds.BIRD_HEIGHT - rand_height,
                                obj_width= Birds.BIRD_WIDTH,
                                obj_height= Birds.BIRD_HEIGHT,
                                status= is_bird)

            else:
                rand_height = choice(Cactus.OBSTACLE_HEIGHT)
                obs = create_obj(obj_x= randint(Config.WIDTH, Config.WIDTH + 500),
                                obj_y= Config.GROUND_Y - rand_height,
                                obj_width= choice(Cactus.OBSTACLE_WIDTH),
                                obj_height= rand_height,
                                status= is_bird)
            # obs.pos[0] = float(obs.pos[0])
            obstacles.append(obs)

            obs_increment = max(300, obs_increment - 5)
            obs_count = 0
            obs_speed += Cactus.OBSTACLE_SPEED_INCREMENT


        # Obstacles
        for obs in obstacles[:]:
            obs.pos[0] -= obs_speed * dt * 100
            # obs.pos[0] = int(obs.pos[0])

            if obs.pos[0] + obs.size[0] < 0:
                obstacles.remove(obs)

            obs_rect = pygame.Rect(obs.pos,obs.size) # type: ignore
            if obs_rect.colliderect(dinosour):
                GameFlags.is_touch = True


        # Check the current position of the object
        # print(dinosour)

        # Check the number of obstacles
        # print(obstacles)


        # Clouds
        if current_time - last_spawn >= Clouds.CLOUD_SPAWN_INTERVAL:

            cloud = create_obj(obj_x= randint(Config.WIDTH, Config.WIDTH + 500),
                            obj_y= choice(Clouds.CLOUD_ALTITUDES),
                            obj_width= Clouds.CLOUD_WIDTH,
                            obj_height= Clouds.CLOUD_HEIGHT)

            clouds.append(cloud)
            last_spawn = current_time

        for cloud in clouds[:]:
            cloud.pos[0] -= Clouds.CLOUD_SPEED * dt * 60 #type: ignore
            if cloud.pos[0] + cloud.size[0] < 0:
                clouds.remove(cloud)


        WINDOW.fill(Color.BLACK)

        for cloud in clouds[:]:
            draw_obj(WINDOW, Color.BLUE, cloud) # Add clouds

        pygame.draw.rect(WINDOW, Color.RED, dinosour) # type: ignore


        for obs in obstacles[:]:
            if obs.status:
                draw_obj(WINDOW, Color.GREEN, obs) # Add birds
            else:
                draw_obj(WINDOW, Color.ORANGE, obs) # Add cactus


        pygame.draw.line(WINDOW, Color.WHITE, Config.GROUND_START, Config.GROUND_END, width= 3)
        pygame.display.set_caption("Dinosour Game")
        pygame.display.flip()

        if GameFlags.is_touch:
            print("GAME OVER")
            break


if __name__ == '__main__':
    main()
    pygame.quit()
