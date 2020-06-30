#!/usr/bin/python3
# -*- coding:utf-8 -*-

from manimlib.imports import *
from from_wangkai.utils.imports import *
import numpy as np
# from NumberCreature.omegeCreature import *
# from NumberCreature.numberCreature import *
from NumberCreature.deltaCreature import *
import random

tex_scale = 0.65
color_dict = {'m_{1}': YELLOW, 'm_{2}': RED, 'v_{1}': YELLOW, 'v_{2}': RED, '{v_{1}}\'': YELLOW,
              '{v_{2}}\'': RED, 'F_{1}': YELLOW, 'F_{2}': RED, 'a_{1}': YELLOW, 'a_{2}': RED,
              "v_{C^{'}}": ORANGE, '\\Rightarrow': BLUE, 't': BLUE}  #


class ColorfulCaption(CodeLine):
    CONFIG = {
        't2c': {
            "黄球": YELLOW,
            "红球": RED,
        }
    }


class test_color(Scene):
    def construct(self):
        color_dict = {'m_{1}': YELLOW, 'm_{2}': RED, 'v_{1}': YELLOW, 'v_{2}': RED, '{v_{1}}\'': YELLOW,
                      '{v_{2}}\'': RED, }
        xy_form = TexMobject('m_{1} = {v_{1}}\'', '+', 'y', 'i').set_color_by_tex_to_color_map(color_dict)
        cs_form = TexMobject('z', '=', 'r', '(', '\\cos{', '\\theta}', '+', 'i', '\\sin{', '\\theta}',
                             ')').set_color_by_tex_to_color_map(color_dict)
        exp_form = TexMobject("\\frac{1}{2}m_{1}v_{1}^{2}", "+", "\\frac{1}{2}m_{2}v_{2}^{2}", "=",
                              "\\frac{1}{2}m_{1}{v_{1}}\'^{2}", "+",
                              "\\frac{1}{2}m_{2}{v_{1}}\'^{2}").set_color_by_tex_to_color_map(color_dict).scale(1.2)
        self.play(Write(xy_form))
        self.wait(1)
        self.play(ReplacementTransform(xy_form, cs_form))
        self.wait(1)
        self.play(ReplacementTransform(cs_form, exp_form))
        self.wait()


class V1_V2(MyGraphScene):
    CONFIG = {
        "x_min": -3,
        "x_max": 3,
        "x_axis_width": 6,
        "x_tick_frequency": 1,
        "x_leftmost_tick": None,  # Change if different from x_min
        "x_labeled_nums": None,
        "x_axis_label": "$v_{1}$",
        "y_min": -3,
        "y_max": 3,
        "y_axis_height": 6,
        "y_tick_frequency": 1,
        "y_bottom_tick": None,  # Change if different from y_min
        "y_labeled_nums": None,
        "y_axis_label": "$v_{2}$",
        "axes_color": GREY,
        "graph_origin": 1 * DOWN + 4 * LEFT,
        "exclude_zero_label": True,
        "default_graph_colors": [BLUE, GREEN, YELLOW],
        "default_derivative_color": GREEN,
        "default_input_color": YELLOW,
        "default_riemann_start_color": BLUE,
        "default_riemann_end_color": GREEN,
        "area_opacity": 0.8,
        "num_rects": 50,
    }


class StartScene(VideoStart):
    CONFIG = {
        "author": "雨落释心",
        "title": "动量定理和动量守恒"
    }


class Scene1_5(SpecialThreeDScene):  # 0:06-0:30
    CONFIG = {
        "default_angled_camera_position": {
            "phi": 65 * DEGREES,  # Angle off z axis
            "theta": -60 * DEGREES,  # Rotation about z axis
            "distance": 50,
            "gamma": 0,  # Rotation about normal vector to camer
        }
    }

    def construct(self):
        # 常量定义
        m1 = 1.0
        m2 = 1.0
        r = 0.4
        t = 2
        n = 15  # 小球碰撞展示次数
        vx_max = 9 // t
        vy_max = 6 // t

        # 对象
        self.set_camera_to_default_position()
        # axes = self.get_axes()
        axes2 = Axes()
        surface = ParametricSurface(lambda u, v: np.array([u, v, 0]),
                                    u_min=-20, u_max=20, v_min=-20, v_max=20, resolution=(20, 20), fill_color=GREY,
                                    fill_opacity=0.2, stroke_width=0.2, stroke_opacity=0.4,
                                    checkerboard_colors=[None, None], )

        yellow_ball = Sphere(radius=r, resolution=(8, 16)).set_color(YELLOW)
        red_ball = Sphere(radius=r, resolution=(8, 16)).set_color(RED)

        balln1_lst = []  # 黄球列表,MObject
        balln2_lst = []  # 红球列表,MObject
        for i in range(n):  # 生成MObject
            balln1_lst.append(yellow_ball.copy())
            balln2_lst.append(red_ball.copy())

        # circle31 = Circle()
        # circle32 = Circle()

        # 随机初始化黄球和红球速度
        rand_v1 = [np.array([np.random.rand() * vx_max, np.random.rand() * vy_max - vy_max / 2, 0]) for i in
                   range(n)]  # 黄
        rand_v2 = [np.array([-np.random.rand() * vx_max, np.random.rand() * vy_max - vy_max / 2, 0]) for i in
                   range(n)]  # 红
        # rand_v2 = [np.array([0, 0, 0]) for i in range(n)]  # 红
        balln1_list = []  # 黄球列表
        balln2_list = []  # 红球列表
        point1_list = []
        point2_list = []
        for i in range(n):
            delta_loc = set_loc0(rand_v1[i], rand_v2[i], r)[0]
            balln1_list.append(Ball_2D(m1, v=rand_v1[i], loc=delta_loc))
            point1_list.append(Circle(radius=0.4, stroke_width=0.5).move_to(twoD2threeD(balln1_list[i].loc)))
            balln2_list.append(Ball_2D(m2, v=rand_v2[i], loc=-delta_loc))
            point2_list.append(Circle(radius=0.4, stroke_width=0.5).move_to(twoD2threeD(balln2_list[i].loc)))

        # 移动
        for i in range(n):
            balln1_lst[i].shift(get_loc(balln1_list[i], -t))  # 黄mob
            balln2_lst[i].shift(get_loc(balln2_list[i], -t))  # 红

        # 动画函数定义
        def meet_action(ball1, ball1_, ball2, ball2_):
            # self.add(ball1, ball2)
            self.play(FadeIn(ball1), FadeIn(ball2), run_time=0.5)
            self.play(ball1.shift, ball1_.v * t, ball2.shift, ball2_.v * t, run_time=t, rate_func=linear, )
            after1, after2 = balls_meet_(ball1_, ball2_)
            self.play(ball1.shift, after1.v * t, ball2.shift, after2.v * t, run_time=t, rate_func=linear, )
            self.wait(1)
            # self.remove(ball1, ball2)
            self.play(FadeOut(ball1), FadeOut(ball2), run_time=0.5)

        def meet_action2(ball1, ball1_, ball2, ball2_):
            # self.add(ball1, ball2)
            self.play(FadeIn(ball1), FadeIn(ball2), run_time=0.5)
            self.play(ball1.shift, ball1_.v * t / 2, ball2.shift, ball2_.v * t / 2, run_time=t / 2, rate_func=linear, )

            dot01 = Dot(ball1_.loc - ball1_.v + OUT, color=WHITE)
            dot02 = Dot(ball2_.loc - ball2_.v + OUT, color=WHITE)
            arrow01 = Arrow(start=ball1_.loc - ball1_.v * t / 2 + OUT, end=ball1.get_center() + OUT, color=WHITE,
                            buff=0)
            arrow02 = Arrow(start=ball2_.loc - ball2_.v * t / 2 + OUT, end=ball2.get_center() + OUT, color=WHITE,
                            buff=0)
            self.add(dot01, dot02, arrow01, arrow02)

            def update_arrow01(arrow):
                arrow.become(
                    Arrow(start=ball1_.loc - ball1_.v * t / 2 + OUT, end=ball1.get_center() + OUT, color=WHITE, buff=0)
                )

            def update_arrow02(arrow):
                arrow.become(
                    Arrow(start=ball2_.loc - ball2_.v * t / 2 + OUT, end=ball2.get_center() + OUT, color=WHITE, buff=0)
                )

            arrow01.add_updater(update_arrow01)
            arrow02.add_updater(update_arrow02)

            self.play(ball1.shift, ball1_.v * t / 2, ball2.shift, ball2_.v * t / 2, run_time=t / 2, rate_func=linear, )
            arrow01.remove_updater(update_arrow01)
            arrow02.remove_updater(update_arrow02)

            after1, after2 = balls_meet_(ball1_, ball2_)
            circle1 = Circle(arc_center=after1.loc + OUT, radius=ball1.radius, color=YELLOW)
            circle2 = Circle(arc_center=after2.loc + OUT, radius=ball2.radius, color=RED)
            self.add(circle1, circle2)

            dot1 = Dot(after1.loc + OUT, color=BLUE)
            dot2 = Dot(after2.loc + OUT, color=BLUE)
            arrow1 = Arrow(start=after1.loc + OUT, end=ball1.get_center() + OUT, color=BLUE, buff=0)
            arrow2 = Arrow(start=after2.loc + OUT, end=ball2.get_center() + OUT, color=BLUE, buff=0)
            self.add(dot1, dot2, arrow1, arrow2)

            def update_arrow1(arrow):
                arrow.become(
                    Arrow(start=after1.loc + OUT, end=ball1.get_center() + OUT, color=BLUE, buff=0)
                )

            def update_arrow2(arrow):
                arrow.become(
                    Arrow(start=after2.loc + OUT, end=ball2.get_center() + OUT, color=BLUE, buff=0)
                )

            arrow1.add_updater(update_arrow1)
            arrow2.add_updater(update_arrow2)
            self.play(ball1.shift, after1.v * t / 2, ball2.shift, after2.v * t / 2, run_time=t / 2, rate_func=linear, )
            arrow1.remove_updater(update_arrow1)
            arrow2.remove_updater(update_arrow2)

            self.play(ball1.shift, after1.v * t / 2, ball2.shift, after2.v * t / 2, run_time=t / 2, rate_func=linear, )
            self.wait(1)
            # self.play(arrow01.copy().shift, -arrow01.start,)
            self.remove(ball1, ball2)
            # self.remove(ball1, ball2)

            Ale = Alex().to_corner(DR)
            palabras_ale = TextMobject("碰撞后的速度 \\\\该如何计算呢?", color=WHITE).scale(0.6)
            self.add(Ale)
            self.play(DeltaCreatureSays(
                Ale, palabras_ale,
                bubble_kwargs={"height": 3, "width": 4},
                target_mode="speaking",
                bubble_class=ThoughtBubble  # SpeechBubble,DoubleSpeechBubble,ThoughtBubble
            ))
            self.wait()
            self.play(Ale.look_at, ORIGIN)
            self.play(Blink(Ale))
            self.wait(0.5)
            self.play(Blink(Ale))
            self.wait(1)

        # 播放

        self.play(FadeIn(surface), run_time=1)
        meet_action(balln1_lst[10], balln1_list[10], balln2_lst[10], balln2_list[10])
        # meet_action(balln1_lst[8], balln1_list[8], balln2_lst[8], balln2_list[8]) #6s
        self.move_camera(phi=0, theta=-90 * DEGREES, run_time=2, added_anims=[])
        self.wait()
        meet_action2(balln1_lst[3], balln1_list[3], balln2_lst[3], balln2_list[3])


