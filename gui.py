#######################################################################
# FILE: game.py
# WRITERS: Samuel Assouline, samuel38, 342472495
#          Daniel Mergy, danielmergy, 342533627
# EXERCISE: intro2cs ex12 2018-2019
########################################################################
import tkinter as tk
from .game import Game
from .ai import AI
import time


class GUI:
    """
    This class represents the GUI of our game
    """
    WIDTH_COL = 98
    HEIGTH_COL = 98
    PLAYER_1 = 1
    PLAYER_2 = 2
    DRAW = 0
    MAX_AI_PLAYER = 2
    TITLE_IMG = 'ex12/TITLE.png'
    GRID_IMG = 'ex12/Grille2.PNG'
    BURGER_IMG = 'ex12/burger.png'
    FRIES_IMG = 'ex12/frittes.png'
    STAR_IMG = 'ex12/star1.png'
    WIN_FRIES_IMG = 'ex12/frieswin.png'
    TURN_FRIES_IMG = 'ex12/tinfries.png'
    EQUAL_IMG = 'ex12/nowin.png'
    WIN_BURGER_IMG = 'ex12/winburger1.png'
    TURN_BURGER_IMG = 'ex12/turnburger.png'
    HUMAN_VS_HUMAN = '1 VS 2'
    HUMAN_VS_AI = '1 VS AI'
    AI_VS_HUMAN = 'AI VS 2'
    AI_VS_AI = 'AI VS AI'

    def __init__(self):
        '''
        This function is the constructor of the GUI class
        :param root: root
        '''
        self.root = tk.Tk()
        self.root.configure(bg='black')
        self.image_title = tk.PhotoImage(file=GUI.TITLE_IMG)
        label_image = tk.Label(self.root, image=self.image_title, bg='black')
        label_image.pack()
        self.coin1 = tk.PhotoImage(file=GUI.BURGER_IMG)
        self.coin2 = tk.PhotoImage(file=GUI.FRIES_IMG)
        self.star = tk.PhotoImage(file=GUI.STAR_IMG)
        self.winf = tk.PhotoImage(file=GUI.WIN_FRIES_IMG)
        self.turnf = tk.PhotoImage(file=GUI.TURN_FRIES_IMG)
        self.equal = tk.PhotoImage(file=GUI.EQUAL_IMG)
        self.winb = tk.PhotoImage(file=GUI.WIN_BURGER_IMG)
        self.turnb = tk.PhotoImage(file=GUI.TURN_BURGER_IMG)
        self.menu_game()
        self.root.mainloop()

    def menu_game(self):
        """
        This function presents the menu of the game
        :return: nothing
        """
        self.canvas = tk.Canvas(self.root, width=692, height=590, bg='black')
        self.canvas.pack()
        self.button1 = tk.Button(self.root, text=GUI.HUMAN_VS_HUMAN,
                                 command=self.callback_1,
                                 font=('Comic sans ms', 25),
                                 fg='yellow', bg='black')
        self.canvas.create_window(346, 200, window=self.button1)
        self.button2 = tk.Button(self.root, text=GUI.HUMAN_VS_AI,
                                 command=self.callback_2,
                                 font=('Comic sans ms', 25),
                                 fg='yellow', bg='black')
        self.canvas.create_window(346, 300, window=self.button2)
        self.button3 = tk.Button(self.root, text=GUI.AI_VS_HUMAN,
                                 command=self.callback_3,
                                 font=('Comic sans ms', 25),
                                 fg='yellow', bg='black')
        self.canvas.create_window(346, 400, window=self.button3)
        self.button4 = tk.Button(self.root, text=GUI.AI_VS_AI,
                                 command=self.callback_4,
                                 font=('Comic sans ms', 25),
                                 fg='yellow', bg='black')
        self.canvas.create_window(346, 500, window=self.button4)

    def initializing_game(self):
        """
        This function initialize a single ga,e by destroying the bouttons and
        the canvas of the menu game and creating our game
        :return: nothing
        """
        self.button1.destroy()
        self.button2.destroy()
        self.button3.destroy()
        self.button4.destroy()
        self.canvas.destroy()
        self.game = Game()
        self.robot_player = []
        self.img = tk.PhotoImage(file=GUI.GRID_IMG)
        self.canvas = tk.Canvas(self.root, width=692, height=590)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
        self.canvas.pack()
        self.canvas1 = tk.Canvas(self.root, width=333, height=184, bg='black')
        self.canvas1.pack()

    def callback_1(self):
        """
        This function is the callback function if the user chooses to play
        human vs human
        :return:
        """
        self.initializing_game()
        self.canvas.bind('<Button-1>', self.callback)
        self.robot = False
        self.game_situation()

    def callback_2(self):
        """
        This function is the callback function if the user chooses to play
        human vs ai
        :return: nothing
        """
        self.initializing_game()
        self.robot_player.append(GUI.PLAYER_2)
        self.robot = False
        self.canvas.bind('<Button-1>', self.callback)
        self.fix_ai_players()
        self.game_situation()

    def callback_3(self):
        """
        This function is the callback function if the user chooses to play
        ai vs human
        :return:nothing
        """
        self.initializing_game()
        self.robot_player.append(GUI.PLAYER_1)
        self.robot = True
        self.canvas.bind('<Button-1>', self.callback)
        self.fix_ai_players()
        self.ai_play()

    def callback_4(self):
        """
        This function is the callback function if the player chooses to play
        ai vs ai
        :return: nothing
        """
        self.initializing_game()
        self.robot_player.append(GUI.PLAYER_1)
        self.robot_player.append(GUI.PLAYER_2)
        self.robot = True
        self.fix_ai_players()
        self.ai_play()

    def fix_ai_players(self):
        """
        This function fixes the player for whom the ai plays and then create
        a AI object in function
        :return: nothing
        """
        if len(self.robot_player) == 2:
            self.ai_1 = AI(self.game, self.robot_player[0])
            self.ai_2 = AI(self.game, self.robot_player[1])
            self.robot = True
        else:
            if self.robot_player[0] == GUI.PLAYER_1:
                self.ai_1 = AI(self.game, GUI.PLAYER_1)
                self.robot = True
            else:  # here the ai is the second player so self.robot isn't true yet
                self.ai_2 = AI(self.game, GUI.PLAYER_2)

    def game_situation(self):
        """
        This function presents the game situation
        :return: nothing
        """
        if self.game.get_winner() == GUI.PLAYER_1:
            self.canvas1.create_image(166, 92, image=self.winb)
            self.canvas1.update()
            self.place_stars()
            time.sleep(1.5)  # this is to have the time to see whose the winner
            self.end_game()  # and where are the four disks
        elif self.game.get_winner() == GUI.PLAYER_2:
            self.canvas1.create_image(166, 92, image=self.winf)
            self.canvas1.update()
            self.place_stars()
            time.sleep(1.5)
            self.end_game()
        elif self.game.get_winner() == GUI.DRAW:
            self.canvas1.create_image(166, 92, image=self.equal)
            self.canvas1.update()
            time.sleep(1.5)
            self.end_game()
        elif self.game.get_current_player() == GUI.PLAYER_1:
            self.canvas1.create_image(166, 92, image=self.turnb)
            self.canvas1.update()
        elif self.game.get_current_player() == GUI.PLAYER_2:
            self.canvas1.create_image(166, 92, image=self.turnf)
            self.canvas1.update()

    def end_game(self):
        """
        This function ends a game by destroying the canvas of the grid and the
        canvas where there is the game situation and presents to the user the
        possibility of replay or quit the game
        :return: nothing
        """
        self.canvas.destroy()
        self.canvas1.destroy()
        self.canvas2 = tk.Canvas(self.root, width=692, height=590, bg='black')
        self.canvas2.pack()
        self.replay_button = tk.Button(self.root, text='Replay',
                                       command=self.callback_replay,
                                       font=('Comic sans ms', 25),
                                       fg='yellow', bg='black')
        self.exit_button = tk.Button(self.root, text='Exit',
                                     command=self.callback_exit,
                                     font=('Comic sans ms', 25),
                                     fg='yellow', bg='black')
        self.canvas2.create_window(346, 200, window=self.replay_button)
        self.canvas2.create_window(346, 300, window=self.exit_button)

    def callback_replay(self):
        """
        This is the callback function if the player chooses to replay
        :return: nothing
        """
        self.canvas2.destroy()
        self.menu_game()

    def callback_exit(self):
        """
        This is the callback function if the user chooses to exit
        :return:
        """
        self.root.destroy()

    def callback(self, event):
        """
        This is the callback function associate to the event <Button-1> notice
        that something happens just if self.robot is False
        :param event: a click on the mouse (left side)
        :return: nothing
        """
        if not self.robot:
            col = event.x // GUI.WIDTH_COL
            try:
                self.game_situation()
                r, c, player = self.game.next_to_fill_in_col(col)[0], \
                               self.game.next_to_fill_in_col(col)[1], \
                               self.game.get_current_player()
                self.game.make_move(col)
                self.place_coin(r, c, player)
                self.game_situation()
                if self.robot_player != []:  # if there is an ai player
                    self.robot = True
                    self.ai_play()
            except:#if the move isn't legal we don't do anything and waiting
                   #for a legal move
                pass

    def ai_play(self):
        """
        This function will executes an ai move just if self.robot is True
        :return: nothing
        """
        if self.robot:
            if self.game.get_current_player() == GUI.PLAYER_1:
                start_time = time.time()
                col = self.ai_1.find_legal_move()
                end_time = time.time()
            else:
                start_time = time.time()
                col = self.ai_2.find_legal_move()
                end_time = time.time()
            try:
                self.game_situation()
                r, c, player = self.game.next_to_fill_in_col(col)[0], \
                               self.game.next_to_fill_in_col(col)[1], \
                               self.game.get_current_player()
                self.game.make_move(col)
                if (end_time - start_time) <= 0.1:
                    time.sleep(1.5)#this is for the firsts strokes where the
                self.place_coin(r, c, player)#runtime of find_legal_move is
                # really small to let the programm update the grid
                self.game_situation()
                if len(self.robot_player) != 2:
                    self.robot = False
                else:
                    self.ai_play()
            except:
                pass


    def place_coin(self, row, col, player):
        """
        This function will places a coins in our grid at the location
        (row, col)
        :param row: int
        :param col: int
        :param player: int
        :return: nothing
        """
        if player == GUI.PLAYER_1:
            self.canvas.create_image(col * GUI.HEIGTH_COL + 52,
                                     row * GUI.WIDTH_COL + 50,
                                     image=self.coin1)
            self.canvas.update()
        else:
            self.canvas.create_image(col * GUI.HEIGTH_COL + 50,
                                     row * GUI.WIDTH_COL + 52, image=self.coin2)
            self.canvas.update()

    def place_stars(self):
        """
        This function will place stars in our grid in case of victory to see
        where are the four winners disks
        :return: nothing
        """
        for coord in self.game.win_coordination():
            self.canvas.create_image(coord[1] * GUI.HEIGTH_COL + 50,
                                     coord[0] * GUI.WIDTH_COL + 50,
                                     image=self.star)
            self.canvas.update()
