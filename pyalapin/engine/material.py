from abc import abstractmethod

from pyalapin.engine.color import Color


class Piece(object):
    """Base class for the different materials on the board.

    Implements the properties, attributes and functions shared by all the different materials.

    Attributes
    ----------
    white : bool
        Whether the piece is white or black.
    x : int
        x coordinate of piece on board
    y : int
        y coordinate of piece on board
    killed: bool
        Whether the piece has been killed by opponent or not. Initialized as False

    """

    def __init__(self, white, x, y):
        """Initialization of the piece.

        Parameters
        ----------
        white : bool
            Whether the piece is white or black.
        x : int
            initial x coordinate of piece on board
        y : int
            initial y coordinate of piece on board

        """
        self.white = white
        self.killed = False

        self.x = x
        self.y = y

    @abstractmethod
    def piece_deepcopy(self):
        """Method to create an uncorrelated clone of the piece.

        Returns
        -------
        Piece
            Exact copy of self.

        """
        copied_piece = Piece(self.white, self.x, self.y)
        copied_piece.killed = self.killed
        return copied_piece

    def is_white(self):
        """Method to access the piece color.

        Returns
        -------
        bool
            color of piece.

        """
        return self.white

    def is_killed(self):
        """Method to access the piece status (killed or not).

        Returns
        -------
        bool
            status of piece.

        """
        return self.killed

    def set_killed(self):
        """Sets the piece status to killed."""
        self.killed = True

    @abstractmethod
    def piece_move_authorized(self, start, end):
        """Method to verify if is a move is authorized in terms of movements.

        Parameters
        ----------
        start: engine.Cell
            Starting cell for movement check (current cell of piece).
        end: engine.Cell
            Landing cell for movement check.

        Returns
        -------
        bool
            Whether the movement is authorized by the piece possibilities or not.
        """
        x_start = start.get_x()
        y_start = start.get_y()
        x_end = end.get_x()
        y_end = end.get_y()

        # If material is already on the landing cell
        if end.get_piece() is not None:
            if end.get_piece().is_white() == self.is_white():
                return False

        if x_start == x_end and y_start == y_end:
            return False
        else:
            if x_start < 0 or x_end < 0:
                return False
            elif x_start > 7 or x_end > 7:
                return False
            elif y_start < 0 or y_end < 0:
                return False
            elif y_start > 7 or y_end > 7:
                return False
            else:
                return True

    def can_move(self, board, move):
        """Method to verify if is a move is authorized in terms of movements.

        Parameters
        ----------
        board: engine.Board
            Board to which the piece belongs to and on which the movement is tested
        move: engine.Move
            Move object to be tested

        Returns
        -------
        bool
            Whether the movement is authorized by the piece possibilities or not.
        """

        is_movement_authorized = self.piece_move_authorized(move.start, move.end)
        return is_movement_authorized

    @abstractmethod
    def get_potential_moves(self, x, y):
        """Method to list all the possible moves from coordinates. Only uses authorized movements, no other pieces on a
        board.

        Parameters
        ----------
        x: int
            x coordinate of the piece
        y: int
            y coordinate of the piece

        Returns
        -------
        bool
            List of authorized moves
        """
        return None

    @abstractmethod
    def get_threatened_cells_on_board(self, board):
        """
        Method to list which cells are threatened by the piece (authorized movement + conditioned on other pieces on board).

        Parameters
        ----------
        board: Board
            game board self belong to

        Returns
        -------
        list
            List of threatened cells

        """
        return []

    @abstractmethod
    def get_str(self):
        """Method to represent the piece as a string.

        Returns
        -------
        str
            String representation of the piece
        """
        return "     "

    def draw(self):
        """Method to represent the piece as a colored string in order to draw a board.

        Returns
        -------
        str
            Colored representation of the piece within a board.
        """
        value = self.get_str()
        if self.is_white():
            return Color.GREEN + value + Color.WHITE
        else:
            return Color.RED + value + Color.WHITE


