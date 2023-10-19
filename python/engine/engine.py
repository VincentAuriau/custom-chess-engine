# Rajouter le changement du pion en autre piece (transformation obligée en reine pour l'instant
# Rajouter fin du game (king menacé (ou pris?) en fin de tour)

# Rajouter toutes les pièces vivantes et mortes dans un stack en attribut de game
# Etablir le check mate
# Sauvegarder état partie

import copy

from engine.move import Move
from player.player import Player, AIRandomPlayer
from player.ai_player import EasyAIPlayer
from player.my_player import MyPlayer
import engine.material as material


class Color:
    GREEN = "\x1b[32m"
    WHITE = '\033[0m'
    RED = "\x1b[31m"


class Cell:
    def __init__(self, x, y, piece):
        self.x = x
        self.y = y
        self.piece = piece
        if piece is not None:
            self.piece.x = x
            self.piece.y = y

    def __deepcopy__(self, memodict={}):
        copy_object = Cell(self.x, self.y, copy.deepcopy(self.piece))
        return copy_object

    def set_piece(self, piece):
        self.piece = piece
        if piece is not None:
            self.piece.x = self.x
            self.piece.y = self.y


    def get_piece(self):
        return self.piece

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def is_threatened(self, board, threaten_color):  # change threaten_color par #white_threatened
        # Check Knights threatening
        for i, j in [(2, 1), (-2, 1), (2, -1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            x_to_check = self.x + i
            y_to_check = self.y + j

            if 0 < x_to_check < 8 and 0 < y_to_check < 8:
                cell_to_check = board.get_cell(x_to_check, y_to_check)
                piece_to_check = cell_to_check.get_piece()

                if isinstance(piece_to_check, material.Knight):
                    if piece_to_check.is_white() != threaten_color:
                        return True

        # King + Rook + Queen
        for i, j in [(1, 0), (0, -1), (-1, 0), (0, -1)]:
            x_to_check = self.x + i
            y_to_check = self.y + j

            if 0 < x_to_check < 8 and 0 < y_to_check < 8:
                cell_to_check = board.get_cell(x_to_check, y_to_check)
                piece_to_check = cell_to_check.get_piece()

                if isinstance(piece_to_check, material.King) or isinstance(piece_to_check, material.Rook) or isinstance(piece_to_check,
                                                                                                                        material.Queen):
                    if piece_to_check.is_white() != threaten_color:
                        return True

        # Rook + Queen
        keep_going = True
        x_to_check = self.x + 1
        y_to_check = self.y
        while x_to_check < 8 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, material.Rook) or isinstance(piece_to_check, material.Queen):
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

            if isinstance(piece_to_check, material.Rook) or isinstance(piece_to_check, material.Queen):
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

            if isinstance(piece_to_check, material.Rook) or isinstance(piece_to_check, material.Queen):
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

            if isinstance(piece_to_check, material.Rook) or isinstance(piece_to_check, material.Queen):
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

            if 0 < x_to_check < 8 and 0 < y_to_check < 8:
                cell_to_check = board.get_cell(x_to_check, y_to_check)
                piece_to_check = cell_to_check.get_piece()

                if isinstance(piece_to_check, material.King) or isinstance(piece_to_check, material.Bishop) or isinstance(piece_to_check,
                                                                                                                 material.Queen):
                    if piece_to_check.is_white() != threaten_color:
                        return True
                elif i > 0 and threaten_color and isinstance(piece_to_check, material.Pawn):
                    if piece_to_check.is_white() != threaten_color:
                        return True
                elif i < 0 and not threaten_color and isinstance(piece_to_check, material.Pawn):
                    if piece_to_check.is_white() != threaten_color:
                        return True

        # Queen + Bishop
        keep_going = True
        x_to_check = self.x + 1
        y_to_check = self.y + 1
        while x_to_check < 8 and y_to_check < 8 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, material.Bishop) or isinstance(piece_to_check, material.Queen):
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

            if isinstance(piece_to_check, material.Bishop) or isinstance(piece_to_check, material.Queen):
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

            if isinstance(piece_to_check, material.Bishop) or isinstance(piece_to_check, material.Queen):
                keep_going = False
                if piece_to_check.is_white() != threaten_color:
                    return True
            elif piece_to_check is not None:
                keep_going = False
            x_to_check += 1
            y_to_check -= 1

        keep_going = True
        x_to_check = self.x - 1
        y_to_check = self.y - 1
        while x_to_check >= 0 and y_to_check >= 0 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, material.Bishop) or isinstance(piece_to_check, material.Queen):
                keep_going = False
                if piece_to_check.is_white() != threaten_color:
                    return True
            elif piece_to_check is not None:
                keep_going = False
            x_to_check -= 1
            y_to_check -= 1

        return False


