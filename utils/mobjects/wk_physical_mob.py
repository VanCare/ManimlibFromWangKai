#!/usr/bin/python3
# -*- coding:utf-8 -*-


"""
自定义的物理Mobject类
"""

from manimlib.imports import *
from from_wangkai.utils.functions.wk_func import *
from from_wangkai.utils.mobjects.wk_axes import Ground_line


class Wall_wk(Line):
    CONFIG = {
        "tiny_line_distance": 0.2
    }

    def __init__(self, start=LEFT, end=RIGHT, **kwargs):
        digest_config(self, kwargs)
        Line.__init__(self, start=start, end=end, **kwargs)

    def generate_points(self):
        l = Line(start=self.start, end=self.end)
        l_tines = [
            Line(start=self.get_start_tiny_line(i), end=self.get_end_tiny_line(i), stroke_width=1, ).rotate(
                45 * DEGREES, axis=OUT,
                about_point=self.get_start_tiny_line(
                    i))
            for i in range(self.get_num_tiny_line())
        ]
        self.clear_points()
        self.append_points(l.points)
        for i in range(len(l_tines)):
            self.append_points(l_tines[i].points)

    def get_num_tiny_line(self):
        return int(get_instance_(self.start, self.end) / self.tiny_line_distance) - 1

    def get_start_tiny_line(self, i):
        return self.start + (i + 1) * normalize(self.end - self.start) * self.tiny_line_distance

    def get_end_tiny_line(self, i):
        return self.start + i * normalize(self.end - self.start) * self.tiny_line_distance


class TestWall(Scene):
    def construct(self):
        w = Wall_wk(LEFT, RIGHT * 2)
        self.add(w)
        self.wait()
        self.remove(w)


class Ball_(Circle):
    # pass
    CONFIG = {
        "radius": 0.3,
        # "fill_color": RED,
        "fill_opacity": 0.9,
        "stroke_color": None,
        "stroke_opacity": 0.0,
        "m": 1,
        "v": 1,
    }


