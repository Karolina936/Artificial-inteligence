class Node():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Node(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def is_on_board(self):
        return min(self.x, self.y) >= 0 and max(self.x, self.y) < 8


    def check(self, end, step):
        if (end.x - self.x) * step.y != (end.y - self.y) * step.x:
            return False

        result = []
        node = self
        while node != end:
            result.append(node)
            node += step
        return result
