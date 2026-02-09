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
    x_count = 0
    o_count = 0
    for i in board:
        for j in i:
            if j == X: 
                x_count += 1
            elif j == O:
                o_count += 1

    if (x_count == 0 and o_count == 0) or x_count == o_count: 
        return X
    else: 
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    row = cell = -1
    for i in board:
        row += 1
        cell = -1
        for j in i:
            cell += 1
            if board[row][cell] is EMPTY:
                actions.add((row, cell))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    acts = actions(board)
    if action not in acts:
        raise ValueError
    
    board_copy = copy.deepcopy(board)
    board_copy[action[0]][action[1]] = player(board)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[1][1] == board[2][2] and board[1][1] is not EMPTY:
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] and board[1][1] is not EMPTY:
        return board[1][1]

    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not EMPTY:
            return board[0][col]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if not any(EMPTY in row for row in board) or winner(board) is not None:
        return True
    
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    player_winner = winner(board)
    if player_winner == X:
        return 1
    elif player_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board): return None

    if player(board) == X: 
        _, best_action = Max_Value(board)
    else:
        _, best_action = Min_Value(board)

    return best_action


def Max_Value(board):
    if terminal(board): return utility(board), None

    v = -2
    max_action = None
    for action in actions(board):
        v_action, _ = Min_Value(result(board, action))
        if v_action > v:
            v = v_action
            max_action = action

    return v, max_action


def Min_Value(board):
    if terminal(board): return utility(board), None

    v = 2
    min_action = None
    for action in actions(board):
        v_action, _ = Max_Value(result(board, action))
        if v_action < v:
            v = v_action
            min_action = action

    return v, min_action