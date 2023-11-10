from stockfish import Stockfish

from pyalapin.player.player import Player
from pyalapin.engine.move import Move


class StockfishPlayer(Player):
    """
    A first AI that plays totally randomly. Selects one move among all possibles and plays it.
    """

    def __init__(self, path_to_dirsave, elo=1000, **kwargs):
        super().__init__(**kwargs)
        self.elo = elo
        self.path_to_dirsave = path_to_dirsave
        self.stockfish = Stockfish()

        self.letter_to_coordinate = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7,
        }

    def __str__(self):
        """Creates a string representation of the player.

        Returns
        -------
        str
            String representation of the player
        """

        return "Stockfish of elo {self.elo}"

    def quit(self):
        self.stockfish.send_quit_command()

    def time_to_play(self, board):
        """Potential method that returns a move.


        Parameters
        ----------
        board : engine.Board on which to play.

        Returns
        -------
        move.Move move to operate on board.
        """

        fen_repr = board.to_fen()
        self.stockfish.set_fen_position(fen_repr)
        stockfish_move = self.stockfish.get_best_move()

        print(stockfish_move)

        start_cell_coordinates = (self.letter_to_coordinate[stockfish_move[0]], 
            int(stockfish_move[1])-1)
        end_cell_coordinates = (self.letter_to_coordinate[stockfish_move[2]], 
            int(stockfish_move[3])-1)

        move = Move(self, board, board.get_cell(*start_cell_coordinates), board.get_cell(*end_cell_coordinates))
        return move
        
