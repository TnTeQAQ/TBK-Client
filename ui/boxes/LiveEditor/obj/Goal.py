import math
import pygfx as gfx
import pylinalg as la

from ui.boxes.LiveEditor.obj.Object import Object


class Goal(Object):
    def __init__(self, **kwargs):
        self.center = kwargs.get("center", (0, 0, 0))
        self.width = kwargs.get("plane_width", 1000)
        self.depth = kwargs.get("depth", 200)
        self.color = kwargs.get("color", (0, 0, 0))
        # 球门的朝向
        self.dir = kwargs.get("dir", -1)
        super().__init__(**kwargs)

    def create(self):
        # 球门的三个板面
        z = 60
        dir = self.dir
        goal_up = gfx.Mesh(
            gfx.box_geometry(10, self.depth, 140),
            gfx.MeshBasicMaterial(color=self.color, flat_shading=True),
        )
        rot = la.quat_from_euler((math.pi / 2), order="Z")
        goal_up.local.rotation = rot
        goal_up.local.position = [
            self.center[0] - dir * (self.depth / 2),
            self.center[1] + dir * (self.width / 2),
            z,
        ]

        goal_middle = gfx.Mesh(
            gfx.box_geometry(10, self.width, 140),
            gfx.MeshBasicMaterial(color=self.color, flat_shading=True),
        )
        goal_middle.local.position = [self.center[0] - dir * self.depth, self.center[1], z]
        goal_down = gfx.Mesh(
            gfx.box_geometry(10, self.depth, 140),
            gfx.MeshBasicMaterial(color=self.color, flat_shading=True),
        )
        rot = la.quat_from_euler((-math.pi / 2), order="Z")
        goal_down.local.rotation = rot
        goal_down.local.position = [
            self.center[0] - dir * (self.depth / 2),
            self.center[1] - dir * (self.width / 2),
            z,
        ]
        self.grp.add(goal_up, goal_middle, goal_down)

