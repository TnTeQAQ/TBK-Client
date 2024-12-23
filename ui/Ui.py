import json
import dearpygui.dearpygui as dpg

from ui.LayoutManager import LayoutManager
from utils.Utils import get_all_subclasses
# from utils.DataProcessor import get_ui_data
from ui.boxes import *
from config.SystemConfig import PROHIBITED_BOXES, UI_TITTLE, UI_WIDTH, UI_HEIGHT, UI_THEME


class UI:
    def __init__(self):
        dpg.create_context()
        self.layout_manager = LayoutManager(UI_THEME)
        # self.ui_data = None
        self.boxes = []
        self.box_count = {}
        self.is_created = False
        self.console_box = None
        self.input_box = None
        self.all_classes = get_all_subclasses(BaseBox)
        self.generate_add_methods()
        self.boxes_init_file = "static/layout/boxes_init.json"

    def create(self):
        # 创建主窗口
        self.add_global_handler()
        dpg.create_viewport(title=UI_TITTLE, width=UI_WIDTH, height=UI_HEIGHT)
        dpg.configure_app(
            docking=True,
            docking_space=True,
        )
        dpg.setup_dearpygui()
        dpg.show_viewport()
        self.create_viewport_menu()
        # self.ui_data = get_ui_data()
        self.console_box = self.add_ConsoleBox(ui=self)
        self.input_box = self.add_InputConsoleBox(ui=self)
        self.load_boxes()
        self.is_created = - True

    def create_viewport_menu(self):
        pass
        # with dpg.viewport_menu_bar():
        #     with dpg.menu(label="File", tag="file_menu"):
        #         dpg.add_menu_item(label="Save Layout")
        #         dpg.add_menu_item(label="Load Layout")
        #         dpg.add_menu_item(label="Exit")
        #     with dpg.menu(label="SSL3D", tag="ssl3d_menu"):
        #         dpg.add_menu_item(
        #             label="Camera option  (F2)",
        #             tag="camera_option_menutiem",
        #             # callback=self.pop_camera_option_window,
        #         )

    def load_boxes(self):
        try:
            with open(self.boxes_init_file, "r") as f:
                boxes_config = json.loads(f.read())
                for box_config in boxes_config:
                    if box_config["cls_name"] in PROHIBITED_BOXES:
                        continue
                    self.new_box(
                        box_config["cls_name"],
                        width=box_config["plane_width"],
                        height=box_config["plane_height"],
                        pos=box_config["pos"]
                    )
        except Exception as e:
            client_logger.log("WARNING", "Box load failed", e)

    def show(self):
        if not self.is_created:
            self.create()

    def update(self):
        for box in self.boxes:
            if box.is_created:
                box.update()

    def new_box(self, box_name, **kwargs):
        method = f"add_{box_name}"
        func = getattr(self, method)
        func(ui=self, **kwargs)

    def destroy_all_boxes(self):
        for box in self.boxes:
            box.destroy()

    def run_loop(self, func=None):
        if func is not None:
            try:
                while dpg.is_dearpygui_running():
                    func()
                    dpg.render_dearpygui_frame()
            except Exception as e:
                client_logger.log("ERROR", f"Loop Failed??? {e}")
            finally:
                self.destroy_all_boxes()
        else:
            dpg.start_dearpygui()

    def add_global_handler(self):
        # 创建全局监听
        with dpg.handler_registry():
            # 松开按键时监听
            dpg.add_key_release_handler(callback=self.on_key_release)
            # 鼠标移动检测
            dpg.add_mouse_move_handler(callback=self.on_mouse_move)
            # # 鼠标滚动检测
            # dpg.add_mouse_wheel_handler(callback=self.on_mouse_wheel)

    # 生成添加类方法
    def generate_add_methods(self):
        for cls in self.all_classes:
            method_name = f"add_{cls.__name__}"
            # 使用闭包捕获cls
            def add_method(self, cls=cls, **kwargs):
                try:
                    if cls.only and self.box_count.get(cls, 0) >= 1:
                        # 如果盒子已经创建则不重复创建
                        raise Exception("This box can only be created once")
                    instance = cls(**kwargs)
                    instance.create_box()
                    return instance
                except Exception as e:
                    client_logger.log("WARNING", f"Unable to instantiate {cls}", e=e)
            # 将生成的方法绑定到当前实例
            setattr(self, method_name, add_method.__get__(self))

    def save_boxes(self):
        with open(self.boxes_init_file, "w+") as f:
            boxes_config = []
            for box in self.boxes:
                if box.__class__.__name__ in PROHIBITED_BOXES:
                    continue
                boxes_config.append(
                    {
                        "cls_name": box.__class__.__name__,
                        "plane_width": dpg.get_item_width(box.tag),
                        "plane_height": dpg.get_item_height(box.tag),
                        "pos": dpg.get_item_pos(box.tag),
                    }
                )
            f.write(json.dumps(boxes_config))
            f.flush()

    # 监听事件
    def on_key_release(self, sender, app_data, user_data):
        if dpg.is_key_down(dpg.mvKey_LControl) and app_data == dpg.mvKey_S:
            self.save_boxes()
            client_logger.log("SUCCESS", "Layout saved successfully!")
        if dpg.is_key_released(dpg.mvKey_F11):
            dpg.toggle_viewport_fullscreen()

    def on_mouse_move(self, sender, app_data):
        pass
        # self.ui_data.draw_mouse_pos_last = self.ui_data.draw_mouse_pos
        # self.ui_data.draw_mouse_pos = dpg.get_drawing_mouse_pos()
        # self.ui_data.mouse_move_pos = tuple(
        #     x - y for x, y in zip(self.ui_data.draw_mouse_pos, self.ui_data.draw_mouse_pos_last)
        # )
