# Rajouter le changement du pion en autre piece (transformation obligée en reine pour l'instant
# Rajouter fin du game (king menacé (ou pris?) en fin de tour)

# Rajouter toutes les pièces vivantes et mortes dans un stack en attribut de game
# Etablir le check mate
# Sauvegarder état partie

import copy

from pyalapin.engine.move import Move
from pyalapin.player.player import Player, AIRandomPlayer
from pyalapin.player.ai_player import EasyAIPlayer
from pyalapin.player.my_player import MyPlayer
import pyalapin.engine.material as material


class Color(object):
    GREEN = "\x1b[32m"
    WHITE = "\033[0m"
    RED = "\x1b[31m"


class Cell(object):
    """
    Cell class representing a base element of a board.

    Attributes
    ----------
    x : int
        x coordinate of the cell on the board.
    y : int
        y coordinate of the cell on the board
    piece: material.Piece or None
        Piece that is on the cell (or None if no Piece is on the cell)
    """

    def __init__(self, x, y, piece):
        """Initialization of the cell.

        Parameters
        ----------
        x : int
            x coordinate of the cell on the board.
        y : int
            y coordinate of the cell on the board
        piece: material.Piece or None
            Piece that is on the cell (or None if no Piece is on the cell)
        """
        self.x = x
        self.y = y
        self.piece = piece
        if piece is not None:
            self.piece.x = x
            self.piece.y = y

    def __deepcopy__(self, memodict={}):
        """Method to create an uncorrelated clone of the cell.

        Returns
        -------
        Cell
            Exact copy of self.
        """
        copy_object = Cell(self.x, self.y, copy.deepcopy(self.piece))
        return copy_object

    def set_piece(self, piece):
        """Sets a Piece in the Cell.

        Parameters
        ----------
        piece: material.Piece
            Piece to set up on self.
        """
        self.piece = piece
        if piece is not None:
            self.piece.x = self.x
            self.piece.y = self.y

    def get_piece(self):
        """Method to access the piece on the Cell.

        Returns
        -------
        Piece
            Piece on the self.
        """
        return self.piece

    def get_x(self):
        """Method to acces Cell x coordinate.

        Returns
        -------
        int
            x-axis coordinate of self.
        """
        return self.x

    def get_y(self):
        """Method to acces Cell y coordinate.

        Returns
        -------
        int
            y-axis coordinate of self.
        """
        return self.y

    def is_threatened(
        self, board, threaten_color
    ):  # change threaten_color par #white_threatened
        """
        Method to check if the Cell is threatened by a given color.

        Parameters
        ----------
        board : Board
            Board to which self belongs to.
        threaten_color : str
            Color of that wants to know if cell is threatened by opponent.

        Returns
        -------
        bool
            Whether the celle is threatened or not.
        """
        # One way that could be more efficient would be to keep at every step the list of threatened cell by each piece
        # And update it at each move.

        # Check Knights threatening
        for i, j in [
            (2, 1),
            (-2, 1),
            (2, -1),
            (-2, -1),
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),
        ]:
            x_to_check = self.x + i
            y_to_check = self.y + j

            if 0 <= x_to_check < 8 and 0 <= y_to_check < 8:
                cell_to_check = board.get_cell(x_to_check, y_to_check)
                piece_to_check = cell_to_check.get_piece()

                if isinstance(piece_to_check, material.Knight):
                    if piece_to_check.is_white() != threaten_color:
                        return True

        # King + Rook + Queen
        # Checking direct surroundings
        for i, j in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
            x_to_check = self.x + i
            y_to_check = self.y + j
            if 0 <= x_to_check < 8 and 0 <= y_to_check < 8:
                cell_to_check = board.get_cell(x_to_check, y_to_check)
                piece_to_check = cell_to_check.get_piece()

                if (
                    isinstance(piece_to_check, material.King)
                    or isinstance(piece_to_check, material.Rook)
                    or isinstance(piece_to_check, material.Queen)
                ):
                    if piece_to_check.is_white() != threaten_color:
                        return True

                elif piece_to_check is None:
                    keep_going = True
                    x_to_check += i
                    y_to_check += j
                    while 0 <= x_to_check < 8 and 0 <= y_to_check < 8 and keep_going:
                        cell_to_check = board.get_cell(x_to_check, y_to_check)
                        piece_to_check = cell_to_check.get_piece()
                        if isinstance(piece_to_check, material.Rook) or isinstance(
                            piece_to_check, material.Queen
                        ):
                            keep_going = False
                            if piece_to_check.is_white() != threaten_color:
                                return True
                        elif piece_to_check is not None:
                            keep_going = False
                        else:
                            x_to_check += i
                            y_to_check += j

        """
        # Rook + Queen
        # Going further
        keep_going = True
        x_to_check = self.x + 2
        y_to_check = self.y
        while x_to_check < 8 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, material.Rook) or isinstance(
                piece_to_check, material.Queen
            ):
                keep_going = False
                if piece_to_check.is_white() != threaten_color:
                    return True
            elif piece_to_check is not None:
                keep_going = False
            x_to_check += 1

        keep_going = True
        x_to_check = self.x - 2
        y_to_check = self.y
        while x_to_check >= 0 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, material.Rook) or isinstance(
                piece_to_check, material.Queen
            ):
                keep_going = False
                if piece_to_check.is_white() != threaten_color:
                    return True
            elif piece_to_check is not None:
                keep_going = False
            x_to_check -= 1

        keep_going = True
        x_to_check = self.x
        y_to_check = self.y + 2
        while y_to_check < 8 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, material.Rook) or isinstance(
                piece_to_check, material.Queen
            ):
                keep_going = False
                if piece_to_check.is_white() != threaten_color:
                    return True
            elif piece_to_check is not None:
                keep_going = False
            y_to_check += 1

        keep_going = True
        x_to_check = self.x
        y_to_check = self.y - 2
        while y_to_check >= 0 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, material.Rook) or isinstance(
                piece_to_check, material.Queen
            ):
                keep_going = False
                if piece_to_check.is_white() != threaten_color:
                    return True
            elif piece_to_check is not None:
                keep_going = False
            y_to_check -= 1
        """

        # King + Queen + Bishop + Pawn
        # Checking direct surroundings
        for i, j in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            x_to_check = self.x + i
            y_to_check = self.y + j

            if 0 <= x_to_check < 8 and 0 <= y_to_check < 8:
                cell_to_check = board.get_cell(x_to_check, y_to_check)
                piece_to_check = cell_to_check.get_piece()

                if (
                    isinstance(piece_to_check, material.King)
                    or isinstance(piece_to_check, material.Bishop)
                    or isinstance(piece_to_check, material.Queen)
                ):
                    if piece_to_check.is_white() != threaten_color:
                        return True
                elif (
                    i > 0
                    and threaten_color
                    and isinstance(piece_to_check, material.Pawn)
                ):
                    if piece_to_check.is_white() != threaten_color:
                        return True
                elif (
                    i < 0
                    and not threaten_color
                    and isinstance(piece_to_check, material.Pawn)
                ):
                    if piece_to_check.is_white() != threaten_color:
                        return True

                elif piece_to_check is None:
                    keep_going = True
                    x_to_check += i
                    y_to_check += j
                    while 0 <= x_to_check < 8 and 0 <= y_to_check < 8 and keep_going:
                        cell_to_check = board.get_cell(x_to_check, y_to_check)
                        piece_to_check = cell_to_check.get_piece()

                        if isinstance(piece_to_check, material.Bishop) or isinstance(
                            piece_to_check, material.Queen
                        ):
                            keep_going = False
                            if piece_to_check.is_white() != threaten_color:
                                return True
                        elif piece_to_check is not None:
                            keep_going = False
                        x_to_check += i
                        y_to_check += j

        """
        # Queen + Bishop
        keep_going = True
        x_to_check = self.x + 2
        y_to_check = self.y + 2
        while x_to_check < 8 and y_to_check < 8 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, material.Bishop) or isinstance(
                piece_to_check, material.Queen
            ):
                keep_going = False
                if piece_to_check.is_white() != threaten_color:
                    return True
            elif piece_to_check is not None:
                keep_going = False
            x_to_check += 1
            y_to_check += 1

        keep_going = True
        x_to_check = self.x - 2
        y_to_check = self.y + 2
        while x_to_check >= 0 and y_to_check < 8 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, material.Bishop) or isinstance(
                piece_to_check, material.Queen
            ):
                keep_going = False
                if piece_to_check.is_white() != threaten_color:
                    return True
            elif piece_to_check is not None:
                keep_going = False
            x_to_check -= 1
            y_to_check += 1

        keep_going = True
        x_to_check = self.x + 2
        y_to_check = self.y - 2
        while x_to_check < 8 and y_to_check >= 0 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, material.Bishop) or isinstance(
                piece_to_check, material.Queen
            ):
                keep_going = False
                if piece_to_check.is_white() != threaten_color:
                    return True
            elif piece_to_check is not None:
                keep_going = False
            x_to_check += 1
            y_to_check -= 1

        keep_going = True
        x_to_check = self.x - 2
        y_to_check = self.y - 2
        while x_to_check >= 0 and y_to_check >= 0 and keep_going:
            cell_to_check = board.get_cell(x_to_check, y_to_check)
            piece_to_check = cell_to_check.get_piece()

            if isinstance(piece_to_check, material.Bishop) or isinstance(
                piece_to_check, material.Queen
            ):
                keep_going = False
                if piece_to_check.is_white() != threaten_color:
                    return True
            elif piece_to_check is not None:
                keep_going = False
            x_to_check -= 1
            y_to_check -= 1
        """

        return False


