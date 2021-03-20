# Rajouter dans les can move que l'on ne peut pas passer au dessus d'une pièce
# En passant taking piece with pawn not finished (comment updater l'attribut last_move_is_double
# Rajouter le changement du pion en autre piece
# Rajouter l'impossibilité du king de bouger si case menacée
# Plus généralement faire attnention aux moments où le roi est maté
# checker le castling -> Updater les has_moved attributes et castling_done etc...
# Rajouter fin du game
# Sauvegarder partie


class Color:
    GREEN = "\x1b[32m"
    WHITE = '\033[0m'
    RED = "\x1b[31m"


class Cell:
    def __init__(self, x, y, piece):
        self.x = x
        self.y = y
        self.piece = piece

    def set_piece(self, piece):
        self.piece = piece

    def get_piece(self):
        return self.piece

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def is_threatened(self, board, threaten_color): #change threaten_color par #white_threatened
        # Check Knights threatening
        for i, j in [(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            x_to_check = self.x + i
            y_to_check = self.y + j

            if x_to_check > 0 and x_to_check < 8 and y_to_check > 0 and y_to_check < 8:
                cell_to_check = board.get_cell(x_to_check, y_to_check)
                piece_to_check = cell_to_check.get_piece()

                if isinstance(piece_to_check, Knight):
                    if piece_to_check.is_white() != threaten_color:
                        return True

        # King + Rook + Queen
        for i, j in [(1, 0), (0, -1), (-1, 0), (0, -1)]:
            x_to_check = self.x + i
            y_to_check = self.y + j

            if x_to_check > 0 and x_to_check < 8 and y_to_check > 0 and y_to_check < 8:
                cell_to_check = board.get_cell(x_to_check, y_to_check)
                piece_to_check = cell_to_check.get_piece()

                if isinstance(piece_to_check, King) or isinstance(piece_to_check, Rook) or isinstance(piece_to_check, Queen):
                    if piece_to_check.is_white() != threaten_color:
                        return True

        # Rook + Queen
        keep_going = True
        x_to_check = self.x + 1
        y_to_check = self.y
        while x_to_check < 8 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, Rook) or isinstance(piece_to_check, Queen):
                keep_going = False
                if piece_to_check.is_white() != threaten_color:
                    return True
            elif piece_to_check is not None:
                keep_going = False
            x_to_check += 1

        keep_going = True
        x_to_check = self.x - 1
        y_to_check = self.y
        while x_to_check >= 0 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, Rook) or isinstance(piece_to_check, Queen):
                keep_going = False
                if piece_to_check.is_white() != threaten_color:
                    return True
            elif piece_to_check is not None:
                keep_going = False
            x_to_check -= 1

        keep_going = True
        x_to_check = self.x
        y_to_check = self.y + 1
        while y_to_check < 8 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, Rook) or isinstance(piece_to_check, Queen):
                keep_going = False
                if piece_to_check.is_white() != threaten_color:
                    return True
            elif piece_to_check is not None:
                keep_going = False
            y_to_check += 1

        keep_going = True
        x_to_check = self.x
        y_to_check = self.y - 1
        while y_to_check >= 0 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, Rook) or isinstance(piece_to_check, Queen):
                keep_going = False
                if piece_to_check.is_white() != threaten_color:
                    return True
            elif piece_to_check is not None:
                keep_going = False
            y_to_check -= 1

        # King + Queen + Bishop + Pawn
        for i, j in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            x_to_check = self.x + i
            y_to_check = self.y + j

            if x_to_check > 0 and x_to_check < 8 and y_to_check > 0 and y_to_check < 8:
                cell_to_check = board.get_cell(x_to_check, y_to_check)
                piece_to_check = cell_to_check.get_piece()

                if isinstance(piece_to_check, King) or isinstance(piece_to_check, Bishop) or isinstance(piece_to_check, Queen):
                    if piece_to_check.is_white() != threaten_color:
                        return True
                elif i > 0 and threaten_color and isinstance(piece_to_check, Pawn):
                    if piece_to_check.is_white() != threaten_color:
                        return True
                        return True
                elif i < 0 and not threaten_color and isinstance(piece_to_check, Pawn):
                    if piece_to_check.is_white() != threaten_color:
                        return True

        # Queen + Bishop
        keep_going = True
        x_to_check = self.x + 1
        y_to_check = self.y + 1
        while x_to_check < 8 and y_to_check < 8 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, Bishop) or isinstance(piece_to_check, Queen):
                keep_going = False
                if piece_to_check.is_white() != threaten_color:
                    return True
            elif piece_to_check is not None:
                keep_going = False
            x_to_check += 1
            y_to_check += 1

        keep_going = True
        x_to_check = self.x - 1
        y_to_check = self.y + 1
        while x_to_check >= 0 and y_to_check < 8 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, Bishop) or isinstance(piece_to_check, Queen):
                keep_going = False
                if piece_to_check.is_white() != threaten_color:
                    return True
            elif piece_to_check is not None:
                keep_going = False
            x_to_check -= 1
            y_to_check += 1

        keep_going = True
        x_to_check = self.x + 1
        y_to_check = self.y - 1
        while x_to_check < 8 and y_to_check >= 0 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, Bishop) or isinstance(piece_to_check, Queen):
                keep_going = False
                if piece_to_check.is_white() != threaten_color:
                    return True
            elif piece_to_check is not None:
                keep_going = False
            x_to_check -= 1
            y_to_check += 1

        keep_going = True
        x_to_check = self.x - 1
        y_to_check = self.y - 1
        while x_to_check >= 0 and y_to_check >= 0 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, Bishop) or isinstance(piece_to_check, Queen):
                keep_going = False
                if piece_to_check.is_white() != threaten_color:
                    return True
            elif piece_to_check is not None:
                keep_going = False
            x_to_check -= 1
            y_to_check -= 1

        return False


