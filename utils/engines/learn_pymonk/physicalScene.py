#!/usr/bin/python3
# -*- coding:utf-8 -*-

from manimlib.imports import *
import pymunk


class PhysicalScene(GraphScene):
    CONFIG = {
        "gravity": (0, -9.8),
        "physical_mob_list": [],
        "dt": 1.0 / 60,
    }

    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        self.space = pymunk.Space()
        self.space.gravity = self.gravity[0], self.gravity[1]
        GraphScene.__init__(self, **kwargs)


    def add_physical_mob(self, physical_mob):
        self.physical_mob_list.append([physical_mob,physical_mob.get_center()])
        self.space.add(physical_mob.body, physical_mob.poly)

    def space_step(self):
        self.space.step(self.dt)
        for physical_mob in self.physical_mob_list:
            physical_mob[1] = np.array([physical_mob[0].body.position[0], physical_mob[0].body.position[1], 0])


from from_wangkai.utils.engines.learn_pymonk.physical_MObject import PhysicalObj


class test_physical_scene(PhysicalScene):
    def construct(self):
        c = PhysicalObj()

        self.add_physical_mob(c)

        for t in range(60):
            self.add(c)
            self.space_step()
            for i in self.physical_mob_list:
                self.play(i[0].move_to,i[1],run_time=self.dt)