class Board(object):
    """
    Board class representing the chess board.

    Attributes
    ----------
    board : list of Cells
        Represents all cells of a chess board from x coordinates [0, 7] and y coordinates [0, 7]
    white_king : material.King
        King piece of white color.
    black_king : material.King
        King piece of black color.
    all_material: dict
        Dictionnary containing all the pieces on the board, killed and not killed.
    """

    def __init__(self, empty_init=False):
        """Initialization of the board.

        Parameters
        ----------
        empty_init: bool
            True if you want to start from an existing board.
        """
        if not empty_init:
            self.white_king, self.black_king, self.all_material = self._reset_board()

    def deepcopy(self, light=True):
        """Method to create an uncorrelated clone of the board.

        Returns
        -------
        Cell
            Exact copy of self.
        """
        copied_object = Board(empty_init=True)
        board = [[Cell(i, j, None) for j in range(8)] for i in range(8)]
        copied_object.board = board
        if light:
            copied_material = self.light_deep_copy_material()
        else:
            copied_material = self.deep_copy_material()

        assert (
            len(copied_material["black"]["alive"]["king"]) > 0
        ), "Black king is dead ?"
        assert (
            len(copied_material["white"]["alive"]["king"]) > 0
        ), "White king is dead ?"
        copied_object.white_king = copied_material["white"]["alive"]["king"][0]
        copied_object.black_king = copied_material["black"]["alive"]["king"][0]
        copied_object.all_material = copied_material

        for piece_list in copied_material["white"]["alive"].values():
            for piece in piece_list:
                copied_object.get_cell(piece.x, piece.y).set_piece(piece)
        for piece_list in copied_material["black"]["alive"].values():
            for piece in piece_list:
                copied_object.get_cell(piece.x, piece.y).set_piece(piece)

        return copied_object

    def light_deep_copy_material(self):
        """Method to create an uncorrelated clone of all the pieces on the board. Light version
        where only alive pieces are returned.

        Returns
        -------
        dict of Pieces
            Exact copy of self.all_material.
        """
        material = {
            "white": {
                "alive": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": [],
                },
                "killed": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": [],
                },
            },
            "black": {
                "alive": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": [],
                },
                "killed": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": [],
                },
            },
        }

        for color in ["white", "black"]:
            for status in ["alive"]:
                for piece_type in ["pawn", "knight", "bishop", "rook", "queen", "king"]:
                    for piece in self.all_material[color][status][piece_type]:
                        material[color][status][piece_type].append(
                            piece.piece_deepcopy()
                        )
        return material

    def deep_copy_material(self):
        """Method to create an uncorrelated clone of all the pieces on the board, killed and not killed.

        Returns
        -------
        dict of Pieces
            Exact copy of self.all_material.
        """
        material = {
            "white": {
                "alive": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": [],
                },
                "killed": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": [],
                },
            },
            "black": {
                "alive": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": [],
                },
                "killed": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": [],
                },
            },
        }

        for color in ["white", "black"]:
            for status in ["alive", "killed"]:
                for piece_type in ["pawn", "knight", "bishop", "rook", "queen", "king"]:
                    for piece in self.all_material[color][status][piece_type]:
                        material[color][status][piece_type].append(
                            piece.piece_deepcopy()
                        )
        return material

    def _deepcopy__(self, memodict={}):
        """Method to create an uncorrelated clone of the board.

        Returns
        -------
        Cell
            Exact copy of self.
        """
        copied_object = Board(empty_init=True)
        board = [[Cell(i, j, None) for j in range(8)] for i in range(8)]
        copied_object.board = board
        copied_material = self.deep_copy_material()

        white_king = copied_material["white"]["alive"]["king"][0]
        black_king = copied_material["black"]["alive"]["king"][0]
        copied_object.all_material = copied_material
        copied_object.white_king = white_king
        copied_object.black_king = black_king
        for piece_list in copied_material["white"]["alive"].values():
            for piece in piece_list:
                copied_object.get_cell(piece.x, piece.y).set_piece(piece)
        for piece_list in copied_material["black"]["alive"].values():
            for piece in piece_list:
                copied_object.get_cell(piece.x, piece.y).set_piece(piece)

        return copied_object

    def to_fen(self):
        """Method to generate a fen representation of the current state of the board

        Returns
        -------
        tuple of str
            fen representation and 'KQkq'
        """
        fen = ""
        for line in reversed(self.board):
            no_piece_count = 0
            for cell in line:
                piece = cell.get_piece()
                if piece is None:
                    no_piece_count += 1
                else:
                    if no_piece_count > 0:
                        fen += str(no_piece_count)
                        no_piece_count = 0
                    letter = piece.get_str().replace(" ", "")
                    # if piece.is_white():
                    #     letter = letter.lower()
                    fen += letter
            if no_piece_count > 0:
                fen += str(no_piece_count)
            fen += "/"
        return fen[:-1]

    def one_hot_encode(self, white_side=True):
        """Method to create a representation of the board with OneHot encode of the pieces.

        Parameters
        ----------
        white_sied : bool
            Whether we want to represent the board from the White side point of view or not. Point of view sees its pieces
            represented by +1 OneHot and opponent side by -1.

        Returns
        -------
        list of list
            8x8 list representing the board with full zeros list when cell is empty or OneHot representation of the piece on
            the cell otherwise.
        """

        # Dict of OneHot transformations
        material_to_one_hot = {
            "pawn": [1, 0, 0, 0, 0, 0],
            "bishop": [0, 1, 0, 0, 0, 0],
            "knight": [0, 0, 1, 0, 0, 0],
            "rook": [0, 0, 0, 1, 0, 0],
            "queen": [0, 0, 0, 0, 1, 0],
            "king": [0, 0, 0, 0, 0, 1],
        }
        # Iterating over cells and add OneHot representations to the list.
        one_hot_board = []
        for line in self.board:
            one_hot_line = []
            for cell in line:
                piece = cell.get_piece()
                # Empty cell
                if piece is None:
                    one_hot_line.append([0] * 6)
                # Piece on the cell
                else:
                    one_hot_piece = material_to_one_hot[piece.type]
                    # Negative OneHot if opponent side
                    if piece.is_white() != white_side:
                        one_hot_piece = [-1 * val for val in one_hot_piece]
                    one_hot_line.append(one_hot_piece)
            one_hot_board.append(one_hot_line)
        return one_hot_board

    def get_cell(self, x, y):
        """Method to access a cell on the board from its coordinates.

        Parameters
        ----------
        x : int
            x-coordinate of the cell.
        y : int
            y-coordinate of the cell.

        Returns
        -------
        cell
            Cell at coordinates (x, y)
        """
        return self.board[x][y]

    def reset(self):
        """
        Resets the board, all the pieces, everything.
        """
        self.white_king, self.black_king, self.all_material = self._reset_board()

    def create_board_from_string(self, string):
        """
        Method to set up a sepecific board with Pieces on specific Celss from a string.
        """
        raise NotImplementedError

    def _reset_board(self):
        """Method to create the board. Creates Pieces and place them on their original cells.

        Returns
        -------
        material.King
            White King on the board
        material.King
            black King on the board
        dict
            Dictionnary with all the board pieces
        """
        # List of cells
        board = []

        # Dictionnary to access easily the pieces
        pieces = {
            "white": {
                "alive": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": [],
                },
                "killed": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": [],
                },
            },
            "black": {
                "alive": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": [],
                },
                "killed": {
                    "pawn": [],
                    "knight": [],
                    "bishop": [],
                    "rook": [],
                    "queen": [],
                    "king": [],
                },
            },
        }

        # Initialize white pieces
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

        line = [
            Cell(0, 0, w_rook_1),
            Cell(0, 1, w_knight_1),
            Cell(0, 2, w_bishop_1),
            Cell(0, 3, w_queen),
            Cell(0, 4, white_king),
            Cell(0, 5, w_bishop_2),
            Cell(0, 6, w_knight_2),
            Cell(0, 7, w_rook_2),
        ]
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
                line.append(Cell(i + 2, j, None))
            board.append(line)

        line = []
        for i in range(8):
            p = material.Pawn(False, 6, i)
            pieces["black"]["alive"]["pawn"].append(p)
            line.append(Cell(6, i, p))
        board.append(line)

        # Initialize black pieces
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

        line = [
            Cell(7, 0, b_rook_1),
            Cell(7, 1, b_knight_1),
            Cell(7, 2, b_bishop_1),
            Cell(7, 3, b_queen),
            Cell(7, 4, black_king),
            Cell(7, 5, b_bishop_2),
            Cell(7, 6, b_knight_2),
            Cell(7, 7, b_rook_2),
        ]
        board.append(line)

        self.board = board
        return white_king, black_king, pieces

    def move_piece_from_coordinates(self, start_coordinates, end_coordinates):
        """Method to move a piece on the board from start and landing coordinates.

        Parameters
        ----------
        start_coordinates : tuple of int
            (x, y) coordinates of move starting cell
        end_coordinates : tuple of int
            (x, y) coordinates of move landing cell
        """
        start_cell = self.get_cell(start_coordinates[0], start_coordinates[1])
        end_cell = self.get_cell(end_coordinates[0], end_coordinates[1])
        piece_to_move = start_cell.get_piece()
        if piece_to_move is None:
            raise ValueError("Empty cells chosen as moved piece")

        end_cell.set_piece(piece_to_move)
        start_cell.set_piece(None)

    def kill_piece_from_coordinates(self, coordinates):
        """Method to kill a piece from its coordinates on the board.

        Parameters
        ----------
        coordinates : tuple of ints
            (x, y) coordinates of cell on which is the piece to kill
        """
        to_kill_piece = self.get_cell(coordinates[0], coordinates[1]).get_piece()
        to_kill_piece.set_killed()

        color = "white" if to_kill_piece.is_white() else "black"
        self.all_material[color]["alive"][to_kill_piece.type].remove(to_kill_piece)
        self.all_material[color]["killed"][to_kill_piece.type].append(to_kill_piece)

    def transform_pawn(self, coordinates):
        """Method to promote a pawn from its coordinates.

        Parameters
        ----------
        coordinates : tuple of ints
            (x, y) coordinates of the cell on which is Pawn to promote
        promote_into : str
            type of piece to promote the Pawn into. Default is "Queen" can also be "Rool", "Bishop" and "Knigh"
        """
        pawn = self.get_cell(coordinates[0], coordinates[1]).get_piece()
        if not isinstance(pawn, material.Pawn):
            raise ValueError("Transforming piece that is not a Pawn")
        else:
            color = "white" if pawn.is_white() else "black"
            self.all_material[color]["alive"][pawn.type].remove(pawn)

            new_queen = material.Queen(pawn.is_white(), pawn.x, pawn.y)
            self.get_cell(pawn.x, pawn.y).set_piece(new_queen)
            self.all_material[color]["alive"]["queen"].append(new_queen)

    def promote_pawn(self, coordinates, promote_into="Queen"):
        """Method to promote a pawn from its coordinates.

        Parameters
        ----------
        coordinates : tuple of ints
            (x, y) coordinates of the cell on which is Pawn to promote
        promote_into : str
            type of piece to promote the Pawn into. Default is "Queen" can also be "Rool", "Bishop" and "Knigh"
        """
        pawn = self.get_cell(coordinates[0], coordinates[1]).get_piece()
        if not isinstance(pawn, material.Pawn):
            raise ValueError("Transforming piece that is not a Pawn")
        else:
            color = "white" if pawn.is_white() else "black"
            self.all_material[color]["alive"][pawn.type].remove(pawn)

            new_piece = pawn.promote(promote_into=promote_into)
            self.get_cell(pawn.x, pawn.y).set_piece(new_piece)
            self.all_material[color]["alive"]["queen"].append(new_piece)

    def draw(self, printing=True):
        """Method to draw the board as a string and potentially print it in the terminal.

        Parameters
        ----------
        printing : bool
            Whether or not to print it in the terminal
        """
        whole_text = "    |  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |"
        boarder_line = "+---+-----+-----+-----+-----+-----+-----+-----+-----+"
        whole_text += "\n"
        whole_text += boarder_line
        for i in range(8):
            current_line = "  " + str(i) + " |"
            for j in range(8):
                cell = self.get_cell(i, j)
                if cell.get_piece() is None:
                    current_line += "     "
                else:
                    current_line += cell.get_piece().draw()
                current_line += "|"
            whole_text += "\n"
            whole_text += current_line
            whole_text += "\n"
            whole_text += boarder_line
        whole_text += "\n"
        whole_text += "    |  a  |  b  |  c  |  d  |  e  |  f  |  g  |  h  |"

        whole_text += "\n"
        whole_text += boarder_line
        if printing:
            print(whole_text + "\n")
        return whole_text


