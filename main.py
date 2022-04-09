import pygame
from argparse import ArgumentParser
from pygame.locals import QUIT,KEYDOWN,K_ESCAPE
from minesweeper import MineSweeper

def is_quit(event):
    if event.type == QUIT:
        return True
    if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
            return True
    return False

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--mine', '-M', action='store_true')
    return parser.parse_args()

def loop(game):
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if is_quit(event):
                return
            game.event(event)

        game.loop()
        game.counter += 1
        pygame.display.update()
        clock.tick(game.fps)

def main():
    args = parse_args()
    game = MineSweeper()
    loop(game)
    pygame.quit()

if __name__ == '__main__':
    main()
