import pygame
from game import Color,Game
from math import floor
from random import randint
from pygame.locals import MOUSEBUTTONDOWN

class Status:
    EMPTY = 0
    OPENED = 1<<0
    BOMB   = 1<<1

class Cell:
    SIZE = 50
    def __init__(self, board, x, y):
        self.board = board
        self.surface = board.game.surface
        self.status = Status.EMPTY
        self.x = x
        self.y = y
        self.rect = (self.x*Cell.SIZE, self.y*Cell.SIZE, Cell.SIZE, Cell.SIZE)

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
        if self.status & Status.OPENED:
            return
        self.status |= Status.OPENED
        if not self.status & Status.BOMB and self.bomb_neighbors() == 0:
            for neighbor in self.neighbors():
                neighbor.open()

    def bomb_neighbors(self):
        return len([cell for cell in self.neighbors() if cell.status & Status.BOMB])

    def draw(self):
        if self.status & Status.BOMB:
            pygame.draw.ellipse(self.surface, Color.YELLOW, self.rect)
        elif self.bomb_neighbors() > 0:
            font = pygame.font.SysFont(None, 36)
            num_image = font.render("{}".format(self.bomb_neighbors()), True, Color.YELLOW)
            self.surface.blit(num_image, (self.x*Cell.SIZE+10, self.y*Cell.SIZE+10))

        if not self.status & Status.OPENED:
            if not (self.board.lose and (self.status & Status.BOMB)):
            # if not self.status & Status.BOMB:
                pygame.draw.rect(self.surface, Color.LIGHT_GRAY, self.rect)

def randpos():
    return randint(0, Board.COLS-1), randint(0, Board.ROWS-1)

class Board:
    BOMBS = 20
    COLS = 20
    ROWS = 15
    CELLS = COLS*ROWS
    WIDTH = COLS*Cell.SIZE
    HEIGHT = ROWS*Cell.SIZE

    def __init__(self, game):
        self.game = game
        self.cells = [[Cell(self, x, y) for x in range(Board.COLS)] for y in range(Board.ROWS)]

        while self.count(Status.BOMB) < Board.BOMBS:
            self.cell(*randpos()).status = Status.BOMB

    @property
    def lose(self):
        return self.count(Status.BOMB|Status.OPENED) > 0
    
    @property
    def win(self):
        return self.count(Status.OPENED) == Board.CELLS-Board.BOMBS
    
    @property
    def in_game(self):
        return not self.lose and not self.win

    def cell(self, x, y):
        if 0 <= x < Board.COLS and 0 <= y < Board.ROWS:
            return self.cells[y][x]

    def count(self, status):
        count = 0
        for y in range(Board.ROWS):
            for x in range(Board.COLS):
                if self.cell(x, y).status == status:
                    count += 1
        return count

    def draw_grid(self):
        for index in range(0, Board.WIDTH, Cell.SIZE):
            pygame.draw.line(self.game.surface, Color.GRAY, (index, 0), (index, Board.HEIGHT))
        for index in range(0, Board.HEIGHT, Cell.SIZE):
            pygame.draw.line(self.game.surface, Color.GRAY, (0, index), (Board.WIDTH, index))

    def draw_message(self, message):
        font = pygame.font.SysFont(None, 72)
        render = font.render(message, True, Color.CYAN)
        rect = render.get_rect()
        rect.center = (Board.WIDTH/2, Board.HEIGHT/2)
        self.game.surface.blit(render, rect.topleft)

    def draw(self):
        self.game.surface.fill(Color.BLACK)
        for y in range(Board.ROWS):
            for x in range(Board.COLS):
                self.cell(x, y).draw()

        self.draw_grid()
        
        if self.win:
            self.draw_message("WIN")
        elif self.lose:
            self.draw_message("LOSE")

        self.game.debug("cells:{}/{} bombs:{}".format(self.count(Status.OPENED), self.count(Status.EMPTY)+self.count(Status.OPENED), self.count(Status.BOMB)), color=Color.WHITE)

def coordinate2pos(pos):
    return floor(pos[0]/Cell.SIZE), floor(pos[1]/Cell.SIZE)

class MineSweeper(Game):
    def __init__(self):
        super().__init__(Board.WIDTH, Board.HEIGHT, "MineSweeper", fps=10)
        self.board = Board(self)

    def event(self, event):
        if self.board.in_game:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = coordinate2pos(event.pos)
                print('({},{}) => ({},{})'.format(event.pos[0], event.pos[1], x, y))
                self.board.cell(x, y).open()

    def loop(self):
        self.board.draw()
