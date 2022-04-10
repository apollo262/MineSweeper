import pygame
from game import Color,Game
from math import floor
from random import randint
from pygame.locals import MOUSEBUTTONDOWN,MOUSEBUTTONUP,Rect
from pygame.locals import KEYDOWN,K_r,K_d

class Status:
    EMPTY = 0
    OPEN = 1<<0
    BOMB = 1<<1
    FLAG = 1<<2

class Cell:
    SIZE = 50

    def __init__(self, board, x, y):
        self.board = board
        self.status = Status.EMPTY
        self.x = x
        self.y = y
        self.rect = Rect(self.x*Cell.SIZE, self.y*Cell.SIZE, Cell.SIZE, Cell.SIZE)

    def __str__(self):
        return '({},{}) status:{}'.format(self.x, self.y, self.status)

    def neighbors(self):
        neighbors = []
        for y in range(-1, 2):
            for x in range(-1, 2):
                cell = self.board.cell(self.x+x, self.y+y)
                if cell is not None and cell != self:
                    neighbors.append(cell)
        return neighbors

    def __eq__(self, cell):
        return self.x == cell.x and self.y == cell.y

    def __ne__(self, cell):
        return not self.__eq__(cell)

    def open(self):
        if self.status & Status.OPEN:
            return
        self.status |= Status.OPEN
        if not self.status & Status.BOMB and self.bomb_neighbors() == 0:
            for neighbor in self.neighbors():
                neighbor.open()

    def flag(self):
        self.status ^= Status.FLAG

    def bomb_neighbors(self):
        return len([cell for cell in self.neighbors() if cell.status & Status.BOMB])

    def inflate(self, rate):
        if rate > 1:
            return self.rect.inflate(Cell.SIZE*(rate-1), Cell.SIZE*(rate-1))
        elif rate < 1:
            return self.rect.inflate(-(Cell.SIZE*rate), -(Cell.SIZE*rate))

    def draw_bomb(self, screen):
        pygame.draw.ellipse(screen, Color.RED, self.inflate(0.5))

    def draw_number(self, screen):
        font = pygame.font.SysFont(None, int(Cell.SIZE))
        text = font.render("{}".format(self.bomb_neighbors()), True, Color.YELLOW)
        rect = text.get_rect(center=(self.rect.centerx, self.rect.centery))
        screen.blit(text, rect)

    def draw_cover(self, screen):
        pygame.draw.rect(screen, Color.LIGHT_GRAY, self.rect)
        for cell in self.board.select:
            if cell == self:
                pygame.draw.rect(screen, Color.DARK_GRAY, self.rect)

    def draw_flag(self, screen):
        pygame.draw.ellipse(screen, Color.BLUE, self.inflate(0.5))

    def draw(self):
        screen = self.board.game.screen

        if self.status & Status.BOMB:
            self.draw_bomb(screen)
        elif self.bomb_neighbors() > 0:
            self.draw_number(screen)

        if not self.status & Status.OPEN:
            if not (self.board.lose and (self.status & Status.BOMB)):
                if not self.board.debug:
                    self.draw_cover(screen)
                if self.status & Status.FLAG:
                    self.draw_flag(screen)

def randpos():
    return randint(0, Board.COLS-1), randint(0, Board.ROWS-1)

class Board:
    BOMBS = 20
    COLS = 20
    ROWS = 15

    def __init__(self, game):
        self.game = game
        self.debug = False
        self.reset()
        self.select = []
    
    def reset(self):
        self.cells = [[Cell(self, x, y) for x in range(Board.COLS)] for y in range(Board.ROWS)]
        while self.count(Status.BOMB, op='&') < Board.BOMBS:
            self.cell(*randpos()).status |= Status.BOMB

    @property
    def lose(self):
        return self.count(Status.BOMB|Status.OPEN) > 0

    @property
    def win(self):
        return self.count(Status.OPEN, op='&') == (Board.COLS*Board.ROWS)-Board.BOMBS

    @property
    def in_game(self):
        return not self.lose and not self.win

    def cell(self, x, y):
        if 0 <= x < Board.COLS and 0 <= y < Board.ROWS:
            return self.cells[y][x]

    def count(self, status, op='=='):
        count = 0
        for y in range(Board.ROWS):
            for x in range(Board.COLS):
                if status is None:
                    match = True
                elif op == '==':
                    match = self.cell(x, y).status == status
                elif op == '&':
                    match = self.cell(x, y).status & status
                if match:
                    count += 1
        return count

    def draw_grid(self):
        for index in range(0, MineSweeper.WIDTH, Cell.SIZE):
            pygame.draw.line(self.game.screen, Color.GRAY, (index, 0), (index, MineSweeper.HEIGHT))
        for index in range(0, MineSweeper.HEIGHT, Cell.SIZE):
            pygame.draw.line(self.game.screen, Color.GRAY, (0, index), (MineSweeper.WIDTH, index))

    def draw_message(self, message):
        font = pygame.font.SysFont(None, int(Cell.SIZE*4))
        text = font.render(message, True, Color.CYAN)
        rect = text.get_rect()
        rect.center = (MineSweeper.WIDTH/2, MineSweeper.HEIGHT/2)
        self.game.screen.blit(text, rect.topleft)

    def draw(self):
        self.game.screen.fill(Color.BLACK)
        for y in range(Board.ROWS):
            for x in range(Board.COLS):
                self.cell(x, y).draw()

        self.draw_grid()

        if self.win:
            self.draw_message("WIN")
        elif self.lose:
            self.draw_message("LOSE")

        self.game.debug("cells:{}/{} bombs:{}".format(
            self.count(Status.OPEN, op='&'), self.count(None), self.count(Status.BOMB, op='&')),color=Color.WHITE)

class MineSweeper(Game):
    WIDTH = None
    HEIGHT = None

    @classmethod
    def update(cls):
        cls.WIDTH = Board.COLS*Cell.SIZE
        cls.HEIGHT = Board.ROWS*Cell.SIZE

    def __init__(self):
        MineSweeper.update()
        super().__init__(MineSweeper.WIDTH, MineSweeper.HEIGHT, "MineSweeper", fps=60)
        self.board = Board(self)

    def pos2cell(self, pos):
        x,y = floor(pos[0]/Cell.SIZE), floor(pos[1]/Cell.SIZE)
        # print('({},{}) => ({},{})'.format(pos[0], pos[1], x, y))
        return self.board.cell(x, y)

    def event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_r:
                self.board.reset()
            elif event.key == K_d:
                self.board.debug = not self.board.debug

        if self.board.in_game:
            if event.type == MOUSEBUTTONUP:
                cell = self.pos2cell(event.pos)
                if event.button == 1:
                    cell.open()
                elif event.button == 3:
                    cell.flag()

    def get_select(self):
        select = []
        if pygame.mouse.get_pressed()[0] == 1:
            select.append(self.pos2cell(pygame.mouse.get_pos()))
        if pygame.mouse.get_pressed() == (1, 0, 1):
            select += self.pos2cell(pygame.mouse.get_pos()).neighbors()
        return select

    def draw(self):
        if self.board.in_game:
            self.board.select = self.get_select()

        self.board.draw()