class Piece:

    def __init__(self, white):
        self.white = white
        self.killed = False

    def is_white(self):
        return self.white

    def is_killed(self):
        return self.killed

    def set_killed(self, killed):
        self.killed = killed

    def can_move(self, board, start, end):
        pass

    def get_str(self):
        return '     '

    def draw(self):
        value = self.get_str()
        if self.is_white():
            return Color.GREEN + value + Color.WHITE
        else:
            return Color.RED + value + Color.WHITE

class Pawn(Piece):

    def __init__(self, white):
        super().__init__(white)
        self.has_moved = False # if the pawn has yet been moved or not to keep ?
        self.last_move_is_double = False # check for en passant, if last move was a double tap

    def can_move(self, board, start, end):
        if end.get_piece() is not None:
            # check if there is not another piece of same color
            if end.get_piece().is_white() == self.is_white():
                return False
            else:
                # Pawn can only take an adversary piece in diagonal
                dx = end.get_x() - start.get_x()
                dy = end.get_y() - start.get_y()
                if dx == 1 and dy == 1:
                    return True

        else:
            dx = end.get_x() - start.get_x()
            dy = end.get_y() - start.get_y()

            if dx == 1 and dy == 0 and self.is_white():
                return True
            elif dx == -1 and dy == 0 and not self.is_white():
                return True

            # En passant taking piece
            else:
                if start.get_x() == 1 and dx == 2 and dy == 0 and self.is_white():
                    return True
                elif start.get_x() == 6 and dx == -2 and dy == 0 and not self.is_white():
                    return True
                else:
                    return False

    def get_str(self):
        return '  P  '


class Bishop(Piece):

    def __init__(self, white):
        super().__init__(white)

    def can_move(self, board, start, end):
        if end.get_piece() is not None:
            if end.get_piece().is_white() == self.is_white():
                return False
        dx = end.get_x() - start.get_x()
        dy = end.get_y() - start.get_y()
        print(dx, dy)
        if abs(dx) == abs(dy):
            return True
        else:
            return False

    def get_str(self):
        return '  B  '

class Rook(Piece):

    def __init__(self, white):
        super().__init__(white)
        self.has_moved = False

    def can_move(self, board, start, end):
        if end.get_piece() is not None:
            print('There is piece')
            if end.get_piece().is_white() == self.is_white():
                return False
        dx = end.get_x() - start.get_x()
        dy = end.get_y() - start.get_y()
        print(dx, dy)
        if dx == 0 or dy == 0:
            return True
        else:
            return False

    def get_str(self):
        return '  R  '

class Knight(Piece):

    def __init__(self, white):
        super().__init__(white)

    def can_move(self, board, start, end):
        if end.get_piece() is not None:
            if end.get_piece().is_white() == self.is_white():
                return False
        dx = start.get_x() - end.get_x()
        dy = start.get_y() - end.get_y()
        return abs(dx) * abs(dy) == 2

    def get_str(self):
        return '  T  '


