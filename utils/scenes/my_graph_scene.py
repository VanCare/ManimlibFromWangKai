#!/usr/bin/python3
# -*- coding:utf-8 -*-
from manimlib.imports import *

"""
GraphScene 坐标系移动 放缩 消失 
My2DCoordinate 为标准坐标系
"""


class MyGraphScene(GraphScene): #
    CONFIG = {
        "x_axis_color": YELLOW,
        "x_axis_opacity":0.6,
        "x_axis_stroke_width":2,
        "y_axis_color": RED,
        "y_axis_opacity": 0.6,
        "y_axis_stroke_width": 2,
    }
    def setup_axes(self, animate=False):
        """
        This method sets up the axes of the graph.

        Parameters
        ----------
        animate (bool=False)
            Whether or not to animate the setting up of the Axes.
        """
        # TODO, once eoc is done, refactor this to be less redundant.
        x_num_range = float(self.x_max - self.x_min)
        self.space_unit_to_x = self.x_axis_width / x_num_range
        if self.x_labeled_nums is None:
            self.x_labeled_nums = []
        if self.x_leftmost_tick is None:
            self.x_leftmost_tick = self.x_min
        x_axis = NumberLine(
            x_min=self.x_min,
            x_max=self.x_max,
            unit_size=self.space_unit_to_x,
            tick_frequency=self.x_tick_frequency,
            leftmost_tick=self.x_leftmost_tick,
            numbers_with_elongated_ticks=self.x_labeled_nums,
            color=self.x_axis_color
        ).set_opacity(self.x_axis_opacity).set_stroke(width=self.x_axis_stroke_width)
        x_axis.shift(self.graph_origin - x_axis.number_to_point(0))
        if len(self.x_labeled_nums) > 0:
            if self.exclude_zero_label:
                self.x_labeled_nums = [x for x in self.x_labeled_nums if x != 0]
            x_axis.add_numbers(*self.x_labeled_nums)
        if self.x_axis_label:
            x_label = TextMobject(self.x_axis_label).scale(0.6).set_color(YELLOW)
            x_label.next_to(
                x_axis.get_tick_marks(), UP + RIGHT,
                buff=SMALL_BUFF
            )
            x_label.shift_onto_screen()
            x_axis.add(x_label)
            self.x_axis_label_mob = x_label

        y_num_range = float(self.y_max - self.y_min)
        self.space_unit_to_y = self.y_axis_height / y_num_range

        if self.y_labeled_nums is None:
            self.y_labeled_nums = []
        if self.y_bottom_tick is None:
            self.y_bottom_tick = self.y_min
        y_axis = NumberLine(
            x_min=self.y_min,
            x_max=self.y_max,
            unit_size=self.space_unit_to_y,
            tick_frequency=self.y_tick_frequency,
            leftmost_tick=self.y_bottom_tick,
            numbers_with_elongated_ticks=self.y_labeled_nums,
            color=self.y_axis_color,
            line_to_number_vect=LEFT,
            label_direction=LEFT,
        ).set_opacity(self.y_axis_opacity).set_stroke(width=self.y_axis_stroke_width)
        y_axis.shift(self.graph_origin - y_axis.number_to_point(0))
        y_axis.rotate(np.pi / 2, about_point=y_axis.number_to_point(0))
        if len(self.y_labeled_nums) > 0:
            if self.exclude_zero_label:
                self.y_labeled_nums = [y for y in self.y_labeled_nums if y != 0]
            y_axis.add_numbers(*self.y_labeled_nums)
        if self.y_axis_label:
            y_label = TextMobject(self.y_axis_label).scale(0.6).set_color(RED)
            y_label.next_to(
                y_axis.get_corner(UP + RIGHT), UP + RIGHT,
                buff=SMALL_BUFF
            )
            y_label.shift_onto_screen()
            y_axis.add(y_label)
            self.y_axis_label_mob = y_label

        if animate:
            self.play(Write(VGroup(x_axis, y_axis)))
        else:
            self.add(x_axis, y_axis)
        self.x_axis, self.y_axis = self.axes = VGroup(x_axis, y_axis)
        self.default_graph_colors = it.cycle(self.default_graph_colors)


class TestMy2DCoordinate(MyGraphScene):
    def x_2(self, x):
        return x ** 2

    def x2(self, t):
        return self.coords_to_point(t, t ** 2 + 1)  # 场景到图的坐标转换

    def x_3(self, t):
        return t ** 0.5

    def construct(self):
        self.setup_axes(animate=True)
        fg = self.get_graph(self.x_2, WHITE, x_min=-1, x_max=3)
        self.add(fg)
        fg2 = ParametricFunction(self.x2, color=BLUE, t_min=-1, t_max=3, step_size=0.05)
        self.add(fg2)
        self.wait()  # 第一幅图完成
        axs1 = VGroup(self.axes, fg, fg2)
        temp = self.axes

        self.graph_origin = ORIGIN
        self.axes_color = BLUE
        self.y_max = 10
        self.setup_axes(animate=True)
        fg3 = self.get_graph(self.x_3, YELLOW, x_min=0, x_max=6)
        self.add(fg3)  # 第二幅图完成
        axs2 = VGroup(self.axes, fg3)
        axs2_ = axs2.copy().shift(RIGHT * 2).scale(0.5)

        # self.play(FadeOutAndShift(axs2), run_time=3)
        self.play(Transform(axs2, axs2_))  # 移动 放缩
        self.play(FadeOut(temp))  # 消失
        self.wait()
        self.play(FadeIn(temp))  # 出现
        self.wait()
