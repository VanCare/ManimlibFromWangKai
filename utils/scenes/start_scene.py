#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
定义视频的开场动画
"""

from manimlib.imports import *
from from_wangkai.utils.Animation.Animation_tex import *

class VideoStart(Scene): # 6s
    CONFIG = {
        "Author": "雨落释心",
        "title": "动量定理和动量守恒",
        "subtitle_name": "动量定理",
        "svg_filename": "apple",
        "def_colors": [RED_A, GREEN, BLUE_B, BLUE_E,PINK],
    }

    def construct(self):
        def run(x, y, z, t):

            x = x + 4 * t
            y = y + 2 * t
            z = 0
            return [x, y, z]

        title = TextMobject(self.title).set_width(FRAME_WIDTH - 4).set_color_by_gradient(self.def_colors[0],
                                                                                             self.def_colors[1])
        title.shift(UP)
        # subtitle = TextMobject(self.subtitle_name).scale(1.5).set_color_by_gradient(self.def_colors[1], self.def_colors[2])
        # subtitle2 = TextMobject(self.subtitle_name).scale(0.6).set_opacity(0.6).set_color_by_gradient(self.def_colors[1], self.def_colors[2])
        # subtitle2.to_corner(UR)
        #
        # title = TextMobject(self.title_name).scale(1.1).set_color_by_gradient(self.def_colors[0], self.def_colors[1])
        # title.next_to(subtitle, UP, buff=0.75)

        author = TextMobject(self.Author).scale(0.8)
        author.set_color_by_gradient(self.def_colors[1], self.def_colors[2])
        author.next_to(title, DOWN,aligned_edge=RIGHT, buff=1.2).shift(LEFT*0.3)
        apple = Apple(file_name = self.svg_filename).scale(0.35).set_color_by_gradient(self.def_colors[0], self.def_colors[1])
        apple.next_to(title,DOWN,0,LEFT)

        # self.add(svg_file,touxiang)
        def update_ball(mob, dt):
            mob.acceleration = np.array((0, -2, 0))
            mob.velocity = mob.velocity + mob.acceleration * dt
            mob.shift(mob.velocity * dt)
            # mob.rotate(dt*PI/2)
            if mob.get_bottom() <= -4:
                mob.velocity[1] = -1*mob.velocity[1]
        apple.add_updater(update_ball)

        # self.add(apple)
        self.play(GrowFromRandom(title[0]),run_time=2)
        self.play(WriteRandom(author[0]),run_time=1)
        # self.add(apple)
        self.wait(4.5)
        self.play(FadeOut(title),FadeOut(author), run_time=0.5)
        self.wait(0.5)


class Apple(SVGMobject):
    def __init__(self, ** kwargs):
        SVGMobject.__init__(self, ** kwargs)
        self.velocity = np.array((0, 0, 0))

    # def get_top(self):
    #     return self.get_center()[1] + self.radius
    #
    def get_bottom(self):
        return self.get_center()[1] - 0.5
    #
    # def get_right_edge(self):
    #     return self.get_center()[0] + self.radius
    #
    # def get_left_edge(self):
    #     return self.get_center()[0] - self.radius
