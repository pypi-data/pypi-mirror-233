from ursina import Entity, Sequence, Func, Wait


class SpriteSheetAnimation(Entity):
    def __init__(self, texture, animation_clips, tileset_size=[4,1], fps=12, model='quad', autoplay=True, **kwargs):
        kwargs['model'] = model
        kwargs['texture'] = texture
        kwargs['tileset_size'] = tileset_size
        super().__init__(**kwargs)

        self.animation_clips = animation_clips # should be a dict
        self.current_animation = None

        for key, value in self.animation_clips.items():
            start_coord, end_coord = value
            s = Sequence(loop=True)
            s.name = key
            # print(s.name)

            for y in range(start_coord[1], end_coord[1]+1):
                for x in range(start_coord[0], end_coord[0]+1):
                    s.extend([
                        Func(setattr, self, 'tile_coordinate', (x,y)),
                        Wait(1/fps)
                    ])
            self.animation_clips[key] = s
            self.animations.append(s)
        print('-------------', self.animation_clips)


    def play_animation(self, animation_name):
        if not self.animation_clips:
            return

        [anim.pause() for anim in self.animation_clips.values()]
        self.current_animation = self.animation_clips[animation_name]

        # if restart:
        self.animation_clips[animation_name].start()
        # else:
        #     self.animation_clips[animation_name].resume()


    @property
    def state(self):
        return self.current_animation

    @state.setter
    def state(self, value):
        if not self.current_animation:
            self.play_animation(value)
            return

        if value != self.current_animation.name:
            print('set state to:', value, self.current_animation.name)
            self.play_animation(value)




if __name__ == '__main__':
    '''
    Sprite sheet coordinate system:
    (0,3) (1,3) (2,3) (3,3)
    (0,2) (1,2) (2,2) (3,2)
    (0,1) (1,1) (2,1) (3,1)
    (0,0) (1,0) (2,0) (3,0)
    '''
    from ursina import Ursina, held_keys, Vec2, time
    app = Ursina()
    class Player(Entity):
        def __init__(self):
            super().__init__()
            self.direction = Vec2(0,0)
            self.velocity = Vec2(0,0)

            self.model = 'quad'
            self.texture='arrow_right'

            self.graphics = SpriteSheetAnimation('example_spritesheet', tileset_size=(4,4), fps=6, animation_clips={
                'idle_up' : ((1,0), (1,0)),     # makes an animation from (0,0) to (0,0), a single frame
                'idle_right' : ((1,1), (1,1)),  # makes an animation from (0,0) to (0,0), a single frame
                'idle_left' : ((1,2), (1,2)),   # makes an animation from (0,0) to (0,0), a single frame
                'idle_down' : ((1,3), (1,3)),   # makes an animation from (0,0) to (0,0), a single frame
                'walk_up' : ((0,0), (3,0)),     # makes an animation from (0,0) to (3,0), the bottom row
                'walk_right' : ((0,1), (3,1)),
                'walk_left' : ((0,2), (3,2)),
                'walk_down' : ((0,3), (3,3)),
            },
            parent=self,
            )

        def input(self, key):
            if key == 'd':      self.velocity = Vec2(1,0)
            # elif key == 'd up':   self.velocity[0] = -held_keys['a']
            elif key == 'a':      self.velocity = Vec2(-1,0)
            # if key == 'a up':   self.velocity[0] = held_keys['d']
            elif key == 'w':      self.velocity = Vec2(0,1)
            if key == 'w up':   self.velocity = Vec2()
            elif key == 's':      self.velocity[1] = -1
            # if key == 's up':   self.velocity[1] = held_keys['w']

            # if held_keys['d'] or held_keys['a'] or held_keys['w'] or held_keys['s']:

            if key in 'wasd':
                self.prev_key = key

            elif key in ('d up', 'a up', 'w up', 's up'):
                self.velocity = Vec2(held_keys['d']-held_keys['a'], held_keys['w']-held_keys['s'])

            # if held_keys['d'] or held_keys['a']:    self.scale_x = self.velocity.x
            # if held_keys['w'] or held_keys['s']:    self.scale_y = self.velocity.y
            # if key in 'wasd':
            #     self.direction = {
            #         'w' : Vec2(0,1),
            #         'a' : Vec2(-1,0),
            #         'd' : Vec2(1,0),
            #         's' : Vec2(0,-1),
            #     }[key]
            # else:
            #     self.direction = Vec2(0,0)
            # if key == 'd':
            #     self.velocity = Vec2(1,0)
            #     # self.scale_x = self._original_scale_x
            # if key == 'd up':
            #     self.velocity = Vec2(-held_keys['a'], 0)
            #
            # if key == 'a':
            #     self.velocity = Vec2(-1, 0)
            #     # self.scale_x = -self._original_scale_x
            # if key == 'a up':
            #     self.velocity = Vec2(held_keys['d'], held_keys['s'])

            # if held_keys['d'] or held_keys['a']:
            #     self.scale_x = self._original_scale_x * self.velocity

        def update(self):
            # go to a specific animation while holding a key.
            # setting .state will not restart the animation like .play_animation would.
            # while this could be done with .play_animation in input, this way we can have
            # the animation code at the same place as the movement code, which would likely be in update.
            self.position += self.velocity * time.dt * 5
            # direction = ''.join([held_keys['w'],held_keys['a'],held_keys['s'], held_keys['d']])
            if held_keys['w']:
                self.graphics.state = 'walk_up'
            elif held_keys['s']:
                self.graphics.state = 'walk_down'
            elif held_keys['d']:
                self.graphics.state = 'walk_right'
            elif held_keys['a']:
                self.graphics.state = 'walk_left'

            # if not moving, go to an idle animation depending on which direction we're facing
            elif self.graphics.current_animation:
                if self.graphics.state.name == 'walk_up':
                    self.graphics.state = 'idle_up'
                elif self.graphics.state.name == 'walk_right':
                    self.graphics.state = 'idle_right'
                elif self.graphics.state.name == 'walk_left':
                    self.graphics.state = 'idle_left'
                elif self.graphics.state.name == 'walk_down':
                    self.graphics.state = 'idle_down'


        # elif key == 'w up':
        #     self.graphics.play_animation('idle')

    # print(self.graphics.animations['walk_up'].funcs)
    player = Player()
    e = Entity(model='quad', texture='example_spritesheet', x=-1)

    # print(self.graphics.animations)
    # from ursina import destroy
    # destroy(self.graphics)
    app.run()
