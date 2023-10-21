import sys

sys.path.append("../../python")
sys.path.append("python")

import engine.engine as engine

def test_blocked_moves():
    """
    Test that a blocked move does not happen.
    """
    print("ok")
    game = engine.Game(automatic_draw=False)
    game.move_from_coordinates(game.player1, 1, 4, 3, 4)
    _, winner = game.move_from_coordinates(game.player2, 7, 0, 5, 0)
    print("win", winner)
    assert winner == 0
