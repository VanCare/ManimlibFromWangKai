#!/usr/bin/python3
# -*- coding:utf-8 -*-

from manimlib.imports import *
from from_wangkai.utils.imports import *
import numpy as np
import random


class TestCS(Scene):  #

    def construct(self):
        # 坐标系
        mob = []
        # CS = CoordinateSystem()
        # mob.append(CS)
        A = Axes().shift((UR * 2))
        mob.append(A)
        TDA = ThreeDAxes()
        mob.append(TDA)
        NP = NumberPlane()
        mob.append(NP)
        CP = ComplexPlane()
        mob.append(CP)

        sentence = [
            # Text("CoordinateSystem()").move_to(UL),
            Text("Axes()").move_to(UL),
            Text("ThreeDAxes()").move_to(UL),
            Text("NumberPlane()").move_to(UL),
            Text("ComplexPlane()").move_to(UL),
        ]
        for i in range(len(mob)):
            self.add(mob[i], sentence[i])
            self.wait()
            self.remove(mob[i], sentence[i])
            self.wait()


class Scene1(GraphScene):
    def construct(self):
        self.setup_axes()
        self.wait()
        self.play(self.axes.move_to, 3 * UP)
        l = Line()
        self.add(l)
        self.wait()


class Scene2(MovingCameraScene):
    def construct(self):
        plane = NumberPlane()
        axes = ThreeDAxes()
        self.add(plane)
        self.wait()
        # ball = Circle().move_to(UP*3)
        # self.get_moving_mobjects()
        self.add(axes)
        self.wait()


class Scene3(ThreeDScene):
    def construct(self):
        plane = NumberPlane()
        axes = ThreeDAxes()
        self.add(plane)
        self.wait()
        self.move_camera(phi=60 * DEGREES, theta=-65 * DEGREES, run_time=1, added_anims=[])
        self.add(axes)
        self.wait()


class Scene4(SpecialThreeDScene):
    CONFIG = {
        "default_angled_camera_position": {
            "phi": 65 * DEGREES,  # Angle off z axis
            "theta": -60 * DEGREES,  # Rotation about z axis
            "distance": 50,
            "gamma": 0,  # Rotation about normal vector to camer
        }
    }

    def construct(self):
        plane = NumberPlane().set_shade_in_3d()
        axes = ThreeDAxes()
        self.set_camera_to_default_position()
        self.add(plane)
        self.wait()
        self.move_camera(phi=60 * DEGREES, theta=-125 * DEGREES, run_time=1, added_anims=[])
        self.add(axes)
        self.wait()


class Scene5(SpecialThreeDScene):
    def construct(self):
        plane = NumberPlane().set_shade_in_3d()
        axes = ThreeDAxes()
        self.add(plane)
        self.wait()
        self.move_camera(phi=60 * DEGREES, theta=-65 * DEGREES, run_time=1, added_anims=[])
        self.add(axes)
        self.wait()


class Scene6(SpecialThreeDScene):
    def construct(self):
        plane = NumberPlane().set_shade_in_3d()
        axes = ThreeDAxes()
        self.add(plane)
        self.wait()
        self.move_camera(phi=60 * DEGREES, theta=-65 * DEGREES, run_time=1, added_anims=[])
        self.add(axes)
        self.wait()


class Scene7(NumberPlane):
    CONFIG = {
        "axis_config": {
            "stroke_color": WHITE,
            "stroke_width": 2,
            "include_ticks": False,
            "include_tip": True,
            "line_to_number_buff": SMALL_BUFF,
            "label_direction": DR,
            "number_scale_val": 0.5,
        },
        "y_axis_config": {
            "label_direction": DR,
            "stroke_opacity": 0.2,
        },
        "background_line_style": {
            "stroke_color": BLUE_D,
            "stroke_width": 2,
            "stroke_opacity": 1,
        },
        # Defaults to a faded version of line_config
        "faded_line_style": None,
        "x_line_frequency": 1,
        "y_line_frequency": 1,
        "faded_line_ratio": 1,
        "make_smooth_after_applying_functions": True,
    }

    def construct(self):
        a = Axes()
        self.add(a)
        self.play(ShowCreation(a))


class Scene8(LinearTransformationScene):
    CONFIG = {
        "include_background_plane": True,
        "include_foreground_plane": True,
        "foreground_plane_kwargs": {
            "x_max": FRAME_WIDTH / 2,
            "x_min": -FRAME_WIDTH / 2,
            "y_max": FRAME_WIDTH / 2,
            "y_min": -FRAME_WIDTH / 2,
            "faded_line_ratio": 0
        },
        "background_plane_kwargs": {
            "color": GREY,
            "axis_config": {
                "stroke_color": LIGHT_GREY,
            },
            "axis_config": {
                "color": GREY,
            },
            "background_line_style": {
                "stroke_color": GREY,
                "stroke_width": 1,
            },
        },
        "show_coordinates": False,
        "show_basis_vectors": True,
        "basis_vector_stroke_width": 6,
        "i_hat_color": X_COLOR,
        "j_hat_color": Y_COLOR,
        "leave_ghost_vectors": False,
        "t_matrix": [[3, 0], [1, 2]],

        "always_update_mobjects": False,
    }

    def construct(self):
        b = TextMobject("foreward")
        c = Circle()
        self.add_foreground_mobject(b)
        self.add_transformable_mobject(c)
        self.wait()
        self.apply_inverse([[1, 2], [-1, 2]])


class LinearTransformation(LinearTransformationScene):
    CONFIG = {
        "include_background_plane": True,
        "include_foreground_plane": True,
        "foreground_plane_kwargs": {
            "x_radius": FRAME_WIDTH,
            "y_radius": FRAME_HEIGHT,
            "secondary_line_ratio": 0
        },
        "background_plane_kwargs": {
            "color": GREY,
            "secondary_color": DARK_GREY,
            "axes_color": GREY,
            "stroke_width": 2,
        },
        "show_coordinates": False,
        "show_basis_vectors": True,
        "basis_vector_stroke_width": 6,
        "i_hat_color": X_COLOR,
        "j_hat_color": Y_COLOR,
        "leave_ghost_vectors": False,
    }

    def construct(self):
        mob = Circle()
        mob.move_to(RIGHT + UP * 2)
        vector_array = np.array([[1], [2]])
        matrix = [[0, 1], [-1, 1]]

        self.add_transformable_mobject(mob)

        self.add_vector(vector_array)

        self.apply_matrix(matrix)

        self.wait()

class RemoveAllObjectsInScreen(Scene):
    def construct(self):
        self.add(
            VGroup(
                *[
                    VGroup(
                        *[
                            Dot()
                            for i in range(30)
                        ]
                    ).arrange_submobjects(RIGHT)
                    for j in range(10)
                ]
            ).arrange_submobjects(DOWN)
        )

        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
            # All mobjects in the screen are saved in self.mobjects
        )

        self.wait()

