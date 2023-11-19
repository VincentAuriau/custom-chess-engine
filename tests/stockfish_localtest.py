if __name__=="__main__":
	import sys
	sys.path.append("../pyalapin")

	import os
	print(os.listdir())
	print(os.listdir("pyalapin"))
	import stockfish

	from pyalapin.player.stockfish_player import StockfishPlayer
	from pyalapin.player.player import Player
	from pyalapin.engine import ChessGame


	sfp = StockfishPlayer("/Users/vincent.auriau/Python/stockfish/bin/stockfish", white_side=True)
	game = ChessGame()
	print("FEN:", game.to_fen())
	print("IS VALID?", sfp.stockfish.is_fen_valid(game.to_fen()))
	co1, co2 = sfp.get_move_from_fen(game.to_fen())
	game.board.draw()

	game.move_from_coordinates(game.player1, *co1, *co2)
	game.board.draw()

	# sfp.quit()

	from pyalapin.interface import ChessApp
	sfp = StockfishPlayer("/Users/vincent.auriau/Python/stockfish/bin/stockfish", white_side=False)
	app = ChessApp(w_player=Player(True), b_player=sfp, play_with_ai=True)
	app.run()
