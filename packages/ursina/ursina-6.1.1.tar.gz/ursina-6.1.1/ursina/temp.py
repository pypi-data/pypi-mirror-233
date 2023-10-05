from main import *

app = Ursina()

from entity import *
from vec3 import Vec3
import color
from color import Color
from collider import Collider, BoxCollider
import time
from time import dt
from panda3d.bullet import BulletWorld, BulletBoxShape, BulletPlaneShape
from prefabs.editor_camera import EditorCamera

world = BulletWorld()
world.setGravity(Vec3(0, -9.81, 0))

cube = Entity(model = 'cube', physics_world = world, collider = 'box', y = 10, color = color.red)
#print(cube.physics_world)
#print(cube.collider)

ground = Entity(model = 'cube', physics_world = world, collider = 'box', position = (0, -5, 0), scale = (25, .1, 25), color = color.blue)

def update():
    dt = time.dt
    world.doPhysics(dt)

EditorCamera()

app.run()