class Queen(Piece):

    def __init__(self, white):
        super().__init__(white)

    def can_move(self, board, start, end):
        if end.get_piece() is not None:
            if end.get_piece().is_white() == self.is_white():
                return False
        dx = end.get_x() - start.get_x()
        dy = end.get_y() - start.get_y()
        if dx == 0 or dy == 0 or (abs(dx) == abs(dy)):
            return True
        else:
            return False

    def get_str(self):
        return '  Q  '


class King(Piece):

    def __init__(self, white):
        super().__init__(white)
        self.castling_done = False
        self.has_moved = False

    def set_castling_done(self, castling_done):
        self.castling_done = castling_done

    def can_move(self, board, start, end):
        if end.get_piece() is not None:
            if end.get_piece().is_white() == self.is_white():
                return False
        dx = end.get_x() - start.get_x()
        dy = end.get_y() - start.get_y()

        ### Check if not chess

        if abs(dx) < 2 and abs(dy) < 2:
            return True
        else:
            return False

    def get_str(self):
        return '  K  '


class Board:

    def __init__(self):
        self.board = self.reset_board()

    def get_cell(self, x, y):

        return self.board[x][y]

    def reset_board(self):
        board = []

        line = [Cell(0, 0, Rook(True)), Cell(0, 1, Knight(True)), Cell(0, 2, Bishop(True)), Cell(0, 3, Queen(True)),
                Cell(0, 4, King(True)), Cell(0, 5, Bishop(True)), Cell(0, 6, Knight(True)), Cell(0, 7, Rook(True))]
        board.append(line)

        line = []
        for i in range(8):
            line.append(Cell(1, i, Pawn(True)))
        board.append(line)

        for i in range(4):
            line = []
            for j in range(8):
                line.append(Cell(i+2, j, None))
            board.append(line)

        line = []
        for i in range(8):
            line.append(Cell(6, i, Pawn(False)))
        board.append(line)

        line = [Cell(7, 0, Rook(False)), Cell(7, 1, Knight(False)), Cell(7, 2, Bishop(False)), Cell(7, 3, Queen(False)),
                Cell(7, 4, King(False)), Cell(7, 5, Bishop(False)), Cell(7, 6, Knight(False)), Cell(7, 7, Rook(False))]
        board.append(line)
        return board

    def draw(self):
        print('    |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |')
        boarder_line = '+---+-----+-----+-----+-----+-----+-----+-----+-----+'
        print(boarder_line)
        for i in range(8):
            current_line = '  ' + str(i) + ' |'
            for j in range(8):
                cell = self.get_cell(i, j)
                if cell.get_piece() is None:
                    current_line += '     '
                else:
                    current_line += cell.get_piece().draw()
                current_line += '|'
            print(current_line)
            print(boarder_line)


class Player:
    def __init__(self, white_side):
        self.white_side = white_side

    def is_white_side(self):
        return self.white_side


class Move:
    def __init__(self, player, start, end):
        self.player = player
        self.start = start
        self.end = end
        self.moved_piece = start.get_piece()
        self.complementary_castling = None
        self.complementary_passant = None

    def set_moved_attribute(self):
        if hasattr(self.moved_piece, 'has_moved'):
            self.moved_piece.has_moved = True

    def set_castling_done(self):
        assert isinstance(self.moved_piece, King)
        self.moved_piece.castling_done = True


