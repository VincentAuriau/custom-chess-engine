import copy
import pickle

import pyalapin.engine.material as material


class Move(object):
    """Base class for material movement.

    Implements various checks and is able to operate a piece movement along additional actions such as taking an
    adversary piece, castling, en passant.

    Attributes
    ----------
    player : player.Player
        Which player wants to play the move.
    board : Engine.Board
        board of the game on which the move is operated.
    start : engine.Cell
        Current cell on which the moved piece is.
    end: engine.Cell
        Cell on which the piece is moved to.
    moved_piece: material.Piece
        Piece of the board that is moved.
    killed_piece: [None or material.Piece]
        If a piece is killed during the move (meaning that there is a piece on cell end) otherwise is None.
    is_castling: bool
        Whether the move it castling.
    complementary_castling: [None or material.Piece]
        If is_castling, holds additional information => To be moved in extras ?
    is_en_passant: bool
        Whether or not the move is taking a Pawn 'En Passant'
    extras: dict
        Used to introduce additional information such as piece for promotion.

    """

    def __init__(self, player, board, start, end, extras={}):
        """Initialization of the piece.

        Parameters
        ----------
        player : player.Player
            Which player wants to play the move.
        board : Engine.Board
            board of the game on which the move is operated.
        start : engine.Cell
            Current cell on which the moved piece is.
        end: engine.Cell
            Cell on which the piece is moved to.
        extras: dict
            Used to introduce additional information such as piece for promotion.

        """
        self.player = player
        self.board = board
        self.start = start  # Should we take only starting coordinates ?
        self.end = end  # Should we take only landing coordinates ?
        self.extras = extras

        self.moved_piece = start.get_piece()  # Check that moved_piece is not None ?

        self.killed_piece = self.end.get_piece()
        self.is_castling = False
        self.complementary_castling = None
        self.en_passant = False

    def deepcopy(self):
        """Method to create an uncorrelated clone of the move.

        Returns
        -------
        Move
            Exact copy of self.

        """
        # Rethink what needs to be copied and what needs not.
        copied_board = self.board.deepcopy()
        copied_move = Move(
            self.player,
            copied_board,
            copied_board.get_cell(self.start.x, self.start.y),
            copied_board.get_cell(self.end.x, self.end.y),
        )
        copied_move.is_castling = self.is_castling
        copied_move.complementary_castling = self.complementary_castling
        copied_move.en_passant = self.en_passant
        return copied_move

    def _set_moved_attribute(self):
        """Method to set the 'has_moved' attributes for the pieces that need to check whether
        they have already moved or not.
        Also, if the piece is a Pawn, changes the last_move_is_double attribute so that it can
        be taken 'En Passant' if this is the case.
        """
        if hasattr(
            self.moved_piece, "has_moved"
        ):  # Check if the moved piece has the attribute
            self.moved_piece.has_moved = True

        if hasattr(self.moved_piece, "last_move_is_double"):  # Check if it is a Pawn
            if (
                abs(self.start.get_x() - self.end.get_x()) > 1
            ):  # If the move is a double forward
                self.moved_piece.last_move_is_double = True
            else:
                self.moved_piece.last_move_is_double = False

    def to_pgn(self):
        """
        Method to return the PGN representation of the move.

        Returns
        -------
        str:
            pgn representation of the move
        """
        rows = ["a", "b", "c", "d", "e", "f", "g", "h"]
        start = f"{rows[self.start.y]}{self.start.x + 1}"
        end = f"{rows[self.end.y]}{self.end.x + 1}"
        piece = self.moved_piece.get_str().replace(" ", "")
        if isinstance(self.moved_piece, material.Pawn):
            piece = ""
        if self.killed_piece is not None:
            start += "x"
        elif self.is_castling:
            if (self.moved_piece.is_white() and self.end.y == 1) or (
                not self.moved_piece.is_white() and self.end.y == 6
            ):
                piece = "O-O-O"
                start = ""
                end = ""
            else:
                piece = "O-O"
                start = ""
                end = ""

        king = (
            self.board.white_king
            if not self.player.white_side
            else self.board.black_king
        )
        if self.board.get_cell(king.x, king.y).is_threatened(
            board=self.board, threaten_color=not self.player.white_side
        ):
            end += "+"
        print(f"{piece}{start}{end}")
        return f"{piece}{start}{end}"

    def _set_castling_done(self):
        """
        If self is a castling move, then when it is done this function sets the castling_done attribute
        of the concerned King to True, so that it cannot use castling twice.
        """
        assert isinstance(self.moved_piece, material.King)
        self.moved_piece.castling_done = True

    def _is_castling(self):
        """
        Checks if the current move is castling. In particular verifies that:
            - the moved piece is a King
            - the moved King has not already used its castling
            - the King has not already moved
            - the comparnion Rook is on the right Cell
            - the companion Rook has not already moved
            - the Cells between the King and the Rook are empty
            - the King landing Cell is not threatened by adversary Pieces
        Also if it is a castling move sets in self.extra the Rook that needs to be moved along the King

        Returns
        -------
        bool
            Whether self is castling or not.
        """
        if not isinstance(self.moved_piece, material.King):
            return False

        elif self.moved_piece.castling_done or self.moved_piece.has_moved:
            return False

        else:
            if self.end.y == 6:  # Castling on the right
                rook_to_move = self.board.get_cell(self.start.x, 7).get_piece()
                if not isinstance(rook_to_move, material.Rook):
                    return False
                elif rook_to_move.has_moved:
                    return False
                else:
                    rook_starting_coordinates = (self.start.x, 7)
                    rook_ending_coordinates = (self.start.x, 5)
                    must_be_empty_cells = [
                        self.board.get_cell(self.start.x, 5),
                        self.board.get_cell(self.start.x, 6),
                    ]
                    must_not_be_threatened_cells = [
                        self.board.get_cell(self.start.x, 4),
                        self.board.get_cell(self.start.x, 5),
                        self.board.get_cell(self.start.x, 6),
                    ]

            elif self.end.y == 2:  # Castling on the left
                rook_to_move = self.board.get_cell(self.start.x, 0).get_piece()
                if not isinstance(rook_to_move, material.Rook):
                    return False
                elif rook_to_move.has_moved:
                    return False
                else:
                    rook_starting_coordinates = (self.start.x, 0)
                    rook_ending_coordinates = (self.start.x, 3)
                    must_be_empty_cells = [
                        self.board.get_cell(self.start.x, 1),
                        self.board.get_cell(self.start.x, 2),
                        self.board.get_cell(self.start.x, 3),
                    ]
                    must_not_be_threatened_cells = [
                        self.board.get_cell(self.start.x, 2),
                        self.board.get_cell(self.start.x, 3),
                        self.board.get_cell(self.start.x, 4),
                    ]
            else:
                return False

            # Verifying that the cells between rook and king are empty and that starting
            # and landing cells for the king are not threatened.
            empty_cells_check = True
            not_threatened_cells = True
            for cll in must_be_empty_cells:
                if cll.get_piece() is not None:
                    empty_cells_check = False
            for cll in must_not_be_threatened_cells:
                if cll.is_threatened(self.board, self.moved_piece.is_white()):
                    not_threatened_cells = False

            # Verifies that both conditions are met
            conditions_to_castling = [empty_cells_check, not_threatened_cells]
            if all(conditions_to_castling):
                self.complementary_castling = (  # To store in self.extras :)
                    rook_to_move,
                    self.board.get_cell(
                        rook_starting_coordinates[0], rook_starting_coordinates[1]
                    ),
                    self.board.get_cell(
                        rook_ending_coordinates[0], rook_ending_coordinates[1]
                    ),
                )
                self.extras["complementary_castling"] = (
                    rook_to_move,
                    self.board.get_cell(
                        rook_starting_coordinates[0], rook_starting_coordinates[1]
                    ),
                    self.board.get_cell(
                        rook_ending_coordinates[0], rook_ending_coordinates[1]
                    ),
                )
                return True

            else:
                return False

    def _is_en_passant(self):
        """
        Checks if the current move is an 'En passant' capture. In particular verifies that:
            - the moved piece is a Pawn
            - the movement of the pices is in diagonal
            - the move crosses another Pawn
            - this crossed Pawn is of different color
            - this crossed Pawn last move is a double forward advance
        Also if it is an 'En passant' capture sets the crossed Pawn as killed_piece
        Returns
        -------
        bool
            Whether self is an 'En passant' capture or not.
        """
        if isinstance(
            self.moved_piece, material.Pawn
        ):  # Only a Pawn can take 'En Passant'
            dx = self.start.get_x() - self.end.get_x()
            dy = self.start.get_y() - self.end.get_y()
            # Needs the movement to be in diagonal and that no piece is on the landing Cell
            if dy == 0 or self.killed_piece is not None:
                return False

            else:
                # Retrieving crossed Piece
                crossed_cell = self.board.get_cell(self.start.get_x(), self.end.get_y())
                crossed_piece = crossed_cell.get_piece()
                # Verifying the crossed Piece is a Pawn
                if isinstance(crossed_piece, material.Pawn):
                    # Verifying color and last move of crossed_piece
                    if (
                        crossed_piece.last_move_is_double
                        and crossed_piece.is_white() != self.moved_piece.is_white()
                    ):
                        # Revoir comment on update cet attribut last_move_is_double
                        self.killed_piece = crossed_piece
                        self.en_passant = True
                        return True
                    else:
                        return False
                else:
                    return False
        else:
            return False

    def _is_pawn_promotion(self):
        """
        Checks if the current move is should ends up with a Pawn promotion, meaning that:
            - the moved piece is a Pawn
            - the Pawn reaches the other side of the board according to its color
        If the Piece it should be promote into is not specified in self.extras then sets Queen as promotion.

        Returns
        -------
        bool
            Whether self should ends up by a Pawn promotion or not.
        """
        # Checks the piece
        if not isinstance(self.moved_piece, material.Pawn):
            return False
        else:
            # Checks if the Pawn has reached the other side of the board.
            if self.end.get_x() == 7 and self.moved_piece.is_white():  # White Piece
                # Standard is to promote into a Queen if not specified
                self.promote_into = self.extras.get("promote_into", "queen")
                return True

            elif (
                self.end.get_x() == 0 and not self.moved_piece.is_white()
            ):  # Black Piece
                # Standard is to promote into a Queen if not specified
                self.promote_into = self.extras.get("promote_into", "queen")
                return True
            else:
                return False

    def _promote_pawn(self):
        """
        Organizes the Pawn promotion.
        """
        coordinates = (self.end.get_x(), self.end.get_y())
        self.board.promote_pawn(coordinates=coordinates, promote_into=self.promote_into)

    def move_pieces(self):
        """
        Effectively moves pieces on board
        """
        # Do everything from coordinates so that only board needs to be copied in self.deepcopy() ?

        if isinstance(self.moved_piece, material.Pawn):
            reset_halfmove_clock = True
        else:
            reset_halfmove_clock = False

        # Kills Piece on landing Cell if needed.
        if self.killed_piece is not None:
            self.board.kill_piece_from_coordinates((self.end.x, self.end.y))
            reset_halfmove_clock = True
        # Moves Piece on the Board
        self.board.move_piece_from_coordinates(
            (self.start.x, self.start.y), (self.end.x, self.end.y)
        )

        # Executes castling if needed
        if self.complementary_castling is not None and self.is_castling:
            castling_rook, rook_start, rook_end = self.complementary_castling
            self.board.move_piece_from_coordinates(
                (rook_start.x, rook_start.y), (rook_end.x, rook_end.y)
            )

            # Sets castling to done
            self._set_castling_done()

        # Promotes Pawn if needed
        if self._is_pawn_promotion():
            self._promote_pawn()

        # Sets the different movement related attributes of Pieces
        self._set_moved_attribute()
        return reset_halfmove_clock

    def is_possible_move(self, check_chess=True):
        # REFONDRE, particulièrement, faire en sorte qu'on ne vérifie chaque condition qu'une seule fois
        # Why castling is checked here ?
        """
        Checks if move is possible. In particular checks that:
            - Landing Cell is different than current Cell
            - Checks the color of the potential Piece on the landing Cell
            - Movement on the Board is authorized according to the Piece type
            - If moved Piece is a King, does not land on a threatened Cell

        If the Piece it should be promote into is not specified in self.extras then sets Queen as promotion.

        Returns
        -------
        bool
            Whether the move is legal or not.
        """
        # Should be kept ?

        dx = self.start.get_x() - self.end.get_x()
        dy = self.start.get_y() - self.end.get_y()

        # If no movement not possible
        if abs(dx) == 0 and abs(dy) == 0:
            return False

        """
        # Check color of player and color of moving piece:
        if self.moved_piece.is_white() != self.player.is_white_side():
            ###print(self.moved_piece, self.moved_piece.is_white(), self.player.is_white_side())
            ###print("Player", self.player, "tries to move adversaries pieces")
            return False
        """

        # check color of receiving piece
        if self.killed_piece is not None:
            if self.moved_piece.is_white() == self.killed_piece.is_white():
                return False
            if self.killed_piece.is_white() == self.player.is_white_side():
                return False

        # good moving for type of piece selected
        is_legal_move = self.moved_piece.can_move(self.board, self)

        # Why here ?
        self.is_castling = self._is_castling()

        if not is_legal_move:
            if not self._is_en_passant() or not self.is_castling:
                return False

        """
        # Check for chess
        def work_future(curr_move, curr_board):
            future_board = copy.deepcopy(curr_board)
            x_start = curr_move.start.get_x()
            y_start = curr_move.start.get_y()
            x_end = curr_move.end.get_x()
            y_end = curr_move.end.get_y()
            future_piece = future_board.get_cell(x_start, y_start).get_piece()

            future_board.get_cell(x_end, y_end).set_piece(future_piece)
            future_board.get_cell(x_start, y_start).set_piece(None)

            if hasattr(future_piece, 'has_moved'):
                future_piece.has_moved = True
            if hasattr(future_piece, 'last_move_is_double'):
                if abs(x_start - x_end) > 1:
                    future_piece.last_move_is_double = True
                else:
                    future_piece.last_move_is_double = False

            # Check for castling
            if curr_move.complementary_castling is not None:
                ###print('Apparently future castling move, working on moving the Rook')
                castling_rook, rook_start, rook_end = curr_move.complementary_castling
                rook_start = future_board.get_cell(rook_start.get_x(), rook_start.get_y())
                rook_end = future_board.get_cell(rook_end.get_x(), rook_end.get_y())
                castling_rook = rook_start.get_piece()

                rook_end.set_piece(castling_rook)
                rook_start.set_piece(None)

            # Check for prise en passant
            if curr_move.complementary_passant is not None:
                ###print('This future move is taking En Passant')
                x_passant = curr_move.complementary_passant.get_x()
                y_passant = curr_move.complementary_passant.get_y()

                en_passant_piece = future_board.get_cell(x_passant, y_passant).get_piece()
                en_passant_piece.set_killed(True)
                future_board.get_cell(x_passant, y_passant).set_piece(None)

            # Checking if future king is chessed
            if curr_move.player.is_white_side():
                king = future_board.white_king
            else:
                king = future_board.black_king

            return future_board.get_cell(king.x, king.y).is_threatened(future_board, king.is_white())
        """
        # Checks if the player's King is threatened after the move.
        if check_chess:
            is_king_threatened_in_future = self._work_future_to_check_chess()
            if is_king_threatened_in_future:
                return False

        return True

    def _work_future_to_check_chess(self):  # Can it be done better ?
        """
        Effectively move the Piece and check if the King is then threatened. In this case, move cannot happen.

        Returns
        -------
        bool
            Whether the player's King is threatened once the move done.
        """

        # Deep Copy everything
        move = self.deepcopy()
        # Move Piece
        move.move_pieces()

        # Select player's King and check if threatened.
        if move.player.is_white_side():
            king = move.board.white_king
        else:
            king = move.board.black_king
        return move.board.get_cell(king.x, king.y).is_threatened(
            move.board, king.is_white()
        )
