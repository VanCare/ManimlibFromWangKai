#!/usr/bin/python3
# -*- coding:utf-8 -*-

from manimlib.imports import *
from from_wangkai.utils.imports import *


# class TitleMobjectTest(TextMobject):
#     CONFIG = {
#         "template_tex_file_body": TEMPLATE_TEXT_FILE_BODY,
#         "alignment": "\\centering",
#         "arg_separator": "",
#
#         "arg_separator": " ",
#         "substrings_to_isolate": [],
#         "tex_to_color_map": {},
#
#         "template_tex_file_body": TEMPLATE_TEX_FILE_BODY,
#         "stroke_width": 0,
#         "fill_opacity": 1.0,
#         "background_stroke_width": 1,
#         "background_stroke_color": BLACK,
#         "should_center": True,
#         "height": None,
#         "organize_left_to_right": False,
#         "alignment": "",
#
#         "template_tex_file_body": TEMPLATE_TEXT_FILE_BODY,
#         "alignment": "\\centering",
#         "arg_separator": "",
#
#         "arg_separator": " ",
#         "substrings_to_isolate": [],
#         "tex_to_color_map": {},
#
#         "template_tex_file_body": TEMPLATE_TEX_FILE_BODY,
#         "stroke_width": 0,
#         "fill_opacity": 1.0,
#         "background_stroke_width": 1,
#         "background_stroke_color": BLACK,
#         "should_center": True,
#         "height": None,
#         "organize_left_to_right": False,
#         "alignment": "",
#
#         "fill_color": None,
#         "fill_opacity": 0.0,
#         "stroke_color": None,
#         "stroke_opacity": 1.0,
#         "stroke_width": DEFAULT_STROKE_WIDTH,
#         # The purpose of background stroke is to have
#         # something that won't overlap the fill, e.g.
#         # For text against some textured background
#         "background_stroke_color": BLACK,
#         "background_stroke_opacity": 1.0,
#         "background_stroke_width": 0,
#         # When a color c is set, there will be a second color
#         # computed based on interpolating c to WHITE by with
#         # sheen_factor, and the display will gradient to this
#         # secondary color in the direction of sheen_direction.
#         "sheen_factor": 0.0,
#         "sheen_direction": UL,
#         # Indicates that it will not be displayed, but
#         # that it should count in parent mobject's path
#         "close_new_points": False,
#         "pre_function_handle_to_anchor_scale_factor": 0.01,
#         "make_smooth_after_applying_functions": False,
#         "background_image_file": None,
#         "shade_in_3d": False,
#         # This is within a pixel
#         # TODO, do we care about accounting for
#         # varying zoom levels?
#         "tolerance_for_point_equality": 1e-6,
#         "n_points_per_cubic_curve": 4,
#
#         "color": WHITE,
#         "name": None,
#         "dim": 3,
#         "target": None,
#     }

class TitleMobject(TexMobject):
    CONFIG = {
        "template_tex_file_body": TEMPLATE_TEXT_FILE_BODY,
        "alignment": "\\centering",
        "arg_separator": "",
    }

class TitleMobject1(TexMobject):
    CONFIG = {
        "template_tex_file_body": TEMPLATE_TEXT_FILE_BODY,
        "alignment": "\\centering",
        "arg_separator": "",

        "stroke_width": 3,
        "stroke_color": None,
        "stroke_opacity": 1.0,
        "fill_color": BLUE,
        "fill_opacity": 0.7,
        # "sheen_factor": 0.0, #光泽
        # "sheen_direction": UL,
        "color": YELLOW,
    }
    def __init__(self, *tex_strings, **kwargs):
        digest_config(self, kwargs)
        TexMobject.__init__(
            self, self.arg_separator.join(tex_strings), **kwargs
        )

class WordTemplate(Scene):
    def construct(self):
        # 标题
        title0 = TitleMobject('ASD')
        #
        title = TitleMobject1('ASD','QWE')
        title.shift(DOWN)


        title2 = TextMobject('$\\vec{r}$')
        title2.shift(DOWN * 2)
        title3 = TexMobject('ASD')
        title3.shift(DOWN * 3)

        # 公式
        # t1 = TextMobject('$\\vec{r}$')

        self.play(Write(title0))
        self.play(Write(title))

