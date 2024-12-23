import time
import pygfx as gfx
from dearpygui import dearpygui as dpg
from ui.boxes.BaseBox import BaseBox
from ui.boxes.LiveEditor.MsgHandler import MsgHandler
from ui.boxes.LiveEditor.obj import *
from ui.boxes.LiveEditor.Utils import load_bg_img
from ui.components.Canvas3D import Canvas3D

from utils.ClientLogManager import client_logger

class LiveBox(BaseBox):
    only = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canvas3D = None
        self.ball = None
        self.field = None
        self.robots = {}
        self.data = {
            "start_time": time.time() * 1e9,
            "is_recording": False,
            "stage_data": None,
        }
        self.msg_handler = MsgHandler(self.data)
        self.bg_img_path = "static/image/bg.jpg"
        for i in range(32):
            Robot(self.canvas3D)

    def create(self):
        self.canvas3D = Canvas3D(self.tag)
        self.create_live_scene()

    def create_live_scene(self):
        load_bg_img(self.canvas3D, self.bg_img_path)
        self.ball = Ball(scene=self.canvas3D)
        self.field = Field(scene=self.canvas3D)

    def update(self):
        self.canvas3D.update()
        if self.data["is_recording"]:
            self.update_stage()

    def update_stage(self):
        balls = self.data["stage_data"].balls
        robots_blue = self.data["stage_data"].robots_blue
        robots_yellow = self.data["stage_data"].robots_yellow
        # print(balls)

    def key_release_handler(self, sender, app_data, user_data):
        if dpg.is_key_released(dpg.mvKey_Return):
            self.data["is_recording"] = not self.data["is_recording"]
