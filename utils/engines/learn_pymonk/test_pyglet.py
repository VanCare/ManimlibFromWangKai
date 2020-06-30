#!/usr/bin/python3
# -*- coding:utf-8 -*-

import pyglet
import pymunk
from pymunk.pyglet_util import DrawOptions

window = pyglet.window.Window(1280,720,"test_pymunk",resizable=False)
options = DrawOptions()

space = pymunk.Space()
space.gravity=0,-300
body = pymunk.Body(1,10)
body.position=640,700
poly = pymunk.Poly.create_box(body,(50,50))
space.add(body,poly)

@window.event
def on_draw():
    window.clear()
    space.debug_draw(options)

def update(dt):
    space.step(dt)

if __name__=="__main__":
    pyglet.clock.schedule_interval(update,1.0/60)
    pyglet.app.run()
