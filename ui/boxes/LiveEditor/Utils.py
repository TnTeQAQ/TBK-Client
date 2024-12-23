import numpy as np
import pygfx as gfx
import imageio.v3 as iio

# 读取并调整图像形状
def load_image(path):
    im = iio.imread(path)
    if len(im.shape) == 2:  # 如果图像是灰度图像，将其转换为RGB
        im = np.stack((im,) * 3, axis=-1)
    if im.shape[2] == 3:  # 如果图像没有Alpha通道，添加一个全不透明的Alpha通道
        im = np.concatenate(
            [im, 255 * np.ones((*im.shape[:2], 1), dtype=np.uint8)], axis=2
        )
    width = im.shape[1]
    height = im.shape[0]
    # 确保调整后的形状是正确的
    im = im.reshape((height, width, 4))
    tex_size = (width, height, 1)  # 更改为2D纹理大小
    tex = gfx.Texture(im, dim=2, size=tex_size)
    return tex

# 加载背景图片
def load_bg_img(canvas, img_path):
    tex = load_image(img_path)
    background = gfx.Background(None, gfx.BackgroundSkyboxMaterial(map=tex))
    canvas.add(background)
