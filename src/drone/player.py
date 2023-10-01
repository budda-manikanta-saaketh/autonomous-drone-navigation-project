import os

import pygame
from pygame.locals import *

from stable_baselines3 import SAC

from drone.PID.controller_PID import PID


class Player:
    def __init__(self):
        self.thruster_mean = 0.04
        self.thruster_amplitude = 0.04
        self.diff_amplitude = 0.003
        (self.angle, self.angular_speed, self.angular_acceleration) = (0, 0, 0)
        (self.x_position, self.x_speed, self.x_acceleration) = (400, 0, 0)
        (self.y_position, self.y_speed, self.y_acceleration) = (500, 0, 0)
        self.target_counter = 0
        self.dead = False
        self.respawn_timer = 3


class PIDPlayer(Player):
    def __init__(self):
        self.name = "PID"
        self.alpha = 50
        super().__init__()

        self.thruster_amplitude = 0.04
        self.diff_amplitude = 0.003

        self.dt = 1 / 60
        self.xPID = PID(0.2, 0, 0.2, 25, -25)
        self.aPID = PID(0.02, 0, 0.01, 1, -1)

        self.yPID = PID(2.5, 0, 1.5, 100, -100)
        self.ydPID = PID(1, 0, 0, 1, -1)

    def act(self, obs):
        thruster_left = self.thruster_mean
        thruster_right = self.thruster_mean

        error_x, xd, error_y, yd, a, ad = obs

        ac = self.xPID.compute(-error_x, self.dt)

        error_a = ac - a
        action1 = self.aPID.compute(-error_a, self.dt)

        ydc = self.yPID.compute(error_y, self.dt)
        error_yd = ydc - yd
        action0 = self.ydPID.compute(-error_yd, self.dt)

        thruster_left += action0 * self.thruster_amplitude
        thruster_right += action0 * self.thruster_amplitude
        thruster_left += action1 * self.diff_amplitude
        thruster_right -= action1 * self.diff_amplitude

        return thruster_left, thruster_right
