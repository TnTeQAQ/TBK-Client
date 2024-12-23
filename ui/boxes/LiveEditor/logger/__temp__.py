class Logger:
    pass

msgs = [
    'ssl_vision',
    'vision_fusion',
    'zss_cmd',
    'zss_debug',
]

raw_msgs = {
    "ssl_vision": ("224.5.23.2",10005),
    "vision_fusion": ("233.233.233.233", 41111)
}

logger = Logger(msgs, raw_msgs, path=...)

if __name__ == "__main__":
    import time
    handler = logger.get_handler("ssl_vision")
    while True:
        time.sleep()
        msgs = logger.msgs_list()
        for msg in msgs:
            logger.get_xxx(msg)
        handler.get_data(...)
        handler.get_info() # return store size, timestamps, file path, ...
            