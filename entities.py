import pygame.sprite
from os.path import join
from pygame import *

PLAYER_W = 40
PLAYER_H = 30

BLOCK_SIZE = 40

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.last_xvel = 0
        self.last_yvel = 0
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image = pygame.image.load(join('data', 'player', 'slime.png'))
        self.image = pygame.transform.scale(self.image, (PLAYER_W, PLAYER_H))
        self.image_rotated = pygame.transform.flip(self.image, True, False)
        self.image.convert()
        self.rect = Rect(x, y, PLAYER_W, PLAYER_H)
        self.can_use_space = True

    def update(self, up, down, left, right, space, level):
        platforms = level.get_platforms()
        if space and not self.onGround:
            if self.can_use_space:
                self.yvel -= 2
                self.can_use_space = False
        if up:
            # only jump if on the ground
            if self.onGround:
                self.yvel -= 7
        if down:
            pass
        if left:
            self.xvel = -5
        if right:
            self.xvel = 5
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 30: self.yvel = 30
        if not (left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False
        self.last_yvel = self.yvel
        self.collide(0, self.yvel, platforms)
        # do y-axis collisions
        if self.xvel != 0:
            self.last_xvel = self.xvel


    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    event.post(event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                    self.can_use_space = True
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel /= 2  # reduce speed on vertical hit

    def draw(self, screen):
        if self.last_xvel >= 0:
            screen.blit(self.image_rotated, self.rect)
        else:
            screen.blit(self.image, self.rect)



class Platform(Entity):
    def __init__(self, x, y, image):
        Entity.__init__(self)
        if image is None:
            self.image = Surface((BLOCK_SIZE, BLOCK_SIZE))
            self.image.fill(Color("#DDDDDD"))
        else:
            self.image = pygame.image.load(join('data', 'tiles', image))
            self.image = pygame.transform.scale(self.image, (BLOCK_SIZE, BLOCK_SIZE))

        self.rect = Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
        self.image.convert()

    def update(self):
        pass


class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y, None)
        self.image.fill(Color("#0033FF"))