class Scene6_42(V1_V2):
    def energy(self, x):
        return np.sqrt(5 - np.square(x)), -np.sqrt(5 - np.square(x)),

    def duichen_line(self, x):
        return (1.0 - x)

    def rand_curve(self, x):
        return -(x ** 3) / 8

    def construct(self):
        Ale = Alex().to_corner(DL).scale(0.7)
        palabras_ale = TextMobject("如果碰撞前两球\\\\速度不等呢?", color=WHITE).scale(0.6)

        def Alex_think(think_mob):
            self.add(Ale)
            self.play(DeltaCreatureSays(
                Ale, think_mob,
                bubble_kwargs={"height": 3, "width": 4},
                target_mode="speaking",
                bubble_class=ThoughtBubble  # SpeechBubble,DoubleSpeechBubble,ThoughtBubble
            ))
            self.wait()
            self.play(Ale.look_at, ORIGIN)
            self.play(Blink(Ale))
            self.wait(1)
            self.play(Blink(Ale))
            self.wait(1)
            self.play(Ale.shrug)

        def get_buff(point, buff):
            return buff * normalize(point.get_center() - self.graph_origin)

        # 播放 0.30-0.44
        cls = Collision()
        self.add(cls)
        self.play(ShowCreation(cls.ground), run_time=1)
        self.wait(0.5)
        self.play(ShowCreation(cls.ball1), ShowCreation(cls.ball2), run_time=1)
        self.wait(0.5)
        self.play(Write(cls.text_v1))
        self.play(Write(cls.v1))
        self.play(Write(cls.text_v2))
        self.play(Write(cls.v2))
        self.play(FadeIn(cls.text_m))
        self.play(Write(cls.m1_m2))
        self.wait(0.5)
        self.play(ShowPassingFlashAround(cls.v1), ShowPassingFlashAround(cls.v2), run_time=1)
        self.wait(0.5)
        self.play(ShowPassingFlashAround(cls.m1_m2), run_time=1)
        self.wait(2)

        # meet1 0.44-
        vg1 = VGroup()
        dcx1 = TexMobject("{v_{1}}\'", "=-", "{v_{2}}\'", ).set_color_by_tex_to_color_map(color_dict).scale(
            tex_scale).move_to(UP + RIGHT * 0.8, aligned_edge=LEFT)
        jxnsh1 = TexMobject("\\frac{1}{2}m_{1}v_{1}^{2}", "+", "\\frac{1}{2}m_{2}v_{2}^{2}", "=",
                            "\\frac{1}{2}m_{1}{v_{1}}\'^{2}", "+",
                            "\\frac{1}{2}m_{2}{v_{2}}\'^{2}").set_color_by_tex_to_color_map(color_dict).scale(
            tex_scale).next_to(dcx1, DOWN * 1, aligned_edge=LEFT)
        eqution_vg = VGroup(dcx1, jxnsh1)
        brace = Brace(eqution_vg, LEFT)
        # right_arrow = TexMobject('\\Rightarrow').set_color_by_tex_to_color_map(color_dict).scale(tex_scale).next_to(dcx1, DOWN * 1, aligned_edge=LEFT)
        therefore = TexMobject('\\therefore', "{v_{1}}\'", "=-", "{v_{2}}\'", "=-2").set_color_by_tex_to_color_map(
            color_dict).scale(tex_scale).next_to(brace, DOWN * 1.6, aligned_edge=LEFT).shift(RIGHT * 0.5)
        vg1.add(eqution_vg, brace, therefore)
        self.wait(1)
        self.play(TransformFromCopy(cls.text_v1, dcx1[0]), TransformFromCopy(cls.text_v2, dcx1[2]), Write(dcx1[1]),
                  run_time=2)
        self.wait(1.5)

        self.play(TransformFromCopy(cls.ball1, jxnsh1[0]), Write(jxnsh1[1]),
                  TransformFromCopy(cls.ball2, jxnsh1[2]), Write(jxnsh1[3]),
                  TransformFromCopy(cls.ball1, jxnsh1[4]), Write(jxnsh1[5]),
                  TransformFromCopy(cls.ball2, jxnsh1[6]),
                  run_time=2)
        self.wait(1)
        self.play(ShowCreation(brace), run_time=0.5)
        self.wait(1)

        self.play(Write(therefore), run_time=1)  # 52s开始
        self.wait()
        cls.start_moving()
        self.wait(3)
        cls.end_moving()
        self.wait(1.5)
        # self.play(FadeOut(vg1))

        # meet2 58.5s开始

        self.add(Ale)
        self.play(DeltaCreatureSays(
            Ale, palabras_ale,
            bubble_kwargs={"height": 3, "width": 4},
            target_mode="speaking",
            bubble_class=ThoughtBubble  # SpeechBubble,DoubleSpeechBubble,ThoughtBubble
        ))
        self.wait(1)
        self.play(Ale.look_at, ORIGIN)
        self.play(Blink(Ale))
        self.wait(0.5)
        self.play(Blink(Ale))

        # 1：04
        self.remove(cls.ground, cls.ball1, cls.ball2, cls.v1, cls.v2, cls.text_v1, cls.text_v2, cls.m1_m2, cls.text_m)
        del cls
        self.wait()
        cls = Collision(ball1_config={
            "fill_color": YELLOW,
            "m": 1,
            "v": 2,
        },
            ball2_config={
                "fill_color": RED,
                "m": 1,
                "v": -1,
            },
        )
        self.add(cls, cls.ground, cls.ball1, cls.ball2, cls.v1, cls.v2, cls.text_v1, cls.text_v2, cls.m1_m2, cls.text_m)
        self.wait(2)
        self.play(ShowPassingFlashAround(VGroup(cls.text_v2, cls.v2)), run_time=2)
        self.wait()

        self.play(RemovePiCreatureBubble(Ale), FadeOut(Ale), run_time=1)
        self.wait(1)
        # 1:12
        self.play(dcx1.set_fill, {"opacity": 0.01},
                  brace.set_fill, {"opacity": 0.01}, run_time=2)
        self.wait(3)
        self.play(ShowPassingFlashAround(jxnsh1), run_time=2)
        self.wait(1)
        therefore2 = TexMobject('\\therefore', "{v_{1}}\'^{2}", "+", "{v_{2}}\'^{2}",
                                "=", "5", ).set_color_by_tex_to_color_map(
            color_dict).scale(tex_scale).next_to(brace, DOWN * 1.6, aligned_edge=LEFT).shift(RIGHT * 0.5)

        # 1:20
        self.play(ReplacementTransform(therefore, therefore2), run_time=2)
        self.wait()
        self.play(ShowPassingFlashAround(therefore2), run_time=2)
        self.wait(4)
        self.play(ShowPassingFlashAround(cls.text_v1), ShowPassingFlashAround(cls.text_v2), run_time=2)
        self.wait(4)
        self.play(ShowPassingFlashAround(jxnsh1), run_time=2)
        self.wait(2.5)

        # 建立v2-v1 1:39.5
        self.setup_axes(animate=True)
        c1 = self.axes
        self.wait(11)
        dot_test = Dot(color=ORANGE)
        dot = Dot(color=ORANGE)
        dot.add_updater(lambda d: d.move_arc_center_to(self.coords_to_point(cls.ball1.v, cls.ball2.v)))
        self.play(FadeIn(dot))
        self.wait(2)
        self.play(FocusOn(dot), run_time=2)
        self.wait(2)
        # l_v1=DashedLine(start=dot.get_center(),end=)
        node1 = Dot(color=YELLOW)
        node2 = Dot(color=RED)
        node1.add_updater(lambda node1: node1.move_arc_center_to(self.coords_to_point(cls.ball1.v, 0)))
        node2.add_updater(lambda node2: node2.move_arc_center_to(self.coords_to_point(0, cls.ball2.v)))

        coord_x = DecimalNumber(
            0,
            num_decimal_places=2,
            include_sign=False,
        ).scale(0.5).set_color(cls.ball1.get_fill_color())
        coord_x.add_updater(lambda d: d.set_value(cls.ball1.v))
        coord_y = DecimalNumber(
            0,
            num_decimal_places=2,
            include_sign=False,
        ).scale(0.5).set_color(cls.ball2.get_fill_color())
        coord_y.add_updater(lambda d: d.set_value(cls.ball2.v))
        text_coord = [TextMobject("(").scale(0.4), coord_x, TextMobject(",").scale(0.4), coord_y,
                      TextMobject(")").scale(0.4)]
        vg_coord = VGroup(*text_coord)
        vg_coord.add_updater(lambda d: d.arrange_submobjects(RIGHT, buff=0.06, aligned_edge=DOWN))
        vg_coord.add_updater(lambda d: d.next_to(dot, direction=get_buff(dot, 0.1)))
        self.add(vg_coord)
        self.play(Write(vg_coord), run_time=2)
        self.wait(2)
        # 2:02.5
        energy = Circle(radius=np.sqrt(5), color=ORANGE).set_stroke(width=2).move_to(self.graph_origin)
        self.wait(4.5)
        # self.play(TransformFromCopy(jxnsh1, energy), run_time=1.5)
        self.play(ShowCreation(energy, run_time=3))
        self.wait(2)
        # 2:12
        bluedot = Dot(color=BLUE).move_arc_center_to(self.coords_to_point(-2, 1))
        self.play(FadeIn(bluedot))
        self.wait()
        self.play(MoveAlongPath(bluedot, energy), run_time=2.5, rate_func=linear)
        self.wait()
        # 2:17.5
        self.wait(5)
        fg_rand = self.get_graph(self.rand_curve, WHITE, x_min=-2.2, x_max=2.2)
        self.play(ShowCreation(fg_rand), run_time=3)
        self.wait()
        bluedot_ = Dot(color=BLUE).move_arc_center_to(self.coords_to_point(-2, 1))
        self.play(CircleIndicate(bluedot_), run_time=1)
        self.wait()
        self.play(bluedot.move_to, self.coords_to_point(-2, 1), run_time=1)
        # 2:32.5
        self.wait(0.5)
        self.play(ApplyWave(fg_rand), run_time=2)
        self.wait()
        self.play(
            jxnsh1.set_fill, {"opacity": 0.01},
            therefore2.set_fill, {"opacity": 0.01},
            FadeOut(fg_rand),
            FadeOut(bluedot)
        )
        self.wait(2)

        # 添加坐标系C' 2:39
        Ale.to_corner(DR)
        thought2 = TextMobject("能否将模型变成和之前\\\\一样的对称模型呢?", color=WHITE).scale(0.6)
        # Alex_think(thought2)
        self.add(Ale)
        self.play(DeltaCreatureSays(
            Ale, thought2,
            bubble_kwargs={"height": 3, "width": 4},
            target_mode="speaking",
            bubble_class=ThoughtBubble  # SpeechBubble,DoubleSpeechBubble,ThoughtBubble
        ))
        self.wait()
        self.play(Ale.look_at, ORIGIN)
        self.play(Blink(Ale))
        self.wait(0.5)
        self.play(Blink(Ale))
        self.wait(0.5)
        self.play(RemovePiCreatureBubble(Ale), FadeOut(Ale))

        # 2：46
        vg_dot = VGroup(Dot(color=ORANGE).move_to(RIGHT * 3.5 + UP).scale(0.5),
                        Dot(color=YELLOW).scale(0.5).move_to(RIGHT * 1.5),
                        Dot(color=RED).scale(0.5).move_to(RIGHT * 4.5),
                        Dot(color=ORANGE).move_to(RIGHT * 3.0).scale(0.1)
                        )
        vg_arrow = VGroup(Arrow(color=ORANGE),
                          Arrow(color=YELLOW),
                          Arrow(color=RED),
                          )
        dl___ = DashedLine(start=RIGHT * 3.5, end=RIGHT * 3.5 + UP).set_color(ORANGE)
        vg_arrow[0].add_updater(lambda a: a.put_start_and_end_on(vg_dot[3].get_center() + UP, vg_dot[0].get_center()))
        vg_arrow[1].add_updater(lambda a: a.put_start_and_end_on(vg_dot[1].get_center(), vg_dot[3].get_center()))
        vg_arrow[2].add_updater(lambda a: a.put_start_and_end_on(vg_dot[2].get_center(), vg_dot[3].get_center()))
        vg_v_ = VGroup(TexMobject("v_{C^{'}}{:}").scale(0.5).move_to(RIGHT * 3 + UP * 1.5),
                       TexMobject("v_{1}{:}").scale(0.5).move_to(RIGHT * 1.8 + DOWN * 0.5),
                       TexMobject("v_{2}{:-}").scale(0.5).move_to(RIGHT * 3.6 + DOWN * 0.5),
                       )
        vg_vv_ = VGroup(
            DecimalNumber(0, num_decimal_places=2, include_sign=True, ).scale(0.4).next_to(vg_v_[0], RIGHT, buff=0.06),
            DecimalNumber(0, num_decimal_places=2, include_sign=True, ).scale(0.4).next_to(vg_v_[1], RIGHT, buff=0.06),
            DecimalNumber(0, num_decimal_places=2, include_sign=False, ).scale(0.4).next_to(vg_v_[2], RIGHT, buff=0.06),
        )
        vg_vv_[0].add_updater(lambda a: a.set_value(vg_arrow[0].get_length()))
        vg_vv_[1].add_updater(lambda a: a.set_value(vg_arrow[1].get_length()))
        vg_vv_[2].add_updater(lambda a: a.set_value(vg_arrow[2].get_length()))
        self.wait()
        self.add(vg_dot, vg_arrow, vg_v_, vg_vv_, dl___)
        self.play(vg_dot[3].shift, LEFT * 0.8, run_time=2)
        self.play(vg_dot[3].shift, RIGHT * 1.2, run_time=3)
        self.play(vg_dot[3].shift, LEFT * 0.4, run_time=2)
        self.wait(2)

        # 2:56
        text_vc1 = TextMobject("参考系", "$v_{C^{'}}$", "的速度:").set_color_by_tex_to_color_map(color_dict).scale(
            tex_scale).move_to(DOWN * 2 + RIGHT * 1, aligned_edge=LEFT)
        text_vc2 = TexMobject("v_{C^{'}}", "=\\frac{1}{2}(", "v_{1}", "+", "v_{2}",
                              ")=0.5").set_color_by_tex_to_color_map(
            color_dict).scale(
            tex_scale).next_to(text_vc1, DOWN * 1, aligned_edge=LEFT)
        self.play(Write(text_vc1))
        self.play(Write(text_vc2))
        self.wait(20)

        # 3:18 - 3:33
        c2 = c1.copy()
        text_dot1_ = [TextMobject("初速度：(").scale(0.5), TextMobject("1.5").scale(0.5).set_color(YELLOW),
                      TextMobject(",").scale(0.5), TextMobject("-1.5").scale(0.5).set_color(RED),
                      TextMobject(")").scale(0.5)]
        text_dot1 = VGroup(*text_dot1_).arrange_submobjects(RIGHT, buff=0.1).next_to(dot, DOWN, 0.2)
        text_c2 = TexMobject("C^{'}").set_color(BLUE).scale(0.7).next_to(self.coords_to_point(0.5, 0.5), UR, 0.3)
        self.play(
            c2.shift, UR * 0.5,
            c1.set_stroke, {"opacity": 0.1},
            energy.set_stroke, {"opacity": 0.03},
            vg_coord.set_fill, {"opacity": 0.01},
            FadeIn(text_dot1),
            FadeIn(text_c2),
            run_time=3,
        )
        self.wait(12)
        # 3:33-3:38
        self.wait(5)
        # vg_coord2 = vg_coord.copy()
        # vg_coord2[1].add_updater(lambda d: d.set_value(cls.ball1.v - 0.5))
        # vg_coord2[3].add_updater(lambda d: d.set_value(cls.ball2.v - 0.5))
        # vg_coord2.add_updater(lambda d: d.arrange_submobjects(RIGHT, buff=0.06, aligned_edge=DOWN))
        # vg_coord2.add_updater(lambda d: d.move_to(vg_coord.get_center()))
        # self.add(vg_coord2)
        dunchen_dot = Dot(color=BLUE).move_arc_center_to(self.coords_to_point(-1, 2))
        origin_dot = Dot().move_arc_center_to(self.coords_to_point(0.5, 0.5))
        dunchen_line = DashedLine(start=dunchen_dot.get_center(), end=dot.get_center()).set_color(BLUE).set_stroke(
            width=1)
        # energy2 = Circle(radius=np.sqrt(4.5), color=ORANGE).move_to(0.5 * DOWN + 3.5 * LEFT)
        text_dot2_ = [TextMobject("末速度：(").scale(0.5), TextMobject("-1.5").scale(0.5).set_color(YELLOW),
                      TextMobject(",").scale(0.5), TextMobject("1.5").scale(0.5).set_color(RED),
                      TextMobject(")").scale(0.5)]
        text_dot2 = VGroup(*text_dot2_).arrange_submobjects(RIGHT, buff=0.1).next_to(dunchen_dot, UP, 0.2)
        # 3:38-3:54
        self.play(ShowCreation(origin_dot))
        self.wait(2)
        self.play(ShowCreation(dunchen_line), run_time=2)
        self.wait(3)
        self.play(FocusOn(dunchen_dot), run_time=2)
        self.add(dunchen_dot)
        self.wait()
        self.play(Write(text_dot2, run_time=2))
        self.wait(3)
        # 3:54-4:00
        self.play(
            c2.set_stroke, {"opacity": 0.1},
            c1.set_stroke, {"opacity": 0.6},
            # energy.set_stroke, {"opacity": 1},
            vg_coord.set_fill, {"opacity": 1},
            FadeOut(text_dot1),
            FadeOut(text_dot2),
            run_time=1.5
        )
        cls.start_moving()
        self.wait(3.4)
        cls.end_moving()
        self.wait(0.1)


