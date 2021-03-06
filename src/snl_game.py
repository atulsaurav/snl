"""Game of Snakes and Ladders"""

from random import sample, choice
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use("seaborn")


class Cell(object):
    """Represents each cell on the board
    """

    def __init__(self, ix):  # , visitors=[]):
        self.ix = ix
        self.goto = None
        self.present = None


class Board(object):
    """Represents the board in Snakes & Ladders

    This is can be a list of N² cells where N is number of cells 
    along an edge

    Attributes
    ----------
    N : int
        Number of cells along an edge
    n : int
        total number of snakes or ladders
    n_snakes : int
        number of snakes on the board (to be implemented)
    n_ladders : int
        number of ladders on the board (to be implemented)
    """

    def __init__(self, N=10, n=10, n_snakes=10, n_ladders=10):
        self.board = []
        self.N = N
        self.n_snakes = 0
        self.n_ladders = 0
        for x in range(N * N):
            self.board.append(Cell(x))

        starts = sample(range(1, N * N - 1), n)
        ends = sample(range(1, N * N - 1), n)
        for start, end in zip(starts, ends):
            if start < end:
                self.board[start].present = "Ladder"
                self.n_ladders += 1
            elif start > end:
                self.board[start].present = "Snake"
                self.n_snakes += 1
            else:
                print(f"Ignoring fake transport from {start} to {end}")
            self.board[start].goto = end

    def describe(self):
        for cell in self.board:
            if cell.present:
                print(f"{cell.present} from {cell.ix} to {cell.goto}")


class Dice:
    def __init__(self, n_faces=6, seed=0):
        self.n_faces = n_faces
        self.seed = seed

    def roll(self):
        return choice(range(1, self.n_faces + 1))


class Player:
    def __init__(self, id):
        self.id = id
        self.pos = None
        self.end = None
        self.rolls = []
        self.positions = [0]

    def move(self, pos, board):
        print(f"Player {self.id} is at {self.pos} and got {pos}")
        self.rolls.append(pos)
        new_pos = self.pos + pos if self.pos else pos
        try:
            new_pos = (
                board.board[new_pos].goto if board.board[new_pos].goto else new_pos
            )
        except IndexError:
            self.positions.append(self.pos)
            return
        if new_pos == len(board.board) - 1:
            self.end = True
        print(f"Player {self.id} moves to {new_pos}")
        self.positions.append(new_pos)
        self.pos = new_pos


class Game:
    def __init__(self, n_players, size=10, sol=10):
        self.players = [Player(x) for x in range(n_players)]
        self.dice = Dice(n_faces=6)
        self.board = Board(N=size, n=sol)

    def play(self):
        while True:
            if len([p for p in self.players if p.end]) >= len(self.players) - 1:
                break
            for player in self.players:
                dice_value = self.dice.roll()
                player.move(dice_value, self.board)
                if player.end:
                    break

    def show(self):
        plt.plot(self.players[0].positions, label="Player 0")
        plt.plot(self.players[1].positions, label="Player 1")
        plt.xlabel("Turn number")
        plt.ylabel("Position on the board")
        plt.title("Game of Snakes & Ladders")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    game = Game(2, size=10, sol=15)
    game.play()
    print("=" * 40)
    game.board.describe()
    game.show()