class Pawn(Piece):
    """Base class for the pawns pieces

    Implements the properties, attributes and functions specific to pawns.

    Attributes
    ----------
    white : bool
        Whether the piece is white or black.
    x : int
        x coordinate of piece on board
    y : int
        y coordinate of piece on board
    killed: bool
        Whether the piece has been killed by opponent or not. Initialized to False
    has_moved: bool
        Whether the piece has already moved during a game or not. Initialized to False
    last_move_is_double: bool
        Whether the piece previous move was a double advance or not. For future En Passant checks. Initialized to False.
    """

    type = "pawn"

    def __init__(self, *args, **kwargs):
        """Initialization of the pawn.

        Parameters
        ----------
        white : bool
            Whether the piece is white or black.
        x : int
            initial x coordinate of piece on board
        y : int
            initial y coordinate of piece on board

        """
        super().__init__(*args, **kwargs)
        self.has_moved = False  # if the pawn has yet been moved or not to keep ?
        self.last_move_is_double = (
            False  # check for en passant, if last move was a double tap
        )

    def piece_deepcopy(self):
        """Method to create an uncorrelated clone of the piece.

        Returns
        -------
        Pawn
            Exact copy of self.
        """
        copied_piece = Pawn(self.white, self.x, self.y)
        copied_piece.killed = self.killed
        copied_piece.has_moved = self.has_moved
        copied_piece.last_move_is_double = self.last_move_is_double
        return copied_piece

    def piece_move_authorized(self, start, end):
        """Method to verify if is a move is authorized in terms of movements.

        Parameters
        ----------
        start: engine.Cell
            Starting cell for movement check (current cell).
        end: engine.Cell
            Landing cell for movement check.

        Returns
        -------
        bool
            Whether the movement is authorized by the piece possibilities or not.
        """
        # Check if there is a piece on the landing cell
        if not super().piece_move_authorized(start=start, end=end):
            return False
        if end.get_piece() is not None:
            # check if there is not another piece of same color
            if end.get_piece().is_white() == self.is_white():
                return False

            else:
                # Pawn can only take an adversary piece in diagonal
                dx = end.get_x() - start.get_x()
                dy = end.get_y() - start.get_y()
                if dx == 1 and abs(dy) == 1 and self.is_white():
                    return True
                elif dx == -1 and abs(dy) == 1 and not self.is_white():
                    return True
                else:
                    return False

        # No piece on landing cell, just checking if movement is authorized.
        else:
            dx = end.get_x() - start.get_x()
            dy = end.get_y() - start.get_y()
            if dx == 1 and dy == 0 and self.is_white():
                return True
            elif dx == -1 and dy == 0 and not self.is_white():
                return True

            else:
                # Initial move authorized to be two cells at once. Should check self.has_moved here ?
                if start.get_x() == 1 and dx == 2 and dy == 0 and self.is_white():
                    return True
                elif (
                    start.get_x() == 6 and dx == -2 and dy == 0 and not self.is_white()
                ):
                    return True
                else:
                    return False

    def can_move(self, board, move):
        """Method to verify if is a move is authorized in terms of movements.

        Parameters
        ----------
        board: engine.Board
            Board to which the piece belongs to and on which the movement is tested
        move: engine.Move
            Move object to be tested

        Returns
        -------
        bool
            Whether the movement is authorized by the piece possibilities or not.
        """
        authorized_move = self.piece_move_authorized(move.start, move.end)

        if not authorized_move:
            """to remove ?"""
            crossed_cell = board.get_cell(move.start.get_x(), move.end.get_y())
            crossed_piece = crossed_cell.get_piece()
            if isinstance(crossed_piece, Pawn):
                if (
                    crossed_piece.last_move_is_double
                    and crossed_piece.is_white() != self.is_white()
                ):
                    # Revoir comment on update cet attribut last_move_is_double
                    authorized_move = True
                    move.complementary_passant = crossed_cell
        else:
            # Checks that no piece (friend or foe) is blocking the cell(s) in front.
            dx = move.end.get_x() - move.start.get_x()

            if dx > 1:
                if (
                    board.get_cell(
                        move.start.get_x() + 1, move.start.get_y()
                    ).get_piece()
                    is not None
                ):
                    return False
            elif dx < -1:
                if (
                    board.get_cell(
                        move.start.get_x() - 1, move.start.get_y()
                    ).get_piece()
                    is not None
                ):
                    return False
        """
        if move.end.get_x() == 7 and self.is_white():
            move.transform_pawn = True
        elif move.end.get_x() == 0 and not self.is_white():
            move.transform_pawn = True
        """
        return authorized_move

    def get_potential_moves(self, x, y):
        """Method to list all the possible moves from coordinates. Only uses authorized movements, no other pieces on a
        board.

        Parameters
        ----------
        x: int
            x coordinate of the piece
        y: int
            y coordinate of the piece

        Returns
        -------
        list
            List of authorized moves
        """

        possible_moves = []
        if self.is_white():
            # Front cell
            if x < 7:
                possible_moves.append((x + 1, y))

                # Diagonal cells
                if y - 1 >= 0:
                    possible_moves.append((x + 1, y - 1))
                if y + 1 <= 7:
                    possible_moves.append((x + 1, y + 1))

            # Double front cell
            if x == 1:
                possible_moves.append((x + 2, y))

        # Symmetric for black pawns
        else:
            if x > 0:
                possible_moves.append((x - 1, y))

                if y - 1 >= 0:
                    possible_moves.append((x - 1, y - 1))
                if y + 1 <= 7:
                    possible_moves.append((x - 1, y + 1))
            if x == 6:
                possible_moves.append((x - 2, y))

        return possible_moves

    @abstractmethod
    def get_threatened_cells_on_board(self, board):
        """
        Method to list which cells are threatened by the piece (authorized movement + conditioned on other pieces on board).

        Parameters
        ----------
        board: Board
            game board self belong to

        Returns
        -------
        list
            List of threatened cells

        """

        cells_threatened = []
        if self.is_white():
            if x < 7:
                # Diagonal cells
                if y - 1 >= 0:
                    cells_threatened.append((x + 1, y - 1))
                if y + 1 <= 7:
                    cells_threatened.append((x + 1, y + 1))

        # Symmetric for black pawns
        else:
            if x > 0:
                if y - 1 >= 0:
                    cells_threatened.append((x - 1, y - 1))
                if y + 1 <= 7:
                    cells_threatened.append((x - 1, y + 1))

        return cells_threatened

    def promote(self, promote_into="Queen"):
        """Method to promote a pawn to other material type. Only happens if the pawn reaches the other side of the board.
        The player can choose which type of material he wants its pawn to be promoted into.

        Parameters
        ----------
        promote_into: str
            Type of material to promote the pawn into.

        Returns
        -------
        Piece
            New piece with right promotion and same coordinates of current pawn.
        """
        # Should we verify color and coordinates of Pawn ?
        if self.is_white():
            assert self.x == 7, "Pawn has not reached other side of the board"
        else:
            assert self.x == 0, "Pawn has not reached the other side of the board"

        if promote_into.lower() == "queen":
            return Queen(white=self.is_white(), x=self.x, y=self.y)
        elif promote_into.lower() == "rook":
            rook = Rook(white=self.is_white(), x=self.x, y=self.y)
            rook.has_moved = True
            return rook
        elif promote_into == "knight":
            return Knight(white=self.is_white(), x=self.x, y=self.y)
        elif promote_into == "bishop":
            return Bishop(white=self.is_white(), x=self.x, y=self.y)
        else:
            raise ValueError(
                f"Cannot promote piece into, {promote_into}, piece unknown"
            )

    def get_str(self):
        """Method to represent the piece as a string.

        Returns
        -------
        str
            String representation of the piece
        """
        repr = "  P  "
        return repr if self.is_white() else repr.lower()