def create_v1v2(self):
    self.v1v2 = V1_V2()
    self.dot = Dot(color=ORANGE)
    self.dot.add_updater(lambda d: d.move_arc_center_to(np.array([self.ball1.v, self.ball2.v, 0])))
    self.add(self.v1v2, self.dot)


class SpringScene(Scene):
    CONFIG = {
        "axes_config": {
            "x_min": -3.7,
            "x_max": 3.7,
            "y_min": -3.7,
            "y_max": 3.7,
            "x_axis_config": {
                "tick_frequency": 1,
                "include_tip": True,

            },
            "num_axis_pieces": 1,
        },
        "t_tracker": ValueTracker(0.01),
        "ritio_tracker": ValueTracker(1),
        "axis_scale": 0.72,
        "axis_v": 0.01,
    }

    def get_vv_axes(self, include_labels=True, include_numbers=False, ):
        config = dict(self.axes_config)
        vv_config = dict(
            x_axis_config={
                "stroke_color": YELLOW,
                "tick_size": 0.06,
                "stroke_opacity": 0.6,
                "stroke_width": 2,
            },
            y_axis_config={
                "stroke_color": RED,
                "tick_size": 0.06,
                "stroke_opacity": 0.6,
                "stroke_width": 2,
            },
        )
        config.update(vv_config)
        axes = Axes(**config)
        axes.set_stroke(width=2)
        if include_numbers:
            self.add_axes_numbers(axes)

        if include_labels:
            self.add_axes_labels(axes, "v_{1}", "v_{2}")

        axes.x_axis.label.set_color(YELLOW)
        axes.y_axis.label.set_color(RED)
        axes.scale(self.axis_scale)
        axes.shift(1.3 * DOWN + 4.3 * LEFT)

        return axes

    def get_vt_axes(self, include_labels=True, include_numbers=False, ):
        config = dict(self.axes_config)
        vt_config = dict(
            x_min=0,
            x_max=TAU + 0.7,
            y_min=-3.7,
            y_max=3.7,
            x_axis_config={
                "stroke_color": BLUE,
                "tick_frequency": 100,
                "tick_size": 0.06,
                "stroke_opacity": 0.6,
                "stroke_width": 2,
            },
            y_axis_config={
                "stroke_color": ORANGE,
                "tick_size": 0.06,
                "stroke_opacity": 0.6,
                "stroke_width": 2,
            },
        )
        config.update(vt_config)
        axes = Axes(**config)
        axes.set_stroke(width=2)
        if include_numbers:
            self.add_axes_numbers(axes)

        if include_labels:
            self.add_axes_labels(axes, "t", "v")

        axes.x_axis.label.set_color(BLUE)
        axes.y_axis.label.set_color(ORANGE)
        axes.scale(self.axis_scale)
        axes.shift(1.3 * DOWN + 0.6 * RIGHT)

        return axes

    def get_model_axes(self):
        axes = Axes().set_stroke(opacity=0.3)
        axes.scale(0.75)
        axes.shift(3.2 * UP + 3 * LEFT)
        return axes

    def add_axes_labels(self, axes, x, y):
        x_label = TexMobject(x)
        x_label.next_to(axes.x_axis.get_end(), RIGHT)
        axes.x_axis.label = x_label

        y_label = TexMobject(y)
        y_label.next_to(axes.y_axis.get_end(), UP)
        axes.y_axis.label = y_label

        for axis in axes:
            axis.add(axis.label)
        return axes

    def get_ball1_graph(self, vt, m1, v1, m2, v2, t, **kwargs):
        ritio1 = m2 / (m1 + m2)
        ritio2 = m1 / (m1 + m2)
        delta_v = v1 - v2
        amp1 = ritio1 * delta_v
        amp2 = ritio2 * delta_v
        offset = v1 - amp1

        config1 = dict(color=YELLOW, stroke_width=2.5)

        config1.update({
            "t_min": 0,
            "t_max": t,
        })
        config1.update(**kwargs)

        l1 = ParametricFunction(
            lambda t: vt.c2p(
                t, amp1 * np.cos(0.5 * t) + offset
            ),
            **config1,
        )
        return l1

    def get_ball2_graph(self, vt, m1, v1, m2, v2, t, **kwargs):
        ritio1 = m2 / (m1 + m2)
        ritio2 = m1 / (m1 + m2)
        delta_v = v1 - v2
        amp1 = ritio1 * delta_v
        amp2 = ritio2 * delta_v
        offset = v1 - amp1

        config2 = dict(color=RED, stroke_width=2.5)

        config2.update({
            "t_min": 0,
            "t_max": t,
        })
        config2.update(**kwargs)

        l2 = ParametricFunction(
            lambda t: vt.c2p(
                t, amp2 * -np.cos(0.5 * t) + offset
            ),
            **config2,
        )
        return l2

    def get_time_dashline(self, vt, ball1_graph, ball2_graph, **kwargs):
        def get_intersection(dot):
            t0, v = vt.p2c(dot.get_center())
            p1 = vt.c2p(t0, 0)
            p2 = vt.c2p(0, v)
            return p1, p2

        config1 = dict(stroke_width=1, stroke_color=YELLOW)
        config2 = dict(stroke_width=1, stroke_color=RED)
        config3 = dict(stroke_width=1, stroke_color=BLUE)

        dot1 = Dot(color=YELLOW).scale(0.5).move_to(ball1_graph.get_end())
        p11, p12 = get_intersection(dot1)
        dl11 = DashedLine(dot1.get_center(), p11, **config3)
        dl12 = DashedLine(dot1.get_center(), p12, **config1)

        dot2 = Dot(color=RED).scale(0.5).move_to(ball2_graph.get_end())
        p21, p22 = get_intersection(dot2)
        dl21 = DashedLine(dot2.get_center(), p21, **config3)
        dl22 = DashedLine(dot2.get_center(), p22, **config2)

        t_num = DecimalNumber(vt.p2c(p11)[0] / PI, num_decimal_places=2, include_sign=False, color=BLUE).scale(
            0.35).next_to(p11, DR,
                          buff=0.06)
        v1_num = DecimalNumber(vt.p2c(p12)[1], num_decimal_places=2, include_sign=True, color=YELLOW).scale(
            0.35).next_to(
            p12, LEFT, buff=0.1)
        v2_num = DecimalNumber(vt.p2c(p22)[1], num_decimal_places=2, include_sign=True, color=RED).scale(0.35).next_to(
            p22, LEFT, buff=0.1)
        # t_num.add_updater(lambda t: t.set_value(vt.p2c(p11)[0]))
        # v1_num.add_updater(lambda v1: v1.set_value(vt.p2c(p12)[1]))
        # v2_num.add_updater(lambda v2: v2.set_value(vt.p2c(p22)[1]))
        vg_dashline = VGroup(dl11, dl12, dl21, dl22, dot1, dot2, t_num, v1_num, v2_num)
        return vg_dashline

    def get_tangent_line(self, ball1_graph, ball2_graph, **kwargs):
        config1 = dict(stroke_width=1, )
        config2 = dict(stroke_width=1, )
        vg = VGroup(TangentLine(ball1_graph, 1, **config1), TangentLine(ball2_graph, 1, **config2), )
        return vg

    def get_dot_vv(self, vv, vt, ball1_graph, ball2_graph, **kwargs):
        x1, y1 = vt.p2c(ball1_graph.get_end())
        x2, y2 = vt.p2c(ball2_graph.get_end())
        dot_vv = Dot(vv.c2p(y1, y2)).scale(0.8).set_color(ORANGE)
        return dot_vv

    def get_vv_line(self, vv, dot_vv):
        config = dict(stroke_width=1.5, color=ORANGE)
        origin_vv = Dot(vv.c2p(2, -1)).scale(0.8).set_color(ORANGE)
        dl = Line(start=origin_vv.get_center(), end=dot_vv.get_center(), **config)
        return VGroup(origin_vv, dl)

    def get_model(self, model_axes, ball1, ball2, t, is_static=False, **kwargs):
        # 整体参数
        x_strength = 2
        t = t / x_strength  # 此处t由实际时刻转化成时间轴的点的值
        spring_len = 6.0
        spring_circle_num = 18
        spring_radius = 0.175
        spring_color = GREEN

        axis_init_loc = model_axes.center_point
        axis_m = ball1.m + ball2.m
        axis_momentum = ball1.m * ball1.v + ball2.m * ball2.v

        # if is_static:
        #     axis_v = 0
        # else:
        #     axis_v = axis_momentum / axis_m
        # axis_t_loc = axis_init_loc + axis_v * t * RIGHT
        # axis_t_loc_x = axis_v * t
        axis_v = axis_momentum / axis_m
        if is_static:
            axis_t_loc_x = 0
        else:
            axis_t_loc = axis_init_loc + axis_v * t * RIGHT
            axis_t_loc_x = axis_v * t

        # 弹簧参数
        offset1 = (ball1.v - axis_v) * np.sin(t)
        offset2 = (ball2.v - axis_v) * np.sin(t)

        min_ = -ball2.m / axis_m * spring_len + offset1 + axis_t_loc_x
        max_ = ball1.m / axis_m * spring_len + offset2 + axis_t_loc_x
        config = dict()
        config.update({
            "t_min": min_,
            "t_max": max_,
            "color": spring_color,
        })
        config.update(**kwargs)
        spring_dense = spring_len / (spring_len - offset1 + offset2)
        spring = ParametricFunction(
            lambda t: model_axes.c2p(
                t, spring_radius * np.sin(spring_dense * spring_circle_num * (t - axis_t_loc_x))
            ),
            **config,
        )
        circle1 = Line(model_axes.c2p(0, -spring_radius - 0.02), model_axes.c2p(0, spring_radius + 0.02),
                       color=spring_color).next_to(spring, LEFT, buff=0)
        circle2 = Line(model_axes.c2p(0, -spring_radius - 0.02), model_axes.c2p(0, spring_radius + 0.02),
                       color=spring_color).next_to(spring, RIGHT, buff=0)

        ball1 = Ball_(m=2, v=2, color=YELLOW).next_to(circle1, LEFT, buff=0)
        ball2 = Ball_(m=1, v=-1).next_to(circle2, RIGHT, buff=0)
        ground = Wall_wk(model_axes.c2p(-3.5 / 0.75, -0.3 / 0.75 - 0.02),
                         model_axes.c2p(9.5 / 0.75, -0.3 / 0.75 - 0.02)).set_stroke(width=3, opacity=0.7)

        m1_m2 = DecimalNumber(0, num_decimal_places=1).scale(0.6).move_to(ground.end + DOWN * 0.4, aligned_edge=UR)
        m1_m2.set_value(2)
        text_m = TexMobject("{", "m_{1}", "\\over", "m_{2}", "}", "=").scale(0.6).next_to(m1_m2, LEFT, buff=0.1).shift(
            0.05 * DOWN)
        text_m[1].set_color(YELLOW)
        text_m[3].set_color(RED)

        vg_spring = VGroup(circle1, spring, circle2, ball1, ball2, ground, m1_m2, text_m)
        t = t * x_strength  # 此处t由时间轴的点的值重新转化成实际时刻

        return vg_spring

    def get_t(self):
        return self.t_tracker.get_value()

    def set_t(self, t_new):
        self.t_tracker.set_value(t_new)

    def construct(self):
        vv = self.get_vv_axes()
        vt = self.get_vt_axes()
        model_axes = self.get_model_axes()
        t = 0.01 + PI / 3 * 4
        ball1_graph, ball2_graph = self.get_ball_graph(vt, 2, 2, 1, -1, t)
        dashline = self.get_time_dashline(vt, ball1_graph=ball1_graph, ball2_graph=ball2_graph)
        tangent_line = self.get_tangent_line(ball1_graph=ball1_graph, ball2_graph=ball2_graph)
        dot_vv = self.get_dot_vv(vv, vt, ball1_graph, ball2_graph)

        ball1 = Ball_(m=2, v=2)
        ball2 = Ball_(m=1, v=-1)
        model_ = self.get_model(model_axes, ball1, ball2, t, is_static=False)

        self.add(vv, vt, ball1_graph, ball2_graph, dashline, tangent_line, dot_vv, model_, )
        # self.play(tangent_line[0].copy().move_to,ORIGIN,tangent_line[1].copy().set_sta,ORIGIN,number_line_static)

        self.wait()


