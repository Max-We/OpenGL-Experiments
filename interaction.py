# Mindestvoraussetzungen
# - Anzeigen einer simplen 3D-Szene mit mindestens drei Objekten
# - Rotation und Zoom der Szene mit Tastatur
# - Objekte haben unterschiedliche Farben
import os.path

import moderngl
import moderngl_window
from moderngl_window import geometry
from moderngl_window.context.base import WindowConfig
from moderngl_window.scene import KeyboardCamera
from moderngl_window.scene.camera import OrbitCamera
from pyrr import Matrix44

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
        self.fullscreen = True

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

class OrbitCameraWindow(WindowConfig):
    """
    Base class for the orbit camera controls

    - Camera rotation with the mouse around the center of the scene

    Source: https://github.com/moderngl/moderngl-window/blob/master/examples/base.py
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera = OrbitCamera(aspect_ratio=self.wnd.aspect_ratio, target=(0,0,-3.5), radius=10)
        self.camera_enabled = True

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys

        if action == keys.ACTION_PRESS:
            if key == keys.C:
                self.camera_enabled = not self.camera_enabled
                self.wnd.mouse_exclusivity = self.camera_enabled
                self.wnd.cursor = not self.camera_enabled
            if key == keys.SPACE:
                self.timer.toggle_pause()

    def mouse_position_event(self, x: int, y: int, dx, dy):
        if self.camera_enabled:
            self.camera.rot_state(dx, dy)

    def mouse_scroll_event(self, x_offset: float, y_offset: float):
        if self.camera_enabled:
            self.camera.zoom_state(y_offset)

    def resize(self, width: int, height: int):
        self.camera.projection.update(aspect_ratio=self.wnd.aspect_ratio)

class InteractiveScene(OrbitCameraWindow):
    """
    https://github.com/moderngl/moderngl-window/blob/master/examples/geometry_cube.py
    """
    title = "Interactive Scene"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wnd.mouse_exclusivity = True
        self.cube = geometry.cube(size=(2, 2, 2))
        self.sphere = geometry.sphere(radius=1)
        self.cube2 = geometry.cube(size=(2, 2, 2))
        self.prog = self.load_program(os.path.join(os.path.dirname(__file__), "interaction.glsl"))

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
        self.cube.render(self.prog)


if __name__ == '__main__':
    moderngl_window.run_window_config(InteractiveScene)
