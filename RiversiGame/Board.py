from collections import OrderedDict

from Node import Node
from Player import Player


class Board:

    def __init__(self, player1: Player = None, player2: Player = None):
        nodesDict = OrderedDict()
        for i in range(8):
            for j in range(8):
                nodesDict[Node(i, j)] = ' '
        nodesDict[Node(3, 3)] = player1.color
        nodesDict[Node(4, 4)] = player1.color
        nodesDict[Node(3, 4)] = player2.color
        nodesDict[Node(4, 3)] = player2.color
        self.nodes = nodesDict

    def set(self, nodes: OrderedDict()):
        nodesDict = OrderedDict()
        for i in range(8):
            for j in range(8):
                nodesDict[Node(i, j)] = nodes[Node(i, j)]
        self.nodes = nodesDict



    def print_board(self):
        print('    1   2   3   4   5   6   7   8')
        for i in range(8):
            print(i + 1, end=' ')
            for j in range(8):
                print('| %s' % (self.nodes[Node(i, j)]), end=' ')
            print('|')


