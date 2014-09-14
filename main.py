import pygame
from pygame import *
from entities import Player
from level import Level

LEVEL_W = 25
LEVEL_H = 15
BLOCK_SIZE = 40

DISPLAY = (BLOCK_SIZE*LEVEL_W, BLOCK_SIZE*LEVEL_H)
DEPTH = 32
FLAGS = 0

FPS = 60

# in blocks, 25 x 20

def main():
    pygame.init()
    screen = display.set_mode(DISPLAY, FLAGS, DEPTH)
    display.set_caption("Use arrows to move!")
    timer = time.Clock()

    up = down = left = right = space = False
    bg = Surface((BLOCK_SIZE, BLOCK_SIZE))
    bg.convert()
    bg.fill(Color("#000000"))

    current_level = Level(LEVEL_W, LEVEL_H)
    player = Player(100, 100)
    entities = pygame.sprite.Group()
    entities.add(player)

    while True:
        timer.tick(FPS)
        for e in pygame.event.get():
            if e.type == QUIT: raise SystemExit, "QUIT"
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit, "ESCAPE"
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_SPACE:
                space = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_SPACE:
                space = False

            if e.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print current_level._identify_img(pos[0]/BLOCK_SIZE, pos[1]/BLOCK_SIZE)

        # draw background
        for y in range(LEVEL_H):
            for x in range(LEVEL_W):
                screen.blit(bg, (x * BLOCK_SIZE, y * BLOCK_SIZE))

        # update player, draw everything else
        player.update(up, down, left, right, space, current_level)
        player.draw(screen)
        #entities.draw(screen)
        current_level.draw(screen)

        pygame.display.flip()





if (__name__ == "__main__"):
    main()