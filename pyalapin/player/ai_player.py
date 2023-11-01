import copy
import pickle
import numpy as np

from pyalapin.player.player import Player
import pyalapin.engine.material as material
import pyalapin.engine.move as move


class EasyAIPlayer(Player):
    """
    AI Player class with simple rules and alpha/beta pruning to speed up research of the best move in the future.

    Attributes
    ----------
    is_white_side : bool
        Whether the player plays with white or black Pieces.
    piece_weights: dict
        Values of the different pieces.
    pieces_positions_weights: dict
        Values for each piece to be on a certain position.
    random_coeff: int
        Coefficient of randomness that will be added to the move score.
    """

    piece_weights = {
        "pawn": 10,
        "knight": 30,
        "bishop": 30,
        "rook": 50,
        "queen": 90,
        "king": 900,
    }
    piece_positions_weights = {
        "pawn": [
            [0.0] * 8,
            [5.0] * 8,
            [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
            [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
            [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
            [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
            [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
            [0.0] * 8,
        ],
        "bishop": [
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
            [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
            [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
            [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
            [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
            [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
        ],
        "knight": [
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
            [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
            [-3.0, 0.0, 1.0, 1.5, 1.5, 1.5, 1.0, 0.0, -3.0],
            [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
            [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
            [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
            [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        ],
        "rook": [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0],
        ],
        "queen": [
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
            [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
            [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
            [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, 0.0],
            [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, -1.0],
            [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
        ],
        "king": [
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
            [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
            [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
            [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0],
        ],
    }

    def __init__(self, white_side, random_coeff=0, *args, **kwargs):
        """Initialization of the player.

        Parameters
        ----------
        white_side : bool
            Whether the player plays with white or black pieces.
        random_coeff: int
            Coefficient of randomness that will be added to the move score.
        """
        super().__init__(white_side=white_side, *args, **kwargs)
        self.color = "white" if self.white_side else "black"
        self.random_coeff = random_coeff
        if self.white_side:
            # Reverse position values for white pieces player
            for key, values in self.piece_positions_weights.items():
                new_values = []
                for i in range(len(values)):
                    new_values.append(values[-i])
                self.piece_positions_weights[key] = new_values

    def __str__(self):
        """Initialization of the player.

        Returns
        -------
        str
            String representation of the player
        """
        return "EasyAIPlayer"

    def _get_possible_moves(self, board, is_white=None):
        """Initialization of the player.

        Parameters
        ----------
        board: Board
            Board on which to look for the possible moves.
        is_white : bool or None
            If we want the possible moves for a different player, can be used.
        """
        if is_white is None:
            is_white = self.white_side()

        if self.white_side != is_white:

            class TempPlayer:
                def __init__(self):
                    self.white_side = is_white

                def is_white_side(self):
                    return self.white_side

            player = TempPlayer()
        else:
            player = self
        color = {True: "white", False: "black"}[is_white]

        possible_moves = []
        # Iterate of pieces
        for type_piece in board.all_material[color]["alive"].keys():
            for piece in board.all_material[color]["alive"][type_piece]:
                # Get potential moves as coordinates
                piece_available_moves = piece.get_potential_moves(piece.x, piece.y)

                # Iterate over piece possible moves
                for mv in piece_available_moves:
                    # Verify that the move is actually possible
                    selected_move = move.Move(
                        player,
                        board,
                        board.get_cell(piece.x, piece.y),
                        board.get_cell(mv[0], mv[1]),
                    )
                    # Keep only of possible
                    # Test letting this test in _alpha_beta
                    if selected_move.is_possible_move(check_chess=False):
                        possible_moves.append(selected_move)

        return possible_moves

    def _select_move_from_score(self, moves, method="max"):
        """Method to select a move according to the score on the board after the move.
        Maximum or minimum score can be selected.

        Parameters
        ----------
        moves : list
            list of moves among which to chose the best one.
        method: str in {"min", "max"}
            Whether to select the move leading to minimum or maximum score

        Returns
        -------
        move.Move
            Selected move
        float
            Score corresponding to the selected move
        """
        # Compute scores
        scores = {}
        for mv in moves:
            mv_ = mv.deepcopy()
            # mv_ = pickle.loads(pickle.dumps(mv, -1))
            # mv_ = copy.deepcopy(mv)
            mv_.move_pieces()
            score = self._score_board(mv_.board)
            scores.append(score)

        # Selection os scores
        if method == "max":
            all_indexes = np.where(scores == np.max(scores))[0]
        elif method == "min":
            all_indexes = np.where(scores == np.min(scores))[0]
        else:
            raise ValueError("MIN OR MAX ALGO, selected %s" % method)
        # If several moves lead to the same score, select randomly
        if len(all_indexes) > 1:
            perm = np.random.permutation(len(all_indexes))[0]
            final_index = all_indexes[perm]

        # Return
        return moves[int(final_index)], scores[final_index]

    # def _def_get_best_score(self, moves, method="max"):
    #     all_scores = []
    #     for mv in moves:
    #         mv_ = copy.deepcopy(mv)
    #         mv_.move_pieces()
    #         score = self._score_board(mv_.board)
    #         all_scores.append(score)
    #
    #     if method == "max":
    #         return np.max(all_scores)
    #     elif method == "min":
    #         return np.min(all_scores)
    #     else:
    #         raise ValueError

    def _search_tree(self, init_board, depth=2, method="max"):
        possible_moves = self._get_possible_moves(init_board)
        if depth == 1:
            best_move, best_score = self._select_move_from_score(
                possible_moves, method=method
            )
            return best_move, best_score
        else:
            new_method = {"max": "min", "min": "max"}
            scores = []
            for p_mv in possible_moves:
                p_mv = p_mv.deepcopy()
                # p_mv = pickle.loads(pickle.dumps(p_mv, -1))
                # p_mv = copy.deepcopy(p_mv)
                p_mv.move_pieces()
                _, score = self._search_tree(
                    p_mv.board, depth=depth - 1, method=new_method[method]
                )
                scores.append(score)

            if method == "max":
                best_score = np.max(scores)
            else:
                best_score = np.min(score)

            best_indexes = np.where(np.array(scores) == best_score)[0]
            final_index = best_indexes[np.random.permutation(len(best_indexes))[0]]
            return possible_moves[int(final_index)], best_score

    def _score_move(self, move):
        all_scores = {}
        mv_ = move.deepcopy()
        # mv_ = pickle.loads(pickle.dumps(move, -1))
        # mv_ = copy.deepcopy(move)
        mv_.move_pieces()
        score = self._score_board(mv_.board)

        return move, score

    def _alpha_beta(
        self,
        init_board,
        init_move=None,
        depth=2,
        alpha=-10000,
        beta=10000,
        is_white=None,
        draw_board=False,
    ):
        """Method to reccursively look for the best move. Implements alpha-beta pruning to test most possible moves.

        Parameters
        ----------
        init_board : engine.Board
            Current state of the game as board
        init_move: move.Move or None
            Not sure yet
        depth: int
            How many turns to look into the future (also used for recursion).
        alpha: int
            Max score value for alpha pruning
        beta: int
            Max score value for beta pruning
        is_white: None or bool
            Can be used if we want to use the method for other color than self
        draw_board: bool
            Whether or not to draw the board in terminal

        Returns
        -------
        int
            score of "best" selected move
        move
            "best" selected move
        """
        # If want to use other color than self.
        if is_white is None:
            is_white = self.white_side

        if draw_board:
            init_board.draw()

        # End of recursion
        if depth == 0:
            # Score current board and return it
            score = self._score_board(init_board)
            return score, init_move
        elif is_white == self.is_white_side():
            # Get moves
            possible_moves = self._get_possible_moves(init_board, is_white=is_white)
            # Iterate over moves and keep the best one.
            best_score = -10000
            best_move = None
            i = 0
            for p_mv in possible_moves:
                i += 1
                p_mv_ = p_mv.deepcopy()
                p_mv_.move_pieces()
                # Get best move if p_mv is actually made
                score, _ = self._alpha_beta(
                    p_mv_.board,
                    init_move=p_mv_,
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
                    is_white=not is_white,
                )
                if self.random_coeff > 0:
                    random_noise = np.random.randint(0, self.random_coeff)
                else:
                    random_noise = 0
                best_move = [best_move, p_mv][
                    np.argmax([best_score, score + random_noise])
                ]
                best_score = np.max([best_score, score + random_noise])

                if best_score >= beta:
                    return best_score, best_move
                alpha = np.max((alpha, best_score))

            return best_score, best_move

        else:
            possible_moves = self._get_possible_moves(init_board, is_white=is_white)

            best_score = 10000
            best_move = None
            for p_mv in possible_moves:
                p_mv_ = p_mv.deepcopy()
                p_mv_.move_pieces()
                score, _ = self._alpha_beta(
                    p_mv_.board,
                    init_move=p_mv_,
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
                    is_white=is_white,
                )

                best_move = [best_move, p_mv][np.argmin([best_score, score])]
                best_score = np.min([best_score, score])

                if best_score <= alpha:
                    return best_score, best_move
                beta = np.min([beta, best_score])
            return best_score, best_move

    def random_move(self, board):
        for i in np.random.permutation(8):
            for j in np.random.permutation(8):
                if board.get_cell(i, j).get_piece() is not None:
                    if (
                        board.get_cell(i, j).get_piece().is_white()
                        == self.is_white_side()
                    ):
                        selected_piece = board.get_cell(i, j).get_piece()
                        ###print('AI Selected Piece', selected_piece)
                        possible_moves = selected_piece.get_potential_moves(i, j)

                        verified_move = False
                        random_move = np.random.permutation(len(possible_moves))
                        index = 0
                        ###print('Verifying Moves,', len(possible_moves), 'Moves Possibles')
                        while not verified_move and index < len(random_move):
                            selected_move = possible_moves[random_move[index]]
                            selected_move = move.Move(
                                self,
                                board,
                                board.get_cell(i, j),
                                board.get_cell(selected_move[0], selected_move[1]),
                            )
                            verified_move = selected_move.is_possible_move()
                            index += 1

                        if verified_move:
                            ###print('Move is verified, ')
                            return selected_move
        ###print('No moved found, aborting...')

    def time_to_play(self, board, depth=3, draw_board=False):
        """Method that must be called to ask AI player to move.

        Parameters
        ----------
        board : engine.Board
            board on which to play
        depth: int
            Tree best move search depth
        draw_board: bool
            Whether or not to draw the board in terminal

        Returns
        -------
        move.Move
            Best move according to board and parameters
        """
        if draw_board:
            board.draw()
        # current_score = self._score_board(board)
        sel_score, sel_move = self._alpha_beta(board, depth=depth)

        return sel_move

    def _score_board(self, board):
        """Method to score a board according to player policy.

        Parameters
        ----------
        board : engine.Board
            board to score

        Returns
        -------
        float
            Score corresponding to the board and the player's parameters
        """
        score = 0
        # Positive score for player pieces
        for piece_type in board.all_material[self.color]["alive"].keys():
            for piece in board.all_material[self.color]["alive"][piece_type]:
                score += self.piece_weights[piece_type]
                score += self.piece_positions_weights[piece_type][piece.x][piece.y]
        own_king = board.all_material[self.color]["alive"]["king"]
        if len(own_king) == 0:
            score -= 1000
        else:
            own_king = own_king[0]
            if board.get_cell(own_king.x, own_king.y).is_threatened(
                board, own_king.is_white()
            ):
                score -= 1000

        adv_color = "white" if self.color == "black" else "black"
        # Negative score for opponent pieces.
        for piece_type in board.all_material[adv_color]["alive"].keys():
            for piece in board.all_material[adv_color]["alive"][piece_type]:
                score -= self.piece_weights[piece_type]
                score -= self.piece_positions_weights[piece_type][piece.x][piece.y]
        adv_king = board.all_material[adv_color]["alive"]["king"]

        if len(adv_king) == 0:
            score -= 1000
        else:
            adv_king = adv_king[0]
            if board.get_cell(adv_king.x, adv_king.y).is_threatened(
                board, adv_king.is_white()
            ):
                score += 1000
        return score