class Bishop(Piece):
    """Base class for the bishop pieces

    Implements the properties, attributes and functions specific to bishops.

    Attributes
    ----------
    white : bool
        Whether the piece is white or black.
    x : int
        x coordinate of piece on board
    y : int
        y coordinate of piece on board
    killed: bool
        Whether the piece has been killed by opponent or not. Initialized to False.
    """

    type = "bishop"

    def __init__(self, *args, **kwargs):
        """Initialization of the bishop.

        Parameters
        ----------
        white : bool
            Whether the piece is white or black.
        x : int
            initial x coordinate of piece on board
        y : int
            initial y coordinate of piece on board

        """
        super().__init__(*args, **kwargs)

    def piece_deepcopy(self):
        """Method to create an uncorrelated clone of the piece.

        Returns
        -------
        Bishop
            Exact copy of self.
        """
        copied_piece = Bishop(self.white, self.x, self.y)
        copied_piece.killed = self.killed
        return copied_piece

    def piece_move_authorized(self, start, end):
        """Method to verify if is a move is authorized in terms of movements.

        Parameters
        ----------
        start: engine.Cell
            Starting cell for movement check (current cell).
        end: engine.Cell
            Landing cell for movement check.

        Returns
        -------
        bool
            Whether the movement is authorized by the piece possibilities or not.
        """
        if not super().piece_move_authorized(start=start, end=end):
            return False

        # Checking movemement
        dx = end.get_x() - start.get_x()
        dy = end.get_y() - start.get_y()
        if abs(dx) == abs(dy):
            return True
        else:
            return False

    def can_move(self, board, move):
        """Method to verify if a move is authorized within a board.

        Parameters
        ----------
        board: engine.Board
            Board to which the piece belongs to and on which the movement is tested
        move: engine.Move
            Move object to be tested

        Returns
        -------
        bool
            Whether the movement is authorized by the piece possibilities or not.
        """
        # Checking if movement is alright
        authorized_move = self.piece_move_authorized(move.start, move.end)
        if authorized_move:
            dx = move.end.get_x() - move.start.get_x()
            dy = move.end.get_y() - move.start.get_y()

            # Checking that no material is blocking the trajectory
            for i in range(1, abs(dx)):
                x_trajectory = i * int(dx / abs(dx)) + move.start.get_x()
                y_trajectory = i * int(dy / abs(dy)) + move.start.get_y()
                if board.get_cell(x_trajectory, y_trajectory).get_piece() is not None:
                    return False
            return True
        else:
            return False

    def get_potential_moves(self, x, y):
        """Method to list all the possible moves from coordinates. Only uses authorized movements, no other pieces on a
        board.

        Parameters
        ----------
        x: int
            x coordinate of the piece
        y: int
            y coordinate of the piece

        Returns
        -------
        list
            List of authorized moves
        """
        possible_moves = []

        # Diagonal 1
        nx = x - 1
        ny = y - 1
        while nx >= 0 and ny >= 0:
            possible_moves.append((nx, ny))
            nx -= 1
            ny -= 1

        # Diagonal 2
        nx = x - 1
        ny = y + 1
        while nx >= 0 and ny <= 7:
            possible_moves.append((nx, ny))
            nx -= 1
            ny += 1

        # Diagonal 3
        nx = x + 1
        ny = y - 1
        while nx <= 7 and ny >= 0:
            possible_moves.append((nx, ny))
            nx += 1
            ny -= 1

        # Diagonal 4
        nx = x + 1
        ny = y + 1
        while nx <= 7 and ny <= 7:
            possible_moves.append((nx, ny))
            nx += 1
            ny += 1

        return possible_moves

    def get_str(self):
        """Method to represent the piece as a string.

        Returns
        -------
        str
            String representation of the piece
        """
        repr = "  B  "
        return repr if self.is_white() else repr.lower()


