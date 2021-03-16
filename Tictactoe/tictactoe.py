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
    Xcount = 0
    Ocount = 0

# count the X or O in each row then add them to the count of the next row
    for row in board:
        Xcount = Xcount + row.count(X)
        Ocount = Ocount + row.count(O)
        Totalcount = Xcount + Ocount
    
    Even = [0,2,4,6,8]

    if Totalcount in Even:
        return X
    else:
        return O



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i,j))
    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    if board_copy[action[0]][action[1]] != EMPTY:
        raise Exception("Invalid Move")
    else:
        board_copy[action[0]][action[1]] = player(board_copy)
    return board_copy

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Horizontal winner
    for i in range(3):
        if (board[i][0] != None and
            board[i][0] == board[i][1] and
            board[i][1] == board[i][2]):
            return board[i][0]

    #Vertical winner
    for j in range(3):
        if (board[0][j] != None and
            board[0][j] == board[1][j] and
            board[1][j] == board[2][j]):
            return board[0][j]

    #Diagonal winner
    if (board[0][0] != None and
        board[0][0] == board[1][1] and
        board[1][1] == board[2][2]):
        return board[0][0]
    
    if (board[0][2] != None and
        board[0][2] == board[1][1] and
        board[1][1] == board[2][0]):
        return board[0][2]

    return None
    #Check if the board is full or game is still ongoing
    # for i in range(3):
    #     for j in range(3):
    #         if board[i][j] == EMPTY:
    #             return None
    #         else:
    #             return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (winner(board) != None):
        return True

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
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
    if (terminal(board) == True):
        return None

    
    if (player(board) == X):
        m = math.inf
        for action in actions(board):
            maxv = maximize(result(board, action))
            if maxv < m:
                m = maxv
                optimal_action = action
                return optimal_action

    if (player(board) == O):
        m = -math.inf
        for action in actions(board):
            minv = minimize(result(board, action))
            if minv > m:
                m = minv
                optimal_action = action
                return optimal_action
            

def maximize(board):
    """
    Maximizing move
    """
    if (terminal(board) == True):
        return utility(board)

    m = -math.inf
            #anticipate opponent's move by maximizing your opponent's scor
    for action in actions(board):
        m = max(m, minimize(result(board, action)))
    return m

def minimize(board):
    """
    Minimizing move
    """
    if (terminal(board) == True):
        return utility(board)
        
    m = math.inf
            #anticipate opponent's move by maximizing your opponent's scor
    for action in actions(board):
        m = min(m, maximize(result(board, action)))
    return m