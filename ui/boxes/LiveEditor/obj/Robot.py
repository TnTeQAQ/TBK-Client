import pygfx as gfx
from ui.boxes.LiveEditor.obj.Object import Object
from static.Params import *

COLORS = {
    "BLUE_BODY_COLOR": (0, 0, 1, 1),
    "BLUE_EYE_COLOR": (0, 0, 0, 1),
    "BLUE_NAME_COLOR": (0, 0, 0, 1),
    "YELLOW_BODY_COLOR": (1, 1, 0, 1),
    "YELLOW_EYE_COLOR": (0, 0, 0, 1),
    "YELLOW_NAME_COLOR": (0, 0, 0, 1),
}


class Robot(Object):

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "ROBOT")
        self.team = kwargs.get("team", BLUE)
        self.length = kwargs.get("length", 130)
        self.width = kwargs.get("width", 130)
        self.height = kwargs.get("height", 130)
        self.robot_name = None
        self.robot_eye = None
        self.robot_body = None
        super().__init__(**kwargs)

    def create(self):
        self.robot_body = gfx.Mesh(
            gfx.box_geometry(self.width, self.length, self.height),
            gfx.MeshPhongMaterial(color=self.get_body_color(), flat_shading=True),
        )

        self.robot_eye = gfx.Mesh(
            gfx.box_geometry(self.width/13, self.length, self.height/3),
            gfx.MeshPhongMaterial(color=self.get_eye_color(), flat_shading=True),
        )
        self.robot_eye.local.position = [70, 0, 50]

        self.robot_name = gfx.Text(
            gfx.TextGeometry(
                markdown=self.name,
                screen_space=True,
                font_size=15,
                anchor="bottomleft",
            ),
            gfx.TextMaterial(color=self.get_name_color()),
        )
        self.robot_name.local.position = (0, 0, 100)

        self.grp.add(self.robot_body, self.robot_eye, self.robot_name)

    def set_color(self, body_color, eye_color, name_color):
        self.robot_body.material.color = body_color
        self.robot_eye.material.color = eye_color
        self.robot_name.material.color = name_color

    def set_team(self, team):
        self.team = team
        if team == BLUE:
            self.set_color(
                COLORS["BLUE_BODY_COLOR"],
                COLORS["BLUE_EYE_COLOR"],
                COLORS["BLUE_NAME_COLOR"],
            )
        elif team == YELLOW:
            self.set_color(
                COLORS["YELLOW_BODY_COLOR"],
                COLORS["YELLOW_EYE_COLOR"],
                COLORS["YELLOW_NAME_COLOR"],
            )
        else:
            raise ValueError("Invalid team!")

    def get_body_color(self):
        return COLORS["BLUE_BODY_COLOR"] if self.team == BLUE else COLORS["YELLOW_BODY_COLOR"]

    def get_eye_color(self):
        return COLORS["BLUE_EYE_COLOR"] if self.team == BLUE else COLORS["YELLOW_EYE_COLOR"]

    def get_name_color(self):
        return COLORS["BLUE_NAME_COLOR"] if self.team == BLUE else COLORS["YELLOW_NAME_COLOR"]