class Scene43_124(SpringScene):
    def construct(self):
        def Delta_think(think_mob):
            self.play(DeltaCreatureSays(
                Ale, think_mob,
                bubble_kwargs={"height": 3, "width": 4},
                target_mode="speaking",
                bubble_class=ThoughtBubble  # SpeechBubble,DoubleSpeechBubble,ThoughtBubble
            ))
            self.wait()
            self.play(Blink(Ale))
            self.play(Blink(Ale))

        Ale = Alex().to_corner(DL).scale(0.7)

        # 引入质量不等 4:00-4:10
        thinking_mob = TextMobject("如果两球质量和速度\\\\大小都不相等呢?", color=WHITE).scale(0.6)
        self.wait()
        self.add(Ale)
        # Delta_think(thinking_mob)
        self.play(DeltaCreatureSays(
            Ale, thinking_mob,
            bubble_kwargs={"height": 3, "width": 4},
            target_mode="speaking",
            bubble_class=ThoughtBubble,  # SpeechBubble,DoubleSpeechBubble,ThoughtBubble
            run_time=2,
        ))
        self.wait()
        self.play(Blink(Ale))
        self.play(Blink(Ale))
        self.wait()
        self.play(Blink(Ale))
        self.play(Blink(Ale))
        self.wait()
        cls = Collision(ball1_config={
            "fill_color": YELLOW,
            "m": 2,
            "v": 2,
        },
            ball2_config={
                "fill_color": RED,
                "m": 1,
                "v": -1,
            },
        )
        # 4:10-4:33
        self.play(FadeIn(
            VGroup(cls, cls.ground, cls.ball1, cls.ball2, cls.v1, cls.v2, cls.text_v1, cls.text_v2, cls.m1_m2,
                   cls.text_m)))
        self.wait()
        self.play(ShowPassingFlashAround(VGroup(cls.text_m, cls.m1_m2)), run_time=2)
        self.wait()
        cls.start_moving()
        # self.wait(2)
        self.play(Ale.look_at, cls.ball1, run_time=0.0001)
        self.play(Ale.look_at, cls.ball1.get_center() + RIGHT * 5, run_time=2)
        cls.end_moving()
        thinking_mob2 = TextMobject("碰撞的瞬间到底发生了\\\\什么了不起的事情呢？", color=WHITE).scale(0.6).move_to(
            thinking_mob.get_center())
        self.play(Transform(thinking_mob, thinking_mob2))
        self.play(Blink(Ale))
        self.play(Blink(Ale), run_time=0.5)  # +10
        self.wait()
        self.play(Blink(Ale))
        self.wait()
        self.play(Blink(Ale))
        self.wait()
        self.play(Ale.look_at, ORIGIN + DOWN * 2, run_time=1)
        self.play(Blink(Ale), run_time=0.5)
        self.play(Blink(Ale))
        self.wait()
        self.play(Ale.look_at, cls.ball1.get_center() + RIGHT * 4, run_time=1)
        self.play(Blink(Ale))
        self.wait()
        self.play(RemovePiCreatureBubble(Ale), FadeOut(Ale), FadeOut(
            VGroup(cls.ground, cls.ball1, cls.ball2, cls.v1, cls.v2, cls.text_v1, cls.text_v2, cls.m1_m2, cls.text_m)))
        self.remove(cls.ground, cls.ball1, cls.ball2, cls.v1, cls.v2, cls.text_v1, cls.text_v2, cls.m1_m2, cls.text_m)
        del cls
        self.wait()

        # 弹簧模型 4:33-4:49
        model_axes = self.get_model_axes()
        ball1 = Ball_(m=2, v=2)
        ball2 = Ball_(m=1, v=-1)

        model = self.get_model(model_axes, ball1, ball2, self.get_t(), is_static=False)
        self.play(FadeInFromPoint(model, ORIGIN + 3 * UP), run_time=3)
        model.add_updater(
            lambda g: g.become(self.get_model(model_axes, ball1, ball2, self.get_t(), is_static=False)
                               )
        )
        self.wait(13)

        # 生成mob
        vv_axes = self.get_vv_axes()
        vt_axes = self.get_vt_axes()

        ball1_graph = self.get_ball1_graph(vt_axes, 2, 2, 1, -1, self.get_t())
        ball1_graph.add_updater(
            lambda g: g.become(self.get_ball1_graph(
                vt_axes, 2, 2, 1, -1, self.get_t())
            )
        )

        ball2_graph = self.get_ball2_graph(vt_axes, 2, 2, 1, -1, self.get_t())
        ball2_graph.add_updater(
            lambda g: g.become(self.get_ball2_graph(
                vt_axes, 2, 2, 1, -1, self.get_t())
            )
        )

        dashline = self.get_time_dashline(vt_axes, ball1_graph=ball1_graph, ball2_graph=ball2_graph)
        dashline.add_updater(
            lambda g: g.become(self.get_time_dashline(vt_axes, ball1_graph=ball1_graph, ball2_graph=ball2_graph)
                               )
        )

        tangent_line = self.get_tangent_line(ball1_graph=ball1_graph, ball2_graph=ball2_graph)
        tangent_line.add_updater(
            lambda g: g.become(self.get_tangent_line(ball1_graph=ball1_graph, ball2_graph=ball2_graph)
                               )
        )

        dot_vv = self.get_dot_vv(vv_axes, vt_axes, ball1_graph=ball1_graph, ball2_graph=ball2_graph)
        dot_vv.add_updater(
            lambda g: g.become(self.get_dot_vv(vv_axes, vt_axes, ball1_graph=ball1_graph, ball2_graph=ball2_graph)
                               )
        )
        line_vv = self.get_vv_line(vv_axes, dot_vv)
        line_vv.add_updater(
            lambda g: g.become(self.get_vv_line(vv_axes, dot_vv))
        )

        dot_ok = Dot(vt_axes.c2p(PI, 1)).scale(0.6).set_color(ORANGE)
        tex_ok = TexMobject("\\text{(O,K)}").scale(0.35).next_to(dot_ok, RIGHT, 0.1, )

        newton3 = TexMobject("\\text{牛顿第三定律： }", "F_{1}", "=-", "F_{2}").set_color_by_tex_to_color_map(
            color_dict).scale(
            tex_scale).move_to(LEFT * 6.0 + UP * 1.5, aligned_edge=LEFT)
        newton2 = TexMobject("\\text{将牛二定律代入：}", "m_{1}a_{1}", " =-", "m_{2}a_{2}").set_color_by_tex_to_color_map(
            color_dict).scale(
            tex_scale).next_to(newton3, DOWN, 0.5, aligned_edge=LEFT)
        newton21 = TexMobject("m_{1}a_{1}", " =-", "m_{2}a_{2}", ).set_color_by_tex_to_color_map(
            color_dict).scale(tex_scale).next_to(newton3, DOWN, 0.5, aligned_edge=LEFT)
        # newton22 = TexMobject(" =-",).set_color_by_tex_to_color_map(
        #     color_dict).scale(tex_scale).next_to(newton21, RIGHT,buff=0)
        # newton23 = TexMobject("m_{2}a_{2}",).set_color_by_tex_to_color_map(
        #     color_dict).scale(tex_scale).next_to(newton22, RIGHT,buff=0)
        # zhengli = TexMobject("\\text{整理得：    }", "\\frac{a_{1}}{a_{2}}", "=-", "\\frac{m_{2}}{m_{1}}", "=-",
        #                      "\\frac{1}{2}").scale(tex_scale).next_to(newton2, DOWN, 0.5, aligned_edge=LEFT)
        zhengli = TexMobject("\\text{整理得：}", "{{a_{1}", "\\over", "{a_{2}}}", "=-", "{{m_{2}}", "\\over", "{m_{1}}}",
                             "=-",
                             "{1", "\\over", "2}").set_color_by_tex_to_color_map(color_dict).scale(tex_scale).next_to(
            newton2, DOWN, 0.5, aligned_edge=LEFT)

        jxnsh = TextMobject("机械能守恒定律").scale(tex_scale).next_to(newton2, DOWN, 0.5, aligned_edge=LEFT)
        e_trans = TexMobject("t\\neq 2", "\\text{:动能}", "\\Rightarrow", "\\text{其他能量}").set_color_by_tex_to_color_map(
            color_dict) \
            .scale(tex_scale).next_to(jxnsh, DOWN, 0.5, aligned_edge=LEFT)
        t15 = TexMobject("t=1.5", "\\text{:非弹性碰撞}").set_color_by_tex_to_color_map(color_dict) \
            .scale(tex_scale).next_to(e_trans, DOWN, 0.5, aligned_edge=LEFT)
        t1 = TexMobject("t=1", "\\text{:完全非弹性碰撞}").set_color_by_tex_to_color_map(color_dict) \
            .scale(tex_scale).next_to(t15, DOWN, 0.5, aligned_edge=LEFT)

        vv_dashline = self.get_dashline(vv_axes, 2, -1, 0, 3).scale(1.4)

        # 动画
        # 4:49-4:55
        self.wait(2)
        self.play(Write(vt_axes), run_time=2)
        self.wait(2)

        # 写公式 4:55-5:10
        self.wait(2)
        self.play(Write(newton3), run_time=3)
        self.wait(3)
        self.play(Write(newton2[0]), run_time=1.5)
        self.play(TransformFromCopy(newton3[1], newton2[1]), TransformFromCopy(newton3[2], newton2[2]),
                  TransformFromCopy(newton3[3], newton2[3]), run_time=1.5)
        self.wait()
        self.play(FadeIn(zhengli))
        self.wait(2)

        # 两球加速度比为定值 5:10-5:5:38
        ritio_graph = self.get_ritio_g(vt_axes, self.get_ritio())
        # self.play(FadeIn(tangent_line))
        self.wait(3)
        # self.play(FadeOut(tangent_line))
        self.play(Write(ritio_graph))
        ritio_graph.add_updater(
            lambda g: g.become(self.get_ritio_g(
                vt_axes, self.get_ritio())
            )
        )
        self.wait(2)
        self.play(
            ApplyMethod(
                self.ritio_tracker.set_value, -2,
                run_time=4,
            ))
        self.wait(2)  # -5:22
        self.wait(5)
        g2_copy = self.get_ritio_g_copy(vt_axes)
        self.play(g2_copy.stretch, 0.5, 1, {"about_point": vt_axes.c2p(0, -1)}, run_time=1)
        self.wait()
        g2_copy2 = g2_copy.copy()
        self.play(g2_copy2.flip, RIGHT, {"about_point": vt_axes.c2p(0, -1)}, run_time=1)
        self.wait()
        self.play(g2_copy2.shift, (vt_axes.c2p(0, 2) - vt_axes.c2p(0, -1)), FadeOut(g2_copy), run_time=1)
        self.wait()
        self.play(FadeOut(g2_copy2))
        self.wait()
        self.play(FadeOut(ritio_graph), run_time=1.5)
        self.wait(1.5)

        # 碰撞过程 #5:38-6:07 13s
        self.add(ball1_graph, ball2_graph, dashline, )
        self.play(
            ApplyMethod(
                self.t_tracker.set_value, PI,
                run_time=13,
                rate_func=linear,
            ),
        )

        self.wait(6)  # -57
        self.play(FadeIn(tangent_line))
        self.wait(2)
        self.play(FadeOut(tangent_line))  # -02
        self.play(Write(dot_ok), Write(tex_ok), run_time=1.5)
        self.wait(3.5)
        # 6:07-6:23
        self.wait(4)
        self.play(
            ApplyMethod(
                self.t_tracker.set_value, 2 * PI,
                run_time=6,
                rate_func=linear,
            ),
        )

        self.wait(3)
        self.play(CircleIndicate(dot_ok), run_time=2)
        self.wait(1)
        # 6:23-6:34
        text_get_end_v = TexMobject("\\text{根据图像：当}", "t=2", "\\text{时刻，}", "{v_{1}}^{'}", "=0", "\\text{,}",
                                    "{v_{2}}^{'}", "=3").set_color_by_tex_to_color_map(color_dict).scale(
            tex_scale).next_to(
            zhengli, DOWN, 0.6, aligned_edge=LEFT)
        self.wait(6)
        self.play(Write(text_get_end_v), run_time=2)
        self.wait(3)

        # 移除公式 6:34-6:45
        self.play(FadeOut(newton2), FadeOut(newton3), FadeOut(zhengli), FadeOut(text_get_end_v))
        self.wait()
        self.add(Ale)
        thinking_mob3 = TextMobject("怎么感觉没用什么定律就\\\\得到了碰撞后的结果呢？", color=WHITE).scale(0.6).move_to(
            thinking_mob.get_center())
        self.play(DeltaCreatureSays(
            Ale, thinking_mob3,
            bubble_kwargs={"height": 3, "width": 4},
            target_mode="speaking",
            bubble_class=ThoughtBubble,
            run_time=2  # SpeechBubble,DoubleSpeechBubble,ThoughtBubble
        ))
        self.wait()
        self.play(Blink(Ale))
        self.play(Blink(Ale))
        self.wait()
        self.play(Blink(Ale))
        self.play(RemovePiCreatureBubble(Ale), FadeOut(Ale), )
        self.wait()
        # 6:45-6:58
        self.wait()
        self.play(Write(newton21), run_time=1.5)
        self.wait(2.5)
        cos_copy = self.get_cos_copy(vt_axes)
        self.play(cos_copy.stretch, 0.5, 1, {"about_point": vt_axes.c2p(0, -1)}, run_time=1)
        self.wait()
        cos_copy2 = cos_copy.copy()
        self.play(cos_copy2.flip, RIGHT, {"about_point": vt_axes.c2p(0, -1)}, run_time=1)
        self.wait()
        self.play(cos_copy2.shift, (vt_axes.c2p(0, 2) - vt_axes.c2p(0, -1)), FadeOut(cos_copy), run_time=1)
        self.wait()
        self.play(FadeOut(cos_copy2), FadeOut(cos_copy2))
        self.wait()
        # 6:58-7:09
        self.play(FocusOn(dot_ok), run_time=1)
        self.wait(1)
        # self.play(Rotating(ball1_graph,about_point=dot_ok.get_center()))
        copy_1 = ball1_graph.copy()
        copy_2 = ball2_graph.copy()
        self.play(Rotating(copy_1, radians=PI, run_time=2, about_point=dot_ok.get_center(), ),
                  Rotating(copy_2, radians=PI, run_time=2, about_point=dot_ok.get_center(), ))
        self.play(FadeOut(copy_1), FadeOut(copy_2))
        self.wait()
        # self.play(Rotating(ball2_graph,radians=PI,run_time=2,about_point=dot_ok.get_center(),))
        # self.play(ball2_graph.rotate, {"angle":PI}, {"about_point":dot_ok.get_center()})
        self.wait(2)
        self.play(TransformFromCopy(dot_ok, jxnsh), run_time=1.5)
        self.wait(1.5)
        # 7:09-7:31
        self.wait(4)
        self.play(
            ApplyMethod(
                self.t_tracker.set_value, 3 / 2 * PI,
                run_time=1,
                rate_func=linear,
            ),
        )
        self.wait(7)
        self.play(Write(e_trans))
        self.wait(9)
        # 7:31-7:46
        self.play(Write(t15))
        self.wait(6)
        self.play(
            ApplyMethod(
                self.t_tracker.set_value, PI,
                run_time=1,
                rate_func=linear,
            ),
        )
        self.wait(5)
        self.play(Write(t1))
        self.wait(0.5)
        self.play(FadeOut(newton21), FadeOut(jxnsh), FadeOut(e_trans), FadeOut(t15), FadeOut(t1), )
        self.wait(0.5)

        # 加vv图 7:46-8:06
        self.play(
            ApplyMethod(
                self.t_tracker.set_value, 0.001,
                run_time=1,
                rate_func=linear,
            ),
        )
        self.wait()
        self.play(Write(vv_axes), run_time=1.5)
        self.wait(2.5)
        self.wait(2)
        self.play(Write(dot_vv), Write(line_vv), run_time=2)
        self.wait(7)
        self.play(Write(vv_dashline), run_time=1.5)
        self.wait(1.5)
        # 8:06-8:20
        energy_g = self.get_energy(vv_axes, ball1, ball2)
        self.wait(1.5)
        self.play(Write(energy_g), run_time=1.5)
        self.wait(1)
        self.play(CircleIndicate(Dot(vv_axes.c2p(0, 3)).set_opacity(0.001)))
        self.wait()
        self.play(
            ApplyMethod(
                self.t_tracker.set_value, 2 * PI,
                run_time=2,
                rate_func=linear,
            ),
        )

        self.wait()  # -15
        self.play(ApplyWave(vv_dashline), run_time=2.5)
        self.wait(2.5)  # -20
        self.play(FadeOut(dot_vv), FadeOut(line_vv), FadeOut(energy_g), )
        self.wait()
        self.play(FadeOut(vv_axes), FadeOut(vv_dashline), FadeOut(vv_dashline))
        self.wait(3)  # -26

        # 数学公式整理动量守恒
        newton3.shift(UP * 0.7)
        self.wait(2)
        self.play(Write(newton3))
        self.wait(3)  # -32
        newton2.next_to(newton3, DOWN, 0.5, aligned_edge=LEFT)
        jifen = TexMobject("\\text{积分得：    }", "m_{1}", "\\cdot\\int_{t_{1}}^{t_{2}}", "a_{1}", "dt", "=-",
                           "m_{2}", "\\cdot\\int_{t_{1}}^{t_{2}}", "a_{2}", "dt",
                           ).set_color_by_tex_to_color_map(
            color_dict).scale(tex_scale).next_to(newton2, DOWN, 0.5, aligned_edge=LEFT)
        dongliang1 = TexMobject("\\text{即：    }", "m_{1}", "\\bigtriangleup", "v_{1}", "=-", "m_{2}", "\\bigtriangleup",
                                "v_{2}", ) \
            .set_color_by_tex_to_color_map(color_dict) \
            .scale(tex_scale).next_to(jifen, DOWN, 0.5, aligned_edge=LEFT)
        dongliang3 = TexMobject("\\text{定义物体的动量：    }", "m", "\\cdot", "v", ) \
            .set_color_by_tex_to_color_map(color_dict) \
            .scale(tex_scale).next_to(dongliang1, DOWN, 0.5, aligned_edge=LEFT)
        dongliang2 = TexMobject("\\text{动量守恒定律：    }", "m_{1}", "\\bigtriangleup", "v_{1}", "+", "m_{2}",
                                "\\bigtriangleup", "v_{2}", "=0") \
            .set_color_by_tex_to_color_map(color_dict) \
            .scale(tex_scale).next_to(dongliang3, DOWN, 0.5, aligned_edge=LEFT)
        self.play(Write(newton2))
        self.wait(4)  # -37
        self.play(Write(jifen))
        self.wait(2)  # 40
        self.play(Write(dongliang1))
        self.wait(5)  # 46
        self.play(Write(dongliang3))
        self.wait(2)
        self.play(ShowPassingFlashAround(dongliang1))
        self.wait(2)  # 52
        self.play(Write(dongliang2[1:]), run_time=1.5)
        self.wait(5.5)  # 01
        self.play(ShowPassingFlashAround(dongliang2[1:]))
        self.wait(9)  # 11
        self.play(Write(dongliang2[0]), run_time=1)
        self.wait(4.5)  # 14.5
        self.play(FadeOut(newton3), FadeOut(newton2), FadeOut(jifen), FadeOut(dongliang1), )
        self.wait(4.5)  # 20

        # 参考系c'
        self.wait(4)
        self.play(FadeOut(dongliang3), FadeOut(dongliang2))
        self.wait(2)
        self.add(Ale)
        thinking_mob4 = TextMobject("$C^{'}$系区别于其他参考\\\\系的特点是什么呢？", color=WHITE).scale(0.6).move_to(
            thinking_mob.get_center())
        self.play(DeltaCreatureSays(
            Ale, thinking_mob4,
            bubble_kwargs={"height": 3, "width": 4},
            target_mode="speaking",
            bubble_class=ThoughtBubble,  # SpeechBubble,DoubleSpeechBubble,ThoughtBubble
            run_time=2,
        ))
        self.wait()
        self.play(Blink(Ale))
        self.play(Blink(Ale))
        self.wait()
        self.play(Blink(Ale))
        self.play(Blink(Ale))
        self.play(RemovePiCreatureBubble(Ale), FadeOut(Ale), )
        self.wait()

        # 平移坐标系
        dl_1 = DashedLine(start=LEFT * 3 + UP * 2, end=LEFT * 3 + UP * (-2)).set_color(GREEN)
        dl_2 = DashedLine(start=LEFT * 3 + UP * 2, end=LEFT * 3 + UP * (-2)).set_color(GREEN)
        vg_dot = VGroup(Dot(color=RED).move_to(LEFT * 6 - UP).scale(0.1),
                        Dot(color=RED).scale(0.1).move_to(LEFT * 2 - UP),
                        Dot(color=ORANGE).scale(0.1).move_to(LEFT * 2.999),
                        Dot(color=YELLOW).move_to(LEFT * 5 + UP).scale(0.1),
                        Dot(color=YELLOW).move_to(LEFT * 2.999 + UP).scale(0.1),
                        Dot(color=ORANGE).scale(0.1).move_to(LEFT * 3),
                        )
        vg_arrow = VGroup(Arrow(color=RED),
                          Arrow(color=RED),
                          Arrow(color=ORANGE),
                          Arrow(color=YELLOW),
                          Arrow(color=YELLOW),
                          )
        vg_arrow[0].add_updater(lambda a: a.put_start_and_end_on(vg_dot[0].get_center(), vg_dot[5].get_center() + DOWN))
        vg_arrow[1].add_updater(lambda a: a.put_start_and_end_on(vg_dot[1].get_center(), vg_dot[5].get_center() + DOWN))
        vg_arrow[2].add_updater(lambda a: a.put_start_and_end_on(vg_dot[2].get_center(), vg_dot[5].get_center()))
        vg_arrow[3].add_updater(lambda a: a.put_start_and_end_on(vg_dot[3].get_center(), vg_dot[5].get_center() + UP))
        vg_arrow[4].add_updater(lambda a: a.put_start_and_end_on(vg_dot[4].get_center(), vg_dot[5].get_center() + UP))
        dl_2.add_updater(lambda a: a.put_start_and_end_on(vg_dot[5].get_center() + DOWN, vg_dot[5].get_center() + UP))
        vg_v_ = VGroup(TexMobject("{v_{2}}^{'}{:}").scale(0.8).next_to(vg_dot[0], DR, buff=0.2),
                       TexMobject("v_{2}{:}").scale(0.8).next_to(vg_dot[1], DL, buff=0.25),
                       TexMobject("v_{C^{'}}{:}").scale(0.8).next_to(vg_dot[2], UL, buff=0.15),
                       TexMobject("v_{1}{:}").scale(0.8).next_to(vg_dot[3], UR, buff=0.25).shift(LEFT * 1.5),
                       TexMobject("{v_{1}}^{'}{:}").scale(0.8).next_to(vg_dot[4], UL, buff=0.2),
                       )
        vg_vv_ = VGroup(
            DecimalNumber(0, num_decimal_places=2, include_sign=True, ).scale(0.66).next_to(vg_v_[0], RIGHT, buff=0.1),
            DecimalNumber(0, num_decimal_places=2, include_sign=True, ).scale(0.66).next_to(vg_v_[1], RIGHT, buff=0.1),
            DecimalNumber(0, num_decimal_places=2, include_sign=True, ).scale(0.66).next_to(vg_v_[2], RIGHT, buff=0.1),
            DecimalNumber(0, num_decimal_places=2, include_sign=True, ).scale(0.66).next_to(vg_v_[3], RIGHT, buff=0.1),
            DecimalNumber(0, num_decimal_places=2, include_sign=True, ).scale(0.66).next_to(vg_v_[4], RIGHT, buff=0.1),
        )
        vg_vv_[0].add_updater(lambda a: a.set_value(vg_arrow[0].get_length()))
        vg_vv_[1].add_updater(lambda a: a.set_value(-vg_arrow[1].get_length()))
        vg_vv_[2].add_updater(lambda a: a.set_value(vg_arrow[2].get_length()))
        vg_vv_[3].add_updater(lambda a: a.set_value(vg_arrow[3].get_length()))
        vg_vv_[4].add_updater(lambda a: a.set_value(-vg_arrow[4].get_length()))

        vt_axes2 = vt_axes.copy()
        vt_axes2.add_updater(
            lambda a: a.move_to(vt_axes.get_center() + vg_arrow[2].get_length() * self.axis_scale * UP))
        # 37 - 52
        text_vt_c2 = TexMobject("C^{'}").set_color(BLUE).scale(0.7).next_to(vt_axes.c2p(0, 1), LEFT, 0.2)
        self.add(vg_dot, vg_arrow, vg_v_, vg_vv_, dl_1, dl_2, vt_axes2)
        self.play(vg_dot[5].shift, LEFT * 1.5, run_time=3)
        self.wait()
        self.play(vg_dot[5].shift, RIGHT * 1, run_time=5)
        self.wait()
        self.play(vg_dot[5].shift, LEFT * 0.5, run_time=3)
        self.play(Write(text_vt_c2))
        self.wait(2)
        # 55-13
        self.play(ShowPassingFlashAround(vg_arrow[2]), run_time=2)
        self.wait(3)
        self.play(ShowPassingFlashAround(VGroup(vg_arrow[3], vg_arrow[4])), run_time=2)
        self.wait()
        self.play(ShowPassingFlashAround(VGroup(vg_arrow[0], vg_arrow[1])), run_time=2)
        self.wait(2)
        self.play(FadeOut(vt_axes), FadeOut(dashline), FadeOut(dot_ok), FadeOut(tex_ok), run_time=1)  #
        self.wait(2)
        self.wait(4)  # -14
        self.play(ShowPassingFlashAround(vg_arrow[2]))
        self.wait(13)
        self.play(FadeOut(vt_axes2), FadeOut(vg_dot), FadeOut(vg_arrow), FadeOut(vg_v_), FadeOut(vg_vv_), FadeOut(dl_1),
                  FadeOut(dl_2), FadeOut(ball1_graph), FadeOut(ball2_graph), FadeOut(text_vt_c2), run_time=1)
        self.wait()  # -28
        speed_c = TexMobject("\\text{系统质心速度: }", "v_{C^{'}}", "=", "{", "{", "m_{1}v_{1}", "+", "m_{2}v_{2}", "}",
                             "\\over", "{", "m_{1}", "+", "m_{2}", "}", "}", "=1") \
            .set_color_by_tex_to_color_map(color_dict).scale(
            tex_scale).move_to(RIGHT * 0.5, aligned_edge=LEFT)
        speed_1 = TexMobject("\\text{黄球末速度: }", "v_{1^{'}}", "=", "{", "2", "v_{C^{'}}", "-", "v_{1}", "}", "=0") \
            .set_color_by_tex_to_color_map(color_dict).scale(
            tex_scale).next_to(speed_c, DOWN, 0.5, aligned_edge=LEFT)
        speed_2 = TexMobject("\\text{红球末速度: }", "v_{2^{'}}", "=", "{", "2", "v_{C^{'}}", "-", "v_{2}", "}", "=3") \
            .set_color_by_tex_to_color_map(color_dict).scale(
            tex_scale).next_to(speed_1, DOWN, 0.5, aligned_edge=LEFT)
        jxnshfc = TextMobject("机械能守恒方程").scale(tex_scale).move_to(jxnsh.get_center() + RIGHT * 8)
        dlsh = TextMobject("动量守恒方程").scale(tex_scale).next_to(jxnshfc, DOWN, 0.5, aligned_edge=LEFT)
        brace_ = Brace(VGroup(jxnshfc, dlsh), LEFT)
        self.play(Write(brace_))
        self.wait(2)
        self.play(Write(jxnshfc))
        self.wait()
        self.play(Write(dlsh))
        self.wait()  # -35
        self.play(Write(vv_axes), )
        self.play(Write(energy_g), run_time=0.5)
        self.play(Write(vv_dashline), run_time=0.5)
        end_dot = Dot(vv_axes.c2p(0, 3)).set_color(ORANGE)

        self.play(FocusOn(end_dot))
        self.play(Write(end_dot), run_time=0.5)
        self.wait(4)  # -46
        self.play(FadeOut(end_dot), FadeOut(energy_g), FadeOut(vv_dashline), FadeOut(brace_), FadeOut(jxnshfc),
                  FadeOut(dlsh), )
        self.wait(2)
        text_with_c_ = TextMobject("通过", "$C^{'}$", "参考系：").set_color_by_tex_to_color_map(color_dict).scale(
            tex_scale + 0.1).move_to(UP * 1.5, aligned_edge=LEFT)
        self.play(Write(text_with_c_), run_time=1)
        self.wait()
        self.play(FadeIn(speed_c), run_time=2)
        self.wait(0.5)  # -51
        self.play(FadeIn(speed_1), run_time=1)
        self.play(FadeIn(speed_2), run_time=1)
        self.wait(4)  # -56

        start_dot = Dot(vv_axes.c2p(2, -1)).set_color(ORANGE)
        c_dot = Dot(vv_axes.c2p(1, 1)).set_color(BLUE)
        text_dot_start = TextMobject("初速度点").scale(0.6).next_to(start_dot, DOWN, 0.2)
        text_dot_end = TextMobject("末速度点").scale(0.6).next_to(end_dot, LEFT, 0.2)
        text_dot_c = TextMobject("系统质心点").scale(0.6).next_to(c_dot, UR, 0.13)
        self.add(start_dot, text_dot_start)
        self.wait(0.5)
        self.play(Write(c_dot))
        self.play(Write(text_dot_c))
        self.wait(1)  # -03
        config_temp = dict(stroke_width=1.5, color=ORANGE)
        origin_vv = Dot(vv_axes.c2p(2, -1)).scale(0.8).set_color(ORANGE)
        line_s2e = Line(start=start_dot.get_center(), end=c_dot.get_center(), **config_temp)
        self.play(Write(line_s2e))
        self.wait(0.5)
        self.play(Rotate(line_s2e.copy(), PI, OUT, about_point=c_dot.get_center()), run_time=1.5)
        self.wait(1)  # -08
        self.play(Write(end_dot))
        self.play(Write(text_dot_end))
        self.wait(15)  # 22

    def get_dashline(self, axis, start_x, start_y, end_x, end_y):
        start_ = axis.c2p(start_x, start_y)
        end_ = axis.c2p(end_x, end_y)
        dl = DashedLine(start=start_, end=end_).set_color(GREEN).set_stroke(width=3)
        return dl

    def get_ritio_g(self, vt, strench_ritio, **kwargs):
        config1 = dict(color=YELLOW, stroke_width=2.5)
        config2 = dict(color=RED, stroke_width=2.5)
        config1.update({
            "t_min": 0,
            "t_max": 2 * PI,
        })
        config1.update(**kwargs)
        config2.update({
            "t_min": 0,
            "t_max": 2 * PI,
        })
        config2.update(**kwargs)

        l1 = ParametricFunction(
            lambda t: vt.c2p(
                t, strench_ritio * 0.2 * (t + np.sin(t)) + 2
            ),
            **config1,
        )
        l2 = ParametricFunction(
            lambda t: vt.c2p(
                t, -0.4 * strench_ritio * (t + np.sin(t)) - 1
            ),
            **config2,
        )

        return VGroup(l1, l2)

    def get_ritio(self):
        return self.ritio_tracker.get_value()

    def get_ritio_g_copy(self, vt, **kwargs):
        config2 = dict(color=RED, stroke_width=2.5)
        config2.update({
            "t_min": 0,
            "t_max": 2 * PI,
        })
        config2.update(**kwargs)
        l2 = ParametricFunction(
            lambda t: vt.c2p(
                t, 0.8 * (t + np.sin(t)) - 1
            ),
            **config2,
        )
        return l2

    def get_cos_copy(self, vt, **kwargs):
        config2 = dict(color=RED, stroke_width=2.5)
        config2.update({
            "t_min": 0,
            "t_max": 2 * PI,
        })
        config2.update(**kwargs)
        l2 = ParametricFunction(
            lambda t: vt.c2p(
                t, -2 * np.cos(0.5 * t) + 1
            ),
            **config2,
        )
        return l2

    def get_energy(self, vv, ball1, ball2):
        strench_ritio = np.sqrt(ball1.m / ball2.m)
        total_2e = (ball1.m * ball1.v * ball1.v + ball2.m * ball2.v * ball2.v) / ball1.m
        circle = Circle(radius=np.sqrt(total_2e), color=ORANGE).move_arc_center_to(vv.c2p(0, 0)).scale(self.axis_scale)
        circle.stretch(factor=strench_ritio, dim=1)
        return circle


