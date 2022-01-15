#######################################################################
# FILE: game.py
# WRITERS: Samuel Assouline, samuel38, 342472495
#          Daniel Mergy, danielmergy, 342533627
# EXERCISE: intro2cs ex12 2018-2019
########################################################################

class Game:
    '''
    This is the class that represents a Game
    '''
    PLAYER1 = 1
    PLAYER2 = 2
    ILL_MOVE_MESSG = 'illegal move'
    MAX_ROW = 5
    MAX_COL = 6
    MIN_COL = 0
    MIN_ROW = 0
    ILL_LOC_MESS = 'illegal location'
    EMPTY_POS = '*'
    DRAW = 0

    def __init__(self):
        '''
        This the constructor of our class
        '''
        self.__current_player = Game.PLAYER1
        self.__game_dic = {(x, y): Game.EMPTY_POS for x in range(Game.MAX_ROW +
                                                                 1)
                           for y in range(Game.MAX_COL+1)}

    def next_to_fill_in_col(self, column):
        '''
        This function finds the next row to fill in a given col
        :param column: int
        :return: the location of the next to fill (-1 if the col is full)
        '''
        for row in range(Game.MAX_ROW, -1, -1):
            if self.get_game_dic()[(row, column)] == Game.EMPTY_POS:
                return row, column
        return -1

    def make_move(self, column):
        '''
        This function make a move in our board if it's possible else it raises
        an exception
        :param column: the col where we wnt to move
        :return: nothing
        '''
        if self.next_to_fill_in_col(column) == -1 or column < Game.MIN_COL or \
                column > Game.MAX_COL or self.get_winner() is not None:
            raise Exception(Game.ILL_MOVE_MESSG)
        else:
                self.set_game_dic((self.next_to_fill_in_col(column)[0],
                                   self.next_to_fill_in_col(column)[1]),
                                   self.get_current_player())
                if self.get_winner() is None: #we change the player only if the
                    self.change_player()      # game is not over

    def in_grid(self, location):
        '''
        This function checks if a location is on our board
        :param location: tuple
        :return: boolean
        '''
        if location[0] < Game.MIN_ROW or location[0] > Game.MAX_ROW or \
                location[1] < Game.MIN_COL or location[1] > Game.MAX_COL:
            return False
        return True

    def __check_four_disks(self, lst):
        '''
        This functions checks if in a list there are four disks that are the
        same
        :param lst: lst
        :return: True if there are 4 identical disks else False
        '''
        temp_lst = []
        i = 0
        while i != len(lst):
            if len(temp_lst) == 4:
                return True
            elif lst[i] == Game.EMPTY_POS:
                i += 1
                temp_lst = []
            elif temp_lst == [] or lst[i] == temp_lst[-1]:
                temp_lst.append(lst[i])
                i += 1
            else:
                temp_lst = []
        if len(temp_lst) == 4:
            return True
        return None

    def __check_row(self):
        '''
        this function checks if there are four identical disk in each row of
        our board
        :return: if there are four identical disks in a row return True and a
        list of all the coordination of this row else None, None
        '''
        for row in range(Game.MAX_ROW, -1, -1):
            actual_row = []
            coord_row = []#list of coordination
            for col in range(Game.MAX_COL+1):
                coord_row.append((row, col))
                actual_row.append((self.get_game_dic()[(row, col)]))
            if self.__check_four_disks(actual_row):
                return True, coord_row
            else:
                continue
        return None, None

    def __check_col(self):
        '''
        This function checks if there are four identical disks in each col of
        our board
        :return: if there are four identical disks in a col return True and a
        list of all the coordination of this col else None, None
        '''
        for col in range(Game.MAX_COL+1):
            actual_col = []
            coord_col = []
            for row in range(Game.MAX_ROW, -1, -1):
                    coord_col.append((row, col))
                    actual_col.append(self.get_game_dic()[(row, col)])
            if self.__check_four_disks(actual_col):
                return True, coord_col
            else:
                continue
        return None, None

    def __check_diag_up(self):
        '''
        This function checks if there are four identical disks in each diag of
        our board that begins at the left side of our board to the middle
        :return: if there are four identical disks in a diag return True and a
        list of all the coordination of this diag else None, None
        '''
        for row in range(3, Game.MAX_ROW+1):#the three diags that are in the
            actual_diag = []                #left side and the first member is
            coord_diag = []                 #in the first col
            col = 0
            while self.in_grid((row, col)) is True:
                actual_diag.append(self.get_game_dic()[(row, col)])
                coord_diag.append((row, col))
                col += 1
                row -= 1
            if self.__check_four_disks(actual_diag):
                return True, coord_diag
            continue
        for col in range(4):#the four diag that are in the left side of the
            actual_diag = []#board and their first member is in the last row
            coord_diag = []
            row = Game.MAX_ROW
            while self.in_grid((row, col)):
                actual_diag.append(self.get_game_dic()[(row, col)])
                coord_diag.append((row, col))
                col += 1
                row -= 1
            if self.__check_four_disks(actual_diag):
                return True, coord_diag
            continue
        return None, None

    def __check_diag_down(self):
        '''
        This function checks if there are four identical disks in each diag of
        our board that begins at the right side of our board to the middle
        :return: if there are four identical disks in a diag return True and a
        list of all the coordination of this diag else None, None
        '''
        for col in range(3, Game.MAX_COL+1):
            actual_diag = []
            coord_diag = []
            row = Game.MAX_ROW
            while self.in_grid((row, col)):
                actual_diag.append(self.get_game_dic()[(row, col)])
                coord_diag.append((row, col))
                col -= 1
                row -= 1
            if self.__check_four_disks(actual_diag):
                return True, coord_diag
            continue
        for row in range(Game.MAX_ROW-1, 2, -1):
            actual_diag = []
            coord_diag = []
            col = Game.MAX_COL
            while self.in_grid((row, col)):
                actual_diag.append(self.get_game_dic()[(row, col)])
                coord_diag.append((row, col))
                col -= 1
                row -= 1
            if self.__check_four_disks(actual_diag):
                return True, coord_diag
            continue
        return None, None

    def get_winner(self):
        '''
        This function return the num of a player if this player wins, 0 if
        there is equality and None if we are in the middle of the game
        :return: int or None
        '''
        if self.__check_row()[0] or self.__check_col()[0] or \
                self.__check_diag_up()[0] or self.__check_diag_down()[0]:
                    return self.get_current_player()
        elif Game.EMPTY_POS not in self.get_game_dic().values():
            return Game.DRAW
        else:
            return None

    def get_player_at(self, row, col):
        '''
        This function returns the player at the location (row, col) and raises
        an exception if the location is not in the board
        :param row: int
        :param col: int
        :return: the player if there is a player else None
        '''
        if not self.in_grid((row, col)):
            raise Exception(Game.ILL_LOC_MESS)
        else:
            if self.get_game_dic()[(row, col)] == Game.EMPTY_POS:
                return None
            else:
                return self.get_game_dic()[(row, col)]

    def __win_coordination_helper(self, coor_lst):
        '''
        This function receives the list of the coordination of the row, col or
        diag where there are four identical disks and return the coordination
        of the four disks
        :param coor_lst: list
        :return: list
        '''
        lst2 = coor_lst
        i = 0
        i2 = 3
        while i2 < len(lst2):
            lst = []
            for coor in lst2[i:i2+1]:
                lst.append(self.get_game_dic()[coor])
            if self.__check_four_disks(lst):
                return lst2[i:i2+1]
            else:
                i += 1
                i2 += 1

    def win_coordination(self):
        '''
        This function returns the coordination of the four disks
        in case of victory
        :return: list
        '''
        if self.__check_row()[0]:
            return self.__win_coordination_helper(self.__check_row()[1])
        elif self.__check_col()[0]:
            return self.__win_coordination_helper(self.__check_col()[1])
        elif self.__check_diag_up()[0]:
            return self.__win_coordination_helper(self.__check_diag_up()[1])
        elif self.__check_diag_down()[1]:
            return self.__win_coordination_helper(self.__check_diag_down()[1])

    def change_player(self):
        '''
        This function changes the player
        :return: nothing
        '''
        if self.get_current_player() == Game.PLAYER1:
            self.set_current_player(Game.PLAYER2)
        else:
            self.set_current_player(Game.PLAYER1)

    def get_current_player(self):
        """
        This function return the current player
        :return: int
        """
        return self.__current_player

    def set_current_player(self, player):
        """
        This function sets the current player
        :param player: int
        :return: nothing
        """
        self.__current_player = player

    def get_game_dic(self):
        """
        This function returns the game dic
        :return: dic
        """
        return self.__game_dic

    def set_game_dic(self, location, player):
        """
        This functions sets the game dic
        :param location: tuple
        :param player: int
        :return: nothing
        """
        self.__game_dic[location] = player