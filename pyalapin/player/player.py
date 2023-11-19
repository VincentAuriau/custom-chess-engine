import numpy as np


class Player:
    """Base class players. If human player only here to ensure that right player is playing right Pieces.
    For AI-based players can implement more operations.

    Attributes
    ----------
    is_white_side : bool
        Whether the player plays with white or black Pieces.

    """

    def __init__(self, white_side):
        """Initialization of the player.

        Parameters
        ----------
        white_side : bool
            Whether the player plays with white or black pieces.
        """
        self.white_side = white_side
        self.random_number = np.random.randint(0, 1000, 1)

    def __str__(self):
        """Creates a string representation of the player.

        Returns
        -------
        str
            String representation of the player

        """
        return "NormalPlayer%i" % self.random_number

    def is_white_side(self):
        """Method to access the player's side.

        Returns
        -------
        bool
            color of pieces played by player.

        """
        return self.white_side

    def time_to_play(self, board):
        """Potential method that returns a move.


        Parameters
        ----------
        board : engine.Board on which to play.

        Returns
        -------
        move.Move move to operate on board.

        """
        pass


class AIRandomPlayer(Player):
    """
    A first AI that plays totally randomly. Selects one move among all possibles and plays it.
    """

    def __str__(self):
        """Creates a string representation of the player.

        Returns
        -------
        str
            String representation of the player
        """

        return "AIRandomPlayer"

    def time_to_play(self, board):
        """Potential method that returns a move.


        Parameters
        ----------
        board : engine.Board on which to play.

        Returns
        -------
        move.Move move to operate on board.
        """

        # Random selection of Piece to play
        for i in np.random.permutation(8):
            for j in np.random.permutation(8):
                # Verfies there is a Piece to play.
                if board.get_cell(i, j).get_piece() is not None:
                    if (
                        board.get_cell(i, j).get_piece().is_white()
                        == self.is_white_side()
                    ):
                        # Get potential moves
                        selected_piece = board.get_cell(i, j).get_piece()
                        print("AI Selected Piece", selected_piece)
                        possible_moves = selected_piece.get_potential_moves(i, j)

                        # We can must verify that a move is playable
                        verified_move = False
                        # Random selection of move
                        random_move = np.random.permutation(len(possible_moves))
                        index = 0
                        print(
                            "Verifying Moves,", len(possible_moves), "Moves Possibles"
                        )
                        # Stop only with a move that can be played.
                        while not verified_move and index < len(random_move):
                            # Select and check move.
                            selected_move = possible_moves[random_move[index]]
                            selected_move = Move(
                                self,
                                board,
                                board.get_cell(i, j),
                                board.get_cell(selected_move[0], selected_move[1]),
                            )
                            verified_move = selected_move.is_possible_move()
                            index += 1

                        # If move is ok, break loop and return it
                        if verified_move:
                            print("Move is verified, ")
                            return selected_move
        print("No moved found, aborting...")
