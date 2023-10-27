import sys

sys.path.append("../../python")
sys.path.append("python")

import engine.engine as engine


def test_blocked_moves():
    """
    Test that a blocked move cannot happen.
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


def test_working_castling():
    """Tests that small and big castling work."""
    game = engine.Game(automatic_draw=False)
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 4, 4, 4)
    game.move_from_coordinates(game.player1, 0, 5, 3, 2)
    game.move_from_coordinates(game.player2, 7, 3, 4, 6)
    game.move_from_coordinates(game.player1, 0, 6, 2, 5)
    game.move_from_coordinates(game.player2, 7, 1, 5, 2)

    # small castling move
    game.move_from_coordinates(game.player1, 0, 4, 0, 6)

    game.move_from_coordinates(game.player2, 6, 3, 5, 3)
    game.move_from_coordinates(game.player1, 0, 1, 2, 2)
    game.move_from_coordinates(game.player2, 7, 2, 6, 3)
    game.move_from_coordinates(game.player1, 0, 3, 1, 4)

    # big castling move
    game.move_from_coordinates(game.player2, 7, 4, 7, 2)
    assert (
        game.board.to_fen()[0]
        == "r1b2rk1/ppppqppp/2n2n2/2b1p3/4P1Q1/2NP4/PPPB1PPP/2KR1BNR"
    )


def test_failing_castling():
    """Tests conditions where castling cannot be done."""
    game = engine.Game(automatic_draw=False)
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
    _, status = game.move_from_coordinates(game.player1, 0, 4, 0, 6)
    assert status == 0
    assert (
        game.board.to_fen()[0]
        == "rnbqk2r/pppp1ppp/5n2/2b1p3/4P1Q1/2N5/PPPP1PPP/R1B1KBNR"
    )


def test_en_passant():
    """Tests that prise en passant can be done."""
    game = engine.Game(automatic_draw=False)
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 0, 5, 0)
    game.move_from_coordinates(game.player1, 3, 4, 4, 4)
    game.move_from_coordinates(game.player2, 6, 5, 4, 5)
    game.move_from_coordinates(game.player1, 4, 4, 5, 5)
    assert game.board.to_fen()[0] == "rnbqkbnr/pppp1ppp/8/8/5P2/P4p2/1PPPP1PP/RNBQKBNR"


def test_blocked_by_mat():
    """Tests that if the king is checked cannot move unless it unchecks the king."""
    game = engine.Game(automatic_draw=True)
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 5, 4, 5)
    game.move_from_coordinates(game.player1, 0, 3, 4, 7)
    _, status = game.move_from_coordinates(game.player2, 4, 5, 3, 4)
    assert status == 0


def test_end_game():
    """Tests what happens when check & mat happens."""
    game = engine.Game(automatic_draw=True)
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 5, 4, 5)
    game.move_from_coordinates(game.player1, 0, 3, 4, 7)
    game.move_from_coordinates(game.player2, 6, 6, 5, 6)
    game.move_from_coordinates(game.player1, 3, 4, 4, 5)
    game.move_from_coordinates(game.player2, 6, 7, 5, 7)
    keep_going, status = game.move_from_coordinates(game.player1, 4, 7, 5, 6)
    print(keep_going, status)


if __name__ == "__main__":
    test_en_passant()
    test_end_game()
