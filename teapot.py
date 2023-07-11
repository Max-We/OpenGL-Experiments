from pathlib import Path

import numpy as np
from pyrr import Matrix44

import moderngl
import os

from interaction import CameraWindow, OrbitCameraWindow


class LoadingOBJ(OrbitCameraWindow):
    title = "Loading OBJ"
    gl_version = (3, 3)
    resource_dir = Path(__file__).parent.resolve() / 'resources'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.obj = self.load_scene('teapot.obj')
        # <a href="https://www.freepik.com/free-photo/close-up-white-marble-texture-background_3472378.htm#query=ceramic%20texture&position=7&from_view=search&track=ais">Image by rawpixel.com</a> on Freepik
        self.texture = self.load_texture_2d('cheramic.jpg')
        self.prog = self.load_program(os.path.join(os.path.dirname(__file__), "teapot.glsl"))

        self.light = self.prog['Light']
        self.color = self.prog['Color']
        self.light.value = (-140.0, 400.0, -350.0)
        self.color.value = (1.0, 1.0, 1.0, 0.1)

        s_factor = 20
        scaling_factor = np.array([s_factor, s_factor, s_factor], dtype=np.float32)
        self.prog['Scale'].write(scaling_factor)

        # Create a vao from the first root node (attribs are auto mapped)
        self.vao = self.obj.root_nodes[0].mesh.vao.instance(self.prog)
        self.ctx.enable(moderngl.DEPTH_TEST)

        # No mouse controls for this view
        self.camera_enabled = False

    def render(self, time, frame_time):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.camera.rot_state(2,0)

        self.prog['m_proj'].write(self.camera.projection.matrix)
        self.prog['m_camera'].write(self.camera.matrix)
        self.prog['CameraPosition'].write(self.camera.position)

        translation = Matrix44.from_translation((0.0, 0.0, -3.5), dtype='f4')
        self.prog['m_model'].write(translation)

        self.texture.use()
        self.vao.render()

if __name__ == '__main__':
    LoadingOBJ.run()
