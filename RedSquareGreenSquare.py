"""
This file will hold all object necessary for the program to function

they key objects are:

Board
TileObject
GreenSquare
RedSquare
Game
"""

from __future__ import annotations
import random
from typing import List, Optional
from AzBot import *
import lightbulb
import hikari
from random import shuffle
from typing import List, Tuple, Optional


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
CARDINAL_DIRECTIONS = [LEFT, UP, RIGHT, DOWN]
CORNER_DIRECTIONS = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
ALL_DIRECTIONS = CORNER_DIRECTIONS + CARDINAL_DIRECTIONS


def get_shuffled_directions() -> List[Tuple[int, int]]:
    """
    Provided helper that returns a shuffled copy of DIRECTIONS.
    You should use this where appropriate
    """
    to_return = CARDINAL_DIRECTIONS[:]
    shuffle(to_return)
    return to_return


class Board:
    """
    This class will act as the area for other objects to be placed into, most importantly it will store the grid
    and use that grid to give information to other objects

    Important data types:
    board
    _width
    _height
    """

    _board: dict[int, dict[int, Optional[TileObject]]]
    _width: int
    _height: int
    _ended: bool  # This determines whether the game has been won
    _top_score: list[int]
    _side_score: list[int]

    def __init__(self, width: int, height: int):
        """
        This initalizes an empty board of the desired size

        >>> b = Board(3, 3)
        >>> b._width == 3
        True
        >>> b._height == 3
        True
        """
        self._width = width
        self._height = height

        _top_score = []
        _side_score = []

        self._board = {}

        self._ended = False

        for x in range(width):
            for y in range(height):
                try:
                    self._board[y][x] = None
                except KeyError:
                    self._board[y] = {x: None}

        for x in range(width):
            for y in range(height):
                EmptyTile(x, y, self)

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def object_at(self, x: int, y: int) -> TileObject:
        """
        Return the object at the position x, y
        if there is nothing there it will return none

        >>> b = Board(3, 3)
        >>> isinstance(b.object_at(0,0), EmptyTile)
        True
        """
        return self._board[y][x]

    def place_object(self, x: int, y: int, new_object: TileObject):
        """
        only used for innit within TileObject to place the new tiles
        """

        self._board[y][x] = new_object

    def get_board(self) -> List[List[chr]]:
        """
        return a list representing the board

        '-' = grass tile
        'r' = tree
        'e' = tent

        >>> b = Board(3, 3)
        >>> o =  GreenSquare(0, 0, b)
        >>> o2 = GreenSquare (0, 1, b)
        >>> e = RedSquare(2, 1, b)
        >>> b.get_board()
        [['r', '-', '-'], ['r', '-', 'e'], ['-', '-', '-']]
        """
        grid_to_return: List[List[chr]] = []
        row_list: List[chr] = []

        for y in range(self.get_width()):
            for x in range(self.get_width()):

                row_list.append(self.object_at(x, y).get_char())
            grid_to_return.append(row_list)
            row_list = []

        return grid_to_return

    def switch_type(self, x, y):
        """
        This function takes the object at the position x,y and switches it
        tents become grass, grass becomes tents.

        trees do nothing

        >>> b = Board(1, 1)
        >>> isinstance( b.object_at(0, 0), EmptyTile)
        True
        >>> b.switch_type(0, 0)
        >>> isinstance(b.object_at(0, 0), EmptyTile)
        False
        >>> isinstance(b.object_at(0 ,0), BlueSquare)
        True
        """
        object_to_switch = self.object_at(x, y)
        object_to_switch.swap_type()

    def row_score(self, row: int) -> int:
        """
        this finds the total number of tents in a row

        >>> b = Board (3, 3)
        >>> e1 = RedSquare (0, 0, b)
        >>> e2 = RedSquare (0, 1, b)
        >>> e3 = RedSquare (0, 2, b)
        >>> e4 = RedSquare (1,1, b)
        >>> b.row_score(0)
        1
        >>> b.row_score(1)
        2
        >>> b.row_score(2)
        1
        """
        total = 0
        for x in range(self.get_width()):
            if self.object_at(x, row).get_char() == "e":
                total += 1
        return total

    def column_score(self, column: int) -> int:
        """
        this finds the total number of tents in a row

        >>> b = Board (3, 3)
        >>> e1 = RedSquare (0, 0, b)
        >>> e2 = RedSquare (0, 1, b)
        >>> e3 = RedSquare (0, 2, b)
        >>> e4 = RedSquare (1,1, b)
        >>> b.column_score(0)
        3
        >>> b.column_score(1)
        1
        >>> b.column_score(2)
        0
        """
        total = 0
        for y in range(self.get_height()):
            if self.object_at(column, y).get_char() == "e":
                total += 1

        return total

    def get_all_tiles(self) -> List[TileObject]:
        """
        This returns a list of all the tiles in the board

        >>> b = Board(3,3)
        >>> e1 = RedSquare(0, 0, b)
        >>> b.get_all_tiles() == []
        False

        """

        list_of_all_elements = []
        for x in range(self.get_width()):
            for y in range(self.get_height()):
                list_of_all_elements.append(self.object_at(x, y))
        return list_of_all_elements

    def get_all_trees(self) -> List[TileObject]:
        """
        This returns a list of all the trees in the board

        >>> b = Board(3,3)
        >>> e1 = RedSquare(0, 0, b)
        >>> r1 = GreenSquare(0, 1, b)
        >>> b.get_all_trees() == [r1]
        True
        """

        list_of_all_trees = []
        for x in range(self.get_width()):
            for y in range(self.get_height()):
                if self.object_at(x, y).get_char() == "r":
                    list_of_all_trees.append(self.object_at(x, y))
        return list_of_all_trees

    def get_all_tents(self) -> List[TileObject]:
        """
        This returns a list of all the tents in the board

        >>> b = Board(3,3)
        >>> e1 = RedSquare(0, 0, b)
        >>> r1 = GreenSquare(0, 1, b)
        >>> b.get_all_tents() == [e1]
        True
        """

        list_of_all_tents = []
        for x in range(self.get_width()):
            for y in range(self.get_height()):
                if self.object_at(x, y).get_char() == "e":
                    list_of_all_tents.append(self.object_at(x, y))
        return list_of_all_tents

    def check_game_won(self) -> bool:
        """
        This function checks if the game has ended using the 3 conditions
        Returns true if the game is over

        :return:
        >>> b = Board(3,3)
        >>> r1 = GreenSquare(0, 0, b)
        >>> e1 = RedSquare(1, 0, b)
        >>> b.prepare_game()
        True
        >>> e1 = RedSquare(1, 0, b)
        >>> b.check_game_won()
        True
        >>> e2 = RedSquare(2, 0, b)
        >>> b.check_game_won()
        False
        >>> e2.swap_type()
        >>> b.check_game_won()
        True
        >>> e3 = RedSquare(2, 2, b)
        >>> b.check_game_won()
        False
        >>> r2 = GreenSquare (2, 1, b)
        >>> b.prepare_game()
        True
        >>> e1 = RedSquare(1, 0, b)
        >>> e3 = RedSquare(2, 2, b)
        >>> b.check_game_won()
        True
        >>> r2 = GreenSquare (1, 1, b)
        >>> b.check_game_won()
        False
        """
        self._ended = False
        # First check the number of tents is equal to number of trees
        if not len(self.get_all_tents()) == len(self.get_all_trees()):
            return False

        # Then check each tent is in a valid position
        for tent in self.get_all_tents():
            if not tent.valid_position():
                return False

        # Then check each tree has at least one tent next to it
        for tree in self.get_all_trees():
            if not tree.valid_position():
                return False

        # test that number of tents in each row is correct
        for y in range(self.get_height()):
            if not self.row_score(y) == self.get_side_score()[y]:
                return False
        for x in range(self.get_width()):
            if not self.column_score(x) == self.get_top_score()[x]:
                return False

        self._ended = True
        return True

    def update_top_score(self):
        """
        Gets the scores that will go on the top of the board and updates them to the score
        :return:
        >>> b = Board(3,3)
        >>> b.update_top_score()
        >>> b._top_score == [0, 0, 0]
        True
        >>> r1 = GreenSquare(0, 0, b)
        >>> e1 = RedSquare(1, 0, b)
        >>> b.update_top_score()
        >>> b._top_score
        [0, 1, 0]
        """

        column_list = []
        for x in range(self.get_width()):
            column_list.append(self.column_score(x))
        self._top_score = column_list

    def update_side_score(self):
        """
        Gets the scores that will go on the top of the board and updates them to the score
        :return:
        >>> b = Board(3,3)
        >>> b.update_side_score()
        >>> b._side_score == [0, 0, 0]
        True
        >>> r1 = GreenSquare(0, 0, b)
        >>> e1 = RedSquare(1, 1, b)
        >>> b.update_side_score()
        >>> b._side_score
        [0, 1, 0]
        """

        row_list = []
        for y in range(self.get_height()):
            row_list.append(self.row_score(y))
        self._side_score = row_list

    def get_top_score(self) -> list[int]:
        return self._top_score

    def get_side_score(self) -> list[int]:
        return self._side_score

    def prepare_game(self) -> bool:
        """
        Prepares the game to be played once the board has been set up.

        First update top and side scores to be displayed later. Then check the game state is valid.
        Then remove the tents and set the game ended value to false

        >>> b = Board(3,3)
        >>> r1 = GreenSquare(0, 0, b)
        >>> e1 = RedSquare(1, 0, b)
        >>> b.prepare_game()
        True
        >>> b.get_all_tents()
        []
        >>> b.get_side_score()
        [1, 0, 0]
        >>> b.get_top_score()
        [0, 1, 0]
        >>> b2 = Board(2,2)
        >>> r1 = GreenSquare(0,0,b2)
        >>> b2.prepare_game()
        False
        """

        self.update_side_score()
        self.update_top_score()

        valid_game_state = self.check_game_won()

        if valid_game_state:
            self.remove_tents()
            self._ended = False
            return True
        else:
            return False

    def remove_tents(self):
        """
        Turns all tents into empty tiles

        >>> b = Board(3,3)
        >>> e1 = RedSquare(0, 0, b)
        >>> e2 = RedSquare(1, 0, b)
        >>> e3 = RedSquare(2, 0, b)
        >>> e4 = RedSquare(0, 1, b)
        >>> r1 = GreenSquare(2, 2, b)
        >>> b.get_all_tents() == [e1,e4,e2,e3]
        True
        >>> b.remove_tents()
        >>> b.get_all_tents()
        []
        """
        for tent in self.get_all_tents():
            tent.swap_type()

    def print_board(self):
        """
        prints the board using the get_char caractrers

        >>> b = Board(3,3)
        >>> e1 = RedSquare(0, 0, b)
        >>> r2 = GreenSquare(1, 0, b)
        >>> b.prepare_game()
        True
        >>> e1 = RedSquare(0, 0, b)
        >>> b.print_board()
        [1, 0, 0]
        1['e', 'r', '-']
        0['-', '-', '-']
        0['-', '-', '-']
        """
        board = self.get_board()
        print(str(self.get_top_score()))
        x = -1
        for row in board:
            x += 1
            print(str(self.get_side_score()[x]) + str(row))

    def get_ended(self) -> bool:
        return self._ended


