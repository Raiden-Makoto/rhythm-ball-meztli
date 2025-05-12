from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from panda3d.core import (
    WindowProperties, # For window title and properties
    Vec3, Vec4, # vector class for positions and velocities
    CollisionTraverser, # Manages collision detection
    CollisionHandlerEvent, # Handles collision events
    CollisionNode, # Node for collision solids
    CollisionSphere, # Spherical collision solid for the ball
    CollisionBox, # Box-shaped collision solid for paddle/bricks
    LPoint3 # 3D point, used for resetting the ball
)

from random import uniform, choice
from sys import stderr

class RhythmBall(ShowBase):
    def __init__(self):
        super().__init__()
        props = WindowProperties()
        props.setTitle('Elemental Breakout')
        self.win.requestProperties(props)
        self.disableMouse()
        self.camera.setPos(0, -20, 10)
        self.camera.lookAt(0, 0, 0)

        # --- Game State Variables ---
        # Ball starts moving straight (along negative Z) with no X velocity
        self.ball_speed = Vec3(0, -5, 0)

        # --- Brick Colors --- 
        self.element_colors = [
            (1.0, 100/255, 0.0, 1.0), # pyro
            (1.0, 188/255, 0.0, 1.0), # default
            (0.0, 235/255, 200/255, 1.0), # anemo
            (180/255, 240/255, 1.0, 1.0), # cryo
            (50/255, 175/255, 1.0, 1.0), # hydro
            (165/255, 0.0, 1.0, 1.0), # electro
            (1.0, 240/255, 0.0, 1.0), # geo
            (1.0, 1.0, 1.0, 1.0) # bass brick
        ]

        # --- Paddle ---
        self.paddle = loader.loadModel('models/box')
        self.paddle.reparentTo(render)
        self.paddle.setScale(3, 1, 0.5)
        self.paddle.setPos(0, 0, -5)
        self.paddle.setColor(0.0, 0.0, 0.0, 1)

        # --- Ball ---
        
