import dearpygui.dearpygui as dpg
from api.PygfxApi import GfxEngine
import pygfx as gfx
from ui.components.Canvas2D import Canvas2D
import math
import numpy as np
import pylinalg as la


class BaseScene(gfx.Scene):
    def __init__(self, scale=1):
        super().__init__()
        self.scale = scale
        self.world.rotation = la.quat_from_euler((-math.pi / 2, 0, -math.pi / 2))
        self.light = gfx.AmbientLight("#ffffff", 3)
        self.add(self.light)
        # self.grid = gfx.GridHelper(100000 * self.scale, 300, color1="#444444", color2="#222222")
        # self.grid.local.up = (0, 0, 1)
        # self.add(self.grid)
        self.direct_light2 = gfx.DirectionalLight("#ffffff", 1)
        self.direct_light2.local.x = -100
        self.direct_light2.local.y = -200
        self.add(self.direct_light2)
        path = [[0, 0, 0], [0, 0, 0]]
        geometry = gfx.Geometry(positions=path)
        material = gfx.LineMaterial(thickness=10.0, color=(0.8, 0.7, 0.0, 1.0))
        self.test_line = gfx.Line(geometry, material)
        self.add(self.test_line)


class World:
    def __init__(self, SIZE=(800, 600), scale=1):
        self.scale = scale
        self.gfx_engine = GfxEngine(size=SIZE)
        self.world = self.gfx_engine.new_world()
        self._canvas = self.gfx_engine.canvas
        self._renderer = self.gfx_engine.renderer
        self._viewport = self.gfx_engine.viewport
        self._scene = BaseScene(scale=self.scale)
        self._scene.add(gfx.AmbientLight())
        directional_light = gfx.DirectionalLight()
        directional_light.world.z = 1
        self._scene.add(directional_light)
        self.mouse_world_position = [0, 0, 0]
        self._camera = gfx.PerspectiveCamera(fov=70, aspect=16 / 9)
        self._camera.world.z = 400 * self.scale
        self.size = SIZE
        self._controller = gfx.OrbitController(self._camera)
        self._canvas.request_draw(lambda: self._renderer.render(self._scene, self._camera))

    def update(self):
        self.handle_event(
            gfx.objects.Event(
                **{
                    "type": "before_render",
                }
            )
        )
        value = (self.gfx_engine.draw()).ravel().astype(np.float32) / 255.0
        return value

    def handle_event(self, event: gfx.objects.Event):
        self._controller.handle_event(event, self._viewport)
        # print(self._renderer.get_pick_info([0,0,0]))


class Handler:
    def __init__(self, SIZE=(800, 600), scale=1):
        self.scale = scale
        self.pressedDown = {}
        self.world = World(SIZE, self.scale)
        self.BUTTON_MAP = {
            0: 1,  # MOUSE_LEFT
            1: 2,  # MOUSE_RIGHT
            2: 3,  # MOUSE_MIDDLE
        }
        self.WHEEL_RATIO = 500 - (1 - self.scale) * 350

    def callback(self, sender, app_data, user_data):
        try:
            if not dpg.is_item_focused(user_data):
                return
        except:
            pass
        info = dpg.get_item_info(sender)
        type = info["type"]
        if type == "mvAppItemType::mvMouseDragHandler":
            self.world.handle_event(
                gfx.objects.PointerEvent(
                    **{
                        "type": gfx.objects.EventType.POINTER_MOVE,
                        "x": dpg.get_drawing_mouse_pos()[0],
                        "y": dpg.get_drawing_mouse_pos()[1],
                        "button": self.BUTTON_MAP[app_data[0]],
                    }
                )
            )
        elif type == "mvAppItemType::mvMouseClickHandler":
            self.world.handle_event(
                gfx.objects.PointerEvent(
                    **{
                        "type": gfx.objects.EventType.POINTER_DOWN,
                        "x": dpg.get_drawing_mouse_pos()[0],
                        "y": dpg.get_drawing_mouse_pos()[1],
                        "button": self.BUTTON_MAP[app_data],
                    }
                )
            )
        elif type == "mvAppItemType::mvMouseReleaseHandler":
            self.world.handle_event(
                gfx.objects.PointerEvent(
                    **{
                        "type": gfx.objects.EventType.POINTER_UP,
                        "x": dpg.get_drawing_mouse_pos()[0],
                        "y": dpg.get_drawing_mouse_pos()[1],
                        "button": self.BUTTON_MAP[app_data],
                    }
                )
            )
        elif type == "mvAppItemType::mvMouseWheelHandler":
            self.world.handle_event(
                gfx.objects.WheelEvent(
                    **{
                        "type": gfx.objects.EventType.WHEEL,
                        "x": dpg.get_drawing_mouse_pos()[0],
                        "y": dpg.get_drawing_mouse_pos()[1],
                        "dx": -app_data * self.WHEEL_RATIO,
                        "dy": 0,
                    }
                )
            )


class Canvas3D:
    def __init__(
            self,
            parent,
            SIZE=(800, 600),
            scale=1,
            is_mouse_controller=True,
    ):
        self.scale = scale
        self.size = SIZE
        self.is_mouse_controller = is_mouse_controller
        self.canvas = Canvas2D(parent=parent, auto_mouse_transfrom=False)
        self.tag = self.canvas.group_tag
        self.handler = Handler(SIZE, self.scale)
        self.handler_registry()
        self.texture_data = self.texture_registry(SIZE)
        self.camera = self.handler.world._camera
        self.viewport = self.handler.world._viewport
        with self.canvas.draw():
            dpg.draw_image(self.texture_data, pmin=[0, 0], pmax=SIZE)

    def handler_registry(self):
        if not self.is_mouse_controller:
            return
        with dpg.handler_registry():
            dpg.add_mouse_wheel_handler(callback=self.handler.callback, user_data=self.canvas.drawlist_tag)
            dpg.add_mouse_release_handler(callback=self.handler.callback, user_data=self.canvas.drawlist_tag)
            dpg.add_mouse_click_handler(callback=self.handler.callback, user_data=self.canvas.drawlist_tag)
            dpg.add_mouse_drag_handler(callback=self.handler.callback, user_data=self.canvas.drawlist_tag)

    def add(self, obj):
        self.handler.world._scene.add(obj)

    def remove(self, obj):
        self.handler.world._scene.remove(obj)

    def texture_registry(self, size):
        width, height = self.size
        texture = np.zeros((size[1], size[0], 4), dtype=np.float32).reshape(-1)
        with dpg.texture_registry():
            texture_tag = dpg.add_raw_texture(
                width=width, height=height, default_value=texture, format=dpg.mvFormat_Float_rgba
            )
        return texture_tag

    def draw(self):
        # scence.draw()
        pass

    def get_world_position(self):
        return self.handler.world.mouse_world_position

    def update(self):
        value = self.handler.world.update()

        dpg.set_value(self.texture_data, value)
