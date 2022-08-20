import time
from abc import ABCMeta, abstractmethod

class Observer(metaclass=ABCMeta):
    """观察者基类"""

    @abstractmethod
    def update(self, observable, object_):
        pass


class Observable:
    """被观察者基类"""

    def __init__(self):
        self.__observers = []

    def add_observer(self, observer):
        self.__observers.append(observer)

    def remove_observer(self, observer):
        self.__observers.remove(observer)

    def notify_observers(self, object_=None):
        for observer in self.__observers:
            observer.update(self, object_)


class WaterHeater(Observable):
    """热水器"""
    def __init__(self):
        super().__init__()
        self.__temperature = 25

    def get_temperature(self):
        return self.__temperature

    def set_temperature(self, temperature):
        self.__temperature = temperature
        print(f'当前温度：{str(self.__temperature)}℃')
        self.notify_observers()


class WashingMode(Observer):
    """洗澡模式"""

    def update(self, observable, object_):
        if isinstance(observable, WaterHeater) and \
            observable.get_temperature() >= 50 and observable.get_temperature() <70:
            print("水烧好了 可以用来洗澡")


class DrinkingMode(Observer):
    """烧水模式"""

    def update(self, observable, object_):
        if isinstance(observable, WaterHeater) and \
            observable.get_temperature() >= 100:
            print('水烧开了 快来喝吧')


class Account(Observable):
    """用户账号"""

    def __init__(self):
        super(Account, self).__init__()
        self.__last_ip = dict()
        self.__last_region = dict()

    def login(self, name, ip, time):
        region = self.__get_region(ip)
        if self.__is_long_distance(name, region):
            obj_dict = {
                "name": name,
                'ip': ip,
                'region': region,
                'time': time
            }
            self.notify_observers(obj_dict)
        self.__last_region[name] = region
        self.__last_ip[name] = ip

    def __get_region(self, ip):
        """通过ip获取region"""
        ip_regions = {
           '101.47.18.5': '重庆',
           '67.217.61.8': '成都'
        }
        region = ip_regions.get(ip)
        return '' if region is None else region

    def __is_long_distance(self, name, region):
        """模拟地区差异"""
        last_region = self.__last_region.get(name)
        return last_region is not None and last_region != region


class SmsSender(Observer):
    """短信发送"""
    def update(self, observable, object_):
        print(f"短信：{object_['name']} 你好 你的账号可能登录异常 最后一次登录：{object_['ip']} {object_['region']}"
              f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(object_['time']))}")


class EmailSender(Observer):
    """邮件发送"""
    def update(self, observable, object_):
        print(f"邮件：{object_['name']} 你好 你的账号可能登录异常 最后一次登录：{object_['ip']} {object_['region']}"
              f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(object_['time']))}")

if __name__ == '__main__':
    # heater = WaterHeater()
    # washing_obser = WashingMode()
    # drinking_obser = DrinkingMode()
    # heater.add_observer(washing_obser)
    # heater.add_observer(drinking_obser)
    # heater.set_temperature(40)
    # heater.set_temperature(60)
    # heater.set_temperature(100)

    account = Account()
    account.add_observer(SmsSender())
    account.add_observer(EmailSender())
    account.login('jayeLiao', '101.47.18.5', time.time())
    account.login('jayeLiao', '67.217.61.8', time.time())