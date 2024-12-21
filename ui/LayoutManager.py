import dearpygui.dearpygui as dpg
import json

from utils.ClientLogManager import client_logger


class LayoutManager:
    def __init__(self, config_file):
        self.config_path = "static/themes/"
        # 从配置文件中加载配置
        self.config = self.load_config(self.config_path+config_file+'.json')
        self.color_config = self.config.get("colors", {})
        self.style_config = self.config.get("styles", {})
        self.font_config = self.config.get("font", {})

        # 设置主题和字体
        self.set_theme()
        self.set_font()

    def load_config(self, config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError as e:
            client_logger.log("WARNING", f"Configuration file {config_file} not found", e)
            print(f"配置文件 {config_file} 未找到")
            return {}
        except json.JSONDecodeError as e:
            client_logger.log("WARNING", f"The configuration file {config_file} is in the wrong format", e)
            return {}

    def set_theme(self):
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                # 设置颜色
                for color_name, color_value in self.color_config.items():
                    color_enum = getattr(dpg, color_name, None)
                    if color_enum:
                        dpg.add_theme_color(color_enum, color_value)
                # 设置样式
                for style_name, style_value in self.style_config.items():
                    style_enum = getattr(dpg, style_name, None)
                    if style_enum:
                        if isinstance(style_value, list) and len(style_value) == 2:
                            dpg.add_theme_style(style_enum, style_value[0], style_value[1])
                        else:
                            dpg.add_theme_style(style_enum, style_value)
        dpg.bind_theme(global_theme)

    def set_font(self):
        font_file = self.font_config.get("file", None)
        font_size = self.font_config.get("size", 15)

        if font_file is None:
            print("字体文件未在配置中指定")
            return

        # 创建字体注册器
        with dpg.font_registry():
            with dpg.font(font_file, font_size, pixel_snapH=True) as custom_font:
                # 添加字体范围提示
                font_hint = self.font_config.get("range_hint", "mvFontRangeHint_Chinese_Full")
                font_hint_enum = getattr(dpg, font_hint, None)
                if font_hint_enum:
                    dpg.add_font_range_hint(font_hint_enum)

        dpg.bind_font(custom_font)


