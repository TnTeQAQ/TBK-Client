import dearpygui.dearpygui as dpg
from ui.boxes.BaseBox import BaseBox


class DemoBox(BaseBox):
    # only = True 表示只能创建一个实例
    only = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create(self):
        # create 会自动创建dpg窗口， 窗口拥有tag，获取的方法是 self.tag
        # 创建按钮
        dpg.add_button(label="test", parent=self.tag, callback=lambda: print("hello"))

    def destroy(self):
        # 销毁之前可以做的事情
        super().destroy()  # 真正销毁Box

    def update(self):
        pass