class Conclusion(Scene):
    def construct(self):
        Ale = Alex().to_corner(DR)
        think1 = TextMobject("是时候做一点总结了...", color=WHITE).scale(0.6)
        self.add(Ale)  # 22-27
        self.play(DeltaCreatureSays(
            Ale, think1,
            bubble_kwargs={"height": 3, "width": 4},
            target_mode="speaking",
            bubble_class=ThoughtBubble  # SpeechBubble,DoubleSpeechBubble,ThoughtBubble
        ))
        self.play(Ale.look_at, ORIGIN)
        self.play(Blink(Ale))
        self.play(Blink(Ale))
        self.wait(1)
        text1 = TextMobject("动量守恒定律可通过牛顿第一定律理解:").set_color(GREEN).scale(tex_scale * 1.2).move_to(LEFT * 3 + UP * 2)
        text2 = TextMobject("对整个系统而言,整个碰撞过程没有受到外力，").set_color(BLUE).scale(tex_scale).next_to(text1, DOWN, 0.7,
                                                                                              LEFT).shift(RIGHT * 0.4)
        text3 = TextMobject("所以整个系统的质心速度不会变化。").set_color(BLUE).scale(tex_scale).next_to(text2, DOWN, 0.4, LEFT)
        text4 = TextMobject("动量定理可以通过牛顿第二定律理解:").set_color(GREEN).scale(tex_scale * 1.2).next_to(text3, DOWN,
                                                                                                 aligned_edge=LEFT,
                                                                                                 buff=1).shift(
            LEFT * 0.4)
        text5 = TextMobject("对小球而言,碰撞时受到的外力：").set_color(BLUE).scale(tex_scale).next_to(text4, DOWN, 0.7, LEFT).shift(
            RIGHT * 0.4)
        text6 = TextMobject("$F=ma$在时间项上积分即$F\\bigtriangleup t=m\\bigtriangleup v$ 。").set_color(BLUE).scale(
            tex_scale).next_to(text5, DOWN, 0.7, LEFT).shift(RIGHT * 0.4)
        self.play(Write(text1), run_time=2)
        self.wait(3)
        self.play(Write(text2), run_time=2)
        self.wait(2.5)
        self.play(Write(text3), run_time=2)
        self.wait(1.5)
        self.play(Write(text4), run_time=2)
        self.wait(2)
        self.play(Write(text5), run_time=1)
        self.play(Write(text6), run_time=2)
        self.wait(4.5)
        # 51.5-05.5
        self.play(FadeOut(text1), FadeOut(text2), FadeOut(text3), FadeOut(text4), FadeOut(text5),
                  FadeOut(text6), )  # RemovePiCreatureBubble(Ale),FadeOut(Ale),run_time=1.5
        self.wait()
        think2 = TextMobject("一个小小的问题...", color=WHITE).scale(0.6).move_to(think1.get_center())
        self.play(Transform(think1, think2))
        self.wait()
        question = VGroup(
            TextMobject("三个质量相等的恒星A,B,C互相受到引力作用,").set_color(BLUE).scale(tex_scale),
            TextMobject("不考虑其他星体对他们的引力,").set_color(BLUE).scale(tex_scale),
            TextMobject("某时刻在某惯性系下观测到A,B,C的位置和速度,").set_color(BLUE).scale(tex_scale),
            TextMobject("一段时间后,再次观测到了A,B的位置和速度,").set_color(BLUE).scale(tex_scale),
            TextMobject("问C星此时的位置和速度是否可以确定?").set_color(BLUE).scale(tex_scale),
        ).arrange_submobjects(
            DOWN, aligned_edge=LEFT, buff=0.3
        ).shift(LEFT * 3)
        self.play(Write(question), run_time=4)
        self.wait(20)


