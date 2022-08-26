from abc import ABCMeta, abstractmethod
from enum import Enum
# python 3.4 之后支持枚举Enum语法

class InteractiveObject:
    """进行交互的对象"""
    pass


class InteractiveObjectImplA:
    """实现类A"""
    pass


class InteractiveObjectImplB:
    """实现类B"""
    pass


class Meditor:
    """中介类"""

    def __init__(self):
        self.__interactive_obj_a = InteractiveObjectImplA()
        self.__interactive_obj_b = InteractiveObjectImplB()

    def interactive(self):
        """进行交互操作"""
        # 通过self.__interactive_obj_a 和 self.__interactive_obj_b 完成相应的交互操作
        pass


class DeviceType(Enum):
    """设备类型"""

    TypeSpeaker = 1
    TypeMicrophone = 2
    TypeCamera = 3


class DeviceItem:
    """设备项"""

    def __init__(self, id_, name, type_, is_default=False):
        self.__id = id_
        self.__name = name
        self.__type = type_
        self.__is_default = is_default

    def __str__(self):
        return f"type:{self.__type} id:{self.__id} name:{self.__name} is Default:{self.__is_default}"

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_type(self):
        return self.__type

    def id_default(self):
        return self.__is_default


class DeviceList:

    def __init__(self):
        self.__devices = []

    def add(self, device_item):
        self.__devices.append(device_item)

    def get_count(self):
        return len(self.__devices)

    def get_by_idx(self, idx):
        if idx < 0 or idx >= self.get_count():
            return None
        return self.__devices[idx]

    def get_by_id(self, id):
        for item in self.__devices:
            if item.get_id() == id:
                return item
        return None


class DeviceMgr(metaclass=ABCMeta):

    @abstractmethod
    def enumerate(self):
        """枚举设备列表， 有设备插拔时都要重新获取设备列表"""
        pass

    @abstractmethod
    def active(self, device_id):
        """选择要使用的设备"""
        pass

    @abstractmethod
    def get_cur_device_id(self):
        """获取当前正在使用的设备 ID"""
        pass


class SpeakerMgr(DeviceMgr):
    """扬声器设备管理类"""

    def __init__(self):
        self.__cur_device_id = None

    def enumerate(self):
        """
        枚举设备列表
        真是项目应该通过驱动程序去读写设备信息， 这里只用初始化来模拟
        """
        devices = DeviceList()
        devices.add(DeviceItem('a445b8a0-4d6d-4dd1-988b-734cf2ee378a', 'Realtek High Definition Audio', DeviceType.TypeSpeaker))
        devices.add(DeviceItem('edb1623e-0fde-41b2-87ca-d07dc908a981', 'NVIDIA High Definition Audio', DeviceType.TypeSpeaker, True))
        return devices

    def active(self, device_id):
        """激活指定的设备作为当前要用的设备"""
        self.__cur_device_id = device_id

    def get_cur_device_id(self):
        return self.__cur_device_id


class DeviceUtil:
    """设备工具类"""

    def __init__(self):
        self.__mgrs = dict()
        self.__mgrs[DeviceType.TypeSpeaker] = SpeakerMgr()
        # 为节省篇幅 MicrophoneMgr 和 CameraMgr 不再实现
        # self.__microphoneMgr = MicrophoneMgr()
        # self.__cameraMgr = CameraMgr()

    def __get_device_mgr(self, type_):
        return self.__mgrs[type_]

    def get_device_list(self, type_):
        return self.__get_device_mgr(type_).enumerate()

    def active(self, type_, device_id):
        self.__get_device_mgr(type_).active(device_id)

    def get_cur_device_id(self, type_):
        return self.__get_device_mgr(type_).get_cur_device_id()


if __name__ == '__main__':
    device_util = DeviceUtil()
    device_list = device_util.get_device_list(DeviceType.TypeSpeaker)
    print('麦克风设备列表：')
    if device_list.get_count() > 0:
        device_util.active(DeviceType.TypeSpeaker, device_list.get_by_idx(0).get_id())
        for idx in range(0, device_list.get_count()):
            device = device_list.get_by_idx(idx)
            print(device)
        print('当前使用设备:' + device_list.get_by_id(device_util.get_cur_device_id(DeviceType.TypeSpeaker)).get_name())
