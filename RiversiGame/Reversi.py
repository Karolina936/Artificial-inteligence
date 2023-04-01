from Board import Board
from Node import Node
from Player import Player


class Reversi:

    BLACK = 'B'
    WHITE = 'W'
    EMPTY = ' '

    DIRECTIONS = [Node(x, y)
                  for x, y in [(-1, -1), (-1, 0), (0, -1), (1, -1),
                               (-1, 1), (0, 1), (1, 0), (1, 1)]]

    GAME_STATES = {
        "IN_PROGRESS": 'In progress',
        "BLACK_WINS": 'Black wins',
        "WHITE_WINS": 'White wins',
        "TIE": 'Tie'
    }

    def __init__(self, single_player=False):
        self.player1 = Player(self.BLACK)
        self.player2 = Player(self.WHITE)

        self.board = Board(self.player2, self.player1)

        self.player = self.player1

        self.player1.result = 2
        self.player2.result = 2
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
            print("Player2 - white color")
        else:
            self.player = self.player1
            print("Player1 - black color")

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
        self.board.print_board()
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


    def play(self):
        while self.game_state == self.GAME_STATES['IN_PROGRESS']:
            node = self.get_player_move()
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

            # update player result after aech move
            self.player1.result = len(self.get_player1_discs())
            self.player2.result = len(self.get_player2_discs())
            self.change_current_player()
            self.game_state = self.check()


        # fields that are flipped after a move


    # run after every move
    def check(self):
        # change player if there is no move for first player
        if not self.available_fields():
            self.change_current_player()

            # if second player had no move determine the winner
            if not self.available_fields():
                if self.player2.result > self.player1.result:
                    return self.GAME_STATES["WHITE_WINS"]
                elif self.player2.result < self.player1.result:
                    return self.GAME_STATES["BLACK_WINS"]
                else:
                    return self.GAME_STATES["TIE"]
        return self.GAME_STATES["IN_PROGRESS"]

    def game_result(self):
        if self.game_state == self.GAME_STATES['TIE']:
            print('Tie')
        elif self.game_state == self.GAME_STATES['"BLACK_WINS"']:
            print("Player1 won")
        else:
            print("Player2 won")
        print("Result")
        print("Player1: ", self.player1.result)
        print("Player2: ", self.player2.result)

    def game_info(self):
        player_map = {
            "B": "black",
            "W": "white"
        }
        return {
            "board": self.board.print_board(),
            "player": player_map[self.player.color],
            "state": self.game_state,
            "white_count": self.player2.result,
            "black_count": self.player1.result
        }
