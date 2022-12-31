from abc import abstractmethod, ABCMeta


class Person(metaclass=ABCMeta):
    """人"""
    def __init__(self, name):
        self._name = name

    @abstractmethod
    def wear(self):
        print("着装：")


class Engineer(Person):
    """工程师"""
    def __init__(self, name, skill):
        super().__init__(name)
        self.__skill = skill

    def get_skill(self):
        return self.__skill

    def wear(self):
        print('我是' + self.get_skill() + '工程师' + self._name, end=', ')
        super().wear()


class Teacher(Person):
    """教师"""

    def __init__(self, name, title):
        super().__init__(name)
        self.__title = title

    def get_title(self):
        return self.__title

    def wear(self):
        print('我是' + self._name + self.get_title(), end=', ')
        super().wear()


class ClothingDecorator(Person):
    """服装装饰器基类"""

    def __init__(self, person):
        self._decorated = person

    def wear(self):
        self._decorated.wear()
        self.decorate()

    @abstractmethod
    def decorate(self):
        pass


class CasualPantDecorator(ClothingDecorator):
    """休闲裤类装饰器"""

    def __init__(self, person):
        super().__init__(person)

    def decorate(self):
        print("一条卡其色休闲裤")


class BeltDecorator(ClothingDecorator):
    """腰带装饰器"""

    def __init__(self, person):
        super().__init__(person)

    def decorate(self):
        print("一条银色针扣头的黑色腰带")


class LeatherShoesDecorator(ClothingDecorator):
    """皮鞋类装饰器"""

    def __init__(self, person):
        super().__init__(person)

    def decorate(self):
        print("一件紫红色针织毛衣")


class KnittedSweaterDecorator(ClothingDecorator):
    """针织毛衣装饰器"""

    def __init__(self, person):
        super().__init__(person)

    def decorate(self):
        print("一件紫红色针织毛衣")


class WhiteShirtDecorate(ClothingDecorator):
    """白色衬衫装饰器"""

    def __init__(self, person):
        super().__init__(person)

    def decorate(self):
        print("一件白色衬衫")


class GlassesDecorator(ClothingDecorator):
    """眼镜装饰器"""

    def __init__(self, person):
        super().__init__(person)

    def decorate(self):
        print("一副方形黑框眼镜")


def test_decorator():
    tony = Engineer("Tony", "客户端")
    pant = CasualPantDecorator(tony)
    # belt = BeltDecorator(pant)
    # shoes = LeatherShoesDecorator(belt)
    # shirt = WhiteShirtDecorate(shoes)
    # sweater = KnittedSweaterDecorator(shirt)
    # glasses = GlassesDecorator(sweater)
    # glasses.wear()
    pant.wear()

    print()

    decorate_teacher = GlassesDecorator(WhiteShirtDecorate(LeatherShoesDecorator(Teacher("wells", "教授"))))
    decorate_teacher.wear()

test_decorator()