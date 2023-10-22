import sys

sys.path.append("../../python")
sys.path.append("python")

import engine.engine as engine


def test_blocked_moves():
    """
    Test that a blocked move does not happen.
    """
    game = engine.Game(automatic_draw=False)
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    _, winner = game.move_from_coordinates(game.player2, 7, 0, 5, 0)
    assert winner == 0


def test_promotion_to_rook():
    """
    Test that the promotion works well
    """
    game = engine.Game(automatic_draw=False)
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 5, 4, 5)
    game.move_from_coordinates(game.player1, 3, 4, 4, 5)
    game.move_from_coordinates(game.player2, 7, 6, 5, 7)
    game.move_from_coordinates(game.player1, 4, 5, 5, 5)
    game.move_from_coordinates(game.player2, 6, 0, 5, 0)
    game.move_from_coordinates(game.player1, 5, 5, 6, 6)
    game.move_from_coordinates(game.player2, 5, 0, 4, 0)
    game.move_from_coordinates(
        game.player1, 6, 6, 7, 6, extras={"promote_into": "rook"}
    )
    assert game.board.to_fen()[0] == "rnbqkbnr/pppp1ppp/8/8/P7/7N/1PPPP2P/RNBQKBrR"


def test_default_promotion():
    """
    Test that the promotion works well
    """
    game = engine.Game(automatic_draw=False)
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 5, 4, 5)
    game.move_from_coordinates(game.player1, 3, 4, 4, 5)
    game.move_from_coordinates(game.player2, 7, 6, 5, 7)
    game.move_from_coordinates(game.player1, 4, 5, 5, 5)
    game.move_from_coordinates(game.player2, 6, 0, 5, 0)
    game.move_from_coordinates(game.player1, 5, 5, 6, 6)
    game.move_from_coordinates(game.player2, 5, 0, 4, 0)
    game.move_from_coordinates(game.player1, 6, 6, 7, 6)
    assert game.board.to_fen()[0] == "rnbqkbnr/pppp1ppp/8/8/P7/7N/1PPPP2P/RNBQKBqR"


if __name__ == "__main__":
    pass