class Board:

    def __init__(self, empty_init=False):
        if not empty_init:
            self.board = None
            self.white_king, self.black_king, self.all_material = self._reset_board()

    def deepcopy(self, memodict={}):
        copied_object = Board(empty_init=True)
        board = [[Cell(i, j, None) for j in range(8)] for i in range(8)]
        copied_object.board = board
        copied_material = self.deep_copy_material()
        white_king = copied_material['white']['alive']['king'][0]
        black_king = copied_material['black']['alive']['king'][0]
        copied_object.all_material = copied_material
        copied_object.white_king = white_king
        copied_object.black_king = black_king
        for piece_list in copied_material['white']['alive'].values():
            for piece in piece_list:
                copied_object.get_cell(piece.x, piece.y).set_piece(piece)
        for piece_list in copied_material['black']['alive'].values():
            for piece in piece_list:
                copied_object.get_cell(piece.x, piece.y).set_piece(piece)

        return copied_object

    def deep_copy_material(self):
        material = {
            "white": {
                "alive": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": []
                },
                "killed": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": []
                }
            },
            "black": {
                "alive": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": []
                },
                "killed": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": []
                }
            }
        }

        for color in ['white', 'black']:
            for status in ['alive', 'killed']:
                for piece_type in ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']:
                    for piece in self.all_material[color][status][piece_type]:
                        material[color][status][piece_type].append(piece.piece_deepcopy())
        return material

    def __deepcopy__(self, memodict={}):
        copied_object = Board(empty_init=True)
        board = [[Cell(i, j, None) for j in range(8)] for i in range(8)]
        copied_object.board = board
        copied_material = self.deep_copy_material()

        white_king = copied_material['white']['alive']['king'][0]
        black_king = copied_material['black']['alive']['king'][0]
        copied_object.all_material = copied_material
        copied_object.white_king = white_king
        copied_object.black_king = black_king
        for piece_list in copied_material['white']['alive'].values():
            for piece in piece_list:
                copied_object.get_cell(piece.x, piece.y).set_piece(piece)
        for piece_list in copied_material['black']['alive'].values():
            for piece in piece_list:
                copied_object.get_cell(piece.x, piece.y).set_piece(piece)

        return copied_object

    def to_fen(self):
        fen = ""
        for line in self.board:
            no_piece_count = 0
            for cell in line:
                piece = cell.get_piece()
                if piece is None:
                    no_piece_count += 1
                else:
                    if no_piece_count > 0:
                        fen += str(no_piece_count)
                        no_piece_count = 0
                    letter = piece.get_str().replace(' ', '')
                    if piece.is_white():
                        letter = letter.lower()
                    fen += letter
            if no_piece_count > 0:
                fen += str(no_piece_count)
            fen += "/"
        return fen[:-1], "KQkq"

    def one_hot_encode(self, white_side=True):
        material_to_one_hot = {
            "pawn": [1, 0, 0, 0, 0, 0],
            "bishop": [0, 1, 0, 0, 0, 0],
            "knight": [0, 0, 1, 0, 0, 0],
            "rook": [0, 0, 0, 1, 0, 0],
            "queen": [0, 0, 0, 0, 1, 0],
            "king": [0, 0, 0, 0, 0, 1]
        }
        one_hot_board = []
        for line in self.board:
            one_hot_line = []
            for cell in line:
                piece = cell.get_piece()
                if piece is None:
                    one_hot_line.append([0]*6)
                else:
                    one_hot_piece = material_to_one_hot[piece.type]
                    if piece.is_white() != white_side:
                        one_hot_piece = [-1*val for val in one_hot_piece]
                    one_hot_line.append(one_hot_piece)
            one_hot_board.append(one_hot_line)
        return one_hot_board

    def get_cell(self, x, y):
        return self.board[x][y]

    def copy(self):
        return self.deepcopy()

    def reset(self):
        self.white_king, self.black_king, self.all_material = self._reset_board()

    def create_board_from_string(self, string):
        return None

    def _reset_board(self):
        board = []

        pieces = {
            "white": {
                "alive": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": []
                },
                "killed": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": []
                }
            },
            "black": {
                "alive": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": []
                },
                "killed": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": []
                }
            }
        }

        white_king = material.King(True, 0, 4)
        pieces["white"]["alive"]["king"].append(white_king)
        black_king = material.King(False, 7, 4)
        pieces["black"]["alive"]["king"].append(black_king)

        w_rook_1 = material.Rook(True, 0, 0)
        w_rook_2 = material.Rook(True, 0, 7)
        pieces["white"]["alive"]["rook"].append(w_rook_1)
        pieces["white"]["alive"]["rook"].append(w_rook_2)

        w_bishop_1 = material.Bishop(True, 0, 2)
        w_bishop_2 = material.Bishop(True, 0, 5)
        pieces["white"]["alive"]["bishop"].append(w_bishop_1)
        pieces["white"]["alive"]["bishop"].append(w_bishop_2)

        w_knight_1 = material.Knight(True, 0, 1)
        w_knight_2 = material.Knight(True, 0, 6)
        pieces["white"]["alive"]["knight"].append(w_knight_1)
        pieces["white"]["alive"]["knight"].append(w_knight_2)

        w_queen = material.Queen(True, 0, 3)
        pieces["white"]["alive"]["queen"].append(w_queen)

        line = [Cell(0, 0, w_rook_1), Cell(0, 1, w_knight_1), Cell(0, 2, w_bishop_1),
                Cell(0, 3, w_queen), Cell(0, 4, white_king), Cell(0, 5, w_bishop_2),
                Cell(0, 6, w_knight_2), Cell(0, 7, w_rook_2)]
        board.append(line)

        line = []
        for i in range(8):
            p = material.Pawn(True, 1, i)
            pieces["white"]["alive"]["pawn"].append(p)
            line.append(Cell(1, i, p))
        board.append(line)

        for i in range(4):
            line = []
            for j in range(8):
                line.append(Cell(i+2, j, None))
            board.append(line)

        line = []
        for i in range(8):
            p = material.Pawn(False, 6, i)
            pieces["black"]["alive"]["pawn"].append(p)
            line.append(Cell(6, i, p))
        board.append(line)

        b_rook_1 = material.Rook(False, 7, 0)
        b_rook_2 = material.Rook(False, 7, 7)
        pieces["black"]["alive"]["rook"].append(b_rook_1)
        pieces["black"]["alive"]["rook"].append(b_rook_2)

        b_bishop_1 = material.Bishop(False, 7, 2)
        b_bishop_2 = material.Bishop(False, 7, 5)
        pieces["black"]["alive"]["bishop"].append(b_bishop_1)
        pieces["black"]["alive"]["bishop"].append(b_bishop_2)

        b_knight_1 = material.Knight(False, 7, 1)
        b_knight_2 = material.Knight(False, 7, 6)
        pieces["black"]["alive"]["knight"].append(b_knight_1)
        pieces["black"]["alive"]["knight"].append(b_knight_2)

        b_queen = material.Queen(False, 7, 3)
        pieces["black"]["alive"]["queen"].append(b_queen)

        line = [Cell(7, 0, b_rook_1), Cell(7, 1, b_knight_1), Cell(7, 2, b_bishop_1),
                Cell(7, 3, b_queen), Cell(7, 4, black_king), Cell(7, 5, b_bishop_2),
                Cell(7, 6, b_knight_2), Cell(7, 7, b_rook_2)]
        board.append(line)

        self.board = board
        return white_king, black_king, pieces

    def move_piece_from_coordinates(self, start_coordinates, end_coordinates):
        start_cell = self.get_cell(start_coordinates[0], start_coordinates[1])
        end_cell = self.get_cell(end_coordinates[0], end_coordinates[1])
        piece_to_move = start_cell.get_piece()
        if piece_to_move is None:
            ###print(start_coordinates, end_coordinates)
            ###print(start_cell, start_cell.piece)
            raise ValueError("Empty cells chosen as moved piece")

        end_cell.set_piece(piece_to_move)
        start_cell.set_piece(None)

    def kill_piece_from_coordinates(self, coordinates):
        to_kill_piece = self.get_cell(coordinates[0], coordinates[1]).get_piece()
        to_kill_piece.set_killed()

        color = "white" if to_kill_piece.is_white() else "black"
        ###print(color)
        ###print(self.all_material[color]['alive'])
        ###print(self.all_material[color]["alive"][to_kill_piece.type])
        ###print(to_kill_piece)
        ###print(to_kill_piece.type)
        self.all_material[color]["alive"][to_kill_piece.type].remove(to_kill_piece)
        self.all_material[color]["killed"][to_kill_piece.type].append(to_kill_piece)

    def transform_pawn(self, coordinates):
        pawn = self.get_cell(coordinates[0], coordinates[1]).get_piece()
        if not isinstance(pawn, material.Pawn):
            ###print(pawn)
            raise ValueError("Transforming piece that is not a Pawn")
        else:
            color = "white" if pawn.is_white() else "black"
            self.all_material[color]["alive"][pawn.type].remove(pawn)

            new_queen = material.Queen(pawn.is_white(), pawn.x, pawn.y)
            self.get_cell(pawn.x, pawn.y).set_piece(new_queen)
            self.all_material[color]["alive"]["queen"].append(new_queen)

    def draw(self, printing=True):
        whole_text = '    |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |'
        # ###print('    |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |')
        boarder_line = '+---+-----+-----+-----+-----+-----+-----+-----+-----+'
        # ###print(boarder_line)
        whole_text += '\n'
        whole_text += boarder_line
        for i in range(8):
            current_line = '  ' + str(i) + ' |'
            for j in range(8):
                cell = self.get_cell(i, j)
                if cell.get_piece() is None:
                    current_line += '     '
                else:
                    current_line += cell.get_piece().draw()
                current_line += '|'
            whole_text += '\n'
            # ###print(current_line)
            whole_text += current_line
            # ###print(boarder_line)
            whole_text += '\n'
            whole_text += boarder_line
        print(whole_text)
        return whole_text


