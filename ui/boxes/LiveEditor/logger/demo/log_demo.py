import sys
sys.path.append("../")
import Logger as logger
import vision_detection_pb2 as detection
from vision_detection_pb2 import Vision_DetectionBall
import log_pb2
def LOG(dir = "logs"):
    log = logger.Logger(dir)
    for i in range(10000):
        res = i
        ball = Vision_DetectionBall()
        ball.vel_x = res
        ball.vel_y = res
        ball.area = res
        ball.x = res
        ball.y = res
        ball.height = res
        ball.ball_state = res
        ball.last_touch = res
        ball.valid = True
        ball.raw_x = res
        ball.raw_y = res
        ball.chip_predict_x = res
        ball.chip_predict_y = res
        ball.SerializeToString()
        log.log(message_data=ball,message_type=log_pb2.MessageType.MESSAGE_PROTO,save_module="Chunking",size=500,energy_saving=True)
        print(i)
def read_log(path):
    log_player = logger.LogPlayer(path)
    msg = log_player.read_log()
    print(msg)

def get_next_log(path):
    b = Vision_DetectionBall()
    log_player = logger.LogPlayer(path)
    msg_len = log_player.get_message_count()

    for i in range(0,msg_len,1):
        msg = log_player.get_next_message()
        b.ParseFromString(msg.message_data)
        print(b)

def play_log(path):
    b = Vision_DetectionBall()
    log_player = logger.LogPlayer(path)
    for msg in log_player.get_next_msg():
        b.ParseFromString(msg.message_data)
        print(b)
        # 
if __name__ == '__main__':
    # log_player = logger.LogPlayer("logs/Rec_2024-08-31_15-00-14-882937.log")
    # print(log_player.get_message_count())
    
    LOG("logs")
    # read_log("logs/Rec_2024-08-31_15-56-00-729781.log")
    # get_next_log("../logs/Rec_2024-08-19_12-52-45-358209.log")
    # play_log("../logs/Rec_2024-08-19_12-52-45-358209.log")