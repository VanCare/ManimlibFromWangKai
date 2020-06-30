#!/usr/bin/python3
# -*- coding:utf-8 -*-

"""
定义视频的背景模板
图层问题：作者和标题永远固定
"""

from manimlib.imports import *


class TemplateScene(Scene):
    CONFIG = {
        "Author": "@注定吃饭",
        "title_name": "如何理解",
        "subtitle_name": "动量定理",
        # "svg_filename": "manim_projects/svg/coin.svg",
        "def_colors": [RED_A, GREEN, BLUE_B, BLUE_E],
    }

    def add_mark(self):
        subtitle2 = TextMobject(self.subtitle_name).scale(0.6).set_opacity(0.6).set_color_by_gradient(
            self.def_colors[1], self.def_colors[2])
        subtitle2.to_corner(UR)

        author2 = TextMobject(self.Author).scale(0.5).set_opacity(0.3)
        author2.to_corner(DR)

        # svg_file = SVGMobject(file_name = self.svg_filename)
        # svg_file.to_corner(UP)

        self.add(subtitle2, author2)
        self.wait()


class Test_TemplateScene(TemplateScene):  # 测试TemplateScene
    def construct(self):
        self.add_mark()


class WordScene(TemplateScene):  # 纯文字
    def all2left(self):  # 全部页面切到左侧
        pass

    def all2right(self):  # 全部页面切到右侧
        pass

    def left2all(self):  # 左侧切回全部页面
        pass

    def right2all(self):  # 右侧切回全部页面
        pass


class GraphScene_(TemplateScene):  # 纯图像
    pass


class GraphScene_(TemplateScene):  # 纯坐标
    pass


class GraphWordScene(TemplateScene):  # 文字+图像
    pass


class GraphWordScene(TemplateScene):  # 文字+坐标
    pass


class GraphWordScene(TemplateScene):  # 图像+坐标
    pass


class GraphWordScene(TemplateScene):  # 文字+图像+坐标
    pass


class GraphWordScene(TemplateScene):  # 文字+图像
    pass