class TileObject:
    """
    This class acts as an abstract class for the tree and tent object types, this allows for shared functions
    to be more easily accessed

    data:
    x_pos
    y_pos

    """
    _x: int
    _y: int
    _board: Board

    def __init__(self, x: int, y: int, board: Board):
        """
        Initialize the tile object and place it on the board where it should be (linking it to the board as well)

        >>> b = Board(3, 3)
        >>> o = TileObject(0, 0, b)
        >>> b.object_at(0, 0) == o
        True
        """

        self._x = x
        self._y = y
        self._board = board
        board.place_object(x, y, self)

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def disc_symbol(self) -> str:
        raise NotImplementedError

    def get_char(self) -> chr:
        raise NotImplementedError

    def swap_type(self):
        raise NotImplementedError

    def valid_position(self):
        raise NotImplementedError

    def get_cardinal_objects(self) -> Optional[list[TileObject]]:
        """
        Checks each cardinal direction and checks if there is a tent adjacent to it
        returns a list of all adjacent tents
        :return:

        >>> b = Board(3,3)
        >>> r1 = GreenSquare(1, 1, b)
        >>> e1 = RedSquare (0, 1, b)
        >>> e2 = RedSquare (1, 0, b)
        >>> r1.get_cardinal_objects()[0] == e1
        True
        >>> r1.get_cardinal_objects()[1] == e2
        True
        >>> type(r1.get_cardinal_objects()[2]) == EmptyTile
        True
        >>> type(r1.get_cardinal_objects()[3]) == EmptyTile
        True
        """

        x = self.get_x()
        y = self.get_y()
        return_list: List[TileObject] = []
        for direction in CARDINAL_DIRECTIONS:
            new_x = x + direction[0]
            new_y = y + direction[1]
            if not (new_y < 0) and not (new_y >= self._board.get_height()):
                if not (new_x < 0) and not (new_x >= self._board.get_width()):
                    object_at = self._board.object_at(new_x, new_y)
                    return_list.append(object_at)

        return return_list

    def get_surrounding_objects(self) -> List[TileObject]:
        """
        returns a list of all tiles around the tent
        >>> b = Board(3,3)
        >>> e1 = RedSquare(0,0, b)
        >>> len(e1.get_surrounding_objects()) == 3
        True
        >>> e2 = RedSquare(1,1, b)
        >>> len(e2.get_surrounding_objects()) == 8
        True


        """

        return_list = []
        x = self.get_x()
        y = self.get_y()

        for direction in ALL_DIRECTIONS:
            new_x = x + direction[0]
            new_y = y + direction[1]

            if not (new_y < 0) and not (new_y >= self._board.get_height()):
                if not (new_x < 0) and not (new_x >= self._board.get_width()):
                    return_list.append(self._board.object_at(new_x, new_y))

        return return_list


