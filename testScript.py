from contextlib import nullcontext
from Script import *
import pytest


@pytest.mark.parametrize('angle_before, angle_add, angle_after',
                         [(15, 8, 23),
                          (1, 20, 21),
                          (115, 22, 137),
                          (135, 856, 271),
                          (1225, -8423, 2),
                          (-125, 8423, 18),
                          (-115, -81, 164),
                          (18957878, 88, 6), ])
def test_paddle_angle(angle_before, angle_add, angle_after):
    boat_params = BoatParams(right_paddle_angle=angle_before)
    boat = Boat(boat_params=boat_params)
    boat.right_paddle_angle += angle_add
    assert boat.right_paddle_angle == angle_after, 'Broken property right_paddle_angle'

    boat_params = BoatParams(left_paddle_angle=angle_before)
    boat = Boat(boat_params=boat_params)
    boat.left_paddle_angle += angle_add
    assert boat.left_paddle_angle == angle_after, 'Broken property left_paddle_angle'



@pytest.mark.parametrize('angle_before, rotate_amount, angle_after',
                         [(15, 8, 55),
                          (1, 20, 101),
                          (115, 22, 225),
                          (135, 856, 95),
                          (1225, 823, 300),
                          (-125, 823, 30),
                          (-115, 81, 290),
                          (18957878, 88, 358), ])
def test_boat_angle(angle_before, rotate_amount, angle_after):
    boat_params = BoatParams(move_angle=angle_before)
    boat_constants = BoatConstants(base_rotate_angle=5)
    boat = Boat(boat_params=boat_params, boat_constants=boat_constants)
    for i in range(rotate_amount):
        boat.rotate_right_paddle()
    assert boat.move_angle == angle_after, 'Broken method rotate_right_paddle'
    for i in range(rotate_amount):
        boat.rotate_left_paddle()
    assert boat.move_angle == angle_before % 360, 'Broken method rotate_left_paddle'


@pytest.mark.parametrize("capacity, add_people_amount, people_after, expected_exception_raised",
                         [(15, 8, 9, False),
                          (1, 20, 0, True),
                          (115, -22, 0, True),
                          (135, 856, 0, True),
                          (1225, -823, 0, True),
                          (125, 823, 0, True),
                          (115, -81, 0, True),
                          (18957878, 88, 89, False), ])
def test_add_people(capacity, add_people_amount, people_after, expected_exception_raised):
    context = nullcontext()
    if expected_exception_raised:
        context = pytest.raises(ValueError)
    with context:
        boat_params = BoatParams(people=1, capacity=capacity)
        boat = Boat(boat_params=boat_params)
        boat.add_people(add_people_amount)
        assert boat.people == people_after, 'Broken method add_people'


@pytest.mark.parametrize("anchor_dropped_before, anchor_dropped_after, expected_exception_raised",
                         [(False, False, True),
                          (True, False, False), ])
def test_anchor_raise(anchor_dropped_before, anchor_dropped_after, expected_exception_raised):
    context = nullcontext()
    if expected_exception_raised:
        context = pytest.raises(ValueError)
    with context:
        boat_params = BoatParams(anchor_dropped=anchor_dropped_before)
        boat = Boat(boat_params=boat_params)
        boat.anchor_raise()
        assert boat.anchor_dropped == anchor_dropped_after, 'Broken method anchor_raise'


@pytest.mark.parametrize("anchor_dropped_before, anchor_dropped_after, expected_exception_raised",
                         [(False, True, False),
                          (True, True, True), ])
def test_anchor_dropped(anchor_dropped_before, anchor_dropped_after, expected_exception_raised):
    context = nullcontext()
    if expected_exception_raised:
        context = pytest.raises(ValueError)
    with context:
        boat_params = BoatParams(anchor_dropped=anchor_dropped_before)
        boat = Boat(boat_params=boat_params)
        boat.anchor_dropped()
        assert boat.anchor_dropped == anchor_dropped_after, 'Broken method anchor_dropped'


def test_boat_working():
    boat_params = BoatParams(x_position=0, y_position=0)
    boat = Boat(boat_params=boat_params)
    for i in range(5):
        boat.rotate_left_paddle()
    for i in range(23):
        boat.rotate_right_paddle()
    boat.wait(100)
    boat.anchor_drop()
    for i in range(23):
        boat.rotate_left_paddle()
    for i in range(5):
        boat.rotate_right_paddle()
    boat.wait(100)
    assert abs(boat.x_position) < 1e-6 and abs(boat.y_position - 2800) < 1e-6
