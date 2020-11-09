import copy
from Player import Player
from Qwirkle import GameBoard
from termcolor import colored


class Agent3(Player):

    def print_tiles(self, tiles):
        tiles_output = ''
        for tile in tiles:
            tiles_output += colored(tile.shape, tile.color) + ' '
        print('\n  Your Tiles: %s' % tiles_output)

    def specialPrint(self, reorderedPlays):
        for seriesPlay in reorderedPlays:
            print(seriesPlay)
            print('')

    def reorderPlays(self, optionalPlays):
        result = []
        for optionalPlay in optionalPlays:
            score = 0
            currOptionalPlay = []
            for play in optionalPlay:
                score += play[3]
                currOptionalPlay.append((play[0], play[1], play[2]))
                result.append((score, currOptionalPlay))
        return result

    def play_turn(self, board):
        self.print_tiles(self._tiles)

        validPlays = board.valid_plays()

        optionalPlays = []
        for x, y in validPlays:
            tiles = self._tiles.copy()

            for tile in tiles:
                optionalPlay = []
                boardCopy = GameBoard(board = board.get_board(), previous_board = board.get_prevoius_board(), plays = board.get_plays(), last_plays = board.get_last_plays())
                if (boardCopy.play(tile, x = x, y = y)):
                    potentialScore = boardCopy.score()
                    optionalPlay.append((tile, x, y, potentialScore))
                    optionalPlays.append(optionalPlay.copy())

                    tiles2 = tiles.copy()
                    tiles2.pop(tiles2.index(tile))

                    for x2, y2 in boardCopy.valid_plays():
                        for tile2 in tiles2:
                            optionalPlay2 = optionalPlay.copy()
                            boardCopy2 = GameBoard(board = boardCopy.get_board(), previous_board = boardCopy.get_prevoius_board(), plays = boardCopy.get_plays(), last_plays = boardCopy.get_last_plays())
                            if (boardCopy2.play(tile2, x = x2, y = y2)):
                                potentialScore2 = boardCopy2.score()
                                optionalPlay2.append((tile2, x2, y2, potentialScore2))
                                optionalPlays.append(optionalPlay2)

                                tiles3 = tiles2.copy()
                                tiles3.pop(tiles3.index(tile2))

                                for x3, y3 in boardCopy2.valid_plays():
                                    for tile3 in tiles3:
                                        optionalPlay3 = optionalPlay2.copy()
                                        boardCopy3 = GameBoard(board = boardCopy2.get_board(), previous_board = boardCopy2.get_prevoius_board(), plays = boardCopy2.get_plays(), last_plays = boardCopy2.get_last_plays())
                                        if (boardCopy3.play(tile3, x = x3, y = y3)):
                                            potentialScore3 = boardCopy3.score()
                                            optionalPlay3.append((tile3, x3, y3, potentialScore3))
                                            optionalPlays.append(optionalPlay3)

        if (len(optionalPlays) == 0):
            return

        reorderedPlays = self.reorderPlays(optionalPlays)
        result = max(reorderedPlays, key = lambda x: x[0])
        bestPlays = result[1]
        for (tile, x, y) in bestPlays:
            board.play(tile, x = x, y = y)
            self._tiles.pop(self._tiles.index(tile))

        return result[0]