class GreenSquare (TileObject):
    """
    This is the tree type object, it is nearly identical to the tent class and acts mostly to track its location on the
    board

    data:
    x_pos
    y_pos
    """
    def get_char(self) -> chr:
        return "r"

    def swap_type(self):
        """
        if called the tile becomes an empty tile
        """
        EmptyTile(self.get_x(), self.get_y(), self._board)

    def disc_symbol(self) -> str:
        return ":green_square:"

    def get_adjacent_tent(self) -> Optional[List[TileObject]]:
        """
        Checks each cardinal direction and checks if there is a tent adjacent to it
        returns a list of all adjacent tents
        :return:

        >>> b = Board(3,3)
        >>> r1 = GreenSquare(0, 0, b)
        >>> e1 = RedSquare (0, 1, b)
        >>> r1.get_adjacent_tent() == [e1]
        True
        >>> r2 = GreenSquare(1, 1, b)
        >>> e2 = RedSquare(2, 2, b)
        >>> e3 = RedSquare(1, 2, b)
        >>> r2.get_adjacent_tent() == [e1, e3]
        True
        """

        return_list = []
        list_of_objects = self.get_cardinal_objects()
        for tile_object in list_of_objects:
            if tile_object.get_char() == "e":
                return_list.append(tile_object)
        return return_list

    def valid_position(self) -> bool:
        """
        Checks if the tree has at least once tent touching it
        if it does, return true, otherwise return false
        :return:

        >>> b = Board(3,3)
        >>> r1 = GreenSquare(0, 0, b)
        >>> e1 = RedSquare (0, 1, b)
        >>> r1.valid_position()
        True
        >>> r2 = GreenSquare(2, 2, b)
        >>> r2.valid_position()
        False
        """

        if len(self.get_adjacent_tent()) > 0:
            return True
        return False


