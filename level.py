import pygame.sprite
from entities import Platform, ExitBlock
from random import randint

BLOCK_SIZE = 40

class Level:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.platforms = platforms = []
        self.entities = entities = pygame.sprite.Group()

        x = y = 0
        level_map = []
        level_map.append(list('P'*width))
        for y in range(height-2):
            level_map.append(list('P' + ' ' * (width - 2) + 'P'))
        level_map.append(list('P'*width))

        # Place Random Lines
        for block in range(20):
            rand_w = randint(1, width-2)
            rand_h = randint(1, height-2)
            max_w = min(width-rand_w-2, 10)
            for n in range(randint(0, max_w)):
                level_map[rand_h][rand_w] = "P"
                level_map[rand_h][rand_w+n] = "P"

        self.level_map = level_map
        # build the level
        for col in range(height):
            for row in range(width):
                block = level_map[col][row]
                if block == "P":
                    img = self._identify_img(row, col)
                    p = Platform(x, y, img)
                    platforms.append(p)
                    entities.add(p)
                if block == "E":
                    e = ExitBlock(x, y)
                    platforms.append(e)
                    entities.add(e)
                x += BLOCK_SIZE
            y += BLOCK_SIZE
            x = 0

    def draw(self, screen):
        self.entities.draw(screen)

    def get_platforms(self):
        return self.platforms

    def _title_at_pos(self, row, col):
        if row < 0 or row >= self.width or col < 0 or col >= self.height:
            return 'P'
        return self.level_map[col][row]

    def _identify_img(self, row, col):

        # Build a list with the adjacent blocks
        adj_pos = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        adjacent_map = ''
        for x,y in adj_pos:
            adjacent_map += self._title_at_pos(row + x, col + y)
        if adjacent_map[0] == 'P':
            return 'slice33_33.png'
        if adjacent_map == ' '*4:
            return 'slice01_01.png'
        if adjacent_map == ' P  ':
            return 'slice02_02.png'
        if adjacent_map[1] == 'P' and adjacent_map[3] == 'P' or adjacent_map == '  P ':
            return 'slice03_03.png'
        if adjacent_map in [' PP ', '  PP']:  # Top left and right corners
            return 'slice03_03.png'
        if adjacent_map == '   P':
            return 'slice04_04.png'
        else:
            return None
