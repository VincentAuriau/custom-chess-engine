if __name__ == "__main__":
    import sys

    sys.path.append("../pyalapin")
    import os
    import stockfish

    from pyalapin.player.stockfish_player import StockfishPlayer
    from pyalapin.player.player import Player
    from pyalapin.engine import ChessGame

    from settings import settings

    sfp = StockfishPlayer(settings["stockfish_path"], white_side=True)
    game = ChessGame()
    co1, co2 = sfp.get_move_from_fen(game.to_fen())
    game.board.draw()

    # sfp.quit()
    from pyalapin.interface import ChessApp

    sfp = StockfishPlayer(settings["stockfish_path"], white_side=False)
    app = ChessApp(w_player=Player(True), b_player=sfp, play_with_ai=True)
    app.run()