class ChessGame(object):
    """
    Game class, used to play a chess game, interact with the board and move pieces.

    Attributes
    ----------
    player1 : player.Player
        player object that will be the one to play white pieces. For now, has to be a human player
    ai : bool
        Whether or not to play with AI. Is set to True, AI will play black pieces.
    player2 : player.Player
        player object that will play the black pieces. Can be human or AI player.
    to_player_player: player1 or player2
        Argument pointing to the player that has to play next. Initialized to white pieces player.
    board: Board
        Board object on which to play.
    status: str
        String indicating if the game is still active or if there is mat or pat.
    played_moves: list
        List storing all the played move during the game.
    automatic draw: bool
        Whether to draw the board in the terminal at each round.
    save_pgn: bool
        Whether to keep track of the moves with PGN.
    history: list of str
        PGN representation of the past move of the game.
    """

    game_status = []

    def __init__(
        self, player1=None, player2=None, automatic_draw=True, ai=False, save_pgn=False
    ):
        """Initialization of the cell.

        Parameters
        ----------
        automatic_draw : bool
            Whether to draw the board in the terminal at each round.
        ai : bool
            Whether or not to play with AI. Is set to True, AI will play black pieces.
        """

        # If ai = True and both players are None, AI plays by default black pieces
        if player2 is None:
            if ai:
                self.player2 = EasyAIPlayer(False)
            else:
                self.player2 = Player(False)

            if player1 is None:
                self.player1 = Player(True)
            else:
                self.player1 = player1

        elif player1 is None:
            if ai:
                self.player1 = EasyAIPlayer(True)
            else:
                self.player1 = Player(True)
            self.player2 = player2
        else:
            self.player1 = player1
            self.player2 = player2

        self.ai = ai
        self.to_play_player = self.player1

        self.board = Board()
        self.status = "ACTIVE"
        self.played_moves = []
        self.save_pgn = save_pgn
        if self.save_pgn:
            self.history = []

        self.automatic_draw = automatic_draw
        self.half_move_clock = 0

    def reset_game(self):
        """Method to reset the game. Recreates the borad, the pieces and restarts the game."""
        self.board.reset()
        self.played_moves = []
        self.history = []
        self.to_play_player = self.player1
        self.half_move_clock = 0

    def to_fen(self):
        """
        Writes the board in fen.

        Returns
        -------
        str
            fen representation of the board.
        """
        board_fen = self.board.to_fen()
        color_playing = "w" if self.to_play_player.is_white_side() else "b"
        castling = self.is_castling_possible(True) + self.is_castling_possible(False)
        full_moves_nb = len(self.played_moves) // 2 + 1
        return f"{board_fen} {color_playing} {castling} {self.fen_en_passant()} {full_moves_nb} {self.half_move_clock}"

    def is_castling_possible(self, is_white_player):
        """Creates FEN representation of possible castling

        Parameters
        ----------
        is_white_player: bool
            If castling possible checked for white player

        Returns
        -------
        str:
            FEN representation of possible castling
        """

        fen_possible_castling = ""
        if is_white_player:
            piece = self.board.get_cell(0, 4).get_piece()
            if not isinstance(piece, material.King):
                return ""
            elif piece.has_moved or piece.castling_done:
                return ""
            else:
                kingside_rook = self.board.get_cell(0, 7).get_piece()
                if isinstance(kingside_rook, material.Rook):
                    if not kingside_rook.has_moved:
                        fen_possible_castling += "K"
                queenside_rook = self.board.get_cell(0, 0).get_piece()
                if isinstance(kingside_rook, material.Rook):
                    if not kingside_rook.has_moved:
                        fen_possible_castling += "Q"
        else:
            piece = self.board.get_cell(0, 4).get_piece()
            if not isinstance(piece, material.King):
                return ""
            elif piece.has_moved or piece.castling_done:
                return ""
            else:
                kingside_rook = self.board.get_cell(7, 7).get_piece()
                if isinstance(kingside_rook, material.Rook):
                    if not kingside_rook.has_moved:
                        fen_possible_castling += "k"
                queenside_rook = self.board.get_cell(7, 0).get_piece()
                if isinstance(kingside_rook, material.Rook):
                    if not kingside_rook.has_moved:
                        fen_possible_castling += "q"
        return fen_possible_castling

    def fen_en_passant(self):
        """
        Creates the part of the FEN representation about En Passant.

        Returns
        -------
        str
            '-' or coordinate of en-passant cell if last move was double
        """
        try:
            last_move = self.played_moves[-1]
        except:
            return "-"
        if not isinstance(last_move.move_piece, material.Pawn):
            return "-"

        dx = last_move.start.get_x() - last_move.end.get_x()
        x_cell = 8 - int(last_move.start.get_x() - last_move.end.get_x()) / 2
        y_cell = ["a", "b", "c", "d", "e", "f", "g", "h"][last_move.start.get_y()]

        if dx == 2:
            return f"{y_cell}{x_cell}"
        else:
            return "-"

    def is_finished(self):
        """
        Method to know if the game is still active or finished (i.e. pat or mat)

        Returns
        -------
        bool
            Whether the game is finished or not.
        """
        return self.status != "ACTIVE"

    def move_from_coordinates(self, player, start_x, start_y, end_x, end_y, extras={}):
        """
        Method to move a piece on the board from its coordinates. Creates the Move object from the coordinates and
        calls the .move() method.

        Parameters
        ----------
        player: player.Player
            player that wants to move a piece
        start_x: int
            x-coordinate of the piece to move
        start_y: int
            y-coordinate of the piece to move
        end_x: int
            x-coordinate of the cell to move the piece to
        end_y: int
            x-coordinate of the cell to move the piece to
        extras: dict
            Dictionnary used to add additional data such as which type a piece a Pawn should be promoted to
            if it reaches the other side of the board.

        Returns
        -------
        self.move()
            Method move of self.
        """
        # Get the cells from the coordinates
        start_cell = self.board.get_cell(start_x, start_y)
        end_cell = self.board.get_cell(end_x, end_y)

        # Create the Move object
        move = Move(player, self.board, start_cell, end_cell, extras=extras)

        # Move
        return self.move(move, player)

    def draw_board(self):
        """
        Draw the game's borad as a string in the terminal.
        """
        return self.board.draw()

    def can_player_move(self, player):
        """
        Methods that verifies if a player can still move at least one piece.

        Parameters
        ----------
        player: player.Player
            player we want to check can still move at least one Piece.

        Returns
        -------
        bool
            Whether player can still move at least a piece.
        """
        # Checks all cells
        for i in range(8):
            for j in range(8):
                # Checks Pieces on cells
                selected_piece = self.board.get_cell(i, j).get_piece()
                if selected_piece is not None:
                    # Checks color of pices
                    if selected_piece.is_white() == player.is_white_side():
                        # Checks if piece can move
                        possible_moves = selected_piece.get_potential_moves(i, j)

                        # Verifies if the move is authorized
                        for k in range(len(possible_moves)):
                            selected_move = possible_moves[k]
                            selected_move = Move(
                                player,
                                self.board,
                                self.board.get_cell(i, j),
                                self.board.get_cell(selected_move[0], selected_move[1]),
                            )
                            verified_move = selected_move.is_possible_move()

                            if verified_move:
                                return True
        return False

    def check_pat_mat(self, player):
        """
        Method to check if a player is in PAT or MAT situation.

        Parameters
        ----------
        player: player.Player
            player that needs to be checked

        Returns
        -------
        int
            0 if the player can move, 1 if PAT, 2 if MAT
        """
        can_player_move = self.can_player_move(player)

        if can_player_move:
            if self.half_move_clock >= 50:
                return 1
            return 0
        # If player cannot move any piece
        else:
            if player.is_white_side():
                king = self.board.white_king
            else:
                king = self.board.black_king
            # If King is threatened, is mat otherwise, is pat
            is_mat = self.board.get_cell(king.x, king.y).is_threatened(
                self.board, not player.is_white_side
            )
            if is_mat:
                return 2
            else:
                return 1

    def move(self, move, player):
        """
        Method to move a piece on the board from player and move objects.

        Parameters
        ----------
        move: move.Move
            move object ready to move a piece.
        player: player.Player
            player that wants to move a piece.

        Returns
        -------
        bool
            Whether the move has happened or not (if not means that it has been blocked by a rule). & Whether the
            game keeps going. (Actually False when not moving should be True)
        int or str
            Status of the game: 0 nothing has happened or no winner, winner otherwise
        """
        moved_piece = move.moved_piece

        # List of checks
        # To change if castling or en passant move
        if moved_piece is None:
            return False, 0
        assert moved_piece is not None

        # Check that right player is playing
        if player != self.to_play_player:
            return False, 0
        assert player == self.to_play_player

        # Check that the move is authorized
        allowed_move = move.is_possible_move()
        if not allowed_move:
            return False, 0
        elif moved_piece.is_white() != player.is_white_side():
            return False, 0
        else:
            assert moved_piece.is_white() == player.is_white_side()
            # Actually move pieces
            reset_half_move_clock = move.move_pieces()
            if reset_half_move_clock:
                self.half_move_clock = 0
            else:
                self.half_move_clock += 1

        # Store move
        self.played_moves.append(move)
        if self.save_pgn:
            self.history.append(move.to_pgn())

        # Change player
        if self.to_play_player == self.player1:
            self.to_play_player = self.player2
        else:
            self.to_play_player = self.player1

        # Draw
        if self.automatic_draw:
            self.board.draw()

        # Check status of Kings
        if self.board.white_king.is_killed():
            print("END OF THE GAME, BLACK HAS WON")
            return False, "black"
        elif self.board.black_king.is_killed():
            print("END OF THE GAME, WHITE HAS WON")
            return False, "white"

        # Checking for PAT & MAT
        check_status, winner = self.update_status()

        return check_status, winner

    def update_status(self):
        """
        Checks the status of the game (on going, pat, mat) and returns it.

        Returns
        -------
        bool
            Whether the game keeps going or not.
        int or str
            Status of the game: 0 nothing has happened or no winner, winner otherwise

        """
        game_status = self.check_pat_mat(self.player1)
        self.game_status.append(game_status)
        # Pat
        if game_status == 1:
            return False, "black&white"
        # Mat
        elif game_status == 2:
            return False, "black"
        else:
            game_status = self.check_pat_mat(self.player2)
            # Pat
            if game_status == 1:
                return False, "black&white"
            # Mat
            elif game_status == 2:
                return False, "white"
            # Keeps going
            else:
                return True, ""

    def save(self, directory="debug_files"):
        """
        Method to save the state of the game as matplotlib figure.
        Uses a str representation of the game moves as figure title.

        Parameters
        ----------
        directory: str
            directory in which to save the figure.
        """
        draw_text = self.draw_board()
        draw_text = draw_text.replace("\x1b[32m", "")
        draw_text = draw_text.replace("\033[0m", "")
        draw_text = draw_text.replace("\x1b[31m", "")
        import os
        import matplotlib.pyplot as plt

        """
        plt.rc("figure", figsize=(12, 7))
        plt.text(
            0.01, 0.05, str(draw_text), {"fontsize": 10}, fontproperties="monospace"
        )
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(os.path.join(directory, str(len(self.played_moves)) + ".png"))
        """
        with open(
            os.path.join(directory, str(len(self.played_moves)) + ".txt"), "w"
        ) as f:
            f.writelines(draw_text)

    def to_pgn(self):
        assert self.save_pgn
        pgn = ""
        for i in range(len(self.history)):
            if i % 2 == 0:
                pgn += f"{int(i/2)+1}. "
            pgn += self.history[i]
            pgn += " "

        return pgn[:-1]
