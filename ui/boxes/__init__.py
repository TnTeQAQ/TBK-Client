from utils.ClientLogManager import client_logger

def try_import(module_path, class_name=None):
    """
    动态尝试导入模块和类，支持单个模块或模块中的特定类。

    :param module_path: 模块路径
    :param class_name: 要导入的类名，如果为 None，则导入整个模块
    :return: 导入的模块或类；如果导入失败则返回 None
    """
    try:
        if class_name:
            client_logger.log("TRACE", f"Trying to import {class_name} from {module_path}")
            module = __import__(module_path, fromlist=[class_name])
            return getattr(module, class_name)
        else:
            return __import__(module_path)
    except ImportError as e:
        client_logger.log("ERROR", f"Failed to import {class_name} from {module_path}", e)
        return None


# 列出所有需要动态导入的模块路径和类名
modules_to_import = [
    ("ui.boxes.BaseBox", "BaseBox"),
    ("ui.boxes.ConsoleBox", "ConsoleBox"),
    ("ui.boxes.InputConsoleBox", "InputConsoleBox"),
    ("ui.boxes.DemoBox", "DemoBox"),
    ("ui.boxes.LiveEditor", None),
]

# 动态导入模块，绑定到全局作用域
for module_path, class_name in modules_to_import:
    imported = try_import(module_path, class_name)
    if imported:
        if class_name:
            globals()[class_name] = imported  # 将类名绑定到全局作用域
        else:
            module_name = module_path.split('.')[-1]
            globals()[module_name] = imported  # 将模块名绑定到全局作用域