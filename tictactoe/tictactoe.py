"""
Tic Tac Toe Player
"""

import math
import copy

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
    countX = 0
    countO = 0
    for row in board:
        countX += row.count(X)
        countO += row.count(O)
    if countX == countO:
        return X
    return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for y,row in enumerate(board):
        for x, tile in enumerate(row):
            if tile == EMPTY:
                moves.add((y,x))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #horizontals
    for row in board:
        if row[0] == row[1] == row[2]:
            return row[0]
    #verticals
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]
    #diagonals
    if board[0][0] == board[1][1] == board[2][2]:
        return board[1][1]
    if board[2][0] == board[1][1] == board[0][2]:
        return board[1][1]
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
    result = winner(board)
    if result == X:
        return 1
    if result == O:
        return -1
    return 0

def MaxValue(board):
    play = None
    if terminal(board):
        return (utility(board), play)
    moves = actions(board)
    v =  -math.inf
    for action in moves:
        a = MinValue(result(board, action))[0]
        if  a > v:
            v = a
            play = action
            if v == 1:
                return v, play
    return (v, play)
   

def MinValue(board):
    play = None
    if terminal(board):
        return (utility(board), play)
    moves = actions(board)
    v =  math.inf
    for action in moves:
        a = MaxValue(result(board, action))[0]
        if a < v:
            v = a
            play = action
            if v == -1:
                return v, play
    return (v, play)

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    turn = player(board)
    if turn == X:
        return MaxValue(board)[1]
    else:
        return MinValue(board)[1]

