# export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
import dearpygui.dearpygui as dpg

from ui.Ui import UI
from utils.ClientLogManager import client_logger

# import dearpygui.demo as demo

def loop(UI):
    try:
        UI.update()
    except Exception as e:
        client_logger.log("ERROR", f"Loop Failed!", e)


def main():
    ui = UI()
    ui.show()
    # dpg.show_style_editor()
    # demo.show_demo()
    ui.run_loop(lambda: loop(ui))


if __name__ == "__main__":
    main()
