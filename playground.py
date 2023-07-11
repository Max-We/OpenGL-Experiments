import os.path

import moderngl
import moderngl_window
from moderngl_window import geometry
from pyrr import Matrix44

from camera import CameraWindow


class Playground(CameraWindow):
    """
    Based on:
    https://github.com/moderngl/moderngl-window/blob/master/examples/geometry_cube.py
    """
    title = "Playground"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        self.cube1 = geometry.cube(size=(2, 2, 2))
        self.cube2 = geometry.cube(size=(2, 2, 2))
        self.sphere = geometry.sphere(radius=1)
        self.prog = self.load_program(os.path.join(os.path.dirname(__file__), "playground.glsl"))
        self.camera.mouse_sensitivity = 0.1

    def render(self, time: float, frametime: float):
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)
        self.prog['m_proj'].write(self.camera.projection.matrix)
        self.prog['m_camera'].write(self.camera.matrix)

        # Without animation
        # Sphere
        translation = Matrix44.from_translation((0.0, 0.0, -3.5), dtype='f4')
        self.prog['m_model'].write(translation)
        self.prog['color'].value = 0.5, 1.0, 1.0, 1.0
        self.sphere.render(self.prog)
        # Cube
        translation_cube2 = Matrix44.from_translation((-4.0, 0.0, -3.5), dtype='f4')
        self.prog['m_model'].write(translation_cube2)
        self.prog['color'].value = 1.0, 0.5, 1.0, 1.0
        self.cube2.render(self.prog)

        # With animation
        # Cube
        rotation = Matrix44.from_eulers((time, time, time), dtype='f4')
        translation_cube = Matrix44.from_translation((4.0, 0.0, -3.5), dtype='f4')
        model_view = translation_cube * rotation
        self.prog['m_model'].write(model_view)
        self.prog['color'].value = 1.0, 1.0, 0.5, 1.0
        self.cube1.render(self.prog)


if __name__ == '__main__':
    moderngl_window.run_window_config(Playground)
