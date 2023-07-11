import struct
from pathlib import Path

import numpy as np
from pyrr import Matrix44

import moderngl
import os

from interaction import CameraWindow, OrbitCameraWindow


class LoadingOBJ(OrbitCameraWindow):
    title = "Crazy Teapot"
    gl_version = (3, 3)
    resource_dir = Path(__file__).parent.resolve() / 'resources'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.obj = self.load_scene('teapot.obj')
        # <a href="https://www.freepik.com/free-photo/close-up-white-marble-texture-background_3472378.htm#query=ceramic%20texture&position=7&from_view=search&track=ais">Image by rawpixel.com</a> on Freepik
        self.texture = self.load_texture_2d('cheramic.jpg')
        self.prog = self.load_program(os.path.join(os.path.dirname(__file__), "teapot.glsl"))

        s_factor = 25
        scaling_factor = np.array([s_factor, s_factor, s_factor], dtype=np.float32)
        self.prog['u_Scale'].write(scaling_factor)

        # Create a vao from the first root node (attribs are auto mapped)
        self.vao = self.obj.root_nodes[0].mesh.vao.instance(self.prog)
        self.ctx.enable(moderngl.DEPTH_TEST)

        # No mouse controls for this view
        self.camera_enabled = False

    def render(self, time, frame_time):
        # Rotate in all directions to see all reflections
        rotation = Matrix44.from_eulers((time, time, time), dtype='f4')
        translation_cube = Matrix44.from_translation((0.0, 0.0, -3.5), dtype='f4')
        model_view = translation_cube * rotation
        self.prog['u_Model'].write(model_view)
        self.prog['u_Camera'].write(self.camera.matrix)
        self.prog['u_Projection'].write(self.camera.projection.matrix)

        self.texture.use()
        self.vao.render()

if __name__ == '__main__':
    LoadingOBJ.run()