class test_spring(Scene):
    def construct(self):
        ball1 = Ball_(m=2, v=2, color=YELLOW)
        ball2 = Ball_(m=1, v=-4, color=RED)
        s = SpringModel(ball1, ball2)
        self.play(ShowCreation(s))
        self.wait()
        s.start_moving()
        self.wait(PI)
        s.end_moving()
        self.wait()


class OneDMeet(Scene):
    CONFIG = {
        "step_size": 0.05,
        "axes_config": {
            "x_min": -1,
            "x_max": 11,
            "y_min": -10,
            "y_max": 100,
            "y_axis_config": {
                "unit_size": 0.06,
                "tick_frequency": 10,
            },
        },
        "y_labels": range(20, 100, 20),
        "graph_x_min": 0,
        "graph_x_max": 10,
        "midpoint": 5,
        "max_temp": 90,
        "min_temp": 10,
        "wait_time": 30,
        "default_n_rod_pieces": 20,
        "alpha": 1.0,
    }

    def construct(self):
        self.set_oneDmeet()
        self.set_v1v2Cord()
        self.set_explain()

        temp = Circle()
        self.play(ShowCreation(temp), Write(self.axes))

    def set_oneDmeet(self):
        pass

    def set_v1v2Cord(self):
        axes = Axes(**self.axes_config)
        axes.center().to_edge(UP)

        y_label = axes.get_y_axis_label("\\text{Temperature}")
        y_label.to_edge(UP)
        axes.y_axis.label = y_label
        axes.y_axis.add(y_label)
        axes.y_axis.add_numbers(*self.y_labels)

        self.axes = axes
        self.y_label = y_label

    def set_explain(self):
        pass


