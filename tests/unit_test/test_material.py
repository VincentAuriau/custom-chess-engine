import sys

sys.path.append("pyalapin")

import engine.engine as engine
import engine.material as material

# Add verifications about own color of piece on end cell
#


def test_pawn_moves():
    x_start = 1
    y_start = 0
    pawn = material.Pawn(white=True, x=x_start, y=y_start)
    start_cell = engine.Cell(x=x_start, y=y_start, piece=pawn)

    # Assert can go forward
    x_end = 2
    y_end = 0
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert pawn.piece_move_authorized(start_cell, end_cell)

    # Assert can go forward by two cells
    x_end = 3
    y_end = 0
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert pawn.piece_move_authorized(start_cell, end_cell)

    # Assert cann go diagonal if adversary piece
    x_end = 2
    y_end = 1
    end_cell = engine.Cell(x=x_end, y=y_end, piece=material.Pawn(False, x_end, y_end))
    assert pawn.piece_move_authorized(start_cell, end_cell)

    # Assert cannot go forward by three cells
    x_end = 4
    y_end = 0
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not pawn.piece_move_authorized(start_cell, end_cell)

    # Assert cannot go backward
    x_end = 0
    y_end = 0
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not pawn.piece_move_authorized(start_cell, end_cell)

    # Assert cannot go on the side
    x_end = 1
    y_end = 1
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not pawn.piece_move_authorized(start_cell, end_cell)

    # Assert cannot go diagonal without piece
    x_end = 2
    y_end = 1
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not pawn.piece_move_authorized(start_cell, end_cell)

    # Assert cannot further than the board
    x_end = 1
    y_end = -1
    end_cell = engine.Cell(x=x_end, y=y_end, piece=material.Pawn(False, x_end, y_end))
    assert not pawn.piece_move_authorized(start_cell, end_cell)


def test_bishop_moves():
    x_start = 1
    y_start = 2
    bishop = material.Bishop(white=True, x=x_start, y=y_start)
    start_cell = engine.Cell(x=x_start, y=y_start, piece=bishop)

    # Assert can go diagonals
    x_end = 0
    y_end = 1
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert bishop.piece_move_authorized(start_cell, end_cell)
    x_end = 0
    y_end = 3
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert bishop.piece_move_authorized(start_cell, end_cell)
    x_end = 3
    y_end = 0
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert bishop.piece_move_authorized(start_cell, end_cell)
    x_end = 6
    y_end = 7
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert bishop.piece_move_authorized(start_cell, end_cell)

    # Assert cannot go differently than diagonals
    x_end = 4
    y_end = 0
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not bishop.piece_move_authorized(start_cell, end_cell)
    x_end = 1
    y_end = 5
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not bishop.piece_move_authorized(start_cell, end_cell)
    x_end = 0
    y_end = 2
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not bishop.piece_move_authorized(start_cell, end_cell)
    x_end = 4
    y_end = 4
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)

    # Assrt cannot go futher than the board
    assert not bishop.piece_move_authorized(start_cell, end_cell)
    x_end = -1
    y_end = 0
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not bishop.piece_move_authorized(start_cell, end_cell)
    x_end = 7
    y_end = 8
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not bishop.piece_move_authorized(start_cell, end_cell)


def test_knight_moves():
    x_start = 2
    y_start = 2
    knight = material.Knight(white=True, x=x_start, y=y_start)
    start_cell = engine.Cell(x=x_start, y=y_start, piece=knight)

    # Assert can go everywhere it is supposed to
    x_end = 0
    y_end = 3
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert knight.piece_move_authorized(start_cell, end_cell)
    x_end = 0
    y_end = 1
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert knight.piece_move_authorized(start_cell, end_cell)
    x_end = 1
    y_end = 0
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert knight.piece_move_authorized(start_cell, end_cell)
    x_end = 3
    y_end = 0
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert knight.piece_move_authorized(start_cell, end_cell)
    x_end = 4
    y_end = 1
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert knight.piece_move_authorized(start_cell, end_cell)
    x_end = 4
    y_end = 3
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert knight.piece_move_authorized(start_cell, end_cell)
    x_end = 3
    y_end = 4
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert knight.piece_move_authorized(start_cell, end_cell)
    x_end = 1
    y_end = 4
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert knight.piece_move_authorized(start_cell, end_cell)

    # Assert cannot go differently
    x_end = 4
    y_end = 0
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not knight.piece_move_authorized(start_cell, end_cell)
    x_end = 2
    y_end = 2
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not knight.piece_move_authorized(start_cell, end_cell)
    x_end = 2
    y_end = 1
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not knight.piece_move_authorized(start_cell, end_cell)
    x_end = 1
    y_end = 2
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not knight.piece_move_authorized(start_cell, end_cell)
    x_end = 4
    y_end = 7
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not knight.piece_move_authorized(start_cell, end_cell)


