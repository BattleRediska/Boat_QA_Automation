import math
from dataclasses import dataclass


@dataclass
class BoatParams:
    x_position: float = 0
    y_position: float = 0
    boat_speed: float = 0
    move_angle: float = 0
    water_level: float = 0
    right_paddle_angle: int = 180
    left_paddle_angle: int = 180
    anchor_dropped: bool = False
    capacity: int = 3
    people: int = 1
    height: float = 1


@dataclass
class BoatConstants:
    base_rotate_angle: float = 5
    base_rotate_speed: float = 1


class Boat:
    def __init__(self, boat_params=None, boat_constants=None):
        if boat_params is None:
            boat_params = BoatParams()
        self.__boat_params = boat_params
        if boat_constants is None:
            boat_constants = BoatConstants()
        self.__boat_constants = boat_constants

    def wait(self, time):
        self.__boat_params.x_position += time * self.__boat_params.boat_speed * math.cos(
            math.radians(self.__boat_params.move_angle))
        self.__boat_params.y_position += time * self.__boat_params.boat_speed * math.sin(
            math.radians(self.__boat_params.move_angle))

    def add_people(self, amount=1):
        if amount < 1:
            raise ValueError('Amount must be > 1')
        if self.__boat_params.people + amount <= self.__boat_params.capacity:
            self.__boat_params.people += amount
        else:
            raise ValueError('People exceed capacity!')

    @property
    def x_position(self):
        return self.__boat_params.x_position

    @property
    def y_position(self):
        return self.__boat_params.y_position

    @property
    def people(self):
        return self.__boat_params.people

    @property
    def move_angle(self):
        return self.__boat_params.move_angle

    @property
    def water_level(self):
        return self.__boat_params.water_level

    @water_level.setter
    def water_level(self, add_water):
        if add_water > 0:
            self.__boat_params.water_level += add_water
        if self.__boat_params.water_level >= self.__boat_params.height:
            print('GG')

    @property
    def anchor_dropped(self):
        return self.__boat_params.anchor_dropped

    def anchor_raise(self):
        if not self.__boat_params.anchor_dropped:
            raise ValueError('Anchor is already raised!')
        self.__boat_params.anchor_dropped = False

    def anchor_drop(self):
        if self.__boat_params.anchor_dropped:
            raise ValueError('Anchor is already dropped!')
        self.__boat_params.anchor_dropped = True
        self.__boat_params.boat_speed = 0

    @property
    def right_paddle_angle(self):
        return self.__boat_params.right_paddle_angle % 360

    @right_paddle_angle.setter
    def right_paddle_angle(self, paddle_value):
        self.__boat_params.right_paddle_angle = paddle_value % 360

    @property
    def left_paddle_angle(self):
        return self.__boat_params.left_paddle_angle % 360

    @left_paddle_angle.setter
    def left_paddle_angle(self, paddle_value):
        self.__boat_params.left_paddle_angle = paddle_value % 360

    def rotate_right_paddle(self, counter_clockwise=True):
        if self.__boat_params.people < 1:
            raise ValueError('Noone can rotate right paddle!')
        if counter_clockwise:
            if not self.__boat_params.anchor_dropped:
                self.__boat_params.boat_speed += self.__boat_constants.base_rotate_speed
            self.__boat_params.move_angle += self.__boat_constants.base_rotate_angle
        else:
            if not self.__boat_params.anchor_dropped:
                self.__boat_params.boat_speed -= self.__boat_constants.base_rotate_speed
            self.__boat_params.move_angle -= self.__boat_constants.base_rotate_angle
        self.__boat_params.move_angle = self.__boat_params.move_angle % 360

    def rotate_left_paddle(self, counter_clockwise=False):
        if self.__boat_params.people < 1:
            raise ValueError('Noone can rotate left paddle!')
        if not counter_clockwise:
            if not self.__boat_params.anchor_dropped:
                self.__boat_params.boat_speed += self.__boat_constants.base_rotate_speed
            self.__boat_params.move_angle -= self.__boat_constants.base_rotate_angle
        else:
            if not self.__boat_params.anchor_dropped:
                self.__boat_params.boat_speed -= self.__boat_constants.base_rotate_speed
            self.__boat_params.move_angle += self.__boat_constants.base_rotate_angle
        self.__boat_params.move_angle = self.__boat_params.move_angle % 360

    def is_right_paddle_submerged(self):
        if 20 < self.__boat_params.right_paddle_angle < 160:
            return True
        else:
            return False

    def is_left_paddle_submerged(self):
        if 20 < self.__boat_params.left_paddle_angle < 160:
            return True
        else:
            return False
