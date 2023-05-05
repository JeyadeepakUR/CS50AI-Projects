"""
Tic Tac Toe Player
"""

from ast import While
import math
from operator import truediv
from queue import Empty
from shutil import move

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x = 0
    o = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                x += 1
            elif board[i][j] == O:
                o += 1
    
    if x <= o:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action.add((i, j))

    return action

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    (x, y) = action
    if x<0 or x>= 3 or y<0 or y>= 3:
        raise IndexError
    final = [row[:] for row in board]
    final[x][y] = player(board)

    return final

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for player in (X, O):
        for row in board:
            if row == [player] * 3:
                return player

        for i in range(3):
            column = [board[x][i] for x in range(3)]
            if column == [player] * 3:
                return player

        if [board[i][i] for i in range(0, 3)] == [player] * 3:
            return player

        elif [board[i][~i] for i in range(0, 3)] == [player] * 3:
            return player
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def max_value(board):
        good_move = ()
        if terminal(board):
            return utility(board), good_move
        v = -5
        for action in actions(board):
            minval = min_value(result(board, action))[0]
            if minval>v:
                v = minval
                good_move = action
        return v, good_move

    def min_value(board):
        good_move = ()
        if terminal(board):
            return utility(board), good_move
        v = 5
        for action in actions(board):
            maxval = max_value(result(board, action))[0]
            if maxval < v:
                v = maxval
                good_move = action
        return v, good_move

    curr_player = player(board)
    if terminal(board):
        return None
    if curr_player == X:
        return max_value(board)[1]
    else:
        return min_value(board)[1]
    

