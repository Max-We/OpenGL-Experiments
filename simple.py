# Mindestvoraussetzungen
# - Anzeigen einer simplen 3D-Szene mit mindestens drei Objekten
# - Rotation und Zoom der Szene mit Tastatur
# - Objekte haben unterschiedliche Farben
import os.path

import moderngl
import moderngl_window
import numpy as np
from moderngl_window.opengl.vao import VAO
from pyrr import Matrix44

from interaction import OrbitCameraWindow, CameraWindow


class InteractiveScene(CameraWindow):
    """
    https://github.com/moderngl/moderngl-window/blob/master/examples/geometry_cube.py
    """
    title = "Interactive Scene"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        self.shape_vertices = np.array([
            [0, 0, 0],
            [0, 0.5, 0],
            [0.5, 0, 0],
            [0, 0, 0.5],
        ], dtype=float)
        self.shape_indices = np.array([
            # 0,1,2,
            # 0,2,3,
            # 0,3,1,
            # 1,2,3
            0,1,2,
            0,3,1,
            0,3,2,
            3,1,2
        ], dtype=np.uint32)
        self.prog = self.load_program(os.path.join(os.path.dirname(__file__), "simple.glsl"))

        self.vao = VAO("geometry:cube", mode=moderngl.LINES)
        self.vao.buffer(self.shape_vertices, "3f", ["in_position"])
        index_buffer = self.ctx.buffer(self.shape_indices)
        self.vao.index_buffer(index_buffer)

    def render(self, time: float, frametime: float):
        self.ctx.enable(moderngl.DEPTH_TEST)

        # self.ctx.enable_only(moderngl.CULL_FACE | moderngl.LINE_STRIP)
        self.prog['m_proj'].write(self.camera.projection.matrix)
        self.prog['m_camera'].write(self.camera.matrix)

        translation = Matrix44.from_translation((0.0, 0.0, -3.5), dtype='f4')
        self.prog['m_model'].write(translation)
        self.prog['color'].value = 1.0, 0.5, 1.0, 1.0

        self.ctx.disable(moderngl.CULL_FACE)
        self.vao.render(self.prog)


if __name__ == '__main__':
    moderngl_window.run_window_config(InteractiveScene)
