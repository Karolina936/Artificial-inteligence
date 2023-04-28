from collections import OrderedDict
import time

from Board import Board
from Node import Node
from Player import Player


class GameHasEndedError(Exception):
    pass


class InvalidMoveError(Exception):
    pass


class Reversi:
    BLACK = 1
    WHITE = 2
    EMPTY = ' '

    DIRECTIONS = [Node(x, y)
                  for x, y in [(-1, -1), (-1, 0), (0, -1), (1, -1),
                               (-1, 1), (0, 1), (1, 0), (1, 1)]]

    GAME_STATES = {
        "IN_PROGRESS": 'In progress',
        "BLACK_WINS": 'Player1 wins',
        "WHITE_WINS": 'Player2 wins',
        "TIE": 'Tie'
    }

    def __init__(self, board=None, player=None):
        self.player1 = Player(self.BLACK)
        self.player2 = Player(self.WHITE)
        if board is None and player is None:
            self.board = Board(self.player2, self.player1)
            self.player = self.player1
            self.player1.result = 2
            self.player2.result = 2
        else:
            self.board = Board(nodes=board)
            self.player = Player(player)

        self.game_state = self.GAME_STATES['IN_PROGRESS']

    def is_disc_other_player(self, node):
        return node.is_on_board() and self.board.nodes[node] not in [self.player.color, self.EMPTY]

    def is_disc_current_player(self, node):
        return node.is_on_board() and self.board.nodes[node] == self.player.color

    def is_empty_disc(self, node):
        return node.is_on_board() and self.board.nodes[node] == self.EMPTY

    def get_all_current_player(self):
        all_nodes = [Node(i, j) for i in range(8) for j in range(8)]
        cp_nodes = []
        for node in all_nodes:
            if self.board.nodes[node] == self.player.color:
                cp_nodes += [node]
        return cp_nodes

    def get_player1_discs(self):
        all_nodes = [Node(i, j) for i in range(8) for j in range(8)]
        p1_nodes = []
        for node in all_nodes:
            if self.board.nodes[node] == self.player1.color:
                p1_nodes += [node]
        return p1_nodes

    def get_player2_discs(self):
        all_nodes = [Node(i, j) for i in range(8) for j in range(8)]
        p2_nodes = []
        for node in all_nodes:
            if self.board.nodes[node] == self.player2.color:
                p2_nodes += [node]
        return p2_nodes

    def change_current_player(self):
        if self.player == self.player1:
            self.player = self.player2
        else:
            self.player = self.player1

    def print_current_player(self):
        if self.player == self.player1:
            print("\nPlayer1")
        else:
            print("\nPlayer2")

    # array of clickable cordinations
    def available_fields(self):
        colors = self.get_all_current_player()
        result = []
        for color in colors:
            for d in self.DIRECTIONS:
                node = color + d
                while self.is_disc_other_player(node):
                    node += d
                    if self.is_empty_disc(node):
                        result += [node]
        return result

    def is_valid_move(self, node):
        return node in self.available_fields()

    def get_player_move(self):
        DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
        while True:
            print('Enter your move')
            move = input().lower()
            if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if self.is_valid_move(Node(x, y)):
                    break
                else:
                    continue
            else:
                print('That is not a valid move. Type the x digit (1-8), then the y digit (1-8).')
                print('For example, 81 will be the top-right corner.')

        return Node(x, y)

    def playComputer(self, player):
        from AI import Algorithms
        move, nodes = Algorithms.get_next_move(self.board.nodes, player.color)
        return move, nodes

    def play(self, node):
        new_colors = []
        for d in self.DIRECTIONS:
            current_node = node + d
            while self.is_disc_other_player(current_node):
                current_node += d

            if self.is_disc_current_player(current_node):
                new_colors += node.check(current_node, d)

        for node in new_colors:
            self.board.nodes[node] = self.player.color

        self.change_current_player()
        self.game_state = self.check()
        self.player1.result = len(self.get_player1_discs())
        self.player2.result = len(self.get_player2_discs())

    def playC(self, node):
            new_colors = []
            for d in self.DIRECTIONS:
                current_node = node + d
                while self.is_disc_other_player(current_node):
                    current_node += d

                if self.is_disc_current_player(current_node):
                    new_colors += node.check(current_node, d)

            # change the field to the player's field
            for node in new_colors:
                self.board.nodes[node] = self.player.color

    def check(self):

        if not self.available_fields():
            self.change_current_player()

            if not self.available_fields():
                if self.player2.result > self.player1.result:
                    return self.GAME_STATES["WHITE_WINS"]
                elif self.player2.result < self.player1.result:
                    return self.GAME_STATES["BLACK_WINS"]
                else:
                    return self.GAME_STATES["TIE"]
        return self.GAME_STATES["IN_PROGRESS"]

    def game_result(self):
        self.player1.result = len(self.get_player1_discs())
        self.player2.result = len(self.get_player2_discs())
        if self.game_state != self.GAME_STATES['IN_PROGRESS']:
            if self.player2.result == self.player1.result:
                print(self.GAME_STATES["TIE"])
            elif self.player2.result < self.player1.result:
                print(self.GAME_STATES["BLACK_WINS"])
            else:
                print(self.GAME_STATES["WHITE_WINS"])
            print("Result")
            print("Player1: ", self.player1.result)
            print("Player2: ", self.player2.result)

    def start(self):
        print('Welcom in Riversi')
        print('Select a game state:')
        print('1. Player vs Player')
        print('2. Player vs Computer')
        print('3. Computer vs Computer')
        choice = input().lower()

        if int(choice) == 1:
            print("You choose player vs player")
            print('Player1 start')
            while self.game_state == self.GAME_STATES['IN_PROGRESS']:
                self.print_current_player()
                self.board.print_board()
                node = self.get_player_move()
                self.play(node)

        elif int(choice) == 2:
            print("You'choose player vs computer")
            self.player2.Computer = True;
            while self.game_state == self.GAME_STATES['IN_PROGRESS']:
                self.print_current_player()
                self.board.print_board()
                if self.player.Computer is True:
                    node, amount_of_nodes = self.playComputer(self.player)
                else:
                    node = self.get_player_move()
                self.play(node)
        elif int(choice) == 3:
            print("You'choose computer vs computer")
            self.player1.Computer = True;
            self.player2.Computer = True;
            self.board.print_board()
            all_nodes_visited = 0
            start_time = time.time()
            while self.game_state == self.GAME_STATES['IN_PROGRESS']:
                self.print_current_player()
                node, amount_of_nodes = self.playComputer(self.player)
                self.play(node)
                self.board.print_board()
                print('Nodes searched: ' + str(amount_of_nodes))
                all_nodes_visited += amount_of_nodes
            end_time = time.time()
            print("All nodes searched: ", all_nodes_visited)
            print("Time: ", end_time - start_time)
        else:
            print("Wrong choice");
            self.finish()

    def finish(self):
        print('What do yuo want to do?')
        print('1. Finish the game')
        print('2. Try again')
        choice = input().lower()
        if int(choice) == 1:
            print("Thank you for the game")
        elif int(choice) == 2:
            self.start()
        else:
            print("Wrong choice");
            self.finish()
