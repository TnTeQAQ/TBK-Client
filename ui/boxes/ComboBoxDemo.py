import dearpygui.dearpygui as dpg
from ui.boxes import Box


class ComboBoxDemo(Box):
    def __init__(self,data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.cbl_tag = None
        self.btn_tag = None

    def create(self):
        self.check_and_create_window()
        # if self.tag:
        #     dpg.add_window(tag=self.tag, label=self.label)
        # else:
        #     self.tag = dpg.add_window(label=self.label)
        if self.label is None:
            dpg.configure_item(self.tag, label="ComboBoxDemo")
        # 创建按钮
        self.btn_tag = dpg.add_button(label="Options     V", parent=self.tag)
        # 创建点击后列表
        self.cbl_tag = dpg.add_window(popup=True, show=False)
        for l in self.data:
            dpg.add_checkbox(label=l, parent=self.cbl_tag)
        dpg.configure_item(item=self.btn_tag, callback=self.on_btn_clicked)

    def on_btn_clicked(self, sender, app_data, user_data):
        x, y = [x1 + x2 for x1, x2 in zip(dpg.get_item_pos(sender), dpg.get_item_pos(self.tag))]
        width, height = dpg.get_item_rect_size(sender)
        dpg.configure_item(item=self.cbl_tag, pos=(x, y + height))
        dpg.configure_item(item=self.cbl_tag, show=True)