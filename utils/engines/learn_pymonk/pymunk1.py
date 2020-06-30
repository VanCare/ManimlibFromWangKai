#!/usr/bin/python3
# -*- coding:utf-8 -*-

import pymunk
import time

#建模空间（重力），对象。绑定对象和形状，参数
space = pymunk.Space()
space.gravity=0,-10
body = pymunk.Body(1,10)
body.position=640,700
# poly = pymunk.Poly.create_box(body,(50,50))
poly = pymunk.Circle(body,1)
space.add(body,poly)

for t in range(20):
    #模拟时间前进
    space.step(0.1)

    print(body.position)
    print()
    time.sleep(0.1)