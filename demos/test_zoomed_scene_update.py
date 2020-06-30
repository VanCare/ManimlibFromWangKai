#!/usr/bin/python3
# -*- coding:utf-8 -*-

from manimlib.imports import *


"""
放大镜
"""
class Test_ZoomedScene(ZoomedScene):

    CONFIG = {
        # 'camera_config': {
        #     'background_color': WHITE,
        #     'cairo_line_width_multiple': 0.008,
        # },
        # "zoomed_display_height": 7,
        # "zoomed_display_width": 7,
        "zoomed_display_center": RIGHT * 3,
        # # "zoomed_display_corner_buff": DEFAULT_MOBJECT_TO_EDGE_BUFFER,
        "zoomed_camera_config": {
            # "default_frame_stroke_width": 3,
            # "default_frame_stroke_color": YELLOW,
            # "background_opacity": 0.9,
            # 'background_color': WHITE,
            # 'frame_center': DOWN * 2 + LEFT * 3,
            # 'cairo_line_width_multiple': 0.016,
        },
        "zoomed_camera_frame_starting_position": DOWN * 2 + LEFT * 3,
        # "zoom_factor": 0.24,
        # "zoom_activated": False,
    }

    def construct(self):
        grid = NumberPlane().set_opacity(0.5)
        circle = Circle(radius=0.2).move_to(DOWN * 2 + LEFT * 3)
        self.activate_zooming(animate=True)
        self.add(grid)
        self.play(ShowCreation(circle))
        self.wait(3)



"""
updata
"""
class Test_updater(Scene):
    def construct(self):
        dot = Dot()
        text = TextMobject("A")
        text.next_to(dot, LEFT)
        self.add(dot, text)
        d = TangentLine

        # Update function 保持文字在点左侧
        def update_text(obj):
            obj.next_to(dot, LEFT, buff=SMALL_BUFF)

        text.add_updater(update_text)  # 把这个函数添加给text
        self.play(Rotating(dot, radians=2 * PI, run_time=10, axis=OUT, about_point=2 * RIGHT))

        self.wait()


# class Test_multiAnimation(Scene):
#     def construct(self):
#         circle=Circle().move_to(RIGHT+UP*2)
#         square = Square()
#
#         self.play(AnimationGroup(Rotating(square,PI/2)))####
#         self.wait()

"""
切线
"""
class TestTangentLine(GraphScene):  # 切线
    def construct(self):
        def xx(x):
            return x ** 2 / 3

        self.setup_axes(animate=True)
        fg = self.get_graph(xx, WHITE, x_min=1, x_max=4)
        self.add(fg)
        self.wait()

        def f(fg, alpha):
            return TangentLine(fg, alpha,length=3)

        # qiexian = TangentLine(fg, 0.3)
        for i in range(1,30):
            temp = f(fg,i/30)
            self.add(temp)
            self.wait(0.1)
            self.remove(temp)


        # self.add(qiexian)
        self.wait()


class Test_temp(Scene):
    def construct(self):
        c=Circle()
        self.add(c)
        self.wait()
        c.move_to(UP)
        self.add(c)
        # self.play(Rotating(dot, radians=2 * PI, run_time=10, axis=OUT, about_point=2 * RIGHT))

        self.wait()


class ChangePositionAndSizeCamera(MovingCameraScene):
    def construct(self):
        text=TexMobject("\\nabla\\textbf{u}").scale(3)
        square=Square()

        # Arrange the objects
        VGroup(text,square).arrange_submobjects(RIGHT,buff=3)

        self.add(text,square)

        # Save the state of camera
        self.camera_frame.save_state()

        # Animation of the camera
        self.play(
            # Set the size with the width of a object
            self.camera_frame.set_width,text.get_width()*1.2,
            # Move the camera to the object
            self.camera_frame.move_to,text
        )
        self.wait()

        # Restore the state saved
        self.play(Restore(self.camera_frame))

        self.play(
            self.camera_frame.set_height,square.get_width()*1.2,
            self.camera_frame.move_to,square
        )
        self.wait()

        self.play(Restore(self.camera_frame))

        self.wait()



class ZoomedSceneExample(ZoomedScene):
    CONFIG = {
        "zoom_factor": 0.3,
        "zoomed_display_height": 1,
        "zoomed_display_width": 6,
        "image_frame_stroke_width": 20,
        "zoomed_camera_config": {
            "default_frame_stroke_width": 3,
        },
    }

    def construct(self):
        # Set objects
        dot = Dot().shift(UL*2)

        image=ImageMobject(np.uint8([[ 0, 100,30 , 200],
                                     [255,0,5 , 33]]))
        image.set_height(7)
        frame_text=TextMobject("Frame",color=PURPLE).scale(1.4)
        zoomed_camera_text=TextMobject("Zommed camera",color=RED).scale(1.4)

        self.add(image,dot)

        # Set camera
        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        frame.move_to(dot)
        frame.set_color(PURPLE)

        zoomed_display_frame.set_color(RED)
        zoomed_display.shift(DOWN)

        # brackground zoomed_display
        zd_rect = BackgroundRectangle(
            zoomed_display,
            fill_opacity=0,
            buff=MED_SMALL_BUFF,
        )

        self.add_foreground_mobject(zd_rect)

        # animation of unfold camera
        unfold_camera = UpdateFromFunc(
            zd_rect,
            lambda rect: rect.replace(zoomed_display)
        )

        frame_text.next_to(frame,DOWN)

        self.play(
            ShowCreation(frame),
            FadeInFromDown(frame_text)
        )

        # Activate zooming
        self.activate_zooming()

        self.play(
            # You have to add this line
            self.get_zoomed_display_pop_out_animation(),
            unfold_camera
        )

        zoomed_camera_text.next_to(zoomed_display_frame,DOWN)
        self.play(FadeInFromDown(zoomed_camera_text))

        # Scale in     x   y  z
        scale_factor=[0.5,1.5,0]

        # Resize the frame and zoomed camera
        self.play(
            frame.scale,                scale_factor,
            zoomed_display.scale,       scale_factor,
            FadeOut(zoomed_camera_text),
            FadeOut(frame_text)
        )

        # Resize the frame
        self.play(
            frame.scale,3,
            frame.shift,2.5*DOWN
        )

        # Resize zoomed camera
        self.play(
            ScaleInPlace(zoomed_display,2)
        )


        self.wait()

        self.play(
            self.get_zoomed_display_pop_out_animation(),
            unfold_camera,
            # -------> Inverse
            rate_func=lambda t: smooth(1-t),
        )
        self.play(
            Uncreate(zoomed_display_frame),
            FadeOut(frame),
        )
        self.wait()

