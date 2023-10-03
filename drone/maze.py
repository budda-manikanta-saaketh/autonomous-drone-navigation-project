import os
from random import randrange
from math import sin, cos, pi, sqrt

import numpy as np
import pygame
from pygame.locals import *
from drone.player import PIDPlayer

def correct_path(current_path):
    """
    This function is used to get the correct path to the assets folder
    """
    return os.path.join(os.path.dirname(__file__), current_path)

def maze():
    """
    Runs the balloon game.
    """
    FPS = 80
    WIDTH = 800
    HEIGHT = 800
    gravity = 0.08
    mass = 1
    arm = 25
    FramePerSec = pygame.time.Clock()

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    player_width = 80
    player_animation_speed = 0.3
    player_animation = []
    for i in range(1, 5):
        image = pygame.image.load(
            correct_path(
                os.path.join(
                    "assets/png/objects/drone/drone-1"
                    + ".png"
                )
            )
        )
        image.convert()
        player_animation.append(
            pygame.transform.scale(image, (player_width, int(player_width * 0.30)))
        )

    target_width = 30
    target_animation_speed = 0.1
    target_animation = []
    for i in range(1, 8):
        image = pygame.image.load(
            correct_path(
                os.path.join(
                    "assets/png/target/target_old"
                    + ".png"
                )
            )
        )
        image.convert()
        target_animation.append(
            pygame.transform.scale(image, (target_width*2, int(target_width * 2)))
        )
    pygame.font.init()
    name_font = pygame.font.Font(correct_path("assets/fonts/Roboto-Bold.ttf"), 20)
    name_hud_font = pygame.font.Font(correct_path("assets/fonts/Roboto-Bold.ttf"), 15)
    score_font = pygame.font.Font(correct_path("assets/fonts/Roboto-Regular.ttf"), 20)
    respawn_timer_font = pygame.font.Font(
        correct_path("assets/fonts/Roboto-Bold.ttf"), 90
    )
    respawning_font = pygame.font.Font(
        correct_path("assets/fonts/Roboto-Regular.ttf"), 15
    )
    def display_info(position):
        name_text = name_font.render(player.name, True, (255, 255, 255))
        screen.blit(name_text, (position, 20))
        target_text = score_font.render(
            "Score : " + str(player.target_counter), True, (255, 255, 255)
        )
        screen.blit(target_text, (position, 45))
        if player.dead == True:
            respawning_text = respawning_font.render(
                "Respawning...", True, (255, 255, 255)
            )
            screen.blit(respawning_text, (position, 70))
    WALL_THICKNESS = 10
    step = 0
    respawn_timer_max = 3
    path_walls = [
        [(150, 790), (150, 120)],
        [(300,10) ,  (300,690)],
        [(450, 790), (450, 120)],
        [(600,10) ,  (600,690)],
        [(750, 790), (750, 120)],
    ]
    players = [PIDPlayer()]
    start=(80,600)
    zero_target=(80,400)
    first_target=(80,100)
    second_target=(150,100)
    third_target=(230,100)
    fourth_target=(230,400)
    fifth_target=(230,730)
    sixth_target=(380,730)
    sixth_target2=(380,400)
    seventh_target=(380,100)
    eighth_target=(450,100)
    ninth_target=(530,100)
    tenth_target=(530,400)
    eleventh_target=(530,730)
    twelveth_target=(680,730)
    twelveth_target2=(680,400)
    thirteenth_target=(680,100)
    targets = []
    for i in range(100):
        targets.append(first_target)
        targets.append(second_target)
        targets.append(third_target)
        targets.append(fourth_target)
        targets.append(fifth_target)
        targets.append(sixth_target)
        targets.append(seventh_target)
        targets.append(eighth_target)
        targets.append(ninth_target)
        targets.append(tenth_target)
        targets.append(eleventh_target)
        targets.append(twelveth_target)
        targets.append(thirteenth_target)
        targets.append(twelveth_target2)
        targets.append(twelveth_target)
        targets.append(eleventh_target)
        targets.append(tenth_target)
        targets.append(ninth_target)
        targets.append(eighth_target)
        targets.append(seventh_target)
        targets.append(sixth_target2)
        targets.append(sixth_target)
        targets.append(fifth_target)
        targets.append(fourth_target)
        targets.append(third_target)
        targets.append(second_target)
        targets.append(first_target)
        targets.append(zero_target)
        targets.append(start)

    while True:
        pygame.event.get()
        screen.fill((135, 206, 250))
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, WIDTH, WALL_THICKNESS))  # Top wall
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, WALL_THICKNESS, HEIGHT))  # Left wall
        pygame.draw.rect(screen, (255, 255, 255), (WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, HEIGHT))  # Right wall
        pygame.draw.rect(screen, (255, 255, 255), (0, HEIGHT - WALL_THICKNESS, WIDTH, WALL_THICKNESS))  # Bottom wall
        player = players[0]
        for wall in path_walls:
            pygame.draw.line(screen, (0, 0, 0), wall[0], wall[1], WALL_THICKNESS)
        if player.dead == False:
            player.x_acceleration = 0
            player.y_acceleration = gravity
            player.angular_acceleration = 0
            thruster_left, thruster_right = player.act(
                [
                    targets[player.target_counter][0] - player.x_position,
                    player.x_speed,
                    targets[player.target_counter][1] - player.y_position,
                    player.y_speed,
                    player.angle,
                    player.angular_speed,
                ]
            )
            player.x_acceleration += (
                -(thruster_left + thruster_right)
                * sin(player.angle * pi / 180)
                / mass
            )
            player.y_acceleration += (
                -(thruster_left + thruster_right)
                * cos(player.angle * pi / 180)
                / mass
            )
            player.angular_acceleration += (
                arm * (thruster_right - thruster_left) / mass
            )
            player.x_speed += player.x_acceleration
            player.y_speed += player.y_acceleration
            player.angular_speed += player.angular_acceleration
            player.x_position += player.x_speed
            player.y_position += player.y_speed
            player.angle += player.angular_speed
            dist = sqrt(
                (player.x_position - targets[player.target_counter][0]) ** 2
                + (player.y_position - targets[player.target_counter][1]) ** 2
            )
            if [(player.x_position,player.y_position),(player.x_position,player.y_position)] in path_walls:
                player.dead=True
            if dist < 50:
                player.target_counter += 1
            elif (player.x_position < WALL_THICKNESS or player.x_position > WIDTH - WALL_THICKNESS or player.y_position < WALL_THICKNESS or player.y_position > HEIGHT - WALL_THICKNESS):
                player.dead = True
        else:
            respawn_text = respawn_timer_font.render(
                str(int(player.respawn_timer) + 1), True, (255, 255, 255)
            )
            respawn_text.set_alpha(124)
            screen.blit(
                respawn_text,
                (
                    WIDTH / 2 - respawn_text.get_width() / 2,
                    HEIGHT / 2 - respawn_text.get_height() / 2,
                ),
            )

            player.respawn_timer -= 1 / 60
            if player.respawn_timer < 0:
                player.dead = False
                (
                    player.angle,
                    player.angular_speed,
                    player.angular_acceleration,
                ) = (
                    0,
                    0,
                    0,
                )
                (player.x_position, player.x_speed, player.x_acceleration) = (
                    80,
                    0,
                    0,
                )
                (player.y_position, player.y_speed, player.y_acceleration) = (
                    700,
                    0,
                    0,
                )

        target_sprite = target_animation[
            int(step * target_animation_speed) % len(target_animation)
        ]
        target_sprite.set_alpha(0)
        screen.blit(
            target_sprite,
            (
                targets[player.target_counter][0]
                - int(target_sprite.get_width() / 2),
                targets[player.target_counter][1]
                - int(target_sprite.get_height() / 2),
            ),
        )

        player_sprite = player_animation[
            int(step * player_animation_speed) % len(player_animation)
        ]
        player_copy = pygame.transform.rotate(player_sprite, player.angle)
        player_copy.set_alpha(255)
        screen.blit(
            player_copy,
            (
                player.x_position - int(player_copy.get_width() / 2),
                player.y_position - int(player_copy.get_height() / 2),
            ),
        )

        # Display player name
        name_hud_text = name_hud_font.render(player.name, True, (255, 255, 255))
        screen.blit(
            name_hud_text,
            (
                player.x_position - int(name_hud_text.get_width() / 2),
                player.y_position - 30 - int(name_hud_text.get_height() / 2),
            ),
        )
        display_info(20)
        pygame.display.update()
        FramePerSec.tick(FPS)
if __name__ == "__main__":
    balloon()