#!/usr/bin/env python3

try:
    from src.game import Game
except (SyntaxError, ImportError) as error:
    from sys import version_info
    message = "{}: Game of Life requires python 3.6 or greater".format(error)
    assert version_info >= (3, 6), message


def main():
    game = Game()
    while True:
        game.new()
        game.run()


if __name__ == '__main__':
    main()
