from argparse import ArgumentParser
from minesweeper import MineSweeper,Config

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--bombs', '-b', type=int, default=20)
    parser.add_argument('--cols', '-c', type=int, default=20)
    parser.add_argument('--rows', '-r', type=int, default=15)
    parser.add_argument('--cell', '-C', type=int, default=25)
    return parser.parse_args()

def main():
    args = parse_args()
    Config.BOMBS = args.bombs
    Config.COLS = args.cols
    Config.ROWS = args.rows
    Config.CELL = args.cell

    game = MineSweeper()
    game.main()

if __name__ == '__main__':
    main()
