import copy

import material


class Move:
    def __init__(self, player, board, start, end):
        self.player = player
        self.board = board
        self.start = start
        self.end = end
        self.moved_piece = start.get_piece()
        if self.moved_piece is None:
            ###print("Empty cell selected as start of a move")
            pass
        self.killed_piece = self.end.get_piece()
        self.is_castling = False
        self.complementary_castling = None
        self.en_passant = False
        self.transform_pawn = False

    def _set_moved_attribute(self):
        if hasattr(self.moved_piece, 'has_moved'):
            self.moved_piece.has_moved = True
            ###print('PIECE', self.moved_piece.is_white(), self.moved_piece, "set to moved")
            ###print(self.start.x, self.start.y, self.end.x, self.end.y)
        if hasattr(self.moved_piece, 'last_move_is_double'):
            if abs(self.start.get_x() - self.end.get_x()) > 1:
                self.moved_piece.last_move_is_double = True
            else:
                self.moved_piece.last_move_is_double = False

    def _set_castling_done(self):
        assert isinstance(self.moved_piece, material.King)
        self.moved_piece.castling_done = True

    def _is_castling(self):
        if not isinstance(self.moved_piece, material.King):
            ###print("not castling becasuse king not moved")
            return False
        elif self.moved_piece.castling_done or self.moved_piece.has_moved:
            ###print("castling already done or king has already moved")
            ###print(self.moved_piece.castling_done)
            ###print(self.moved_piece.has_moved)
            return False

        else:
            if self.end.y == 6:  # Castling in the right
                rook_to_move = self.board.get_cell(self.start.x, 7).get_piece()
                if not isinstance(rook_to_move, material.Rook):
                    ###print("no rook to move")
                    return False
                elif rook_to_move.has_moved:
                    ###print("rook has already moved")
                    return False
                else:
                    rook_starting_coordinates = (self.start.x, 7)
                    rook_ending_coordinates = (self.start.x, 5)
                    must_be_empty_cells = [self.board.get_cell(self.start.x, 5),
                                           self.board.get_cell(self.start.x, 6)]
                    must_not_be_threatened_cells = [self.board.get_cell(self.start.x, 4),
                                                    self.board.get_cell(self.start.x, 5),
                                                    self.board.get_cell(self.start.x, 6)]

            elif self.end.y == 2:  # Castling on the left
                rook_to_move = self.board.get_cell(self.start.x, 0).get_piece()
                if not isinstance(rook_to_move, material.Rook):
                    ###print('no rook to move')
                    return False
                elif rook_to_move.has_moved:
                    ###print('rook has already moved')
                    return False
                else:
                    rook_starting_coordinates = (self.start.x, 0)
                    rook_ending_coordinates = (self.start.x, 3)
                    must_be_empty_cells = [self.board.get_cell(self.start.x, 1),
                                           self.board.get_cell(self.start.x, 2),
                                           self.board.get_cell(self.start.x, 3)]
                    must_not_be_threatened_cells = [self.board.get_cell(self.start.x, 2),
                                                    self.board.get_cell(self.start.x, 3),
                                                    self.board.get_cell(self.start.x, 4)]
            else:
                ###print('king did not move to a castling position')
                return False

            empty_cells_check = True
            not_threatened_cells = True
            for cll in must_be_empty_cells:
                if cll.get_piece() is not None:
                    empty_cells_check = False
            for cll in must_not_be_threatened_cells:
                if cll.is_threatened(self.board, self.moved_piece.is_white()):
                    not_threatened_cells = False
                    ###print("CELL THREATENED: ", cll.get_x(), cll.get_y())

            conditions_to_castling = [empty_cells_check, not_threatened_cells]
            if all(conditions_to_castling):
                self.complementary_castling = rook_to_move, \
                                              self.board.get_cell(rook_starting_coordinates[0],
                                                                  rook_starting_coordinates[1]), \
                                              self.board.get_cell(rook_ending_coordinates[0],
                                                                  rook_ending_coordinates[1])
                return True

            else:
                ###print('Conditions for castling:')
                ###print('Rook has not moved:', rook_to_move.has_moved)
                ###print('Cells in between empty:', empty_cells_check)
                ###print('Cells in between not threatened:', not_threatened_cells)
                return False

    def _is_en_passant(self):
        if isinstance(self.moved_piece, material.Pawn):

            dx = self.start.get_x() - self.end.get_x()
            dy = self.start.get_y() - self.end.get_y()
            if dy == 0 or self.killed_piece is not None:
                return False

            else:
                crossed_cell = self.board.get_cell(self.start.get_x(), self.end.get_y())
                crossed_piece = crossed_cell.get_piece()
                if isinstance(crossed_piece, material.Pawn):
                    if crossed_piece.last_move_is_double and crossed_piece.is_white() != self.moved_piece.is_white():
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

    def _is_pawn_transformation(self):
        if not isinstance(self.moved_piece, material.Pawn):
            return False
        else:
            if self.end.get_x() == 7 and self.moved_piece.is_white():
                return True
            elif self.end.get_x() == 0 and not self.moved_piece.is_white():
                return True
            else:
                return False

    def _transform_pawn(self):
        ###print("TRANSFORM PAWN 2", self.moved_piece, self.moved_piece.is_white())
        coordinates = (self.end.get_x(), self.end.get_y())
        self.board.transform_pawn(coordinates)

    def move_pieces(self):
        """
        Effectively moves pieces on board
        """

        if self.killed_piece is not None:
            self.board.kill_piece_from_coordinates((self.end.x, self.end.y))
        self.board.move_piece_from_coordinates((self.start.x, self.start.y), (self.end.x, self.end.y))
        # ADD CASTLING

        if self.complementary_castling is not None and self.is_castling:
            castling_rook, rook_start, rook_end = self.complementary_castling
            self.board.move_piece_from_coordinates((rook_start.x, rook_start.y), (rook_end.x, rook_end.y))
            ###print("CASTLING DETECTED PPPPPPPPP")
            self._set_castling_done()

        if self._is_pawn_transformation():
            self._transform_pawn()
        self._set_moved_attribute()

    def is_possible_move(self): # REFONDRE
        # To be implemented
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
                ###print("Move is not legal, trying to move piece toward a cell with piece of same color")
                return False
            if self.killed_piece.is_white() == self.player.is_white_side():
                ###print('Player cannot take his own material')
                return False

        # CHECK NOT THREATENED CELL IF KING

        # good moving for type of piece selected
        is_legal_move = self.moved_piece.can_move(self.board, self)
        self.is_castling = self._is_castling()

        if not is_legal_move:
            if not self._is_en_passant() or not self.is_castling:
                ###print('Move is not legal, %s authorized movements not allowing it to go on this cell (%i, %i) from cell (%i, %i)' %
                ### (self.moved_piece.__str__(), self.end.get_x(), self.end.get_y(), self.start.get_x(), self.start.get_y()))
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
        is_king_threatened_in_future = self._work_future_to_check_chess()
        if is_king_threatened_in_future:
            ###print('King will be threatened / checked if this move is operated')
            return False

        return True

    def _work_future_to_check_chess(self):
        """TO BE DONE LAST"""
        move = copy.deepcopy(self)
        move.move_pieces()

        if move.player.is_white_side():
            king = move.board.white_king
        else:
            king = move.board.black_king
        return move.board.get_cell(king.x, king.y).is_threatened(move.board, king.is_white())