import sys

sys.path.append("pyalapin")

import engine.engine as engine
import importlib
import engine.move as move
import time

importlib.reload(engine)
import player.ai_player as ai_player


def test_working_castling():
    game = engine.Game()
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    print("///", game.board.all_material["black"]["alive"]["king"][0].has_moved)
    game.move_from_coordinates(game.player2, 6, 4, 4, 4)
    print("///", game.board.all_material["black"]["alive"]["king"][0].has_moved)
    game.move_from_coordinates(game.player1, 0, 5, 3, 2)
    print("///", game.board.all_material["black"]["alive"]["king"][0].has_moved)
    game.move_from_coordinates(game.player2, 7, 3, 4, 6)
    print("///", game.board.all_material["black"]["alive"]["king"][0].has_moved)
    game.move_from_coordinates(game.player1, 0, 6, 2, 5)
    print("///", game.board.all_material["black"]["alive"]["king"][0].has_moved)
    game.move_from_coordinates(game.player2, 7, 1, 5, 2)
    print("///", game.board.all_material["black"]["alive"]["king"][0].has_moved)

    # small castling move
    game.move_from_coordinates(game.player1, 0, 4, 0, 6)
    print("///", game.board.all_material["black"]["alive"]["king"][0].has_moved)

    game.move_from_coordinates(game.player2, 6, 3, 5, 3)
    print("///", game.board.all_material["black"]["alive"]["king"][0].has_moved)
    game.move_from_coordinates(game.player1, 0, 1, 2, 2)
    print("///", game.board.all_material["black"]["alive"]["king"][0].has_moved)
    game.move_from_coordinates(game.player2, 7, 2, 6, 3)
    print("///", game.board.all_material["black"]["alive"]["king"][0].has_moved)
    game.move_from_coordinates(game.player1, 0, 3, 1, 4)
    print("///", game.board.all_material["black"]["alive"]["king"][0].has_moved)

    # big castling move
    print("big castling")
    print("///", game.board.all_material["black"]["alive"]["king"][0].has_moved)
    game.move_from_coordinates(game.player2, 7, 4, 7, 2)
    game.draw_board()


def test_failing_castling():
    game = engine.Game()
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 4, 4, 4)
    game.move_from_coordinates(game.player1, 0, 5, 3, 2)
    game.move_from_coordinates(game.player2, 7, 3, 4, 6)
    game.move_from_coordinates(game.player1, 0, 6, 2, 5)
    game.move_from_coordinates(game.player2, 7, 1, 5, 2)

    # Rook movement
    game.move_from_coordinates(game.player1, 0, 7, 0, 6)
    game.move_from_coordinates(game.player2, 4, 6, 4, 7)
    game.move_from_coordinates(game.player1, 0, 6, 0, 7)
    game.move_from_coordinates(game.player2, 4, 7, 4, 6)

    # small castling move
    game.move_from_coordinates(game.player1, 0, 4, 0, 6)


def test_blocked_moves():
    game = engine.Game()
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 7, 0, 5, 0)


def test_en_passant():
    game = engine.Game()
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 0, 5, 0)
    game.move_from_coordinates(game.player1, 3, 4, 4, 4)
    game.move_from_coordinates(game.player2, 6, 5, 4, 5)
    game.move_from_coordinates(game.player1, 4, 4, 5, 5)


def test_end_game():
    game = engine.Game()
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 5, 4, 5)
    game.move_from_coordinates(game.player1, 0, 3, 4, 7)
    game.move_from_coordinates(game.player2, 4, 5, 3, 4)
    game.move_from_coordinates(game.player1, 4, 7, 7, 4)


def test_pawn_transformation():
    game = engine.Game()
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 5, 4, 5)
    game.move_from_coordinates(game.player1, 0, 3, 4, 7)
    game.move_from_coordinates(game.player2, 4, 5, 3, 4)
    game.move_from_coordinates(game.player1, 0, 4, 0, 3)
    game.move_from_coordinates(game.player2, 3, 4, 2, 4)
    game.move_from_coordinates(game.player1, 1, 3, 2, 3)
    game.move_from_coordinates(game.player2, 2, 4, 1, 4)
    game.move_from_coordinates(game.player1, 1, 5, 2, 5)
    game.move_from_coordinates(game.player2, 1, 4, 0, 4)


