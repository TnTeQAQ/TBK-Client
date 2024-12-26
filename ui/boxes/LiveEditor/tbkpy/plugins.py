
class BasePlugin:
    def encode(self, data):
        raise NotImplementedError
    def decode(self, data):
        raise NotImplementedError

class ProtobufParser(BasePlugin):
    def __init__(self, pb_class):
        self.pb_class = pb_class
    def encode(self, data):
        return data.SerializeToString()
    def decode(self, data):
        obj = self.pb_class()
        obj.ParseFromString(data)
        return obj