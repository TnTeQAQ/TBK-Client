from ui.boxes.LiveEditor.event_pb2 import EventMessage
from tbkpy.socket.udp import UDPMultiCastReceiver, UDPSender
from tbkpy.socket.plugins import ProtobufParser
from tzcp.ssl.rocos.zss_vision_detection_pb2 import Vision_DetectionFrame
from tzcp.ssl.rocos.zss_debug_pb2 import Debug_Heatmap, Debug_Msgs, Debug_Msg
from tzcp.ssl.rocos.zss_geometry_pb2 import Point
from ui.boxes.LiveEditor.logger.Logger import log
import time


class MsgHandler:
    def __init__(self, data=None, SENDERIP='233.233.233.233', VISION_PORT=41001):
        self.data = data
        self.receiver_vision = UDPMultiCastReceiver(
            SENDERIP,
            VISION_PORT,
            callback=self.callback_vision
        )
        self.receiver_event = UDPMultiCastReceiver(
            "233.233.233.233",
            1670,
            callback=self.callback_event,
            plugin=ProtobufParser(EventMessage)
        )

    def callback_vision(self, recv):
        if self.data["is_recording"]:
            packge = recv[0]
            time_now = time.time()
            index_time = int(time_now * 1e9)
            log.log(packge, index_time, 2)
            packge = ProtobufParser(Vision_DetectionFrame).decode(packge)
            self.data["stage_data"] = packge
            # elapsed_time = time_now - self.start_time
            # shareData.time.elapsed_time = elapsed_time
            # shareData.ui.plot_timeshapes_x.append(elapsed_time)
            # shareData.ui.plot_timeshapes_y.append(self.y_add)
            # shareData.ui.detection_data_real_tiem = packge

    def callback_event(self, recv):
        event_info = recv[0]
        event_name = event_info.name
        event_type = event_info.type
        event_start_time = (event_info.start_time - self.data["start_time"]) / 1e9
        event_end_time = (event_info.end_time - self.data["start_time"]) / 1e9
        event_color = event_info.color_rgba
        event_color = [1 if x < 1 else x for x in event_color]

        event_tag = event_info.tag
        event_level = abs(event_info.level)
        event_index = event_info.index
        # shareData.event.event = {
        #     "name": event_name,
        #     "start_time": event_start_time,
        #     "end_time": event_end_time,
        #     "type": event_type,
        #     "tag": event_tag,
        #     "color_rgba": event_color,
        #     "level": event_level
        # }

