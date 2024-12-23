import pygfx as gfx

from ui.boxes.LiveEditor.obj.Object import Object


class Ball(Object):
    def __init__(self, **kwargs):
        self.ball = None
        self.ball_radius = kwargs.get("radius", 43)
        super().__init__(**kwargs)

    def create(self):
        self.ball = gfx.Mesh(
            gfx.sphere_geometry(self.ball_radius, self.ball_radius, self.ball_radius),
            gfx.MeshPhongMaterial(color=(1, 0.647, 0, 1), flat_shading=True),
        )
        self.ball.local.position = [0, 0, self.ball_radius]
        self.grp.add(self.ball)

