from dearpygui import dearpygui as dpg
from scipy.ndimage import label

from utils.ClientLogManager import client_logger

sub_box_x = 300
sub_box_y = 50
pos_offset = 20


class BaseBox(object):
    only = False

    def __init__(self, ui, **kwargs):
        self.ui = ui
        self.tag = None
        self.label = None
        self.is_created = False
        self.only = True
        self.window_settings = kwargs
        self.handler = dpg.add_handler_registry()

    def create(self):
        # 创建
        global sub_box_x, sub_box_y, pos_offset
        if self.is_created:
            client_logger.log("ERROR", "BaseBox has already been created")
            return
        default_settings = {
            "width": 800,
            "height": 800,
            "pos": (sub_box_x, sub_box_y),
            "label": self.__class__.__name__,
        }
        merged_settings = {**default_settings, **self.window_settings}
        self.tag = dpg.add_window(
            on_close=self.destroy,
            **merged_settings,
        )
        sub_box_x += pos_offset
        sub_box_y += pos_offset
        self.ui.boxes.append(self)
        self.ui.box_count[self.__class__] = self.ui.box_count.setdefault(self.__class__, 0) + 1
        client_logger.log("INFO", f"{self} instance has been added to the boxes list.")

        self.on_create()

        dpg.add_key_press_handler(callback=self.key_press_handler, parent=self.handler)
        dpg.add_key_release_handler(callback=self.key_release_handler, parent=self.handler)
        self.is_created = True

    def on_create(self):
        pass

    def show(self):
        # 显示盒子
        if not dpg.does_item_exist(self.tag):
            self.on_create()
        dpg.show_item(self.tag)

    def hide(self):
        # 隐藏盒子
        dpg.hide_item(self.tag)

    def update(self):
        # raise f"{self.__name__} does not implement update()"
        pass

    def key_release_handler(self, sender, app_data, user_data):
        pass
    def key_press_handler(self, sender, app_data, user_data):
        pass
    def destroy(self):
        # 销毁盒子
        global sub_box_x, sub_box_y, pos_offset
        self.ui.boxes.remove(self)
        self.ui.box_count[self.__class__] -= 1
        dpg.delete_item(self.tag)
        dpg.delete_item(self.handler)
        sub_box_x -= pos_offset
        sub_box_y -= pos_offset
        client_logger.log("INFO", f"{self} has been destroyed.")

    @property
    def x(self):
        return dpg.get_item_pos(self.tag)[0]

    @property
    def y(self):
        return dpg.get_item_pos(self.tag)[1]
