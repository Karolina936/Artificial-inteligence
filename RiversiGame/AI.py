from collections import OrderedDict

from Board import Board
from Reversi import Reversi

from Node import Node
from Player import Player


class AI:
    MAX = 'W'
    MIN = 'B'
    INFINITY = 1.0e+10

    def __init__(self, board=None):
        self.game = Reversi()
        if board:
            self.set_board(board)

        # changes to board form ai to game board

    def set_board(self, board):
        self.game.board = Board(self.game.player2, self.game.player1)
        self.game.board.set(board)

        # finding available moves

    def available_moves(self, board, player):
        self.set_board(board)
        self.game.player = Player(player)
        return self.game.available_fields()

        # gets the changes of the human player

    def get_resulting_board(self, board, player, coord):
        self.set_board(board)
        self.game.player = Player(player)
        self.game.play(coord)
        return board

    def player_pool(self, board, player):
        self.set_board(board)
        return ''.join(''.join(row) for row in self.board).count(player)

        # defines if the game is over or not

    def is_game_over(self, board):
        self.set_board(board)
        return self.game.check() != self.game.GAME_STATES["IN_PROGRESS"]

class MinMax:
    @staticmethod
    def get_next_move(board, player):
        # the depth argument defines how many levels deep we go before using heuristic
        _, move = MinMax.minimax(board, 2, player)
        return move

    @staticmethod
    def minimax(board, depth, player):
        ai = AI();
        # if game is over then return something
        best_move = None
        # if it is a max node
        if ai.is_game_over(board) or depth == 0:
            return (MinMax.game_heuristic(board), None)

        if player == ai.MAX:
            best_score = -ai.INFINITY
            available_moves = ai.available_moves(board, ai.MAX)
            for move in available_moves:
                node = ai.get_resulting_board(
                    board, ai.MAX, move)
                value, _ = MinMax.minimax(node, depth - 1, ai.MIN)
                if value > best_score:
                    best_score = value
                    best_move = move
            return (best_score, best_move)

        # if it is a min node
        else:
            best_score = ai.INFINITY
            available_moves = ai.available_moves(board,ai.MIN)
            for move in available_moves:
                node = ai.get_resulting_board(
                    board, ai.MIN, move)
                value, _ = MinMax.minimax(node, depth - 1,ai.MAX)
                if value < best_score:
                    best_score = value
                    best_move = move
            return (best_score, best_move)

    @staticmethod
    def game_heuristic(board):
        # defining the ai and Opponent color
        my_color = AI.MAX
        opp_color = AI.MIN

        my_tiles = 0
        opp_tiles = 0
        my_front_tiles = 0
        opp_front_tiles = 0

        p = 0
        c = 0
        l = 0
        m = 0
        f = 0
        d = 0

        # these two are used for going in every 8 directions
        X1 = [-1, -1, 0, 1, 1, 1, 0, -1]
        Y1 = [0, 1, 1, 1, 0, -1, -1, -1]

        # wondering where this came from? check the link in the github ripo from University of Washington
        V = [
            [20, -3, 11, 8, 8, 11, -3, 20],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [8, 1, 2, -3, -3, 2, 1, 8],
            [11, -4, 2, 2, 2, 2, -4, 11],
            [-3, -7, -4, 1, 1, -4, -7, -3],
            [20, -3, 11, 8, 8, 11, -3, 20]
        ]

        # =============================================================================================
        # 1- Piece difference, frontier disks and disk squares
        # =============================================================================================
        for i in range(8):
            for j in range(8):
                if board[Node(i, j)] == my_color:
                    d += V[i][j]
                    my_tiles += 1
                elif board[Node(i,j)] == opp_color:
                    d -= V[i][j]
                    opp_tiles += 1

                # calculates the number of blank spaces around me
                # if the tile is not empty take a step in each direction
                if board[Node(i,j)] != ' ':
                    for k in range(8):
                        x = i + X1[k]
                        y = j + Y1[k]
                        if (x >= 0 and x < 8 and y >= 0 and y < 8 and
                                board[Node(i, j)] == ' '):
                            if board[Node(i,j)] == my_color:
                                my_front_tiles += 1
                            else:
                                opp_front_tiles += 1
                            break

        # =============================================================================================
        # 2 - calculates the difference between current colored tiles
        # =============================================================================================
        if my_tiles > opp_tiles:
            p = (100.0 * my_tiles) / (my_tiles + opp_tiles)
        elif my_tiles < opp_tiles:
            p = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)
        else:
            p = 0

        # =============================================================================================
        # 3- calculates the blank Spaces around my tiles
        # =============================================================================================
        if my_front_tiles > opp_front_tiles:
            f = -(100.0 * my_front_tiles) / (my_front_tiles + opp_front_tiles)
        elif my_front_tiles < opp_front_tiles:
            f = (100.0 * opp_front_tiles) / (my_front_tiles + opp_front_tiles)
        else:
            f = 0

        # ===============================================================================================
        # 4 - Corner occupancy
        '''
        Examine all 4 corners :
        if they were my color add a point to me 
        if they were enemies add a point to the enemy
        '''
        # ===============================================================================================
        my_tiles = opp_tiles = 0
        if board[Node(0,0)] == my_color:
            my_tiles += 1
        elif board[Node(0,0)]  == opp_color:
            opp_tiles += 1
        if board[Node(0,7)]  == my_color:
            my_tiles += 1
        elif board[Node(0,7)]  == opp_color:
            opp_tiles += 1
        if board[Node(7,0)]  == my_color:
            my_tiles += 1
        elif board[Node(7,0)]  == opp_color:
            opp_tiles += 1
        if board[Node(7,7)]  == my_color:
            my_tiles += 1
        elif board[Node(7,7)]  == opp_color:
            opp_tiles += 1
        c = 25 * (my_tiles - opp_tiles)

        # ===============================================================================================
        # 5 - CORNER CLOSENESS
        '''
        If the corner is empty then find out how many of the 
        adjacent block to the corner are AI's or the player's
        if AI's tiles were mote than players than it's a bad thing.
        '''
        # ===============================================================================================
        my_tiles = opp_tiles = 0
        if board[Node(0,0)] == ' ':
            if board[Node(0,1)] == my_color:
                my_tiles += 1
            elif board[Node(0,1)] == opp_color:
                opp_tiles += 1
            if board[Node(1,1)] == my_color:
                my_tiles += 1
            elif board[Node(1,1)] == opp_color:
                opp_tiles += 1
            if board[Node(1,0)] == my_color:
                my_tiles += 1
            elif board[Node(1,0)] == opp_color:
                opp_tiles += 1

        if board[Node(0,7)] == ' ':
            if board[Node(0,6)] == my_color:
                my_tiles += 1
            elif board[Node(0,6)] == opp_color:
                opp_tiles += 1
            if board[Node(1,6)] == my_color:
                my_tiles += 1
            elif board[Node(1,6)] == opp_color:
                opp_tiles += 1
            if board[Node(1,7)] == my_color:
                my_tiles += 1
            elif board[Node(1,7)] == opp_color:
                opp_tiles += 1

        if board[Node(7,0)] == ' ':
            if board[Node(7,1)] == my_color:
                my_tiles += 1
            elif board[Node(7,1)]== opp_color:
                opp_tiles += 1
            if board[Node(6,1)] == my_color:
                my_tiles += 1
            elif board[Node(6,1)] == opp_color:
                opp_tiles += 1
            if board[Node(6,0)] == my_color:
                my_tiles += 1
            elif board[Node(6,0)] == opp_color:
                opp_tiles += 1

        if board[Node(7,7)] == ' ':
            if board[Node(6,7)] == my_color:
                my_tiles += 1
            elif board[Node(6,7)] == opp_color:
                opp_tiles += 1
            if board[Node(6,6)] == my_color:
                my_tiles += 1
            elif board[Node(6,6)] == opp_color:
                opp_tiles += 1
            if board[Node(7,6)] == my_color:
                my_tiles += 1
            elif board[Node(7,6)] == opp_color:
                opp_tiles += 1

        l = -12.5 * (my_tiles - opp_tiles)

        # ===============================================================================================
        # 6 - Mobility
        # ===============================================================================================
        '''
        It attempts to capture the relative difference between 
        the number of possible moves for the max and the min players,
        with the intent of restricting the
        opponent’s mobility and increasing one’s own mobility
        '''
        # basically it calculates the difference between available moves
        my_tiles = len(AI().available_moves(board, AI.MAX))
        opp_tiles = len(AI().available_moves(board, AI.MIN))

        if my_tiles > opp_tiles:
            m = (100.0 * my_tiles) / (my_tiles + opp_tiles)
        elif my_tiles < opp_tiles:
            m = -(100.0 * opp_tiles) / (my_tiles + opp_tiles)
        else:
            m = 0

        # =============================================================================================
        # =============================================================================================
        # final weighted score
        # adding different weights to different evaluations
        return (10 * p) + (801.724 * c) + (382.026 * l) + \
               (78.922 * m) + (74.396 * f) + (10 * d)