class Rook(Piece):
    """Base class for the rook pieces

    Implements the properties, attributes and functions specific to rooks.

    Attributes
    ----------
    white : bool
        Whether the piece is white or black.
    x : int
        x coordinate of piece on board
    y : int
        y coordinate of piece on board
    killed: bool
        Whether the piece has been killed by opponent or not. Initialized to False.
    has_moved: bool
        Whether the piece has already moved during a game or not. Initialized to False.
    """

    type = "rook"

    def __init__(self, *args, **kwargs):
        """Initialization of the rook.

        Parameters
        ----------
        white : bool
            Whether the piece is white or black.
        x : int
            initial x coordinate of piece on board
        y : int
            initial y coordinate of piece on board

        """
        super().__init__(*args, **kwargs)
        self.has_moved = False

    def piece_deepcopy(self):
        """Method to create an uncorrelated clone of the piece.

        Returns
        -------
        Rook
            Exact copy of self.
        """
        copied_piece = Rook(self.white, self.x, self.y)
        copied_piece.killed = self.killed
        copied_piece.has_moved = self.has_moved
        return copied_piece

    def piece_move_authorized(self, start, end):
        """Method to verify if is a move is authorized in terms of movements.

        Parameters
        ----------
        start: engine.Cell
            Starting cell for movement check (current cell).
        end: engine.Cell
            Landing cell for movement check.

        Returns
        -------
        bool
            Whether the movement is authorized by the piece possibilities or not.
        """
        if not super().piece_move_authorized(start=start, end=end):
            return False

        # Checking movement
        dx = end.get_x() - start.get_x()
        dy = end.get_y() - start.get_y()
        if dx == 0 or dy == 0:
            return True
        else:
            return False

    def can_move(self, board, move):
        """Method to verify if a move is authorized within a board.

        Parameters
        ----------
        board: engine.Board
            Board to which the piece belongs to and on which the movement is tested
        move: engine.Move
            Move object to be tested

        Returns
        -------
        bool
            Whether the movement is authorized by the piece possibilities or not.
        """

        # Checking that movement is authorized
        authorized_move = self.piece_move_authorized(move.start, move.end)
        if authorized_move:
            dx = move.end.get_x() - move.start.get_x()
            dy = move.end.get_y() - move.start.get_y()
            # Checking that no material in x axis is blocking the trajectory
            for i in range(1, abs(dx)):
                x_trajectory = i * int(dx / abs(dx)) + move.start.get_x()
                y_trajectory = move.start.get_y()
                if board.get_cell(x_trajectory, y_trajectory).get_piece() is not None:
                    return False

            # Checking that no material in the y axis is blocking the trajectory
            for i in range(1, abs(dy)):
                x_trajectory = move.start.get_x()
                y_trajectory = i * int(dy / abs(dy)) + move.start.get_y()
                if board.get_cell(x_trajectory, y_trajectory).get_piece() is not None:
                    return False
            return True
        else:
            return False

    def get_potential_moves(self, x, y):
        """Method to list all the possible moves from coordinates. Only uses authorized movements, no other pieces on a
        board.

        Parameters
        ----------
        x: int
            x coordinate of the piece
        y: int
            y coordinate of the piece

        Returns
        -------
        list
            List of authorized moves
        """
        possible_moves = []

        # X-axis left
        nx = x - 1
        while nx >= 0:
            possible_moves.append((nx, y))
            nx -= 1

        # X-axis right
        ny = y + 1
        while ny <= 7:
            possible_moves.append((x, ny))
            ny += 1

        # Y-axis top
        nx = x + 1
        while nx <= 7:
            possible_moves.append((nx, y))
            nx += 1

        # Y-axis down
        ny = y - 1
        while ny >= 0:
            possible_moves.append((x, ny))
            ny -= 1

        return possible_moves

    def get_str(self):
        """Method to represent the piece as a string.

        Returns
        -------
        str
            String representation of the piece
        """
        repr = "  R  "
        return repr if self.is_white() else repr.lower()


