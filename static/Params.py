from tzcp.ros.geometry_pb2 import (
    Vector3,
    Point,
    Quaternion,
    Pose2D,
    Pose,
    PoseStamped,
    PoseWithCovariance,
    Twist,
    TwistWithCovariance,
    Transform,
    Accel,
    Wrench,
)
from tzcp.ros.std_pb2 import (
    Float64,
    Int8,
    Int16,
    Int32,
    Int64,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
    String,
    ColorRGBA,
    Duration,
    Empty,
    Time,
    Header,
    MultiArrayDimension,
    MultiArrayLayout,
    ByteMultiArray,
    UInt32MultiArray,
    UInt64MultiArray,
    Int32MultiArray,
    Int64MultiArray,
    Float32MultiArray,
    Float64MultiArray,
)
from tzcp.ros.ackermann_pb2 import AckermannDrive, AckermannDriveStamped
from tzcp.ros.sensor_pb2 import LaserScan,RegionOfInterest,CameraInfo,Image,IMU
class TypeParams:
    TBK_TYPES = {
        'Vector3': Vector3(),
        'Point': Point(),
        'Quaternion': Quaternion(),
        'Pose2D': Pose2D(),
        'Pose': Pose(),
        'PoseStamped': PoseStamped(),
        'PoseWithCovariance': PoseWithCovariance(),
        'Twist': Twist(),
        'TwistWithCovariance': TwistWithCovariance(),
        'Transform': Transform(),
        'Accel': Accel(),
        'Wrench': Wrench(),
        'Float64': Float64(),
        'Int8': Int8(),
        'Int16': Int16(),
        'Int32': Int32(),
        'Int64': Int64(),
        'UInt8': UInt8(),
        'UInt16': UInt16(),
        'UInt32': UInt32(),
        'UInt64': UInt64(),
        'String': String(),
        'ColorRGBA': ColorRGBA(),
        'Duration': Duration(),
        'Empty': Empty(),
        'Time': Time(),
        'Header': Header(),
        'MultiArrayDimension': MultiArrayDimension(),
        'MultiArrayLayout': MultiArrayLayout(),
        'ByteMultiArray': ByteMultiArray(),
        'UInt32MultiArray': UInt32MultiArray(),
        'UInt64MultiArray': UInt64MultiArray(),
        'Int32MultiArray': Int32MultiArray(),
        'Int64MultiArray': Int64MultiArray(),
        'Float32MultiArray': Float32MultiArray(),
        'Float64MultiArray': Float64MultiArray(),
        'AckermannDrive': AckermannDrive(),
        'AckermannDriveStamped': AckermannDriveStamped(),
        'LaserScan': LaserScan(),
        'RegionOfInterest': RegionOfInterest(),
        'CameraInfo': CameraInfo(),
        'Image': Image(),
        'IMU': IMU(),
    }
    PLOT_SUPPORT_TYPES = [
        'Vector3',
        'Point',
        'Quaternion',
        'Float64',
        'IMU',
        'Int8',
        'Int16',
        'Int32',
        'Int64',
        'UInt8',
        'UInt16',
        'UInt32',
        'UInt64',
        'float',
        'int',
        'list',
        'dict',
        'tuple',
        'array',
    ]
    PYTHON_TYPES = ['int', 'float', 'list', 'tuple', 'dict']


class LanguageParams:
    def __init__(self):
        self._language_settings = {
            "en": {
                "dark_theme": "Dark",
                "light_theme": "Light",
                "theme_menu": "Themes",
                "chineseS_menu": "中文简体",
                "english_menu": "English",
                "language_label": "language",
                "view_menu": "View",
            },
            "zh": {
                "dark_theme": "黑暗",
                "light_theme": "明亮",
                "theme_menu": "主题",
                "chineseS_menu": "中文简体",
                "english_menu": "English",
                "language_label": "语言",
                "view_menu": "视图",
            },
        }

    def __getitem__(self, lang):
        return self._language_settings.get(lang)

