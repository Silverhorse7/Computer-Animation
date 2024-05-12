import random


class TicTacToe:

    def __init__(self):
        """Initialize with empty board"""
        self.board = [" ", " ", " ",
                      " ", " ", " ",
                      " ", " ", " "]

    def show(self):
        """Format and print board"""
        print("""
          {} | {} | {}
         -----------
          {} | {} | {}
         -----------
          {} | {} | {}
        """.format(*self.board))

    def clearBoard(self):
        self.board = [" ", " ", " ",
                      " ", " ", " ",
                      " ", " ", " "]

    def whoWon(self):
        if self.checkWin() == "X":
            return "X"
        elif self.checkWin() == "O":
            return "O"
        elif self.gameOver() == True:
            return "Nobody"

    def availableMoves(self):
        """Return empty spaces on the board"""
        moves = []
        for i in range(0, len(self.board)):
            if self.board[i] == " ":
                moves.append(i)
        return moves

    def getMoves(self, player):
        """Get all moves made by a given player"""
        moves = []
        for i in range(0, len(self.board)):
            if self.board[i] == player:
                moves.append(i)
        return moves

    def makeMove(self, position, player):
        """Make a move on the board"""
        if self.board[position] == " ":
            self.board[position] = player
            return True
        elif self.board[position] != " " and player == " ":
            self.board[position] = player
            return True
        else:
            print("Invalid Move")
            return False

    def checkWin(self):
        """Return the player that wins the game"""
        combos = ([0, 1, 2], [3, 4, 5], [6, 7, 8],
                  [0, 3, 6], [1, 4, 7], [2, 5, 8],
                  [0, 4, 8], [2, 4, 6])

        for player in ("X", "O"):
            positions = self.getMoves(player)
            for combo in combos:
                win = True
                for pos in combo:
                    if pos not in positions:
                        win = False
                if win:
                    return player

    def gameOver(self):
        """Return True if X wins, O wins, or draw, else return False"""
        if self.checkWin() != None:
            return True
        for i in self.board:
            if i == " ":
                return False
        return True

    def minimax(self, board, depth, player):
        if player == "O":
            best = -float('inf')
        else:
            best = float('inf')

        # TODO: Check for depth 
        if board.checkWin() or not board.availableMoves():
            if board.checkWin() == "O":
                return 100 + depth # Faster Win
            elif board.checkWin() == "X":
                return depth # Shorter Loss
            else:
                return 0

        for move in board.availableMoves():
            board.makeMove(move, player)
            if player == "O":
                val = self.minimax(board, depth - 1, changePlayer(player))
                best = max(best, val)
            else:
                val = self.minimax(board, depth - 1, changePlayer(player))
                best = min(best, val)
            board.makeMove(move, " ")  # Undo the move

        return best


def changePlayer(player):
    """Returns the opposite player given any player"""
    if player == "X":
        return "O"
    else:
        return "X"


def make_best_move(board, depth, player):
    best_val = -float('inf')
    best_move = None
    moves = board.availableMoves()

    for move in moves:
        board.makeMove(move, player)
        move_val = board.minimax(board, depth-1, changePlayer(player))
        board.makeMove(move, " ")  # Undo the move

        if move_val > best_val:
            best_val = move_val
            best_move = move

    return best_move


# Actual game
if __name__ == '__main__':
    game = TicTacToe()
    game.show()

    while game.gameOver() == False:

        isValid = False
        while not isValid:
            person_move = int(input("You are X: Choose number from 1-9: "))
            isValid = game.makeMove(person_move - 1, "X")
        game.show()

        if game.gameOver() == True:
            break

        print("Computer choosing move...")
        ai_move = make_best_move(game, -1, "O")
        game.makeMove(ai_move, "O")
        game.show()

print("Game Over. " + game.whoWon() + " Wins")
