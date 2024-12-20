import dearpygui.dearpygui as dpg

from config.SystemConfig import FONT_FILE
from static.Params import LanguageParams


class LayoutManager:
    def __init__(self, theme="Dark", font_size=20, init_file="static/layout/ui_layout.ini",
                 settings_file="layout_settings.json"):
        # 初始化布局管理器，设置保存布局的文件名
        self.settings_file = settings_file
        self.init_file = init_file
        self.theme = theme
        self.language = LanguageParams()
        self.font_size = font_size
        self.set_theme(self.theme)
        self.set_font(self.font_size)

    # 主题
    def set_theme(self, theme):
        with dpg.theme() as global_theme:
            with dpg.theme_component(dpg.mvAll):
                if theme == "Dark":
                    dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (36, 36, 36, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (60, 60, 60, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (80, 80, 80, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_Button, (80, 80, 80, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (100, 100, 100, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (120, 120, 120, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (50, 50, 50, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (70, 70, 70, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (90, 90, 90, 255))
                    dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10)
                    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                    dpg.add_theme_color(dpg.mvThemeCol_Header, (70, 70, 70, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (90, 90, 90, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (110, 110, 110, 255))
                    dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 5, 5)

                if theme == "Light":
                    dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (240, 240, 240, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (220, 220, 220, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (200, 200, 200, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_Button, (200, 200, 200, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (180, 180, 180, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (160, 160, 160, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (230, 230, 230, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (210, 210, 210, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (190, 190, 190, 255))
                    dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10)
                    dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                    dpg.add_theme_color(dpg.mvThemeCol_Header, (70, 70, 70, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (90, 90, 90, 255))
                    dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (110, 110, 110, 255))
                    dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 5, 5)
        dpg.bind_theme(global_theme)

    def set_font(self, size=25):
        # 创建字体注册器
        with dpg.font_registry():
            # 加载字体，并设置字体大小为15
            with dpg.font(
                    FONT_FILE, size, pixel_snapH=True
            ) as chinese_font:
                # 添加字体范围提示，指定字体应包含完整的中文字符集
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
                # 以下是其他语言的字符集
                #    Options:
                #        mvFontRangeHint_Japanese
                #        mvFontRangeHint_Korean
                #        mvFontRangeHint_Chinese_Full
                #        mvFontRangeHint_Chinese_Simplified_Common
                #        mvFontRangeHint_Cyrillic
                #        mvFontRangeHint_Thai
                #        mvFontRangeHint_Vietnamese
        dpg.bind_font(chinese_font)

    # 语言
    def choose_lanuage(self, country):
        current_language = country
        label = self.language[current_language]
        dpg.set_item_label("main_window", label["main_window"])
        dpg.set_item_label("view_menu", label["view_menu"])
        dpg.set_item_label("theme_menu", label["theme_menu"])
        dpg.set_item_label("dark_theme", label["dark_theme"])
        dpg.set_item_label("light_theme", label["light_theme"])
        dpg.set_item_label("language_label", label["language_label"])
        dpg.set_item_label("chineseS_menu", label["chineseS_menu"])
        dpg.set_item_label("english_menu", label["english_menu"])
        dpg.set_item_label("english_menu", label["english_menu"])