class Knight(Piece):
    """Base class for the knoght pieces

    Implements the properties, attributes and functions specific to knights.

    Attributes
    ----------
    white : bool
        Whether the piece is white or black.
    x : int
        x coordinate of piece on board
    y : int
        y coordinate of piece on board
    killed: bool
        Whether the piece has been killed by opponent or not. Initialized to False.
    """

    type = "knight"

    def __init__(self, *args, **kwargs):
        """Initialization of the knight.

        Parameters
        ----------
        white : bool
            Whether the piece is white or black.
        x : int
            initial x coordinate of piece on board
        y : int
            initial y coordinate of piece on board

        """
        super().__init__(*args, **kwargs)

    def piece_deepcopy(self):
        """Method to create an uncorrelated clone of the piece.

        Returns
        -------
        Knight
            Exact copy of self.
        """
        copied_piece = Knight(self.white, self.x, self.y)
        copied_piece.killed = self.killed
        return copied_piece

    def piece_move_authorized(self, start, end):
        """Method to verify if is a move is authorized in terms of movements.

        Parameters
        ----------
        start: engine.Cell
            Starting cell for movement check (current cell).
        end: engine.Cell
            Landing cell for movement check.

        Returns
        -------
        bool
            Whether the movement is authorized by the piece possibilities or not.
        """
        if not super().piece_move_authorized(start=start, end=end):
            return False

        dx = start.get_x() - end.get_x()
        dy = start.get_y() - end.get_y()
        return abs(dx) * abs(dy) == 2

    def can_move(self, board, move):
        """Method to verify if a move is authorized within a board.

        Parameters
        ----------
        board: engine.Board
            Board to which the piece belongs to and on which the movement is tested
        move: engine.Move
            Move object to be tested

        Returns
        -------
        bool
            Whether the movement is authorized by the piece possibilities or not.
        """
        # The knight is jumping, no need to verify blocking material
        return self.piece_move_authorized(move.start, move.end)

    def get_str(self):
        """Method to represent the piece as a string.

        Returns
        -------
        str
            String representation of the piece
        """
        repr = "  N  "
        return repr if self.is_white() else repr.lower()

    def get_potential_moves(self, x, y):
        """Method to list all the possible moves from coordinates. Only uses authorized movements, no other pieces on a
        board.

        Parameters
        ----------
        x: int
            x coordinate of the piece
        y: int
            y coordinate of the piece

        Returns
        -------
        list
            List of authorized moves
        """
        possible_moves = []

        # All difference position that a knight can move to
        combos = [
            (2, 1),
            (1, 2),
            (-2, 1),
            (2, -1),
            (-2, -1),
            (-1, 2),
            (1, -2),
            (-1, -2),
        ]
        for nx, ny in combos:
            if 0 <= nx + x <= 7 and 0 <= ny + y <= 7:
                possible_moves.append((x + nx, y + ny))

        return possible_moves


