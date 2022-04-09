import pygame
from argparse import ArgumentParser
from pygame.locals import QUIT,KEYDOWN,K_ESCAPE
from minesweeper import MineSweeper,Board,Cell

def is_quit(event):
    if event.type == QUIT:
        return True
    if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            return True
    return False

def loop(game):
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if is_quit(event):
                return
            game.event(event)

        game.draw()
        game.counter += 1
        pygame.display.update()
        clock.tick(game.fps)

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--bombs', '-b', type=int, default=20)
    parser.add_argument('--cols', '-c', type=int, default=20)
    parser.add_argument('--rows', '-r', type=int, default=15)
    parser.add_argument('--cell', '-C', type=int, default=25)
    return parser.parse_args()

def main():
    args = parse_args()
    Board.BOMBS = args.bombs
    Board.COLS = args.cols
    Board.ROWS = args.rows
    Cell.SIZE = args.cell

    game = MineSweeper()
    loop(game)
    pygame.quit()

if __name__ == '__main__':
    main()
