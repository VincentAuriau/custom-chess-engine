import sys

sys.path.append("pyalapin")

import pyalapin.engine.engine as engine


def test_blocked_moves():
    """
    Test that a blocked move cannot happen.
    """
    game = engine.ChessGame(automatic_draw=False)
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    _, winner = game.move_from_coordinates(game.player2, 7, 0, 5, 0)
    assert winner == 0


def test_promotion_to_rook():
    """
    Test that the promotion works well
    """
    game = engine.ChessGame(automatic_draw=False)
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
    assert (
        game.board.to_fen() == "rnbqkbRr/1pppp2p/7n/p7/8/8/PPPP1PPP/RNBQKBNR"
    ), game.board.to_fen()


def test_default_promotion():
    """
    Test that the promotion works well
    """
    game = engine.ChessGame(automatic_draw=False)
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 5, 4, 5)
    game.move_from_coordinates(game.player1, 3, 4, 4, 5)
    game.move_from_coordinates(game.player2, 7, 6, 5, 7)
    game.move_from_coordinates(game.player1, 4, 5, 5, 5)
    game.move_from_coordinates(game.player2, 6, 0, 5, 0)
    game.move_from_coordinates(game.player1, 5, 5, 6, 6)
    game.move_from_coordinates(game.player2, 5, 0, 4, 0)
    game.move_from_coordinates(game.player1, 6, 6, 7, 6)
    assert (
        game.board.to_fen() == "rnbqkbQr/1pppp2p/7n/p7/8/8/PPPP1PPP/RNBQKBNR"
    ), game.board.to_fen()


def test_working_castling():
    """Tests that small and big castling work."""
    game = engine.ChessGame(automatic_draw=False)
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
        game.board.to_fen()
        == "2kr1bnr/pppb1ppp/2np4/4p1q1/2B1P3/2N2N2/PPPPQPPP/R1B2RK1"
    ), game.board.to_fen()


def test_failing_castling():
    """Tests conditions where castling cannot be done."""
    game = engine.ChessGame(automatic_draw=False)
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
        game.board.to_fen() == "r1b1kbnr/pppp1ppp/2n5/4p1q1/2B1P3/5N2/PPPP1PPP/RNBQK2R"
    ), game.board.to_fen()


def test_en_passant():
    """Tests that prise en passant can be done."""
    game = engine.ChessGame(automatic_draw=False)
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 0, 5, 0)
    game.move_from_coordinates(game.player1, 3, 4, 4, 4)
    game.move_from_coordinates(game.player2, 6, 5, 4, 5)
    game.move_from_coordinates(game.player1, 4, 4, 5, 5)
    assert (
        game.board.to_fen() == "rnbqkbnr/1pppp1pp/p4P2/5p2/8/8/PPPP1PPP/RNBQKBNR"
    ), game.board.to_fen()


def test_blocked_by_mat():
    """Tests that if the king is checked cannot move unless it unchecks the king."""
    game = engine.ChessGame(automatic_draw=False)
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 5, 4, 5)
    game.move_from_coordinates(game.player1, 0, 3, 4, 7)
    _, status = game.move_from_coordinates(game.player2, 4, 5, 3, 4)
    assert status == 0


def test_end_game():
    """Tests what happens when check & mat happens."""
    game = engine.ChessGame(automatic_draw=False)
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 5, 4, 5)
    game.move_from_coordinates(game.player1, 0, 3, 4, 7)
    game.move_from_coordinates(game.player2, 6, 6, 5, 6)
    game.move_from_coordinates(game.player1, 3, 4, 4, 5)
    game.move_from_coordinates(game.player2, 6, 7, 5, 7)
    keep_going, status = game.move_from_coordinates(game.player1, 4, 7, 5, 6)
    print(keep_going, status)


def test_pgn():
    """Tests the pgn history of the game."""
    game = engine.ChessGame(automatic_draw=False, save_pgn=True)
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    game.move_from_coordinates(game.player2, 6, 5, 4, 5)
    game.move_from_coordinates(game.player1, 0, 3, 4, 7)
    game.move_from_coordinates(game.player2, 6, 6, 5, 6)
    print(game.to_pgn())
    assert game.to_pgn() == "1. e2e4 f7f5 2. Qd1h5+ g7g6"
