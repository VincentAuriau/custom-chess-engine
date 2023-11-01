import os

import numpy as np

# import tensorflow as tf

from pyalapin.player.player import Player
import pyalapin.engine.material as material
import pyalapin.engine.move as move


class Memory(object):
    def __init__(self, max_memory=200):
        self.max_memory = max_memory
        self.memory = list()

    def remember(self, m):
        self.memory.append(m)
        self.memory = self.memory[max(len(self.memory) - self.max_memory, 0) :]

    def random_access(self):
        rn = np.random.randint(0, max(len(self.memory), 1))
        return self.memory[rn]


class MyPlayer(Player):
    def __init__(self, path_to_model="", epsilon_explorer=0.15, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = "white" if self.white_side else "black"
        self.path_to_model = path_to_model
        self.epsilon_explorer = epsilon_explorer

        in_ = tf.keras.layers.Input(shape=(8, 8, 6))
        out = tf.keras.layers.Conv2D(16, kernel_size=3, padding="SAME")(in_)
        out = tf.keras.layers.Conv2D(32, kernel_size=3, padding="SAME")(out)
        out = tf.keras.layers.Conv2D(16, kernel_size=3, padding="SAME", strides=2)(out)
        out = tf.keras.layers.Conv2D(8, kernel_size=3, padding="SAME", strides=2)(out)
        out = tf.keras.layers.Flatten()(out)
        out = tf.keras.layers.Dense(8)(out)
        out = tf.keras.layers.Dense(1)(out)
        if path_to_model == "":
            self.path_to_model = "./"
            for _ in range(10):
                self.path_to_model += str(np.random.randint(10))

        if not os.path.exists(path_to_model):
            self.model = tf.keras.Model(inputs=in_, outputs=out)
            self.model.compile(loss="mse", optimizer="Adam")
        else:
            print("Loading Model")
            self.model = tf.keras.models.load_model(path_to_model)
            self.model.compile(loss="mse", optimizer="Adam")
            print("Model Loaded")
        print(self.model.summary())
        self.memory = Memory()

    def _score_board(self, board, white_side=None):
        if white_side == None:
            white_side = self.white_side

        one_hot_encode_board = board.one_hot_encode()

        if self.white_side != white_side:
            one_hot_encode_board = np.flip(one_hot_encode_board)

        score = self.model.predict(
            np.expand_dims(one_hot_encode_board, 0).astype("float32")
        )
        return score[0][0]

    def _get_possible_moves(self, board, is_white=None):
        if is_white is None:
            is_white = self.white_side()

        color = {True: "white", False: "black"}[is_white]
        possible_moves = []
        for type_piece in board.all_material[color]["alive"].keys():
            for piece in board.all_material[color]["alive"][type_piece]:
                piece_available_moves = piece.get_potential_moves(piece.x, piece.y)
                for mv in piece_available_moves:
                    selected_move = move.Move(
                        self,
                        board,
                        board.get_cell(piece.x, piece.y),
                        board.get_cell(mv[0], mv[1]),
                    )
                    if selected_move.is_possible_move():
                        possible_moves.append(selected_move)
        return possible_moves

    def _select_move_from_score(self, moves, train=True):
        if train:
            do_random_move = np.random.randint(100) <= self.epsilon_explorer * 100
            if do_random_move:
                print("RANDOM MOVE SELECTED")
                index_random_move = np.random.randint(len(moves))
                random_move = moves[index_random_move]
                mv_ = random_move.deepcopy()
                mv_.move_pieces()
                random_score = self._score_board(mv_.board)
                return random_move, random_score

        all_scores = {}
        for mv in moves:
            mv_ = mv.deepcopy()
            mv_.move_pieces()
            score = self._score_board(mv_.board)
            all_scores[mv] = score

        scores = list(all_scores.values())
        all_indexes = np.where(scores == np.max(scores))[0]

        perm = np.random.permutation(len(all_indexes))[0]
        final_index = all_indexes[perm]
        return list(all_scores.keys())[int(final_index)], scores[final_index]

    def _base_scoring(self, board, game_is_won="", white_side=None):
        if white_side is None:
            white_side = self.white_side
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

        score = 0
        for piece_type in board.all_material["white"]["alive"].keys():
            for piece in board.all_material["white"]["alive"][piece_type]:
                score += piece_weights[piece_type]
                score += np.flip(piece_positions_weights[piece_type])[piece.x][piece.y]

        for piece_type in board.all_material["black"]["alive"].keys():
            for piece in board.all_material["black"]["alive"][piece_type]:
                score -= piece_weights[piece_type]
                score -= piece_positions_weights[piece_type][piece.x][piece.y]
        if not white_side:
            score = -1 * score
        if game_is_won:
            score += 1000
        elif not game_is_won:
            score -= 1000

        return score

    def _reinforce(self, board, best_next_score, batch_size=12, white_side=None):
        if white_side is None:
            white_side = self.white_side
        score = self._base_scoring(board, white_side=white_side)
        print("SCORE during reinforce phase", score)
        self.memory.remember((board.one_hot_encode(white_side=white_side), score))

        input_states = np.zeros((batch_size, 8, 8, 6))
        target_q = np.zeros((batch_size, 1))

        for i in range(batch_size):
            (s_i, r_i) = self.memory.random_access()
            input_states[i] = s_i
            target_q[i] = r_i
        self.model.train_on_batch(input_states, target_q)
        self.model.save(self.path_to_model)

    def __str__(self):
        return "MyAIPlayer"

    def time_to_play(self, board, white_side=None):
        if white_side is None:
            white_side = self.is_white_side()
        possible_moves = self._get_possible_moves(board, is_white=white_side)
        best_move, best_score = self._select_move_from_score(possible_moves)

        self._reinforce(board, best_score, white_side=white_side)
        return best_move