def test_rook_moves():
    x_start = 2
    y_start = 2
    rook = material.Rook(white=True, x=x_start, y=y_start)
    start_cell = engine.Cell(x=x_start, y=y_start, piece=rook)

    # Assert can go everywhere it is supposed to
    x_end = 2
    y_end = 7
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert rook.piece_move_authorized(start_cell, end_cell)
    x_end = 2
    y_end = 0
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert rook.piece_move_authorized(start_cell, end_cell)
    x_end = 7
    y_end = 2
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert rook.piece_move_authorized(start_cell, end_cell)
    x_end = 0
    y_end = 2
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert rook.piece_move_authorized(start_cell, end_cell)

    # Assert cannot go differently
    x_end = 4
    y_end = 0
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not rook.piece_move_authorized(start_cell, end_cell)
    x_end = 0
    y_end = 4
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not rook.piece_move_authorized(start_cell, end_cell)
    x_end = 2
    y_end = -1
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not rook.piece_move_authorized(start_cell, end_cell)
    x_end = 8
    y_end = 2
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not rook.piece_move_authorized(start_cell, end_cell)


def test_queen_moves():
    x_start = 2
    y_start = 2
    queen = material.Queen(white=True, x=x_start, y=y_start)
    start_cell = engine.Cell(x=x_start, y=y_start, piece=queen)

    # Assert can go everywhere it is supposed to
    x_end = 2
    y_end = 7
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert queen.piece_move_authorized(start_cell, end_cell)
    x_end = 7
    y_end = 2
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert queen.piece_move_authorized(start_cell, end_cell)
    x_end = 2
    y_end = 0
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert queen.piece_move_authorized(start_cell, end_cell)
    x_end = 0
    y_end = 2
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert queen.piece_move_authorized(start_cell, end_cell)
    x_end = 0
    y_end = 0
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert queen.piece_move_authorized(start_cell, end_cell)
    x_end = 7
    y_end = 7
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert queen.piece_move_authorized(start_cell, end_cell)
    x_end = 0
    y_end = 4
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert queen.piece_move_authorized(start_cell, end_cell)
    x_end = 4
    y_end = 0
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert queen.piece_move_authorized(start_cell, end_cell)

    # Assert cannot go differently
    x_end = 4
    y_end = 1
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not queen.piece_move_authorized(start_cell, end_cell)
    x_end = 1
    y_end = 4
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not queen.piece_move_authorized(start_cell, end_cell)
    x_end = 3
    y_end = 6
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not queen.piece_move_authorized(start_cell, end_cell)
    x_end = 6
    y_end = 3
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not queen.piece_move_authorized(start_cell, end_cell)
    x_end = 2
    y_end = -2
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not queen.piece_move_authorized(start_cell, end_cell)
    x_end = 8
    y_end = 2
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not queen.piece_move_authorized(start_cell, end_cell)


def test_king_moves():
    x_start = 2
    y_start = 2
    king = material.King(white=True, x=x_start, y=y_start)
    start_cell = engine.Cell(x=x_start, y=y_start, piece=king)

    # Assert can go everywhere it is supposed to
    x_end = 2
    y_end = 1
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert king.piece_move_authorized(start_cell, end_cell)
    x_end = 1
    y_end = 2
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert king.piece_move_authorized(start_cell, end_cell)
    x_end = 2
    y_end = 3
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert king.piece_move_authorized(start_cell, end_cell)
    x_end = 3
    y_end = 2
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert king.piece_move_authorized(start_cell, end_cell)
    x_end = 1
    y_end = 3
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert king.piece_move_authorized(start_cell, end_cell)
    x_end = 1
    y_end = 1
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert king.piece_move_authorized(start_cell, end_cell)
    x_end = 3
    y_end = 1
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert king.piece_move_authorized(start_cell, end_cell)
    x_end = 3
    y_end = 3
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert king.piece_move_authorized(start_cell, end_cell)

    # Assert cannot go differently
    x_end = 4
    y_end = 1
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not king.piece_move_authorized(start_cell, end_cell)
    x_end = 1
    y_end = 4
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not king.piece_move_authorized(start_cell, end_cell)
    x_end = 2
    y_end = 2
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not king.piece_move_authorized(start_cell, end_cell)
    x_end = 4
    y_end = 4
    end_cell = engine.Cell(x=x_end, y=y_end, piece=None)
    assert not king.piece_move_authorized(start_cell, end_cell)