class test(Scene):
    def construct(self):
        jxnsh = TextMobject("机械能守恒定律").scale(tex_scale)
        jxnsh.shift(RIGHT * 2)
        dlsh = TextMobject("动量守恒定律").scale(tex_scale).next_to(jxnsh, DOWN, 0.5, aligned_edge=LEFT)
        brace_ = Brace(VGroup(jxnsh, dlsh))
        self.play(Write(brace_), Write(dlsh), Write(jxnsh))
        jxnshfc = TextMobject("机械能守恒方程").scale(tex_scale).move_to(jxnsh.get_center() + LEFT * 4)
        newton2 = TexMobject("\\text{将牛二定律代入：}", "m_{1}a_{1}", " =-", "m_{2}a_{2}").set_color_by_tex_to_color_map(
            color_dict).scale(
            tex_scale).next_to(jxnsh, DOWN, 0.5, aligned_edge=LEFT)
        newton2.next_to(jxnshfc, DOWN, 0.5, aligned_edge=LEFT)
        self.add(newton2)
        self.play(Write(jxnshfc))


color_dict_ = {'m_{1}': YELLOW, 'm_{2}': RED, 'v_{1}': YELLOW, 'v_{2}': RED, '{v_{1}}\'': YELLOW,
               '{v_{2}}\'': RED, 'F_{1}': YELLOW, 'F_{2}': RED, 'a_{1}': YELLOW, 'a_{2}': RED,
               "v_{C^{'}}": ORANGE, "v=0": BLUE,"v=1": BLUE, }


