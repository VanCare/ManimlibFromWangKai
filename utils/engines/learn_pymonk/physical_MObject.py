#!/usr/bin/python3
# -*- coding:utf-8 -*-

from manimlib.imports import *
import pymunk


class PhysicalObj(Circle):
    """
    Physical Mathematical Object
    """
    CONFIG = {
        "physical": {
            "body": {
                "mass": 1,
                "moment": 1,
                "body_type": ["dynamic","kinematic","static"]
            },
        }
    }

    def __init__(self,mass=1,moment=1,bodytype=0, **kwargs):
        self.mass=mass
        self.moment = moment
        self.bodytype = bodytype
        Circle.__init__(self, **kwargs)
        self.body = self.get_body()
        self.poly = self.get_poly()
    def get_body(self):
        body = pymunk.Body(self.mass, self.moment,self.bodytype)
        loc =self.get_center()
        body.position = loc[0],loc[1]
        return body
    def get_poly(self):
        poly = pymunk.Circle(body=self.body, radius=self.radius)  # 只能是圆形
        return poly
    def get_loc(self,dt):
        pass

class test_PhysicalObj(Scene):
    def construct(self):
        c = PhysicalObj()