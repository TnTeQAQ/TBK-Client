# import imageio.v3 as iio
import cv2
import numpy as np
import pygfx as gfx
from wgpu.gui.offscreen import WgpuCanvas


class Camera:
    def __init__(self):
        self.camera = gfx.PerspectiveCamera(fov=60, aspect=16 / 9, zoom=1)


class GfxEngine:
    def __init__(self, size=(800, 600), pixel_ratio=1, max_fps=999):
        self.canvas = WgpuCanvas(
            size=size,
            pixel_ratio=pixel_ratio,
            max_fps=max_fps,
        )
        self.renderer = gfx.renderers.WgpuRenderer(self.canvas)
        self.viewport = gfx.Viewport.from_viewport_or_renderer(self.renderer)

    def new_world(self):
        return World(self)

    def draw(self):
        image = np.array(self.canvas.draw())
        return image


class World:
    def __init__(self, gfx_engine: GfxEngine):
        self.world = gfx.Group()
        self.camera = gfx.PerspectiveCamera(fov=60, aspect=16 / 9, zoom=1)
        self.directional_light = gfx.DirectionalLight(color="#ffffff", intensity=1, cast_shadow=False)
        self.world.add(self.directional_light)
        self.gfx_engine = gfx_engine
        self.gfx_engine.canvas.request_draw(lambda: self.gfx_engine.renderer.render(self.world, self.camera))

    def load_image(self, path):  # 读取并调整图像形状
        im = cv2.imread(path, cv2.IMREAD_UNCHANGED)  # 读取图像，保留所有通道信息
        im = cv2.flip(im, 0)  # 翻转图像
        if len(im.shape) == 2:  # 如果图像是灰度图像，将其转换为RGBA
            im = cv2.cvtColor(im, cv2.COLOR_GRAY2RGBA)
        elif im.shape[2] == 3:  # 如果图像是RGB格式，添加一个全不透明的Alpha通道
            alpha_channel = 255 * np.ones((*im.shape[:2], 1), dtype=np.uint8)
            im = np.concatenate([im, alpha_channel], axis=2)
        elif im.shape[2] == 4:  # 如果图像已经是RGBA格式，则保持不变
            im = cv2.cvtColor(im, cv2.COLOR_BGRA2RGBA)

        width = im.shape[1]
        height = im.shape[0]
        # 确保调整后的形状是正确的
        im = im.reshape((height, width, 4))
        tex_size = (width, height, 1)  # 更改为2D纹理大小
        tex = gfx.Texture(im, dim=2, size=tex_size)
        return tex

    def load_background(self, path):
        tex = self.load_image(path)
        background = gfx.Background(None, gfx.BackgroundSkyboxMaterial(map=tex))
        self.world.add(background)

    def add_plane(
            self, width=10, height=10, position=(0, 0, 0), rotation=(0, 0, 0), flat_shading=True, color=(1, 1, 1, 1)
    ):
        plane = gfx.Mesh(
            gfx.plane_geometry(width, height),
            gfx.MeshBasicMaterial(color=color, flat_shading=flat_shading),
        )
        self.world.add(plane)

    def add_cube(
        self,
        width=1,
        height=1,
        depth=1,
        width_segments=1,
        height_segments=1,
        depth_segments=1,
        position=(0, 0, 0),
        rotation=(0, 0, 0),
        flat_shading=True,
        color=(1, 1, 1, 1),
    ):
        cube = gfx.Mesh(
            gfx.box_geometry(width=1, height=1, depth=1, width_segments=1, height_segments=1, depth_segments=1),
            gfx.MeshBasicMaterial(color=color, flat_shading=flat_shading),
        )
        self.world.add(cube)
        return self.world

    def add_object(self, obj):
        self.world.add(obj)

    def draw_image(self):
        return self.gfx_engine.draw()

    def draw(self):
        return self.gfx_engine.draw().ravel().astype("float32") / 255


_engine = GfxEngine()

if __name__ == "__main__":
    engine = GfxEngine()
    world = engine.new_world()
    world.add_plane()
    world.load_background("static/image/Heartbeat.png")
    world.camera.local.position = (0, 0, 20)
    res = world.draw_image()
    cv2.imshow("123", res)
    cv2.waitKey(0)
