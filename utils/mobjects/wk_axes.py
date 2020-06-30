#!/usr/bin/python3
# -*- coding:utf-8 -*-

from manimlib.imports import *


class Ground_line(NumberLine):
    CONFIG = {
        "color": LIGHT_GREY,
        "x_min": -FRAME_X_RADIUS+1,
        "x_max": FRAME_X_RADIUS-1,
        "unit_size": 1,
        "include_ticks": True,
        "tick_size": 0.1,
        "tick_frequency": 1,
        # Defaults to value near x_min s.t. 0 is a tick
        # TODO, rename this
        "leftmost_tick": None,
        # Change name
        "numbers_with_elongated_ticks": [0],
        "include_numbers": False,
        "numbers_to_show": None,
        "longer_tick_multiple": 2,
        "number_at_center": 0,
        "number_scale_val": 0.75,
        "label_direction": DOWN,
        "line_to_number_buff": MED_SMALL_BUFF,
        "include_tip": False,
        "tip_width": 0.25,
        "tip_height": 0.25,
        "decimal_number_config": {
            "num_decimal_places": 0,
        },
        "exclude_zero_from_default_numbers": False,
        "stroke_width": 2,
    }

class V1V2(Axes):
    CONFIG = {
        "axis_config": {
            "color": LIGHT_GREY,
            "include_tip": False,
            "exclude_zero_from_default_numbers": True,
            "unit_size": 0.7,
            "stroke_width": 2,
            "include_ticks": True,
            "tick_size": 0.05,
            "tick_frequency": 1,
            "leftmost_tick": None,
            "include_numbers": False,
            "numbers_to_show": None,
            "number_at_center": 0,
            "number_scale_val": 0.75,
        },
        "x_axis_config": {
            "color":YELLOW,
            "label_direction": DOWN,
            "x_min": -3.5,
            "x_max": 3.5,
            "line_to_number_buff": MED_SMALL_BUFF,
        },
        "y_axis_config": {
            "color":RED,
            "label_direction": LEFT,
            "x_min": -3.5,
            "x_max": 3.5,
        },
        "center_point": 1.5 * DOWN + 3.5 * LEFT,
    }


class test_axes(Scene):
    """
    希望结果：坐标缩放，update，将坐标属性放进config内,使得坐标更漂亮
    """

    def construct(self):
        a1 = V1V2()
        self.add(a1)
        self.wait()