class Queen(Piece):
    """Base class for the queen pieces

    Implements the properties, attributes and functions specific to queens.

    Attributes
    ----------
    white : bool
        Whether the piece is white or black.
    x : int
        x coordinate of piece on board
    y : int
        y coordinate of piece on board
    killed: bool
        Whether the piece has been killed by opponent or not. Initialized to False.
    """

    type = "queen"

    def __init__(self, *args, **kwargs):
        """Initialization of the queen.

        Parameters
        ----------
        white : bool
            Whether the piece is white or black.
        x : int
            initial x coordinate of piece on board
        y : int
            initial y coordinate of piece on board

        """
        super().__init__(*args, **kwargs)

    def piece_deepcopy(self):
        """Method to create an uncorrelated clone of the piece.

        Returns
        -------
        Queen
            Exact copy of self.
        """
        copied_piece = Queen(self.white, self.x, self.y)
        copied_piece.killed = self.killed
        return copied_piece

    def piece_move_authorized(self, start, end):
        """Method to verify if is a move is authorized in terms of movements.

        Parameters
        ----------
        start: engine.Cell
            Starting cell for movement check (current cell).
        end: engine.Cell
            Landing cell for movement check.

        Returns
        -------
        bool
            Whether the movement is authorized by the piece possibilities or not.
        """

        if not super().piece_move_authorized(start=start, end=end):
            return False

        dx = end.get_x() - start.get_x()
        dy = end.get_y() - start.get_y()

        return (dx == 0) or (dy == 0) or (abs(dx) == abs(dy))

    def can_move(self, board, move):
        """Method to verify if a move is authorized within a board.

        Parameters
        ----------
        board: engine.Board
            Board to which the piece belongs to and on which the movement is tested
        move: engine.Move
            Move object to be tested

        Returns
        -------
        bool
            Whether the movement is authorized by the piece possibilities or not.
        """
        # Checking if movement is authorized
        authorized_move = self.piece_move_authorized(move.start, move.end)

        # Checking that no material is blocking the trajectory
        if authorized_move:
            dx = move.end.get_x() - move.start.get_x()
            dy = move.end.get_y() - move.start.get_y()

            # Queen going along an axis
            if dx == 0 or dy == 0:
                # Along X-axis
                for i in range(1, abs(dx)):
                    x_trajectory = i * int(dx / abs(dx)) + move.start.get_x()
                    y_trajectory = move.start.get_y()
                    if (
                        board.get_cell(x_trajectory, y_trajectory).get_piece()
                        is not None
                    ):
                        return False
                # Along Y-axis
                for i in range(1, abs(dy)):
                    x_trajectory = move.start.get_x()
                    y_trajectory = i * int(dy / abs(dy)) + move.start.get_y()
                    if (
                        board.get_cell(x_trajectory, y_trajectory).get_piece()
                        is not None
                    ):
                        return False
                return True

            # Queen going in diagonal
            elif abs(dx) == abs(dy):
                for i in range(1, abs(dx)):
                    x_trajectory = i * int(dx / abs(dx)) + move.start.get_x()
                    y_trajectory = i * int(dy / abs(dy)) + move.start.get_y()
                    if (
                        board.get_cell(x_trajectory, y_trajectory).get_piece()
                        is not None
                    ):
                        return False
                return True
        else:
            return False

    def get_potential_moves(self, x, y):
        """Method to list all the possible moves from coordinates. Only uses authorized movements, no other pieces on a
        board.

        Parameters
        ----------
        x: int
            x coordinate of the piece
        y: int
            y coordinate of the piece

        Returns
        -------
        list
            List of authorized moves
        """
        possible_moves = []

        # Diagonal 1
        nx = x - 1
        ny = y - 1
        while nx >= 0 and ny >= 0:
            possible_moves.append((nx, ny))
            nx -= 1
            ny -= 1

        # Diagonal 2
        nx = x - 1
        ny = y + 1
        while nx >= 0 and ny <= 7:
            possible_moves.append((nx, ny))
            nx -= 1
            ny += 1

        # Diagonal 3
        nx = x + 1
        ny = y - 1
        while nx <= 7 and ny >= 0:
            possible_moves.append((nx, ny))
            nx += 1
            ny -= 1

        # Diagonal 4
        nx = x + 1
        ny = y + 1
        while nx <= 7 and ny <= 7:
            possible_moves.append((nx, ny))
            nx += 1
            ny += 1

        # X-axis left
        nx = x - 1
        while nx >= 0:
            possible_moves.append((nx, y))
            nx -= 1

        # X-axis right
        nx = x + 1
        while nx <= 7:
            possible_moves.append((nx, y))
            nx += 1

        # Y-axis down
        ny = y - 1
        while ny >= 0:
            possible_moves.append((x, ny))
            ny -= 1

        # Y-axis top
        ny = y + 1
        while ny <= 7:
            possible_moves.append((x, ny))
            ny += 1

        return possible_moves

    def get_str(self):
        """Method to represent the piece as a string.

        Returns
        -------
        str
            String representation of the piece
        """
        repr = "  Q  "
        return repr if self.is_white() else repr.lower()


