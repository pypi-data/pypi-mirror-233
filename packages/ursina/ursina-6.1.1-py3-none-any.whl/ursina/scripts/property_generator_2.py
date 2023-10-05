from functools import wraps

def generate_properties_for_class(getter_suffix='_getter', setter_suffix='_setter', deleter_suffix='_deleter'):
    def decorator(cls):
        getters = {}
        setters = {}
        deleters = {}

        for name in dir(cls):
            if name.endswith(getter_suffix):
                getters[name[:-len(getter_suffix)]] = getattr(cls, name)

            if name.endswith(setter_suffix):
                setters[name[:-len(setter_suffix)]] = getattr(cls, name)

            if name.endswith(deleter_suffix):
                deleters[name[:-len(deleter_suffix)]] = getattr(cls, name)

            # print('---------------has func', attribute, attribute_value)

        for name, value in getters.items():
            getter = getters.get(name, None)
            setter = setters.get(name, None)
            deleter = deleters.get(name, None)

            if not getter:
                def default_getter(self):
                    return getattr(self, f'_{name}')
                getter = default_getter

            if not setter:
                def default_setter(self, value):
                    setattr(self, f'_{name}', value)
                setter = default_setter

            if not deleter:
                def default_deleter(self):
                    delattr(self, f'_{name}')
                deleter = default_deleter

            setattr(cls, name, property(getter, setter, deleter))

        return cls
    return decorator



if __name__ == '__main__':
    from ursina import *
    # def getter(func):
    #     print(func)
    #
    class Z:
        pass

    @generate_properties_for_class(getter_suffix='_getter', setter_suffix='_setter')
    class A(Entity):
        def x_getter(self):
            print('get orignal x')
            return self._x

        def x_setter(self, value):
            self._x = value
            print('A setter side effect')


    # @generate_properties_for_class()
    class B(A):
        def __init__(self):
            super().__init__()

        pass
        # def x_setter(self, value):
        #     super().x_setter(value) # enables you to use getters and setters with inheritance while keeping the parent class's behavior
        #     print('B setter side effect')
        # @Property
        # def x(self):
        #     print('aa')
        #
        # @x.setter
        # def x(self, value):
        #     setattr(super(), 'x', value)
        #     print('-----', )



    # how you'd do it wouth the property generator, using __getattr__ and __setattr__
    # class B(A):
    #     def __setattr__(self, name, value):
    #         super().__setattr__(name, value)
    #
    #         if name == 'x':
    #             print('custom x stuff!')


    print(A.x)
    e = B()
    e.x = 2
    print('xxxxxxxx', e.x)

    from ursina import *

    app = Ursina()
    b = Button(on_click=application.quit)

    app.run()
    # del e.x
