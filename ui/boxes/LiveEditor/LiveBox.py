import time
import math
import pygfx as gfx
from dearpygui import dearpygui as dpg
from ui.boxes.BaseBox import BaseBox
from ui.boxes.LiveEditor.MsgHandler import MsgHandler
from ui.boxes.LiveEditor.obj import *
from ui.boxes.LiveEditor.Utils import load_bg_img
from ui.components.Canvas3D import Canvas3D

from static.Params import *
from utils.ClientLogManager import client_logger


class LiveBox(BaseBox):
    only = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas3D = None
        self.ball = None
        self.field = None
        self.robots = {
            "blue": {},
            "yellow": {},
        }
        self.data = {
            "start_time": time.time() * 1e9,
            "is_recording": False,
            "stage_data": None,
        }
        self.msg_handler = MsgHandler(self.data)
        self.bg_img_path = "static/image/bg.jpg"

    def create(self):
        self.canvas3D = Canvas3D(self.tag)
        self.create_live_scene()

    def create_live_scene(self):
        load_bg_img(self.canvas3D, self.bg_img_path)
        self.field = Field(scene=self.canvas3D)

    def update(self):
        self.canvas3D.update()
        if self.data["is_recording"] and self.data["stage_data"] is not None:
            self.update_stage()

    def update_stage(self):
        ball = self.data["stage_data"].balls
        robots_blue = self.data["stage_data"].robots_blue
        robots_yellow = self.data["stage_data"].robots_yellow
        # 更新球的位置
        if self.ball is None:
            self.ball = Ball(scene=self.canvas3D)
        self.ball.set_position((ball.x, ball.y, self.field.get_z()))

        self.update_robots(robots_blue, self.robots["blue"], BLUE)
        self.update_robots(robots_yellow, self.robots["yellow"], YELLOW)

    def update_robots(self, current_robots, previous_robots, team_constant):
        current_ids = {robot.robot_id for robot in current_robots}
        previous_ids = set(previous_robots.keys())
        removed_ids = previous_ids - current_ids
        for rb in current_robots:
            robot = previous_robots.get(rb.robot_id)
            if robot is None:
                robot = Robot(
                    scene=self.canvas3D,
                    name=str(rb.robot_id),
                    team=team_constant,
                )
                previous_robots[rb.robot_id] = robot
            robot.set_position((rb.x, rb.y, self.field.get_z() + robot.height/2))
            robot.set_rotation(rb.orientation)
            robot.is_removed = False

        for removed_id in removed_ids:
            robot = previous_robots[removed_id]
            if not getattr(robot, "is_removed", False):
                robot.add_position((99999, 0, 0), 1)
                robot.is_removed = True

    def key_release_handler(self, sender, app_data, user_data):
        if dpg.is_key_released(dpg.mvKey_Return):
            self.data["is_recording"] = not self.data["is_recording"]
