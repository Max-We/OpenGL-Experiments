# Mindestvoraussetzungen
# - Anzeigen einer simplen 3D-Szene mit mindestens drei Objekten
# - Rotation und Zoom der Szene mit Tastatur
# - Objekte haben unterschiedliche Farben
import os.path
from pathlib import Path

import moderngl
import moderngl_window
from moderngl_window import geometry
from moderngl_window.context.base import WindowConfig
from moderngl_window.scene import KeyboardCamera
from pyrr import Matrix44


# Wahlpflichtfeatures
# - Rotation/Zoom der Szene mit der Maus
# - Bewegen in der Szene mittels Maus / Tastatur
# - Eine Lichtquelle, entsprechendes Shading
# - Animation mindestens eines Objekts (abschaltbar)

class CameraWindow(WindowConfig):
    """
    Base class for the camera controls

    - WASD-Movement
    - Camera rotation with the mouse

    Source: https://github.com/moderngl/moderngl-window/blob/master/examples/base.py
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = KeyboardCamera(self.wnd.keys, aspect_ratio=self.wnd.aspect_ratio)
        self.camera_enabled = True

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if self.camera_enabled:
            self.camera.key_input(key, action, modifiers)

        if action == keys.ACTION_PRESS:
            if key == keys.C:
                self.camera_enabled = not self.camera_enabled
                self.wnd.mouse_exclusivity = self.camera_enabled
                self.wnd.cursor = not self.camera_enabled
            if key == keys.SPACE:
                self.timer.toggle_pause()

    def mouse_position_event(self, x: int, y: int, dx, dy):
        if self.camera_enabled:
            self.camera.rot_state(-dx, -dy)

    def resize(self, width: int, height: int):
        self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)

class InteractiveScene(CameraWindow):
    """
    https://github.com/moderngl/moderngl-window/blob/master/examples/geometry_cube.py
    """
    title = "Interactive Scene"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        self.cube1 = geometry.cube(size=(2, 2, 2))
        self.cube2 = geometry.sphere(radius=2)
        # self.cube2 = geometry.cube(size=(2, 2, 2), center=(1,1,1))
        self.cube3 = geometry.cube(size=(2, 2, 2), center=(4,4,4))

        self.prog = self.load_program(os.path.join(os.path.dirname(__file__), "cube.glsl"))
        self.prog['color'].value = 1.0, 1.0, 1.0, 1.0

    def render(self, time: float, frametime: float):
        self.ctx.enable_only(moderngl.CULL_FACE | moderngl.DEPTH_TEST)

        # Without animation
        translation = Matrix44.from_translation((0.0, 0.0, -3.5), dtype='f4')
        self.prog['m_model'].write(translation)
        self.prog['m_proj'].write(self.camera.projection.matrix)
        self.prog['m_camera'].write(self.camera.matrix)
        self.cube2.render(self.prog)
        self.cube3.render(self.prog)

        # With animation
        rotation = Matrix44.from_eulers((time, time, time), dtype='f4')
        model_view = translation * rotation
        self.prog['m_model'].write(model_view)
        self.cube1.render(self.prog)


if __name__ == '__main__':
    moderngl_window.run_window_config(InteractiveScene)
