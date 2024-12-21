from utils.ClientLogManager import client_logger


def try_import(module_path, class_name):
    try:
        client_logger.log("TRACE", f"Trying to import {class_name} from {module_path}")
        module = __import__(module_path, fromlist=[class_name])
        return getattr(module, class_name)
    except ImportError as e:
        client_logger.log("ERROR", f"Failed to import {class_name} from {module_path}", e)
        return None
    except Exception as e:
        client_logger.log("ERROR", f"Unexpected error while importing {class_name} from {module_path}", e)
        return None


# 列出所有需要动态导入的模块路径和类名
modules_to_import = [
    ("ui.boxes.BaseBox", "BaseBox"),
    ("ui.boxes.ConsoleBox", "ConsoleBox"),
    ("ui.boxes.InputConsoleBox", "InputConsoleBox"),
    ("ui.boxes.DemoBox", "DemoBox"),
]

# 尝试导入每个模块，并将其绑定到全局命名空间
for module_path, class_name in modules_to_import:
    imported_class = try_import(module_path, class_name)
    if imported_class:
        globals()[class_name] = imported_class  # 动态添加到全局作用域