class RedSquare (TileObject):
    """
    This object is like the tree and simply tracks where it is, it will also have the function to check valid position
    for the check game finished function within the board class

    data:
    x_pos
    y_pos
    """

    def get_char(self) -> chr:
        return "e"

    def disc_symbol(self) -> str:
        return ":red_square:"

    def swap_type(self):
        EmptyTile(self.get_x(), self.get_y(), self._board)

    def valid_position(self) -> bool:
        """
        Check all sides of the tent to see if there is another redsquare around. if
        there is it returns false.

        This does not check for trees, simply for tents

        >>> b = Board(3,3)
        >>> e1 = RedSquare(0,0, b)
        >>> e2 = RedSquare(1,0, b)
        >>> e3 = RedSquare(2, 2, b)
        >>> e1.valid_position()
        False
        >>> e3.valid_position()
        True
        """

        for tile in self.get_surrounding_objects():
            if tile.get_char() == "e":
                return False

        return True


class BlueSquare (TileObject):
    """
    This is simply the class for grass tiles, it makes get_char more usable
    """

    def get_char(self) -> chr:
        return "G"

    def disc_symbol(self) -> str:
        return ":blue_square:"

    def swap_type(self):
        RedSquare(self.get_x(), self.get_y(), self._board)

    def valid_position(self):
        # This should never be called
        raise NotImplementedError


