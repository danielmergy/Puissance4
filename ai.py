#######################################################################
# FILE: game.py
# WRITERS: Samuel Assouline, samuel38, 342472495
#          Daniel Mergy, danielmergy, 342533627
# EXERCISE: intro2cs ex12 2018-2019
########################################################################
from .game import Game
from itertools import product
import operator

class AI:
    """
    This class represent the AI of our game
    """
    COL_NUM = 7
    ROW_NUM = 6
    ALL_COL_STR = '0123456'
    WRNG_PLAY_MESS = 'Wrong Player'
    MIDLLE_COL = 3
    PLAYER1 = 1
    PLAYER2 = 2
    FULL_COL = 200000
    MAX_VICTORY = 20000
    MIN_DEFEAT = -20000
    MAX_ROW = 5
    IMP_COMB = 1000
    VERY_IMP_COMB = 200000
    BIG_TIME = 3200
    MIDLLE_TIME = 300
    SMALL_TIME = 50

    def __init__(self, game, player):
        """
        This is the constructor of our ai
        :param game: an object of type Game
        :param player: the number of the player for whom this ai 'plays'
        """
        self.__game = game
        self.__player = player
        self.__best_col = AI.MIDLLE_COL

    def __copy_game(self):
        """
        This function copy the the game given in the constructor by creating an
        object game of mine
        :return: the copy of self.__game
        """
        copy_game = Game()
        for row in range(AI.ROW_NUM):
            for col in range(AI.COL_NUM):
                if self.get_game().get_player_at(row, col) is not None:
                    copy_game.set_game_dic((row, col),
                                self.get_game().get_player_at(row, col))
                continue
        copy_game.set_current_player(self.get_game().get_current_player())
        return copy_game

    def __find_legal_move_helper(self, depth):
        """
        This function is a helper function for find legal move and checks the
        result of each combination of len depth
        :param depth: int
        :return: a dic with all the column in key and an int number in value
        the key with the bigger value will be the column returned
        """
        col_dic = {x: 0 for x in range(AI.COL_NUM)}
        all_combination_lst = list(product(AI.ALL_COL_STR, repeat=depth))
        for tup in all_combination_lst:
            copy_game = self.__copy_game()
            if self.__start_game(copy_game) is not None:
                self.set_best_col(self.__start_game(copy_game))
                return self.__start_game(copy_game)
            else:
                if copy_game.get_player_at(0, int(tup[0])):
                    col_dic[int(tup[0])] -= AI.FULL_COL
                if col_dic[int(tup[0])] <= AI.MIN_DEFEAT or \
                        col_dic[int(tup[0])] >= AI.MAX_VICTORY:
                    continue
                count = 0
                for col in tup:
                    self.__make_move(copy_game, int(col))
                    if copy_game.get_winner() is None or \
                        copy_game.get_winner() == 0:
                        col_dic[int(tup[0])] += 0
                        count += 1
                    elif copy_game.get_winner() == self.get_player():
                        if count == 0:
                            col_dic[int(tup[0])] += AI.VERY_IMP_COMB
                            break
                        else:
                            col_dic[int(tup[0])] += AI.IMP_COMB
                            break
                    else:
                            col_dic[int(tup[0])] -= AI.IMP_COMB
                            break
                self.set_best_col(max(col_dic.items(),
                                      key=operator.itemgetter(1))[0])
        return max(col_dic.items(), key=operator.itemgetter(1))[0]

    def __next_to_fill(self, game, col):
        """
        This function finds the next to fill in our copy_game
        :param game: Game object
        :param col: int
        :return: the row of the next location to fill in the col
        """
        for row in range(AI.ROW_NUM-1, -1, -1):
            if game.get_player_at(row, col) is not None:
                continue
            else:
                return row

    def __make_move(self, game, col):
        """
        This functions make a move in our copy game object
        :param game: copy game
        :param col: int
        :return: nothing
        """
        game.set_game_dic((self.__next_to_fill(game, col), col),
                          game.get_current_player())
        if game.get_winner() is None:
            game.change_player()

    def find_legal_move(self, timeout=None):
        """
        This function retrun the col where the ai would play
        :param timeout: the time that we let to the function before stopping
        it
        :return: the best col
        """
        if self.get_player() != self.get_game().get_current_player():
            raise Exception(AI.WRNG_PLAY_MESS)
        else:
            if timeout is None or timeout > AI.BIG_TIME:
                return self.__find_legal_move_helper(4)
            elif timeout > AI.MIDLLE_TIME:
                return self.__find_legal_move_helper(3)
            elif timeout > AI.SMALL_TIME:
                return self.__find_legal_move_helper(2)
            else:
                return self.__find_legal_move_helper(1)

    def __start_game(self, game):
        """
        This function receives the copy game in param and play only in col 3
        if we are at the beginning of the game(the row 5 has no disk in other
        col than 3)
        :param game: copy game
        :return: int
        """
        count = 0
        for col in range(AI.COL_NUM):
            if col == AI.MIDLLE_COL:
                continue
            else:
                if game.get_player_at(AI.MAX_ROW, col) is None:
                    count += 1
                else:
                    continue
        if count == AI.COL_NUM-1 and game.get_player_at(0, AI.MIDLLE_COL) is \
                None:
            return 3
        elif count == AI.COL_NUM-1 and game.get_player_at(0, AI.MIDLLE_COL) \
                is not None:
            return 0
        else:
            return None


    def get_last_found_move(self):
        """
        :return: the las found move
        """
        return self.get_best_col()

    def get_game(self):
        """
        :return: the game
        """
        return self.__game

    def get_best_col(self):
        """
        :return: the best col
        """
        return self.__best_col

    def set_best_col(self, col):
        """
        this functions sets the best col
        :param col:int
        :return: nothing
        """
        self.__best_col = col

    def get_player(self):
        """
        :return: the player
        """
        return self.__player