class P2(SpringScene):  # 运动
    def construct(self):
        model_axes = self.get_model_axes()
        ball1 = Ball_(m=2, v=2)
        ball2 = Ball_(m=1, v=-1)

        model = self.get_model(model_axes, ball1, ball2, self.get_t(), is_static=False)
        model.add_updater(
            lambda g: g.become(self.get_model(model_axes, ball1, ball2, self.get_t(), is_static=False)
                               )
        )

        # 生成mob
        vv_axes = self.get_vv_axes()
        vt_axes = self.get_vt_axes()

        ball1_graph = self.get_ball1_graph(vt_axes, 2, 2, 1, -1, self.get_t())
        ball1_graph.add_updater(
            lambda g: g.become(self.get_ball1_graph(
                vt_axes, 2, 2, 1, -1, self.get_t())
            )
        )

        ball2_graph = self.get_ball2_graph(vt_axes, 2, 2, 1, -1, self.get_t())
        ball2_graph.add_updater(
            lambda g: g.become(self.get_ball2_graph(
                vt_axes, 2, 2, 1, -1, self.get_t())
            )
        )

        dashline = self.get_time_dashline(vt_axes, ball1_graph=ball1_graph, ball2_graph=ball2_graph)
        dashline.add_updater(
            lambda g: g.become(self.get_time_dashline(vt_axes, ball1_graph=ball1_graph, ball2_graph=ball2_graph)
                               )
        )

        tangent_line = self.get_tangent_line(ball1_graph=ball1_graph, ball2_graph=ball2_graph)
        tangent_line.add_updater(
            lambda g: g.become(self.get_tangent_line(ball1_graph=ball1_graph, ball2_graph=ball2_graph)
                               )
        )

        dot_vv = self.get_dot_vv(vv_axes, vt_axes, ball1_graph=ball1_graph, ball2_graph=ball2_graph)
        dot_vv.add_updater(
            lambda g: g.become(self.get_dot_vv(vv_axes, vt_axes, ball1_graph=ball1_graph, ball2_graph=ball2_graph)
                               )
        )
        line_vv = self.get_vv_line(vv_axes, dot_vv)
        line_vv.add_updater(
            lambda g: g.become(self.get_vv_line(vv_axes, dot_vv))
        )

        word11 = TexMobject("\\text{当}", "m_{1}=2", "\\text{，}", "v_{1}=2", "\\text{；}", "m_{2}=1", "\\text{，}",
                            "v_{2}=-1", "\\text{时,}", ).set_color_by_tex_to_color_map(color_dict_).scale(
            tex_scale + 0.3).shift(UP)
        word12 = TexMobject("\\text{在}", "v=0", "\\text{的参考系下看到的碰撞瞬间过程:}", ).set_color_by_tex_to_color_map(
            color_dict_).scale(tex_scale + 0.3).next_to(
            word11, DOWN, 0.7, aligned_edge=LEFT)

        word21 = TexMobject("\\text{当}", "m_{1}=2", "\\text{，}", "v_{1}=2", "\\text{；}", "m_{2}=1", "\\text{，}",
                            "v_{2}=-1", "\\text{时}", ).set_color_by_tex_to_color_map(color_dict_).scale(
            tex_scale + 0.3).shift(UP)
        word22 = TexMobject("\\text{在}", "v_{'}=1", "\\text{的参考系下看到的碰撞瞬间过程}", ).set_color_by_tex_to_color_map(
            color_dict_).scale(tex_scale + 0.3).next_to(
            word11, DOWN, 0.7, aligned_edge=LEFT)

        # play
        self.play(Write(word11), run_time=1.5)
        self.play(Write(word12), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(word11), FadeOut(word12), )

        self.add(model,vt_axes, ball1_graph, ball2_graph, dashline, vv_axes, dot_vv, line_vv)
        self.play(
            ApplyMethod(
                self.t_tracker.set_value, 2*PI,
                run_time=2,
                rate_func=linear,
            ),
        )
        self.wait()


class P2_still(SpringScene):  # 运动
    def get_vv_line(self, vv, dot_vv):
        config = dict(stroke_width=1.5, color=ORANGE)
        origin_vv = Dot(vv.c2p(1, -2)).scale(0.8).set_color(ORANGE)
        dl = Line(start=origin_vv.get_center(), end=dot_vv.get_center(), **config)
        return VGroup(origin_vv, dl)
    def construct(self):
        model_axes = self.get_model_axes()
        ball1 = Ball_(m=2, v=1)
        ball2 = Ball_(m=1, v=-2)

        model = self.get_model(model_axes, ball1, ball2, self.get_t(), is_static=True)
        model.add_updater(
            lambda g: g.become(self.get_model(model_axes, ball1, ball2, self.get_t(), is_static=True)
                               )
        )

        # 生成mob
        vv_axes = self.get_vv_axes()
        vt_axes = self.get_vt_axes()

        ball1_graph = self.get_ball1_graph(vt_axes, 2, 1, 1, -2, self.get_t())
        ball1_graph.add_updater(
            lambda g: g.become(self.get_ball1_graph(
                vt_axes, 2, 1, 1, -2, self.get_t())
            )
        )

        ball2_graph = self.get_ball2_graph(vt_axes, 2, 1, 1, -2, self.get_t())
        ball2_graph.add_updater(
            lambda g: g.become(self.get_ball2_graph(
                vt_axes, 2, 1, 1, -2, self.get_t())
            )
        )

        dashline = self.get_time_dashline(vt_axes, ball1_graph=ball1_graph, ball2_graph=ball2_graph)
        dashline.add_updater(
            lambda g: g.become(self.get_time_dashline(vt_axes, ball1_graph=ball1_graph, ball2_graph=ball2_graph)
                               )
        )

        tangent_line = self.get_tangent_line(ball1_graph=ball1_graph, ball2_graph=ball2_graph)
        tangent_line.add_updater(
            lambda g: g.become(self.get_tangent_line(ball1_graph=ball1_graph, ball2_graph=ball2_graph)
                               )
        )

        dot_vv = self.get_dot_vv(vv_axes, vt_axes, ball1_graph=ball1_graph, ball2_graph=ball2_graph)
        dot_vv.add_updater(
            lambda g: g.become(self.get_dot_vv(vv_axes, vt_axes, ball1_graph=ball1_graph, ball2_graph=ball2_graph)
                               )
        )
        line_vv = self.get_vv_line(vv_axes, dot_vv)
        line_vv.add_updater(
            lambda g: g.become(self.get_vv_line(vv_axes, dot_vv))
        )

        word11 = TexMobject("\\text{当}", "m_{1}=2", "\\text{，}", "v_{1}=2", "\\text{；}", "m_{2}=1", "\\text{，}",
                            "v_{2}=-1", "\\text{时,}", ).set_color_by_tex_to_color_map(color_dict_).scale(
            tex_scale + 0.3).shift(UP)
        word12 = TexMobject("\\text{在}", "v=0", "\\text{的参考系下看到的碰撞瞬间过程:}", ).set_color_by_tex_to_color_map(
            color_dict_).scale(tex_scale + 0.3).next_to(
            word11, DOWN, 0.7, aligned_edge=LEFT)

        word21 = TexMobject("\\text{当}", "m_{1}=2", "\\text{，}", "v_{1}=2", "\\text{；}", "m_{2}=1", "\\text{，}",
                            "v_{2}=-1", "\\text{时，}", ).set_color_by_tex_to_color_map(color_dict_).scale(
            tex_scale + 0.3).shift(UP)
        word22 = TexMobject("\\text{在}", "v=1", "\\text{的参考系下看到的碰撞瞬间过程：}", ).set_color_by_tex_to_color_map(
            color_dict_).scale(tex_scale + 0.3).next_to(
            word11, DOWN, 0.7, aligned_edge=LEFT)

        # play
        self.play(Write(word21), run_time=1.5)
        self.play(Write(word22), run_time=1.5)
        self.wait(2)
        self.play(FadeOut(word21), FadeOut(word22), )

        self.add(model, vt_axes, ball1_graph, ball2_graph, dashline, vv_axes, dot_vv, line_vv)
        self.play(
            ApplyMethod(
                self.t_tracker.set_value, 2 * PI,
                run_time=2,
                rate_func=linear,
            ),
        )
        self.wait()