class Game:

    game_status = []

    def __init__(self):
        self.player1 = Player(True)
        self.player2 = Player(False)
        self.to_play_player = self.player1

        self.board = Board()
        self.status = 'ACTIVE'
        self.played_moves = []

    def is_finished(self):
        return self.status != 'ACTIVE'

    def move_from_coordinates(self, player, start_x, start_y, end_x, end_y):
        start_cell = self.board.get_cell(start_x, start_y)
        end_cell = self.board.get_cell(end_x, end_y)

        move = Move(player, start_cell, end_cell)

        return self.move(move, player)

    def move(self, move, player):
        moved_piece = move.moved_piece

        ### List of checks
        ### To change if castling or en passant move
        assert moved_piece is not None
        assert player == self.to_play_player
        assert moved_piece.is_white() == player.is_white_side()
        can_move = moved_piece.can_move(self.board, move.start, move.end)

        # En passant
        if isinstance(moved_piece, Pawn):
            if not can_move:
                crossed_cell = self.board.get_cell(move.end.get_x(), move.start.get_y())
                crossed_piece = crossed_cell.get_piece()
                if isinstance(crossed_piece(), Pawn):
                    if crossed_piece.last_move_is_double:
                        # Revoir comment on update cet attribut last_move_is_double
                        can_move = True

        ### castling & check if end cell is not threatened?
        if isinstance(moved_piece, King):
            if move.end.is_threatened(self.board, moved_piece.is_white()):
                raise ValueError('King cannot move to a threatened celle')
            # Move to King can_move method ?
            if not can_move:

                print('King moving, not threatened in new cell but cannot move toward it')

                if not moved_piece.castling_done and not moved_piece.has_moved and (move.end.y == 6 or move.end.y == 2):
                    if move.end.y == 6: # Roque vers la droite
                        rook_to_move = self.board.get_cell(move.start.x, 7).get_piece()
                        rook_starting_coordinates = (move.start.x, 7)
                        rook_ending_coordinates = (move.start.x, 5)
                        if isinstance(rook_to_move, Rook):
                            must_be_empty_cells = [self.board.get_cell(move.start.x, 5),
                                                   self.board.get_cell(move.start.x, 6)]
                            must_not_be_threatened_cells = [self.board.get_cell(move.start.x, 4),
                                                            self.board.get_cell(move.start.x, 5),
                                                            self.board.get_cell(move.start.x, 6)]

                    if move.end.y == 2:  # Roque vers la gauche
                        rook_to_move = self.board.get_cell(move.start.x, 0).get_piece()
                        rook_starting_coordinates = (move.start.x, 0)
                        rook_ending_coordinates = (move.start.x, 3)
                        if isinstance(rook_to_move, Rook):
                            must_be_empty_cells = [self.board.get_cell(move.start.x, 1),
                                                   self.board.get_cell(move.start.x, 2),
                                                   self.board.get_cell(move.start.x, 3)]
                            must_not_be_threatened_cells = [self.board.get_cell(move.start.x, 2),
                                                            self.board.get_cell(move.start.x, 3),
                                                            self.board.get_cell(move.start.x, 4)]

                    empty_cells_check = True
                    not_threatened_cells = True
                    for cll in must_be_empty_cells:
                        if cll.get_piece() is not None:
                            empty_cells_check = False
                    for cll in must_not_be_threatened_cells:
                        if cll.is_threatened(self.board, moved_piece.is_white()):
                            not_threatened_cells = False

                    conditions_to_castling = [not rook_to_move.has_moved, empty_cells_check, not_threatened_cells]
                    if all(conditions_to_castling):
                        move.complementary_castling = rook_to_move, \
                                                      self.board.get_cell(rook_starting_coordinates[0],
                                                                          rook_starting_coordinates[1]), \
                                                      self.board.get_cell(rook_ending_coordinates[0],
                                                                          rook_ending_coordinates[1])
                        can_move = True
                    else:
                        print('Conditions for castling:')
                        print('Rook has not moved:', rook_to_move.has_moved)
                        print('Cells in between empty:', empty_cells_check)
                        print('Cells in between not threatened:', not_threatened_cells)

                    # # check if rook has moved
                    # # check if cells empty
                    # # check if cells not threatened
                    # end_piece = move.end.get_piece()
                    # if isinstance(end_piece, Rook) and end_piece.is_white() == moved_piece.is_white():
                    #     if not end_piece.has_moved and not moved_piece.has_moved:
                    #         # Checker si les cellules ne sont pas menacées et sont vides
                    #         can_move = True
                    #         move.set_castling(True)

        # Check if piece can move
        assert can_move

        ### take piece ?
        destination_piece = move.end.get_piece()
        if destination_piece is not None:
            assert destination_piece.is_white() != player.is_white_side()
            destination_piece.set_killed(True)
            # move.set_killed_piece(detination_piece) ?

        self.played_moves.append(move)

        ### Move pieces
        move.end.set_piece(move.start.get_piece())
        move.start.set_piece(None)
        move.set_moved_attribute()

        ### Check for castling
        if move.complementary_castling is not None:
            print('Apparently castling move, working on moving the Rook')
            castling_rook, rook_start, rook_end = move.complementary_castling
            rook_end.set_piece(castling_rook)
            rook_start.set_piece(None)
            move.set_castling_done()


        ### Check Chess
            ### Recherche les deux rois et checker can_move?

        ### Change player
        if self.to_play_player == self.player1:
            self.to_play_player = self.player2
        else:
            self.to_play_player = self.player1

        self.board.draw()

