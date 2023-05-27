import numpy as np

from engine.move import Move


class Player:
    def __init__(self, white_side):
        self.white_side = white_side
        self.random_number = np.random.randint(0, 1000, 1)

    def __str__(self):
        return 'NormalPlayer%i' % self.random_number

    def is_white_side(self):
        return self.white_side

    def time_to_play(self, board):
        pass


class AIRandomPlayer(Player):

    def __str__(self):
        return 'AIRandomPlayer'

    def time_to_play(self, board):

        for i in np.random.permutation(8):
            for j in np.random.permutation(8):
                if board.get_cell(i, j).get_piece() is not None:
                    if board.get_cell(i, j).get_piece().is_white() == self.is_white_side():
                        selected_piece = board.get_cell(i, j).get_piece()
                        print('AI Selected Piece', selected_piece)
                        possible_moves = selected_piece.get_potential_moves(i, j)

                        verified_move = False
                        random_move = np.random.permutation(len(possible_moves))
                        index = 0
                        print('Verifying Moves,', len(possible_moves), 'Moves Possibles')
                        while not verified_move and index < len(random_move):
                            selected_move = possible_moves[random_move[index]]
                            selected_move = Move(self, board, board.get_cell(i, j),
                                                 board.get_cell(selected_move[0], selected_move[1]))
                            verified_move = selected_move.is_possible_move()
                            index += 1

                        if verified_move:
                            print('Move is verified, ')
                            return selected_move
        print('No moved found, aborting...')
