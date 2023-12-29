import numpy as np
import os

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from kivy.graphics import Rectangle, Color, Canvas

from pyalapin.engine.engine import ChessGame


class DisplayableCell(Button):
    """Base class to represent a Cell as Button"""

    def __init__(self, row, column, **kwargs):
        """
        Initialization of the representation of the cell.

        Parameters
        ----------

        row: int
            row coordinate of the Cell
        column: int
            column coordinate of the Cell
        """
        super(DisplayableCell, self).__init__(**kwargs)
        self.row = row
        self.column = column


class BoardInterface(GridLayout):
    """
    Main class to represent and display the board, as well as to play a chess game.

    Attributes
    ----------
    path_to_illustrations: str
        Path to the images to use to display cells & pieces
    game: engine.ChessGame
        game to actually represent
    ai_playing: bool
        whether or not an AI is playing (only one of the players for now)
    cols: int
        number of columns of the board
    rows: int
        number of rows of the board
    to_play_player: player.Player
        player who should play next
    first_cell_clicked: engince.Cell or None
        First part of a piece movement, used to memorize the first cell selected by user who would like to move a piece.
    cells: list of DisplayableCells
        List of cells constituting the board
    """

    def __init__(self, game, **kwargs):
        """
        Initialization of the board display.

        Parameters
        ----------
        game: engine.Game to represent

        """
        super(BoardInterface, self).__init__(**kwargs)
        if os.path.isdir("temp_images"):
            imgs = []
            for z in os.listdir("temp_images"):
                if "png" in z:
                    imgs.append(z)
            if len(imgs) == len(os.listdir("illustrations")):
                self.path_to_illustrations = "temp_images"
            else:
                self.path_to_illustrations = "illustrations"
        else:
            self.path_to_illustrations = "illustrations"

        self.game = game

        if game.ai:
            self.ai_playing = True
        else:
            self.ai_playing = False

        self.cols = 8
        self.rows = 8

        self.to_play_player = game.player1

        self.first_cell_clicked = None

        self.cells = []

        # Initialization of the display of the board
        for i in range(self.rows):
            line = []
            for j in range(self.cols):
                # Alternate cells color for better board perception
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    color = (0.4, 0.4, 0.8, 1)
                    c_img = "b"
                else:
                    color = (0.4, 0.8, 0.4, 1)
                    c_img = "w"
                # self.add_widget(Button(text='Button %i %i' % (i, j), background_color=color,
                #                 background_down='illustrations/white_pawn.png',
                #                 background_normal='illustrations/white_queen.png'))
                piece = game.board.get_cell(i, j).get_piece()

                if piece is not None:
                    path_to_img = c_img

                    if piece.is_white():
                        piece_color = (1, 1, 1, 1)  # For text color, could be removed
                        path_to_img += "w"
                    else:
                        piece_color = (0, 0, 0, 1)
                        path_to_img += "b"
                    path_to_img += "_" + piece.get_str().replace(" ", "") + ".png"
                    path_to_down_img = "down_" + path_to_img

                    path_to_img = os.path.join(self.path_to_illustrations, path_to_img)
                    path_to_down_img = os.path.join(
                        self.path_to_illustrations, path_to_down_img
                    )

                    piece = piece.get_str()
                    button = DisplayableCell(
                        # text=piece, # Remove it for prettier results :)
                        on_press=self.click_cell,
                        row=i,
                        column=j,
                        color=piece_color,
                        background_normal=path_to_img,
                        border=(0, 0, 0, 0),
                        background_down=path_to_down_img,
                    )
                else:
                    # No piece to display
                    piece = ""
                    piece_color = (1, 1, 1, 1)  # For text color could be removed
                    path_to_img = c_img + ".png"
                    # Unclicked
                    path_to_down_img = "down_" + path_to_img

                    path_to_img = os.path.join(self.path_to_illustrations, path_to_img)
                    path_to_down_img = os.path.join(
                        self.path_to_illustrations, path_to_down_img
                    )

                    button = DisplayableCell(
                        # text=piece, # Remove for prettier results :)
                        background_normal=path_to_img,
                        on_press=self.click_cell,
                        row=i,
                        column=j,
                        color=piece_color,
                        border=(0, 0, 0, 0),
                        background_down=path_to_down_img,
                    )
                self.add_widget(button)
                line.append(button)
            self.cells.append(line)

    def reset_game(self, button):
        """
        Method used to reset a game when clicked on the reset button

        Parameters
        ----------
        button: Button
            button used to click for reset
        """
        print("On click, Reset", button)
        self.game.reset_game()
        self.update()

    def update(self):
        """
        Method used to update the display of the board. Actually redraws everythin from start.
        """
        board = self.game.board
        for i in range(self.rows):
            for j in range(self.cols):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    c_img = "b"
                else:
                    c_img = "w"

                piece = board.get_cell(i, j).get_piece()
                if piece is not None:
                    path_to_img = c_img
                    if piece.is_white():
                        piece_color = (1, 1, 1, 1)
                        path_to_img += "w"
                    else:
                        piece_color = (0, 0, 0, 1)
                        path_to_img += "b"
                    piece = piece.get_str()
                    path_to_img += "_" + piece.replace(" ", "") + ".png"
                else:
                    piece = ""
                    piece_color = (1, 1, 1, 1)
                    path_to_img = c_img + ".png"

                path_to_down_img = "down_" + path_to_img
                path_to_img = os.path.join(self.path_to_illustrations, path_to_img)
                path_to_down_img = os.path.join(
                    self.path_to_illustrations, path_to_down_img
                )
                # self.cells[i][j].text = piece
                # self.cells[i][j].color = piece_color
                self.cells[i][j].background_normal = path_to_img
                self.cells[i][j].background_down = path_to_down_img

    def finish_game(self, winner):
        """
        Method used to trigger a display of the end of a game.

        Parameters
        ----------
        winner: player.Player
            Winner of self.Game if the game is finished.
        """
        popup = Popup(title="Game finished", auto_dismiss=False)
        popup.bind(on_dismiss=self.reset_game)

        box = BoxLayout()
        box.add_widget(Label(text="Congratulations %s has won" % winner))
        restart_button = Button(text="Restart a game!")
        restart_button.bind(on_press=popup.dismiss)
        box.add_widget(restart_button)

        popup.bind(on_dismiss=self.reset_game)
        popup.content = box
        popup.open()

    def click_cell(self, event):
        """
        Main trigger when a cell is clicked.
        Works in a serie of two clicks:
            - First click is to define start cell (or cell of the piece we want to move)
            - Second click is to define the landing cell (or cell we want to move the piece to)

        Parameters
        ----------
        event: Event
            Click on a Board's cell event triggering the method.
        """
        # Reverse the backgrounds when a cell is clicked, to indicate it has been clicked.
        (
            self.cells[event.row][event.column].background_normal,
            self.cells[event.row][event.column].background_down,
        ) = (
            self.cells[event.row][event.column].background_down,
            self.cells[event.row][event.column].background_normal,
        )
        # If no previous cell has been clicked, then it's the start cell that has been clicked,
        # In this case it is store, waiting fot the click on the landinc cell.
        if self.first_cell_clicked is None:
            self.first_cell_clicked = (event.row, event.column)
        # In this case the player has clicked twice on the same cell.
        # It is considered as a cancellation of the first click
        elif (
            self.first_cell_clicked[0] == event.row
            and self.first_cell_clicked[1] == event.column
        ):
            print("Selection Aborted")
            self.first_cell_clicked = None
        # In this cas, actually move the piece.
        else:
            start_x = self.first_cell_clicked[0]
            start_y = self.first_cell_clicked[1]
            end_x = event.row
            end_y = event.column

            # Try and move if possible the piece
            validated_move, winner = self.game.move_from_coordinates(
                self.game.to_play_player, start_x, start_y, end_x, end_y
            )

            # In case move is ok
            if validated_move:
                self.update()

                # If AI is playing, then trigger its next move with time_to_play method.
                if self.ai_playing:
                    print("Time for AI")

                    # Resets background colors of player
                    ai_move = self.game.player2.time_to_play(self.game.board)
                    print(ai_move)
                    self.game.board.draw()
                    game_is_on = self.game.move(ai_move, self.game.player2)

                    # Verify game is still going on
                    # Actually we consider that an AI cannot trigger an impossible move here
                    # Maybe should be modified ?
                    print("game_is_on", game_is_on)
                    if game_is_on[0]:
                        self.update()
                        (
                            self.cells[ai_move.start.x][
                                ai_move.start.y
                            ].background_normal,
                            self.cells[ai_move.start.x][
                                ai_move.start.y
                            ].background_down,
                        ) = (
                            self.cells[ai_move.start.x][
                                ai_move.start.y
                            ].background_down,
                            self.cells[ai_move.start.x][
                                ai_move.start.y
                            ].background_normal,
                        )
                        (
                            self.cells[ai_move.end.x][ai_move.end.y].background_normal,
                            self.cells[ai_move.end.x][ai_move.end.y].background_down,
                        ) = (
                            self.cells[ai_move.end.x][ai_move.end.y].background_down,
                            self.cells[ai_move.end.x][ai_move.end.y].background_normal,
                        )
                    else:
                        if isinstance(game_is_on[1], str):
                            self.finish_game(game_is_on[1])
                        else:
                            # Can we be here ?
                            pass

            # Verify is there is or not a winner and if game is finished.
            elif isinstance(winner, str):
                print("WINNER", winner)
                self.finish_game(winner)
                return None

            # In this case, game was not possible, reset last clicks so that the player can restart
            # and redefine its move.
            else:
                popup = Popup(
                    title="Unable Move",
                    content=Label(
                        text="Your selected move is not possible, please, select another one."
                    ),
                    size_hint=(None, None),
                    size=(15, 15),
                )
                popup.open()

            if not self.ai_playing:
                # Resets values befor next move
                # If AI is playing, it is handled with self.update()
                row, col = self.first_cell_clicked
                (
                    self.cells[row][col].background_normal,
                    self.cells[row][col].background_down,
                ) = (
                    self.cells[row][col].background_down,
                    self.cells[row][col].background_normal,
                )
                (
                    self.cells[event.row][event.column].background_normal,
                    self.cells[event.row][event.column].background_down,
                ) = (
                    self.cells[event.row][event.column].background_down,
                    self.cells[event.row][event.column].background_normal,
                )

            self.first_cell_clicked = None
            if not validated_move:
                self.update()


class ChessApp(App):
    """
    Main app to use to play game, by calling ChessApp().build() and then players.
    """

    def __init__(self, play_with_ai=False, w_player=None, b_player=None, **kwargs):
        """
        Initialization, with precision whether or not playing with AI.
        """
        super().__init__(**kwargs)
        self.play_with_ai = play_with_ai
        self.w_player = w_player
        self.b_player = b_player

    def build(self):
        """
        Builds the game and the display board along with it.
        """
        game = ChessGame(
            automatic_draw=False,
            ai=self.play_with_ai,
            player1=self.w_player,
            player2=self.b_player,
        )
        print("game created")
        return BoardInterface(game)