def check_unchecking():
    game = engine.Game()
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 5, 4, 5)
    game.move_from_coordinates(game.player1, 0, 3, 4, 7)
    game.move_from_coordinates(game.player2, 6, 6, 5, 6)


def test_blocked_double_pawn():
    game = engine.Game()
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 5, 4, 5)
    game.move_from_coordinates(game.player1, 3, 4, 4, 4)
    game.move_from_coordinates(game.player2, 4, 5, 3, 5)
    game.move_from_coordinates(game.player1, 4, 4, 5, 4)
    game.move_from_coordinates(game.player2, 6, 4, 4, 4)


def test_king_taking_queen():
    game = engine.Game()
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 0, 5, 0)
    game.move_from_coordinates(game.player1, 0, 3, 4, 7)
    game.move_from_coordinates(game.player2, 5, 0, 4, 0)
    game.move_from_coordinates(game.player1, 4, 7, 6, 7)
    game.move_from_coordinates(game.player2, 4, 0, 3, 0)
    game.move_from_coordinates(game.player1, 6, 7, 7, 7)
    game.move_from_coordinates(game.player2, 3, 0, 2, 0)
    game.move_from_coordinates(game.player1, 7, 7, 7, 6)
    game.move_from_coordinates(game.player2, 6, 1, 5, 1)
    game.move_from_coordinates(game.player1, 7, 6, 7, 5)
    game.move_from_coordinates(game.player2, 7, 4, 7, 5)


def specific_test():
    game = engine.Game()
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 5, 5, 5)
    game.move_from_coordinates(game.player1, 0, 3, 4, 7)
    game.move_from_coordinates(game.player2, 6, 6, 5, 6)

    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% barrel 1")

    game.move_from_coordinates(game.player1, 4, 7, 6, 7)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% barrel 2")
    game.move_from_coordinates(game.player2, 6, 0, 5, 0)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% barrel 3")
    game.move_from_coordinates(game.player1, 6, 7, 7, 7)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% barrel 4")

    game.move_from_coordinates(game.player2, 7, 5, 5, 7)
    game.move_from_coordinates(game.player1, 7, 7, 7, 6)
    game.move_from_coordinates(game.player2, 5, 7, 7, 5)
    game.move_from_coordinates(game.player1, 7, 6, 5, 6)
    game.move_from_coordinates(game.player2, 7, 0, 6, 0)
    # game.save()


def possible_moves():
    game = engine.Game()
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 7, 1, 5, 2)
    game.move_from_coordinates(game.player1, 3, 4, 4, 4)
    game.move_from_coordinates(game.player2, 5, 2, 4, 4)
    game.move_from_coordinates(game.player1, 0, 3, 4, 7)
    game.move_from_coordinates(game.player2, 4, 4, 3, 2)
    game.draw_board()
    print(game.board.all_material["white"]["alive"]["bishop"])
    for piece in game.board.all_material["white"]["alive"]["bishop"]:
        piece_available_moves = piece.get_potential_moves(piece.x, piece.y)
        print(piece_available_moves)
        for mv in piece_available_moves:
            print(mv)
            selected_move = move.Move(
                game.player1,
                game.board,
                game.board.get_cell(piece.x, piece.y),
                game.board.get_cell(mv[0], mv[1]),
            )
            if selected_move.is_possible_move():
                print("move ok")
            else:
                print("move not ok")


def test_player():
    player = ai_player.EasyAIPlayer(False)
    game = engine.Game()
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 4, 4, 4)
    score = player._score_board(game.board)
    print("score", score)
    game = engine.Game()
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 4, 5, 4)
    score = player._score_board(game.board)
    print(score)


if __name__ == "__main__":
    check_unchecking()
    test_working_castling()
    test_failing_castling()
    test_blocked_moves()
    test_en_passant()
    test_end_game()
    test_pawn_transformation()
    test_blocked_double_pawn()
    test_king_taking_queen()
    specific_test()
    possible_moves()
    test_player()
    print("Tests finished")

    import sys

    print(sys.executable)