class Game:

    game_status = []

    def __init__(self, automatic_draw=True, ai=False):
        self.player1 = Player(True)
        self.ai = ai
        if ai:
            # self.player2 = AIRandomPlayer(False)
            self.player2 = EasyAIPlayer(False)
            # self.player2 = MyPlayer(white_side=False, path_to_model="./test1")
        else:
            self.player2 = Player(False)
        self.to_play_player = self.player1

        self.board = Board()
        self.status = 'ACTIVE'
        self.played_moves = []

        self.automatic_draw = automatic_draw

    def reset_game(self):
        self.board.reset()
        self.played_moves = []
        self.to_play_player = self.player1

    def to_fen(self):
        pieces, castling = self.board.to_fen()
        color_playing = 'w' if self.to_play_player.is_white_side() else "b"
        return pieces + " " + color_playing + " " + castling + " - 0 1"

    def is_finished(self):
        return self.status != 'ACTIVE'

    def move_from_coordinates(self, player, start_x, start_y, end_x, end_y):
        start_cell = self.board.get_cell(start_x, start_y)
        end_cell = self.board.get_cell(end_x, end_y)

        move = Move(player, self.board, start_cell, end_cell)

        return self.move(move, player)

    def draw_board(self):
        return self.board.draw()

    def can_player_move(self, player):
        ###print('CHECK IF PLAYER CAN MOVE')
        for i in range(8):
            for j in range(8):
                selected_piece = self.board.get_cell(i, j).get_piece()
                if selected_piece is not None:
                    if selected_piece.is_white() == player.is_white_side():

                        possible_moves = selected_piece.get_potential_moves(i, j)
                        for k in range(len(possible_moves)):
                            selected_move = possible_moves[k]
                            selected_move = Move(player, self.board, self.board.get_cell(i, j),
                                                 self.board.get_cell(selected_move[0], selected_move[1]))
                            verified_move = selected_move.is_possible_move()

                            if verified_move:
                                ###print('==== CHECK FINISHED ====')
                                return True
        ###print('==== CHECK FINISHED ====')
        return False

    def check_pat_mat(self, player):
        can_player_move = self.can_player_move(player)

        if can_player_move:
            return 0
        else:
            if player.is_white_side():
                king = self.board.white_king
            else:
                king = self.board.black_king
            is_mat = self.board.get_cell(king.x, king.y).is_threatened(self.board, not player.is_white_side)
            if is_mat:
                return 2
            else:
                return 1

    def move(self, move, player):

        moved_piece = move.moved_piece

        # List of checks
        # To change if castling or en passant move
        if moved_piece is None:
            ###print('There is no moved piece, move is aborted')
            return False, 0
        assert moved_piece is not None

        if player != self.to_play_player:
            ###print('The wrong player has played, move is aborted')
            ###print(self.to_play_player, 'supposed to play and', player, 'has played')
            return False, 0
        assert player == self.to_play_player

        allowed_move = move.is_possible_move()
        if not allowed_move:
            ###print('Move method checking legality of move rejected it')
            return False, 0
        elif moved_piece.is_white() != player.is_white_side():
            ###print("Engine detected player to move other side piece")
            return False, 0

        else:
            assert moved_piece.is_white() == player.is_white_side()
            move.move_pieces()

        self.played_moves.append(move)

        # Change player
        if self.to_play_player == self.player1:
            self.to_play_player = self.player2
        else:
            self.to_play_player = self.player1

        if self.automatic_draw:
            self.board.draw()
        # self.save()
        if self.board.white_king.is_killed():
            print('END OF THE GAME, BLACK HAS WON')
            return False, 'black'
        elif self.board.black_king.is_killed():
            print('END OF THE GAME, WHITE HAS WON')
            return False, 'white'

        ###print('PLAYER TO PLAY:', self.to_play_player)

        # Checking for PAT & MAT
        check_status, winner = self.update_status()

        return check_status, winner

    def update_status(self):
        game_status = self.check_pat_mat(self.player1)
        if game_status == 1:
            ###print('PAT, white & black do not differentiate each other')
            return False, 'black&white'
        elif game_status == 2:
            ###print('END OF THE GAME, MAT DETECTED, BLACK HAS WON')
            return False, 'black'
        else:
            game_status = self.check_pat_mat(self.player2)
            if game_status == 1:
                ###print('PAT, white & black do not differentiate each other')
                return False, 'black&white'
            elif game_status == 2:
                ###print('END OF THE GAME, MAT DETECTED WHITE HAS WON')
                return False, 'white'
            else:
                ###print('Game keeps going')
                return True, ''

    def save(self, directory='debug_files'):
        draw_text = self.draw_board()
        draw_text = draw_text.replace("\x1b[32m", "")
        draw_text = draw_text.replace('\033[0m', "")
        draw_text = draw_text.replace("\x1b[31m", "")
        import os
        import matplotlib.pyplot as plt
        plt.rc('figure', figsize=(12, 7))
        plt.text(0.01, 0.05, str(draw_text), {"fontsize": 10}, fontproperties='monospace')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(os.path.join(directory, str(len(self.played_moves))+'.png'))
