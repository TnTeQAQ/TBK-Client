import pygfx as gfx
import numpy as np
import pylinalg as la

from utils.ClientLogManager import client_logger


class Object:
    def __init__(self, **kwargs):
        if "scene" not in kwargs:
            client_logger.log("WARNING", f"{self.__class__} unspecified scene!")
        self.scene = kwargs.get("scene", gfx.Group())
        self.grp = gfx.Group(visible=True)
        self.scene.add(self.grp)
        # 平滑移动,旋转
        self.threshold_pos = 1.0
        self.threshold_dir = 5

        self.create()

    def create(self):
        pass

    def add_position(self, pos, rate, threshold=None):
        if threshold is None:
            threshold = self.threshold_pos

        current_position = np.array(self.grp.local.position)
        pos = np.array(pos)
        # 计算当前位置与目标位置的差异
        difference = np.linalg.norm(current_position - pos)
        if difference > threshold:
            # 在当前位置和目标位置之间进行插值
            pos = current_position + (pos - current_position) * rate
        # 更新机器人的位置
        self.grp.local.position = pos

    def add_rotation(self, dir, rate, threshold=None):
        if threshold is None:
            threshold = self.threshold_dir

        dir_robot = la.quat_to_euler(self.grp.local.rotation)
        error = -dir - dir_robot[2]
        error = (error + np.pi) % (2 * np.pi) - np.pi
        threshold = threshold * (np.pi / 180)
        if np.abs(error) < threshold:
            rate = 1
        res = error * rate
        rot = la.quat_from_euler((res), order="Z")
        self.grp.local.rotation = la.quat_mul(rot, self.grp.local.rotation)

    def delete(self):
        self.scene.remove(self.grp)
        self.grp = None

    # def set_name(self, name):
    #     self.grp_name.geometry.set_markdown(name[0] + name.split("_")[-1])

    def set_position(self, pos):
        x, y, z = pos
        self.grp.local.position = [x, y, z]

    def set_rotation(self, dir):
        rot = la.quat_from_euler((-dir), order="Z")
        self.grp.local.rotation = rot

    def set_color(self, **kwargs):
        pass
    #     self.grp_body.material.color = color
    #     self.grp_eye.material.color = (
    #         [1, 1, 1, 1] if color == [0.0, 0.0, 1.0, 1.0] else [0, 0, 0, 1]
    #     )
    #     self.grp_name.material.color = (
    #         [1, 1, 1, 1] if color == [0.0, 0.0, 1.0, 1.0] else [0, 0, 0, 1]
    #     )