class King(Piece):
    """Base class for the king pieces

    Implements the properties, attributes and functions specific to kings.

    Attributes
    ----------
    white : bool
        Whether the piece is white or black.
    x : int
        x coordinate of piece on board
    y : int
        y coordinate of piece on board
    killed: bool
        Whether the piece has been killed by opponent or not. Initialized to False
    has_moved: bool
        Whether the piece has already moved during a game or not. Initialized to False
    castling_done: bool
        Whether the piece has already realized castling. Initialized to False.
    """

    type = "king"

    def __init__(self, *args, **kwargs):
        """Initialization of the king.

        Parameters
        ----------
        white : bool
            Whether the piece is white or black.
        x : int
            initial x coordinate of piece on board
        y : int
            initial y coordinate of piece on board

        """
        super().__init__(*args, **kwargs)
        self.castling_done = False
        self.has_moved = False

    def piece_deepcopy(self):
        """Method to create an uncorrelated clone of the piece.

        Returns
        -------
        King
            Exact copy of self.
        """
        copied_piece = King(self.white, self.x, self.y)
        copied_piece.killed = self.killed
        copied_piece.castling_done = self.castling_done
        copied_piece.has_moved = self.has_moved
        return copied_piece

    def set_castling_done(self, castling_done):
        self.castling_done = castling_done

    def piece_move_authorized(self, start, end):
        """Method to verify if is a move is authorized in terms of movements.

        Parameters
        ----------
        start: engine.Cell
            Starting cell for movement check (current cell).
        end: engine.Cell
            Landing cell for movement check.

        Returns
        -------
        bool
            Whether the movement is authorized by the piece possibilities or not.
        """

        if not super().piece_move_authorized(start=start, end=end):
            return False
        dx = end.get_x() - start.get_x()
        dy = end.get_y() - start.get_y()

        if abs(dx) < 2 and abs(dy) < 2:
            return True
        else:
            return False

    def can_move(self, board, move):
        """Method to verify if a move is authorized within a board.

        Parameters
        ----------
        board: engine.Board
            Board to which the piece belongs to and on which the movement is tested
        move: engine.Move
            Move object to be tested

        Returns
        -------
        bool
            Whether the movement is authorized by the piece possibilities or not.
        """
        # Checking if movement is authorized
        authorized_move = self.piece_move_authorized(move.start, move.end)
        if authorized_move:
            # Verifying that the landing cell is not threatened by some adversary material
            if move.end.is_threatened(board, self.is_white()):
                return False
            else:
                return True
        # If move is not authorized it could mean that player is trying to do a special move, i.e. castling
        else:
            # Checking castling conditions on the right then on the left
            if (
                not self.castling_done
                and not self.has_moved
                and (move.end.y == 6 or move.end.y == 2)
            ):
                if move.end.y == 6:  # Roque vers la droite
                    # Getting the rook for castling
                    rook_to_move = board.get_cell(move.start.x, 7).get_piece()
                    rook_starting_coordinates = (move.start.x, 7)
                    rook_ending_coordinates = (move.start.x, 5)

                    # Listing cells that must not have material on
                    if isinstance(rook_to_move, Rook):
                        must_be_empty_cells = [
                            board.get_cell(move.start.x, 5),
                            board.get_cell(move.start.x, 6),
                        ]
                        must_not_be_threatened_cells = [
                            board.get_cell(move.start.x, 4),
                            board.get_cell(move.start.x, 5),
                            board.get_cell(move.start.x, 6),
                        ]
                    else:
                        return False

                elif move.end.y == 2:  # Roque vers la gauche
                    rook_to_move = board.get_cell(move.start.x, 0).get_piece()
                    rook_starting_coordinates = (move.start.x, 0)
                    rook_ending_coordinates = (move.start.x, 3)

                    # Getting the rook
                    if isinstance(rook_to_move, Rook):
                        # Listing cells that must not have material on
                        must_be_empty_cells = [
                            board.get_cell(move.start.x, 1),
                            board.get_cell(move.start.x, 2),
                            board.get_cell(move.start.x, 3),
                        ]
                        must_not_be_threatened_cells = [
                            board.get_cell(move.start.x, 2),
                            board.get_cell(move.start.x, 3),
                            board.get_cell(move.start.x, 4),
                        ]
                    else:
                        return False

                else:
                    return False

                # Verifying conditions for listed cells
                empty_cells_check = True
                not_threatened_cells = True
                for cll in must_be_empty_cells:
                    if cll.get_piece() is not None:
                        empty_cells_check = False
                for cll in must_not_be_threatened_cells:
                    if cll.is_threatened(board, self.is_white()):
                        not_threatened_cells = False

                # Verify that all conditions are met and completes the move so that it has the full castling information
                # to operate all the movements
                conditions_to_castling = [
                    not rook_to_move.has_moved,
                    empty_cells_check,
                    not_threatened_cells,
                ]
                if all(conditions_to_castling):
                    move.complementary_castling = (
                        rook_to_move,
                        board.get_cell(
                            rook_starting_coordinates[0], rook_starting_coordinates[1]
                        ),
                        board.get_cell(
                            rook_ending_coordinates[0], rook_ending_coordinates[1]
                        ),
                    )
                    return True
                else:
                    return False
            return False

    def get_potential_moves(self, x, y):
        """Method to list all the possible moves from coordinates. Only uses authorized movements, no other pieces on a
        board.

        Parameters
        ----------
        x: int
            x coordinate of the piece
        y: int
            y coordinate of the piece

        Returns
        -------
        list
            List of authorized moves
        """
        possible_moves = []

        # All possible moves
        combos = [(1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1), (0, 1), (0, -1), (-1, 0)]
        for nx, ny in combos:
            if 0 <= x + nx <= 7 and 0 <= y + ny <= 7:
                possible_moves.append((nx + x, ny + y))

        # Add castling as potential moves if not done yet
        if not self.has_moved:
            possible_moves.append((x, 1))
            possible_moves.append((x, 6))

        return possible_moves

    def get_str(self):
        """Method to represent the piece as a string.

        Returns
        -------
        str
            String representation of the piece
        """
        repr = "  K  "
        return repr if self.is_white() else repr.lower()

    def is_checked(self, board):
        """Method to verify that the king at its current position is not threatened / checked by opponent material.

        Parameters
        ----------
        board: engine.Board
            Board to which the piece belongs to

        Returns
        -------
        bool
            Whether the king is checked or not.
        """

        return board.get_cell(self.x, self.y).is_threatened(board, self.white)

    # def is_checked_mate(self, board):
    #     if not self.is_checked(board):
    #         return False
    #
    #     for i in range(8):
    #         for j in range(8):
    #             piece = board.get_cell(i, j).get_piece()
    #             if piece is not None:
    #                 if piece.is_white() == self.is_white():
    #                     for move in piece.get_potential_moves(piece.x, piece.y):
    #                         selected_move = Move(None, board.get_cell(i, j),
    #                                              board.get_cell(move[0], move[1]))
    #                         verified_move = piece.can_move(board, selected_move)
    #
    #                         if verified_move:
    #                             copied_board = board.copy()
