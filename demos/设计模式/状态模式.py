from abc import ABCMeta, abstractmethod

class Context(metaclass=ABCMeta):
    """状态模式上下文环境类"""

    def __init__(self):
        self.__states = []
        self.__cur_state = None

        # 状态发生变化依赖的属性， 当这一变量由多个变量共同决定时可以将其单独定义成一个类
        self.__state_info = 0

    def add_state(self, state):
        if state not in self.__states:
            self.__states.append(state)

    def change_state(self, state):
        if state is None:
            return False
        if self.__cur_state is None:
            print("初始化", state.get_name())
        else:
            print(f"由 {self.__cur_state.get_name()} 变为 {state.get_name()}")
        self.__cur_state = state
        self.add_state(state)
        return True

    def get_state(self):
        return self.__cur_state

    def _set_state_info(self, state_info):
        self.__state_info = state_info
        for state in self.__states:
            if state.is_match(state_info):
                self.change_state(state)

    def _get_state_info(self):
        return self.__state_info


class State:
    """状态的基类"""

    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    @abstractmethod
    def is_match(self, state_info):
        "状态属性state_info 是否在当前状态范围内"
        return False

    @abstractmethod
    def behavior(self, context):
        pass


class Water(Context):
    """水"""

    def __init__(self):
        super().__init__()
        self.add_state(SolidState("固态"))
        self.add_state((LiquidState("液态")))
        self.add_state((GaseousState("气态")))
        self.set_temperature(25)

    def get_temperature(self):
        return self._get_state_info()

    def set_temperature(self, temperature):
        self._set_state_info(temperature)

    def rise_temperature(self, step):
        self.set_temperature(self.get_temperature() + step)

    def reduce_temperature(self, step):
        self.set_temperature(self.get_temperature() - step)

    def behavior(self):
        state = self.get_state()
        if isinstance(state, State):
            state.behavior(self)


# 单例装饰器
def singleton(cls, *args, **kwargs):
    instance = dict()

    def singleton(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    return singleton


@singleton
class SolidState(State):
    """固态"""

    def __init__(self, name):
        super().__init__(name)

    def is_match(self, state_info):
        return state_info < 0

    def behavior(self, context):
        print(f"当前温度 {context._get_state_info()}℃ 固体")


@singleton
class LiquidState(State):
    """液态"""

    def __init__(self, name):
        super().__init__(name)

    def is_match(self, state_info):
        return state_info >= 0 and state_info < 100

    def behavior(self, context):
        print(f"当前温度 {context._get_state_info()}℃ 液体")


@singleton
class GaseousState(State):
    def __init__(self, name):
        super().__init__(name)

    def is_match(self, state_info):
        return state_info >= 100

    def behavior(self, context):
        print(f"当前温度 {context._get_state_info()}℃ 气体")


if __name__ == '__main__':
    water = Water()
    water.behavior()
    water.set_temperature(-4)
    water.behavior()
    water.rise_temperature(18)
    water.behavior()
    water.rise_temperature(110)
    water.behavior()