class EmptyTile (TileObject):
    """
    Empty tile class for ease of use
    """

    def get_char(self) -> chr:
        return "-"

    def disc_symbol(self) -> str:
        return ":black_large_square:"

    def swap_type(self):
        BlueSquare(self.get_x(), self.get_y(), self._board)

    def valid_position(self):
        # This should never be called
        raise NotImplementedError


class Game:
    """
    This class holds the board object and has functions for creating new games and will take input to play the game

    """

    _board: Optional[Board]

    def __init__(self):
        self._board = None

    def new_board(self, width: int, height: int):
        """
        set _board to a new board with width and height
        >>> g = Game()
        >>> g.new_board(1,1)
        >>> g._board.get_width()
        1
        """
        self._board = Board(width, height)

    def get_board(self) -> Optional[Board]:
        """
        Returns _board
        >>> g = Game()
        >>> g.new_board(1,1)
        >>> g.get_board() == g._board
        True
        """
        return self._board

    def place_random_tree(self) -> bool:
        """
        find a place for a tree and corresponding tent, if no position can be found return false, otherwise
        return true
        :return: true or false if it worked or not

        >>> g = Game()
        >>> g.new_board(1, 1)
        >>> g.place_random_tree()
        False
        >>> g.new_board(2,2)
        >>> g.place_random_tree()
        True
        >>> g.place_random_tree()
        False
        >>> g.new_board(3, 3)
        >>> g.place_random_tree()
        True
        >>> g.place_random_tree()
        True
        >>> g.place_random_tree()
        True
        >>> g.get_board().get_board()
        """
        # generate a random position and start loop
        potential_positions = self.list_of_valid_tiles()

        if len(potential_positions) == 1:
            ran_x = potential_positions[0].get_x()
            ran_y = potential_positions[0].get_y()
        elif len(potential_positions) > 1:
            random_position = random.randint(0, len(potential_positions)-1)
            ran_x = potential_positions[random_position].get_x()
            ran_y = potential_positions[random_position].get_y()
        else:
            return False

        # check if a new tree can be placed there, including valid tent position

        worked = self.place_tent(ran_x, ran_y)
        if worked:
            return True

        return False

    def place_tent(self, ran_x, ran_y) -> bool:
        """
        try to place a tent at the desired position, if it doesn't work, return false
        this should only fail if the cardinal directions are all either the edge or tents
        """

        object_at_position = self.get_board().object_at(ran_x, ran_y)
        if isinstance(object_at_position, EmptyTile):
            # position is potentially valid, try placing a tree and check results
            new_tent = RedSquare(ran_x, ran_y, self.get_board())
            for direction in get_shuffled_directions():
                # for each direction try placing a tent, if the position is valid return true
                new_tree_x = ran_x + direction[0]
                new_tree_y = ran_y + direction[1]
                if not (new_tree_y < 0) and not (new_tree_y >= self.get_board().get_height()):
                    if not (new_tree_x < 0) and not (new_tree_x >= self.get_board().get_width()):
                        tree_space = self.get_board().object_at(new_tree_x, new_tree_y)

                        if isinstance(tree_space, EmptyTile):
                            new_tree = GreenSquare(new_tree_x, new_tree_y, self.get_board())
                            valid = new_tree.valid_position()
                            if valid:
                                return True
                            else:
                                new_tree.swap_type()
            new_tent.swap_type()
        return False

    def get_position_list(self) -> List[TileObject]:
        """
        Return every object on the bored in a signle list

        >>> g = Game()
        >>> g.new_board(5, 5)
        >>> len(g.get_position_list()) == 25
        True
        """
        return_list = []

        for x in range(self.get_board().get_width()):
            for y in range(self.get_board().get_height()):
                return_list.append(self.get_board().object_at(x, y))
        return return_list

    def get_invalid_positions(self) -> List[TileObject]:
        """
        returns a list of every tile that is touching a tent
        >>> g = Game()
        >>> g.new_board(5, 5)
        >>> e1 = RedSquare(0,0, g.get_board())
        >>> len(g.get_invalid_positions())
        4
        >>> e1 = RedSquare(1,0, g.get_board())
        >>> len(g.get_invalid_positions())
        6
        """
        list_of_invalid_tiles = []

        for tent in self.get_board().get_all_tents():
            list_of_invalid_tiles.append(tent)
            for adjacent in tent.get_surrounding_objects():
                list_of_invalid_tiles.append(adjacent)

        # remove duplicate entries
        return_list = []
        for invalid_tile in list_of_invalid_tiles:
            tile_valid = True
            for entry in return_list:
                if entry == invalid_tile:
                    tile_valid = False
            if tile_valid:
                return_list.append(invalid_tile)

        return return_list

    def list_of_valid_tiles(self) -> List[TileObject]:
        """
        take the list of all tiles and take away the invalid ones to create a list of valid ones

        >>> g = Game()
        >>> g.new_board(3, 3)
        >>> e1 = RedSquare(0,0, g.get_board())
        >>> len(g.list_of_valid_tiles())
        5
        >>> e1 = RedSquare(1,0, g.get_board())
        >>> len(g.list_of_valid_tiles())
        3
        """
        return_list = []
        for tile in self.get_position_list():
            tile_valid = True
            for invalid in self.get_invalid_positions():
                if invalid == tile:
                    tile_valid = False
            if tile_valid:
                return_list.append(tile)
        return return_list

    def new_game(self, width: int, height: int, number_of_trees: int):
        """
        Creates a new game board with the desired number of trees and makes sure it is valid

        >>> g = Game()
        >>> g.new_game(5, 5, 6)
        >>> g.get_board().print_board()
        """
        self.new_board(width, height)
        for x in range(number_of_trees):
            self.place_random_tree()

        self.get_board().prepare_game()

    def print_board(self):
        """
        calls _board.print_board
        """
        self.get_board().print_board()

    def play(self, bot: AzBot, guild: hikari.Guild):
        """
        Runs a loop allowing for user input and placing of trees until the game is won

        self.new_game must be run before running this

        """
        while not self.get_board().get_ended():
            # print the board and reset variables
            self.print_board()
            tile_x = -1
            tile_y = -1

            # take user input of a tile
            tile = input("Enter position in format |x,y|")
            tile = tile.split(sep=",")
            if len(tile) > 1:
                try:
                    tile_x = int(tile[0])
                    tile_y = int(tile[1])
                except ValueError:
                    tile_x = -1
                    tile_y = -1
                    print("1")

            # check that it is in range and not a tree
            if not (tile_y < 0) and not (tile_y >= self.get_board().get_height()):
                if not (tile_x < 0) and not (tile_x >= self.get_board().get_width()):
                    if not self.get_board().object_at(tile_x, tile_y).get_char() == "r":
                        # swap the tile on that space
                        self.get_board().switch_type(tile_x, tile_y)
                        self.get_board().check_game_won()
                    else:
                        print("tile has a tree already")

        self.print_board()
        print("Congratulations, you win!")

    def discord_display(self) -> str:
        number_to_symbol = {0: ":zero:", 1: ":one:", 2: ":two:", 3: ":three:", 4: ":four:", 5: ":five:",
                            6: ":six:", 7: ":seven:", 8: ":eight:", 9: ":nine:", 10: ":ten:"}

        return_string = ":blue_square:"
        for number in self.get_board().get_top_score():
            return_string += number_to_symbol[number]

        for y in range(self.get_board().get_height()):
            return_string += "\n"
            return_string += number_to_symbol[self.get_board().get_side_score()[y]]
            for x in range(self.get_board().get_width()):
                return_string += self.get_board().object_at(x, y).disc_symbol()

        return return_string
