import copy
from Player import Player
from Qwirkle import GameBoard
from termcolor import colored


class Agent1(Player):

    def print_tiles(self, tiles):
        tiles_output = ''
        for tile in tiles:
            tiles_output += colored(tile.shape, tile.color) + ' '
        print('\n  Your Tiles: %s' % tiles_output)

    def argmax(self, list):
        return max(enumerate(list), key = lambda x: x[1][3])[0]

    def play_turn(self, board):
        self.print_tiles(self._tiles)

        validPlays = board.valid_plays()

        optionalPlays = []
        for x, y in validPlays:
            tiles = self._tiles.copy()

            for tile in tiles:
                boardCopy = GameBoard(board = board.get_board(), previous_board = board.get_prevoius_board(), plays = board.get_plays(), last_plays = board.get_last_plays())
                boardCopy.play(tile, x = x, y = y)
                potentialScore = boardCopy.score()
                optionalPlays.append((tile, x, y, potentialScore))

        if (len(optionalPlays) == 0):
            return

        bestPlay = max(optionalPlays, key = lambda x: x[3])
        tileToPlay = bestPlay[0]
        x = bestPlay[1]
        y = bestPlay[2]

        board.play(tileToPlay, x = x, y = y)
        self._tiles.pop(self._tiles.index(tileToPlay))

        return bestPlay[3]
