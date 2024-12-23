import dearpygui.dearpygui as dpg
from contextlib import contextmanager
import numpy as np


class Transform:
    def __init__(self):
        self.scale = [1, 1, 1]
        self.scale_matrix = dpg.create_scale_matrix(self.scale)
        self.translation = [0, 0, 0]
        self.translation_matrix = dpg.create_translation_matrix(self.translation)
        self.transform_matrix = self.translation_matrix * self.scale_matrix

    def matrix2list(self, matrix):
        transform = []
        for i in range(16):
            transform.append(matrix[i])
        data_array = np.array(transform)
        matrix = data_array.reshape(4, 4)
        matrix[0, 3] = -1 * matrix[-1, 0]
        matrix[1, 3] = -1 * matrix[-1, 1]
        matrix[-1, 0] = 0
        matrix[-1, 1] = 0
        return np.array(matrix)

    def pos_apply_transform(self, pos, translation_matrix, scale):
        x, y = pos
        scale = scale[0]
        x1, y1 = (self.matrix2list(translation_matrix) @ np.array([x, y, 1, 1]))[:2]
        return (int(x1 / scale), int(y1 / scale))


class CanvasCallBack:
    def __init__(self, tranform: Transform, scale_step):
        self._tranform = tranform
        self.scale_step = scale_step
        self.draw_mouse_pos = (0, 0)
        self.draw_mouse_pos_last = (0, 0)
        self.mouse_move_pos = (0, 0)

    def window_resize_callback(self, sender, app_data, user_data):
        width, height, drawlist_tag, drawlist_parent_tag, size_offset = user_data
        parent_width, parent_height = dpg.get_item_rect_size(drawlist_parent_tag)
        if width == -1:
            dpg.configure_item(drawlist_tag, width=parent_width + size_offset[0])
        if height == -1:
            dpg.configure_item(drawlist_tag, height=parent_height + size_offset[1])

    def update_canvas_data(self):
        self.draw_mouse_pos_last = self.draw_mouse_pos
        self.draw_mouse_pos = dpg.get_drawing_mouse_pos()
        self.mouse_move_pos = tuple(
            x - y for x, y in zip(self.draw_mouse_pos, self.draw_mouse_pos_last)
        )

    def drag_callback(self, sender, app_data, user_data):
        canvas_tag, auto_apply, drawlist_tag = user_data
        if not dpg.does_item_exist(drawlist_tag):
            return
        if not dpg.is_item_focused(drawlist_tag):
            return
        self._tranform.translation = tuple(
            x + y for x, y in zip(self._tranform.translation, tuple(self.mouse_move_pos) + (0,))
        )

        self._tranform.translation_matrix = dpg.create_translation_matrix(self._tranform.translation)
        self._tranform.transform_matrix = self._tranform.translation_matrix * self._tranform.scale_matrix
        if auto_apply:
            dpg.apply_transform(canvas_tag, self._tranform.transform_matrix)

    def wheel_callback(self, sender, app_data, user_data):
        canvas_tag, auto_apply, drawlist_tag = user_data
        if not dpg.does_item_exist(drawlist_tag):
            return
        if not dpg.is_item_focused(drawlist_tag):
            return
        mouse_x, mouse_y = self.draw_mouse_pos
        tl0, tl1, _ = self._tranform.translation
        scale = self._tranform.scale[0]
        world_mouse_x = (mouse_x - tl0) / scale
        world_mouse_y = (mouse_y - tl1) / scale
        scale_step = self.scale_step
        scale += scale_step if app_data > 0 else -scale_step
        scale = max(0.03, scale)
        scale = min(10, scale)
        self._tranform.scale = [scale, scale, 1]
        self._tranform.scale_matrix = dpg.create_scale_matrix(self._tranform.scale)
        new_translation_x = mouse_x - world_mouse_x * scale
        new_translation_y = mouse_y - world_mouse_y * scale
        self._tranform.translation = [new_translation_x, new_translation_y, 0]
        self._tranform.translation_matrix = dpg.create_translation_matrix(self._tranform.translation)
        self._tranform.transform_matrix = self._tranform.translation_matrix * self._tranform.scale_matrix
        if auto_apply:
            dpg.apply_transform(canvas_tag, self._tranform.transform_matrix)


class Canvas2D:
    def __init__(
            self,
            parent,
            size=(-1, -1),
            size_offset=(0, -50),
            pos=[],
            auto_mouse_transfrom=True,
            drop_callback=None,
            scale_step=0.1
    ):
        super().__init__()
        self.apply_mouse_transfrom = auto_mouse_transfrom
        self._transform = Transform()
        self._callback = CanvasCallBack(self._transform, scale_step)
        self.drawlist_tag = None
        self.canvas_tag = None
        self.group_tag = None
        self.background_tag = None
        self.drawlist_parent_tag = parent
        self.width, self.height = size
        self.size_offset = size_offset
        self._create(self.drawlist_parent_tag, self.width, self.height, pos)
        self._create_handler()

    def _create(self, parent, width=-1, height=-1, pos=[]):
        with dpg.group(parent=parent) as self.group_tag:
            with dpg.drawlist(width=width, height=height, pos=pos) as self.drawlist_tag:
                with dpg.draw_node() as canvas_tag:
                    self.canvas_tag = canvas_tag
                with dpg.draw_node() as background_tag:
                    self.background_tag = background_tag

            return self.drawlist_tag

    def _create_handler(self, parent=None):
        with dpg.item_handler_registry() as handler:
            dpg.add_item_resize_handler(
                callback=self._callback.window_resize_callback,
                user_data=(
                    self.width,
                    self.height,
                    self.drawlist_tag,
                    self.drawlist_parent_tag,
                    self.size_offset,
                ),
            )
        dpg.bind_item_handler_registry(self.drawlist_parent_tag, handler)

        if not self.apply_mouse_transfrom:
            return

        with dpg.handler_registry() as global_handler:
            dpg.add_mouse_drag_handler(
                button=dpg.mvMouseButton_Middle,
                callback=self._callback.drag_callback,
                user_data=(self.canvas_tag, self.apply_mouse_transfrom, self.drawlist_tag),
            )
            dpg.add_mouse_wheel_handler(
                callback=self._callback.wheel_callback,
                user_data=(self.canvas_tag, self.apply_mouse_transfrom, self.drawlist_tag),
            )

    def add_layer(self, parent=None, tag=None):
        if parent is None:
            parent = self.canvas_tag
        if tag is None:
            tag = dpg.generate_uuid()
        dpg.add_draw_node(parent=parent, tag=tag)
        return tag

    def pos_apply_transform(self, pos):
        self._transform.transform_matrix = self._transform.translation_matrix * self._transform.scale_matrix
        res = self._transform.pos_apply_transform(pos, self._transform.translation_matrix, self._transform.scale)
        return res

    @contextmanager
    def draw(self, parent=None):
        draw_tag = dpg.generate_uuid()
        if parent is None:
            parent = self.canvas_tag
        with dpg.draw_node(parent=parent) as draw_tag:
            yield draw_tag
