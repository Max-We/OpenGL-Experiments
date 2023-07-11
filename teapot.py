from pathlib import Path

import numpy as np
from pyrr import Matrix44

import moderngl
import os

from camera import OrbitCameraWindow


class LoadingOBJ(OrbitCameraWindow):
    title = "Crazy Teapot"
    gl_version = (3, 3)
    resource_dir = Path(__file__).parent.resolve() / 'resources'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Obj: https://www.cgtrader.com/free-3d-models/household/kitchenware/white-porcelain-teapot-57e2cfe2-6112-4c26-a1c7-c18610204b6b
        self.obj = self.load_scene('teapot.obj')
        # Texture: https://www.freepik.com/free-photo/close-up-white-marble-texture-background_3472378.htm
        self.texture = self.load_texture_2d('cheramic.jpg')
        self.prog = self.load_program(os.path.join(os.path.dirname(__file__), "teapot.glsl"))

        scaling_factor = 25
        v_scaling_factor = np.full(3, scaling_factor, dtype=np.float32)
        self.prog['u_Scale'].write(v_scaling_factor)

        # https://github.com/moderngl/moderngl/blob/master/examples/loading_obj_files.py
        self.vao = self.obj.root_nodes[0].mesh.vao.instance(self.prog)

        # Config
        self.ctx.enable(moderngl.DEPTH_TEST)

        # No mouse controls for this view
        self.camera_enabled = False

    def render(self, time, frame_time):
        # Rotate in all directions to see all reflections
        rotation = Matrix44.from_eulers((time, time, time), dtype='f4')
        translation = Matrix44.from_translation((0.0, 0.0, -3.5), dtype='f4')
        model = translation * rotation

        self.prog['u_Model'].write(model)
        self.prog['u_Camera'].write(self.camera.matrix)
        self.prog['u_Projection'].write(self.camera.projection.matrix)

        self.texture.use()
        self.vao.render()

if __name__ == '__main__':
    LoadingOBJ.run()
