import numpy as np
import pygfx as gfx
from ui.boxes.LiveEditor.obj.Goal import Goal

from ui.boxes.LiveEditor.obj.Object import Object


class Field(Object):
    def __init__(self, **kwargs):
        self.objz = kwargs.get("objz", 50)
        self.center = kwargs.get("center", (0, 0, 0))
        self.width = kwargs.get("width", 9000)
        self.height = kwargs.get("height", 6000)
        self.plane_width = kwargs.get("plane_width", 12000)
        self.plane_height = kwargs.get("plane_height", 9000)
        self.penalty_length = kwargs.get("penalty_length", 2000)
        self.penalty_width = kwargs.get("penalty_width", 1000)
        self.goal_width = kwargs.get("goal_width", 1000)
        self.goal_depth = kwargs.get("goal_depth", 200)
        self.radius = kwargs.get("radius", 500)
        self.line_color = kwargs.get("line_color", (1.0, 1.0, 1.0, 0.8))
        self.line_width = kwargs.get("line_width", 2)
        self.plane_color = kwargs.get("plane_color", (0.2, 0.5, 0.2, 0.99))
        
        self.goal_blue = None
        self.goal_yellow = None
        super().__init__(**kwargs)

    def create(self):
        self.field_plane()
        self.create_goal()

    def field_plane(self):
        plane = gfx.Mesh(
            gfx.plane_geometry(self.plane_width, self.plane_height),
            gfx.MeshBasicMaterial(color=self.plane_color, flat_shading=True),
        )
        plane.local.position = self.center
        self.grp.add(plane)
        self.field_line()

    def field_line(self):
        # 定义颜色和宽度
        color = self.line_color  # 归一化到[0, 1]范围
        width = self.line_width
        # 定义点
        x = self.center[0]
        y = self.center[1]
        z = self.center[2] + 1
        p1 = [-self.width / 2 + x, self.height / 2 + y, z]
        p2 = [self.width / 2 + x, self.height / 2 + y, z]
        p3 = [self.width / 2 + x, -self.height / 2 + y, z]
        p4 = [-self.width / 2 + x, -self.height / 2 + y, z]
        # 绘制线条
        positions = np.array([p1, p2, p3, p4, p1], dtype=np.float32)
        line = gfx.Line(
            gfx.Geometry(positions=positions),
            gfx.LineMaterial(thickness=width, color=color),
        )
        self.grp.add(line)

        # 中线和中竖线
        middle_line_positions = np.array(
            [
                middle_pos(p1, p4) + [z],
                middle_pos(p2, p3) + [z],
                middle_pos(p1, p2) + [z],
                middle_pos(p3, p4) + [z],
                ],
            dtype=np.float32,
        )

        for i in range(0, len(middle_line_positions), 2):
            line = gfx.Line(
                gfx.Geometry(positions=middle_line_positions[i: i + 2]),
                gfx.LineMaterial(thickness=width, color=color),
            )
            self.grp.add(line)

        # 矩形
        rect_positions = [
            [
                [-self.width/2+x, self.penalty_length/2+y, z],
                [-self.width/2+x, -self.penalty_length/2+y, z],
                [-(self.width/2-self.penalty_width)+x, -self.penalty_length/2+y, z],
                [-(self.width/2-self.penalty_width)+x, self.penalty_length/2+y, z],
                [-self.width/2+x, self.penalty_length/2+y, z],
            ],
            [
                [(self.width/2-self.penalty_width)+x, self.penalty_length/2+y, z],
                [(self.width/2-self.penalty_width)+x, -self.penalty_length/2+y, z],
                [self.width/2+x, -self.penalty_length/2+y, z],
                [self.width/2+x, self.penalty_length/2+y, z],
                [(self.width/2-self.penalty_width)+x, self.penalty_length/2+y, z],
            ],
            [
                [-(self.width/2+self.goal_depth)+x, self.goal_width/2+y, z],
                [-(self.width/2+self.goal_depth)+x, -self.goal_width/2+y, z],
                [-self.width/2+x, -self.goal_width/2+y, z],
                [-self.width/2+x, self.goal_width/2+y, z],
                [-(self.width/2+self.goal_depth)+x, self.goal_width/2+y, z],
            ],
            [
                [self.width/2+x, self.goal_width/2+y, z],
                [self.width/2+x, -self.goal_width/2+y, z],
                [(self.width/2+self.goal_depth)+x, -self.goal_width/2+y, z],
                [(self.width/2+self.goal_depth)+x, self.goal_width/2+y, z],
                [self.width/2+x, self.goal_width/2+y, z],
            ],
        ]
        for rect in rect_positions:
            rect_line = gfx.Line(
                gfx.Geometry(positions=np.array(rect, dtype=np.float32)),
                gfx.LineMaterial(thickness=width, color=color),
            )
            self.grp.add(rect_line)

        # 圆弧 - 近似为一个多边形
        arc_points = []
        for angle in np.linspace(0, 2 * np.pi, 100):
            x = self.radius * np.cos(angle)
            y = self.radius * np.sin(angle)
            arc_points.append([x, y, z])
        arc = gfx.Line(
            gfx.Geometry(positions=np.array(arc_points, dtype=np.float32)),
            gfx.LineMaterial(thickness=width, color=color),
        )
        self.grp.add(arc)

    def create_goal(self):
        x = self.center[0]
        y = self.center[1]
        z = self.center[2] + 1
        self.goal_blue = Goal(scene=self.grp, center=[self.width/2+x, y, z], width=self.goal_width, depth=self.goal_depth, color=[1, 1, 0, 255], dir=-1)
        self.goal_yellow = Goal(scene=self.grp, center=[-self.width/2+x, y, z], width=self.goal_width, depth=self.goal_depth, color=[0, 0, 1, 1], dir=1)


def middle_pos(pos1, pos2):
    return [(pos1[0] + pos2[0]) / 2, (pos1[1] + pos2[1]) / 2]