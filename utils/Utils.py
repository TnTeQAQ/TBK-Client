# from utils.DataProcessor import UiData


# 获取所有子类
def get_all_subclasses(cls):
    subclasses = cls.__subclasses__()
    all_subclasses = []
    for subclass in subclasses:
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))
    return all_subclasses


# _ui_data_instance = None
# def get_ui_data():
#     global _ui_data_instance
#     if _ui_data_instance is None:
#         _ui_data_instance = UiData()
#     return _ui_data_instance
