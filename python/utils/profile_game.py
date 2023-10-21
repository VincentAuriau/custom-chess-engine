import copy
import sys

sys.path.append("../")

import engine.engine as engine

# import move
# import time
# import ai_player

game = engine.Game(automatic_draw=False, ai=True)
print(game.board.one_hot_encode())
print(game.board.to_fen())
print(game.to_fen())
validated_move, winner = game.move_from_coordinates(game.player1, 1, 4, 3, 4)
ai_move = game.player2.time_to_play(game.board)
game_is_on = game.move(ai_move, game.player2)

from player.my_player import MyPlayer

my_player = MyPlayer(white_side=False)
game = engine.Game(automatic_draw=False, ai=True)
validated_move, winner = game.move_from_coordinates(game.player1, 1, 4, 3, 4)
ai_move = my_player.time_to_play(game.board)
game_is_on = game.move(ai_move, game.player2)
score = my_player._score_board(game.board)
print(my_player.model.summary())