class Collision(VGroup):
    CONFIG = {
        "numberline_config": {},
        "wall_config": {
            "height": 3,
            "start": -6,
            "end": 6,
        },
        "ball1_config": {
            "fill_color": YELLOW,
            "m": 1,
            "v": 2,
        },
        "ball2_config": {
            "fill_color": RED,
            "m": 1,
            "v": -2,
        },
        "play_time": 4,
        "n_steps_per_frame": 1
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.create_numberline()
        self.create_wall()
        self.create_ball()
        self.add_text()
        self.update_number()
        self.update()

    def create_numberline(self):
        self.number_line = Ground_line()
        self.number_line.shift(self.wall_config["height"] * UP)
        self.add(self.number_line)
        # return self

    def create_wall(self):
        start = self.wall_config["start"] * RIGHT + self.wall_config["height"] * UP
        end = self.wall_config["end"] * RIGHT + self.wall_config["height"] * UP
        self.ground = Wall_wk(start=start, end=end, stroke_opacity=0.7, stroke_width=3)
        # self.add(self.ground)
        # return self

    def create_ball(self):
        self.ball1 = ball1 = Ball_(**self.ball1_config)
        self.ball2 = ball2 = Ball_(**self.ball2_config)
        ball1.shift(
            (-ball1.v * self.play_time / 2 - ball1.radius) * RIGHT + (self.wall_config["height"] + ball1.radius) * UP)
        ball2.shift(
            (-ball2.v * self.play_time / 2 + ball2.radius) * RIGHT + (self.wall_config["height"] + ball2.radius) * UP)
        # self.add(self.ball1, self.ball2)

    def add_text(self):
        pass

    def get_loc(self):
        loc1 = self.ball1.get_center()[0]
        loc2 = self.ball2.get_center()[0]
        return loc1, loc2

    def set_loc(self, d_shift1, d_shift2):
        self.ball1.shift(d_shift1 * RIGHT)
        self.ball2.shift(d_shift2 * RIGHT)

    def start_moving(self):
        self.add_updater(Collision.update_by_dt)

    def end_moving(self):
        self.remove_updater(Collision.update_by_dt)

    def update_number(self):
        decimal1 = DecimalNumber(
            0,
            num_decimal_places=2,
            include_sign=True,
            # unit="\\rm cm", # Change this with None
        ).scale(0.4).set_color(self.ball1.get_fill_color())
        decimal1.add_updater(lambda d: d.next_to(self.ball1, UP * 0.1))
        decimal1.add_updater(lambda d: d.set_value(self.ball1.get_center()[0] + self.ball1.radius))
        # self.add(decimal1)

        decimal2 = decimal1.copy().set_color(self.ball2.get_fill_color())
        decimal2.add_updater(lambda d: d.next_to(self.ball2, UP * 0.1))
        decimal2.add_updater(lambda d: d.set_value(self.ball2.get_center()[0] - self.ball2.radius))
        # self.add(decimal2)

        self.m1_m2 = DecimalNumber(0, num_decimal_places=1).scale(0.6).move_to(self.ground.end + DOWN * 0.4, aligned_edge=UR)
        self.m1_m2.add_updater(lambda d: d.set_value(self.ball1.m / self.ball2.m))
        self.text_m = TexMobject("{", "m_{1}", "\\over", "m_{2}", "}", "=").scale(0.6).next_to(self.m1_m2, LEFT,buff=0.1).shift(0.05*DOWN)
        self.text_m[1].set_color(self.ball1.get_fill_color())
        self.text_m[3].set_color(self.ball2.get_fill_color())
        # self.add(self.m1_m2, self.text_m)

        self.v2 = DecimalNumber(0, num_decimal_places=2,include_sign=True,).scale(0.6).next_to(self.m1_m2, LEFT,buff=1.7).shift(0.03*UP)
        self.v2.add_updater(lambda d: d.set_value(self.ball2.v))
        self.text_v2 = TexMobject("v_{2}", "=").scale(0.6).next_to(self.m1_m2, LEFT,buff=2.6)
        self.v2.add_updater(lambda d: d.set_value(self.ball2.v))
        self.text_v2[0].set_color(self.ball2.get_fill_color())
        # self.add(self.v2, self.text_v2)

        self.v1 = DecimalNumber(0, num_decimal_places=2,include_sign=True,).scale(0.6).next_to(self.m1_m2, LEFT,buff=3.7).shift(0.03*UP)
        self.v1.add_updater(lambda d: d.set_value(self.ball1.v))
        self.text_v1 = TexMobject("v_{1}", "=").scale(0.6).next_to(self.m1_m2, LEFT,buff=4.6)
        self.v1.add_updater(lambda d: d.set_value(self.ball1.v))
        self.text_v1[0].set_color(self.ball1.get_fill_color())
        # self.add(self.v1, self.text_v1)

    def update_by_dt(self, dt):
        if (self.ball2.get_center()[0] - self.ball1.get_center()[0]) <= (self.ball1.radius + self.ball2.radius):
            self.while_meet()
        d_shift1 = self.ball1.v * dt# / nspf
        d_shift2 = self.ball2.v * dt# / nspf
        self.set_loc(d_shift1, d_shift2)
        # return self

    def while_meet(self):
        v_sys = (self.ball1.m * self.ball1.v + self.ball2.m * self.ball2.v) / (self.ball1.m + self.ball2.m)
        self.ball1.v = 2 * v_sys - self.ball1.v
        self.ball2.v = 2 * v_sys - self.ball2.v

    def refresh(self,ball1,ball2):
        self.ball1 = ball1
        self.ball2 = ball2
        self.ball1.shift(
            (-self.ball1.v * self.play_time / 2 - self.ball1.radius) * RIGHT + (self.wall_config["height"] + ball1.radius) * UP)
        self.ball2.shift(
            (-self.ball2.v * self.play_time / 2 + self.ball2.radius) * RIGHT + (self.wall_config["height"] + ball2.radius) * UP)


class SpiralModel(VGroup):
    CONFIG = {
        "k": 1,  # 2/3
        "x": 6,
        "r": 0.15,
        "color": BLUE,
        "stroke_width": 4,
        "ball1_config": {
            "radius": 0.3,
            "color": YELLOW,
        },
        "ball2_config": {
            "radius": 0.3,
            "color": RED,
        },
        "n_steps_per_frame": 1,
        "t": 0,
        "total_time": PI,
        "pre_stretch": 1,
    }

    def __init__(self, ball1, ball2, **kwargs):
        super().__init__(**kwargs)
        self.ball1 = ball1
        self.ball2 = ball2
        self.calcu_param()
        self.creat_spiral_line()
        self.update_ball()
        self.update()

    def calcu_param(self):
        self.m_axis = self.ball1.m + self.ball2.m
        self.v_axis = (self.ball1.m * self.ball1.v + self.ball2.m * self.ball2.v) / self.m_axis
        self.ball1.v_r = self.ball1.v - self.v_axis  # 相对坐标系
        self.ball2.v_r = self.ball2.v - self.v_axis

        self.p1 = -self.ball2.m / self.m_axis * self.x  # 将弹簧分割为p1,p2长度
        self.p2 = self.ball1.m / self.m_axis * self.x

        self.max_ritio = self.get_max_ritio()

    def get_max_ritio(self):  # 压缩最大时,Δx与x之比
        t = self.ball2.m / self.m_axis
        return np.sqrt(self.ball1.m / (self.k * t)) * self.ball1.v_r / self.x

    def creat_spiral_line(self):

        self.circle1 = Circle(radius=self.r, color=self.color, stroke_width=self.stroke_width).shift(OUT * self.p1)
        self.spiral = ParametricFunction(lambda t: self.r * complex_to_R3(np.exp(4 * TAU * 1j * t)) + OUT * t,
                                         t_min=self.p1,
                                         t_max=self.p2, color=self.color, stroke_width=self.stroke_width)
        self.circle2 = Circle(radius=self.r, color=self.color, stroke_width=self.stroke_width).shift(OUT * self.p2)
        self.spiral_line = VGroup(self.circle1, self.spiral, self.circle2).rotate(90 * DEGREES, UP, about_point=ORIGIN)
        self.add(self.spiral_line)
        self.spiral_line_copy = self.spiral_line.copy()

    def update_ball(self):
        self.ball1.add_updater(lambda loc: loc.move_to(self.circle1.get_center() + LEFT * self.ball1_config["radius"]))
        self.ball2.add_updater(lambda loc: loc.move_to(self.circle2.get_center() + RIGHT * self.ball2_config["radius"]))
        self.add(self.ball1, self.ball2)
        # v_scale = 1
        # # v1=Vector()
        v1 = Arrow()
        # # v1 = Vector(RIGHT*np.cos(self.t)*v_scale)
        # v1.add_updater(lambda v1: v1.next_to(self.ball1, UP * 0.3))
        # # v1.set_length()
        # v1.add_updater(lambda v1: v1.set_length(RIGHT * np.cos(self.t) * v_scale))
        # self.add(v1)
        #
        # decimal1 = DecimalNumber(
        #     0,
        #     num_decimal_places=2,
        #     include_sign=True,
        #     # unit="\\rm cm", # Change this with None
        # ).scale(0.4).set_color(self.ball1.get_fill_color())
        # decimal1.add_updater(lambda d: d.next_to(v1, UP * 0.1))
        # decimal1.add_updater(lambda d: d.set_value(self.ball1.get_center()[0] + self.ball1.radius))
        # self.add(decimal1)
        #
        # decimal2 = decimal1.copy().set_color(self.ball2.get_fill_color())
        # decimal2.add_updater(lambda d: d.next_to(self.ball2, UP * 0.1))
        # decimal2.add_updater(lambda d: d.set_value(self.ball2.get_center()[0] - self.ball2.radius))
        # self.add(decimal2)

    def get_mass_center(self):
        return (self.circle1.get_center() * self.ball1.m + self.circle2.get_center() * self.ball2.m) / (self.m_axis)

    def update_by_dt(self, dt):
        nspf = self.n_steps_per_frame
        self.t += dt
        if self.t < 1:
            pass
        elif self.t < 3:
            self.set_ball_fixed()
            streth_ritio = (1 - self.max_ritio * np.sin(self.t + dt)) / (1 - self.max_ritio * np.sin(self.t))
            self.spiral_line.stretch(streth_ritio, 0, about_point=ORIGIN)
        elif self.t >= 3:
            self.set_ball_free()

    def update_by_dt2(self, dt):
        # nspf = self.n_steps_per_frame
        self.t += dt
        streth_ritio = (1 - self.max_ritio * np.sin(self.t + dt)) / (1 - self.max_ritio * np.sin(self.t))
        self.spiral_line.stretch(streth_ritio, 0, about_point=ORIGIN)  # .shift(dt*self.v_axis*RIGHT)

    def start_moving(self):
        self.add_updater(SpiralModel.update_by_dt2)

    def end_moving(self):
        self.remove_updater(SpiralModel.update_by_dt2)


# class test_SpiralModel(ThreeDScene):
class test_SpiralModel(Scene):
    def construct(self):
        # self.move_camera(phi=65 * DEGREES,
        #                  theta=-60 * DEGREES,
        #                  distance=100,
        #                  gamma=None,
        #                  frame_center=[2, 2, -2],
        #                  added_anims=[])  # ShowCreation(Circle())

        ball1 = Ball_3D(m=2, v=2, radius=0.3).set_color(YELLOW)
        ball2 = Ball_3D(m=1, v=-1, radius=0.3).set_color(RED)
        s = SpiralModel(ball1, ball2)
        s.shift(UP * 3)
        self.add(s)
        self.wait()
        s.start_moving()
        # self.play(axes2.shift,2*RIGHT,rate_func=linear,run_time=2)
        self.wait(1)
        # self.move_camera(phi=0 * DEGREES,
        #                  theta=-90 * DEGREES,
        #                  distance=100,
        #                  gamma=None,
        #                  # frame_center=[2, 2, 2],
        #                  added_anims=[])  # ShowCreation(Circle())
        self.wait(2)
        s.end_moving()
        self.wait(2)
        # #重新播放一遍
        # self.remove(s)
        # ball1 = Ball_3D(m=2, v=2, radius=0.3).set_color(YELLOW)
        # ball2 = Ball_3D(m=1, v=-1, radius=0.3).set_color(RED)
        # s = SpiralModel(ball1, ball2)
        # s.shift(UP*3)
        # self.add(s)
        # s.start_moving()
        # self.wait(2)
        # s.end_moving()
        # self.wait()


class Ball_3D(Sphere):
    CONFIG = {
        "m": 1,
        "v": 1,
        "v_r": 1,  # 相对坐标速度
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.e = 0.5 * self.m * np.square(self.v)
