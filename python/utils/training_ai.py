from my_player import MyPlayer
import engine

# ai = MyPlayer(white_side=True, path_to_model="./test1")

for kiwi in range(100):
    print("KIWI __ KIWI:", kiwi)
    ai = MyPlayer(white_side=True, path_to_model="./test3")
    game = engine.Game(automatic_draw=False, ai=False)
    for i in range(100):
        print(i)
        ai_move = ai.time_to_play(game.board, white_side=True)
        game_is_on = game.move(ai_move, game.player1)
        game.board.draw()
        print(game_is_on)
        if not game_is_on[0]:
            print(game_is_on)
            break

        ai_move = ai.time_to_play(game.board, white_side=False)
        game_is_on = game.move(ai_move, game.player2)
        game.board.draw()
        if not game_is_on[0]:
            print(game_is_on)
            break
