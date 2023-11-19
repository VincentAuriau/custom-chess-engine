from stockfish import Stockfish

from pyalapin.player.player import Player
from pyalapin.engine.move import Move


class StockfishPlayer(Player):
    """
    A first AI that plays totally randomly. Selects one move among all possibles and plays it.
    """

    def __init__(
        self, path_to_dirsave, elo=1000, depth=18, threads=1, hash_pow=4, **kwargs
    ):
        super().__init__(**kwargs)
        self.elo = elo
        self.path_to_dirsave = path_to_dirsave
        self.depth = depth
        self.threads = threads
        self.hash = 2**hash_pow

        params = {
            "Threads": self.threads,
            "Hash": self.hash,
            "UCI_Elo": self.elo,
        }
        self.stockfish = Stockfish(
            path=self.path_to_dirsave, depth=self.depth, parameters=params
        )

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

    def _sf_to_own_coordinates(self, coordinates):
        return (int(coordinates[1]) - 1, self.letter_to_coordinate[coordinates[0]])

    def get_move_from_fen(self, fen):
        self.stockfish.set_fen_position(fen)
        stockfish_move = self.stockfish.get_best_move()
        print(f"StockFish best move: {stockfish_move}")
        start_cell_coordinates = self._sf_to_own_coordinates(stockfish_move[:2])
        end_cell_coordinates = self._sf_to_own_coordinates(stockfish_move[2:])

        print("Transformed Coordinates", start_cell_coordinates, end_cell_coordinates)
        return start_cell_coordinates, end_cell_coordinates

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
        print(fen_repr)
        start, end = self.get_move_from_fen(fen_repr)
        move = Move(self, board, board.get_cell(*start), board.get_cell(*end))
        print(move, board.get_cell(*start), board.get_cell(*end))
        return move
