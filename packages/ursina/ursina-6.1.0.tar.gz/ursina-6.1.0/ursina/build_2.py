from ursina import *



app = Ursina()

for key, value in sys.modules.items():
    if hasattr(value, '__file__'):
        print(key, value.__file__)
print('----num modules:', len(sys.modules))
