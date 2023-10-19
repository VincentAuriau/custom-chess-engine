import numpy as np
import os
import time

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from kivy.graphics import Rectangle, Color, Canvas

from engine.engine import Game



class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 8
        self.add_widget(Label(text=''))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

        self.add_widget(Label(text='password2'))
        self.password2 = TextInput(password=True, multiline=False)
        self.add_widget(self.password2)

        self.add_widget(Rectangle(pos=(10, 10), size=(500, 500)))


class DisplayableCell(Button):

    def __init__(self, row, column, **kwargs):
        super(DisplayableCell, self).__init__(**kwargs)
        self.row = row
        self.column = column


class TableScreen(GridLayout):

    def __init__(self, game, **kwargs):
        super(TableScreen, self).__init__(**kwargs)
        self.path_to_illustrations = 'own_illustrations'
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

        for i in range(8):
            line = []
            for j in range(8):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    color = (0.4, 0.4, 0.8, 1)
                    c_img = 'b'
                else:
                    color = (0.4, 0.8, 0.4, 1)
                    c_img = 'w'
                # self.add_widget(Button(text='Button %i %i' % (i, j), background_color=color,
                #                 background_down='illustrations/white_pawn.png',
                #                 background_normal='illustrations/white_queen.png'))
                piece = game.board.get_cell(i, j).get_piece()

                if piece is not None:

                    path_to_img = c_img

                    if piece.is_white():
                        piece_color = (1, 1, 1, 1)
                        path_to_img += 'w'
                    else:
                        piece_color = (0, 0, 0, 1)
                        path_to_img += 'b'
                    path_to_img += ('_' + piece.get_str().replace(' ', '') + '.png')
                    path_to_down_img = 'down_' + path_to_img

                    path_to_img = os.path.join(self.path_to_illustrations, path_to_img)
                    path_to_down_img = os.path.join(self.path_to_illustrations, path_to_down_img)

                    piece = piece.get_str()
                    button = DisplayableCell(text=piece, on_press=self.click_cell, row=i, column=j,
                                             color=piece_color, background_normal=path_to_img, border=(0, 0, 0, 0),
                                             background_down=path_to_down_img)
                else:
                    piece = ''
                    piece_color = (1, 1, 1, 1)
                    path_to_img = c_img + '.png'
                    path_to_down_img = 'down_' + path_to_img

                    path_to_img = os.path.join(self.path_to_illustrations, path_to_img)
                    path_to_down_img = os.path.join(self.path_to_illustrations, path_to_down_img)

                    button = DisplayableCell(text=piece, background_normal=path_to_img, on_press=self.click_cell, row=i,
                                             column=j, color=piece_color, border=(0, 0, 0, 0),
                                             background_down=path_to_down_img)
                self.add_widget(button)
                line.append(button)
            self.cells.append(line)

    def reset_game(self, button):
        print('On click, Reset', button)
        self.game.reset_game()
        self.update()

    def update(self):
        board = self.game.board
        for i in range(8):
            for j in range(8):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    c_img = 'b'
                else:
                    c_img = 'w'

                piece = board.get_cell(i, j).get_piece()
                if piece is not None:
                    path_to_img = c_img
                    if piece.is_white():
                        piece_color = (1, 1, 1, 1)
                        path_to_img += 'w'
                    else:
                        piece_color = (0, 0, 0, 1)
                        path_to_img += 'b'
                    piece = piece.get_str()
                    path_to_img += ('_' + piece.replace(' ', '') + '.png')
                else:
                    piece = ''
                    piece_color = (1, 1, 1, 1)
                    path_to_img = c_img + '.png'

                path_to_down_img = 'down_' + path_to_img
                path_to_img = os.path.join(self.path_to_illustrations, path_to_img)
                path_to_down_img = os.path.join(self.path_to_illustrations, path_to_down_img)
                self.cells[i][j].text = piece
                self.cells[i][j].color = piece_color
                self.cells[i][j].background_normal = path_to_img
                self.cells[i][j].background_down = path_to_down_img

    def finish_game(self, winner):
        popup = Popup(title='Game finished', auto_dismiss=False)
        popup.bind(on_dismiss=self.reset_game)

        box = BoxLayout()
        box.add_widget(Label(text='Congratulations %s has won' % winner))
        restart_button = Button(text='Restart a game!')
        restart_button.bind(on_press=popup.dismiss)
        box.add_widget(restart_button)

        popup.bind(on_dismiss=self.reset_game)
        popup.content = box
        popup.open()

    def click_cell(self, event):
        self.cells[event.row][event.column].background_normal, self.cells[event.row][event.column].background_down = \
           self.cells[event.row][event.column].background_down, self.cells[event.row][event.column].background_normal
        if self.first_cell_clicked is None:
            self.first_cell_clicked = (event.row, event.column)
        elif self.first_cell_clicked[0] == event.row and self.first_cell_clicked[1] == event.column:
            print('Selection Aborted')
            self.first_cell_clicked = None
        else:
            start_x = self.first_cell_clicked[0]
            start_y = self.first_cell_clicked[1]
            end_x = event.row
            end_y = event.column

            print(self.game.player1, self.game.to_play_player)
            validated_move, winner = self.game.move_from_coordinates(self.game.to_play_player, start_x, start_y, end_x, end_y)
            print('Validated move ?', validated_move, self.game.to_play_player, start_x, start_y, end_x, end_y, winner)

            if validated_move:
                self.update()

                if self.ai_playing:

                    print('Time for AI')
                    ai_move = self.game.player2.time_to_play(self.game.board)
                    self.game.board.draw()
                    print(self.game.player2.memory.memory)
                    game_is_on = self.game.move(ai_move, self.game.player2)

                    if game_is_on[0]:
                        self.update()
                    else:
                        if isinstance(game_is_on[1], str):
                            self.finish_game(game_is_on[1])
                        else:
                            pass

            elif isinstance(winner, str):
                print('WINNER', winner)
                self.finish_game(winner)
                return None

            row, col = self.first_cell_clicked
            self.cells[row][col].background_normal, self.cells[row][col].background_down = \
                self.cells[row][event.column].background_down, self.cells[event.row][col].background_normal
            self.first_cell_clicked = None
            self.cells[event.row][event.column].background_normal, self.cells[event.row][event.column].background_down = \
                self.cells[event.row][event.column].background_down, self.cells[event.row][event.column].background_normal



class MyApp(App):

    def __init__(self, play_with_ai=False, **kwargs):
        super().__init__(**kwargs)
        self.play_with_ai = play_with_ai
        
    def build(self):
        game = Game(automatic_draw=False, ai=self.play_with_ai)
        print('game created')
        return TableScreen(game)


