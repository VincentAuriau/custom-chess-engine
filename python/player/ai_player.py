import copy
import pickle
import numpy as np

from player.player import Player
import engine.material as material
import engine.move as move


class EasyAIPlayer(Player):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = "white" if self.white_side else "black"
        if self.color == "white":
            for key, values in self.piece_positions_weights.items():
                new_values = []
                for i in range(len(values)):
                    new_values.append(values[-i])
                self.piece_positions_weights[key] = new_values

    def __str__(self):
        return "EasyAIPlayer"

    def _get_possible_moves(self, board, is_white=None):
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
        ###print("LOOKING FOR MOVES FOR COLOR", color)
        for type_piece in board.all_material[color]["alive"].keys():
            ###print('               >>>>>>>>>>>>>>>>> TYPE PCE', type_piece)
            for piece in board.all_material[color]["alive"][type_piece]:
                piece_available_moves = piece.get_potential_moves(piece.x, piece.y)
                for mv in piece_available_moves:
                    if isinstance(piece, material.Pawn):
                        ###print("POSSIBLE MOVES FOR PAWN", piece_available_moves)
                        pass
                    selected_move = move.Move(
                        player,
                        board,
                        board.get_cell(piece.x, piece.y),
                        board.get_cell(mv[0], mv[1]),
                    )
                    if selected_move.is_possible_move():
                        possible_moves.append(selected_move)
                        ###print("possible move +1")
        ###print("NB possible moves", len(possible_moves))
        return possible_moves

    def _select_move_from_score(self, moves, method="max"):
        all_scores = {}
        for mv in moves:
            mv_ = pickle.loads(pickle.dumps(mv, -1))
            # mv_ = copy.deepcopy(mv)
            mv_.move_pieces()
            score = self._score_board(mv_.board)
            all_scores[mv] = score

        scores = list(all_scores.values())
        if method == "max":
            all_indexes = np.where(scores == np.max(scores))[0]
        elif method == "min":
            all_indexes = np.where(scores == np.min(scores))[0]
        else:
            raise ValueError("MIN OR MAX ALGO, selected %s" % method)

        perm = np.random.permutation(len(all_indexes))[0]
        final_index = all_indexes[perm]
        return list(all_scores.keys())[int(final_index)], scores[final_index]

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
            ###print(final_index)
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
    ):
        if is_white is None:
            is_white = self.white_side
        ###print('ALPHA BETA FOR BOARD:', "with depth", depth)
        init_board.draw()
        if depth == 0:
            ###print("SCORING BOARD")
            init_board.draw()
            score = self._score_board(init_board)
            ###print("SCORE FOUND:", score)
            return score, init_move
        elif is_white == self.is_white_side():
            possible_moves = self._get_possible_moves(init_board, is_white=is_white)
            ###print(depth, "nb moves:", len(possible_moves))
            best_score = -10000
            best_move = None
            i = 0
            for p_mv in possible_moves:
                ###print("Move", i, "on", len(possible_moves), "for depth", depth, p_mv.end.x)
                i += 1
                # p_mv_ = pickle.loads(pickle.dumps(p_mv, -1))
                # p_mv_ = copy.deepcopy(p_mv)
                p_mv_ = p_mv.deepcopy()
                p_mv_.move_pieces()
                score, _ = self._alpha_beta(
                    p_mv_.board,
                    init_move=p_mv_,
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
                    is_white=not is_white,
                )
                ###print(score, p_mv.start.x, p_mv.start.y, p_mv.end.x, p_mv.end.y)
                best_move = [best_move, p_mv][np.argmax([best_score, score])]
                best_score = np.max([best_score, score])
                ###print("BEST SCORE", best_score)
                ###print("BEST MOVE", best_move, best_move.start.x, best_move.start.y, best_move.end.x, best_move.end.y)
                if best_score >= beta:
                    return best_score, best_move
                alpha = np.max((alpha, best_score))
            ###print("BBBBESTTT MOOVEEE", best_move, best_move.start.x, best_move.start.y, best_move.end.x, best_move.end.y, best_score)
            return best_score, best_move

        else:
            possible_moves = self._get_possible_moves(init_board, is_white=is_white)
            ###print(depth, "nb moves:", len(possible_moves))
            best_score = 10000
            best_move = None
            for p_mv in possible_moves:
                # p_mv_ = pickle.loads(pickle.dumps(p_mv, -1))
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
                ###print(score, p_mv.start.x, p_mv.start.y, p_mv.end.x, p_mv.end.y)
                best_move = [best_move, p_mv][np.argmin([best_score, score])]
                best_score = np.min([best_score, score])
                ###print("BEST SCORE", best_score)
                ###print(np.argmax([best_score, score]))
                ###print("BEST MOVE", best_move, best_move.start.x, best_move.start.y, best_move.end.x, best_move.end.y)
                if best_score <= alpha:
                    return best_score, best_move
                beta = np.min([beta, best_score])
            ###print("BBBBESTTT MOOVEEE", best_move, best_move.start.x, best_move.start.y, best_move.end.x, best_move.end.y, best_score)
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

    def time_to_play(self, board, depth=3):
        board.draw()
        current_score = self._score_board(board)
        ###print("SCORE:", current_score)

        # all_possible_moves = self._get_possible_moves(board)
        # sel_move, sel_score = self._select_move_from_score(all_possible_moves)
        # sel_move, sel_score = self._search_tree(board, depth=3)
        board.draw()
        sel_score, sel_move = self._alpha_beta(board, depth=depth)
        board.draw()
        ###print("future score:", sel_score)
        ###print(sel_move.start.x, sel_move.start.y, sel_move.end.x, sel_move.end.y, self.color)

        return sel_move

    def _score_board(self, board):
        score = 0
        for piece_type in board.all_material[self.color]["alive"].keys():
            for piece in board.all_material[self.color]["alive"][piece_type]:
                score += self.piece_weights[piece_type]
                ###print(piece_type, piece.x, piece.y)
                score += self.piece_positions_weights[piece_type][piece.x][piece.y]

        adv_color = "white" if self.color == "black" else "black"

        for piece_type in board.all_material[adv_color]["alive"].keys():
            for piece in board.all_material[adv_color]["alive"][piece_type]:
                score -= self.piece_weights[piece_type]
                score -= self.piece_positions_weights[piece_type][piece.x][piece.y]
        return score
