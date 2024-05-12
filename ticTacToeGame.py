import random


class TicTacToe:

    def __init__(self):
        """Initialize with empty board"""
        self.board = [" ", " ", " ",
                      " ", " ", " ",
                      " ", " ", " "]
        self.memoization = {}

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

    def minimax(self, board, depth, player, alpha, beta):

        memo_key = (tuple(board.board), depth, player)
        if memo_key in board.memoization:
            return board.memoization[memo_key]
        
        if board.checkWin() or not board.availableMoves():
            if board.checkWin() == "O":
                return_value = 100 + depth # Prefer faster win
            elif board.checkWin() == "X":
                return_value = depth # Prefer slower loss
            else:
                return_value = 0
            
            board.memoization[memo_key] = return_value
            return return_value

        if player == "O":
            value = -float('inf')
            for move in board.availableMoves():
                board.makeMove(move, player)
                value = max(value, self.minimax(board, depth - 1, changePlayer(player), alpha, beta))
                board.makeMove(move, " ")  # Undo the move

                alpha = max(alpha, value) 
                if alpha >= beta:
                    break  # Beta cut-off

        else:
            value = float('inf')
            for move in board.availableMoves():
                board.makeMove(move, player)
                value = min(value, self.minimax(board, depth - 1, changePlayer(player), alpha, beta))
                board.makeMove(move, " ")  # Undo the move

                beta = min(beta, value) 
                if beta <= alpha:
                    break  # Alpha cut-off

        board.memoization[memo_key] = value
        return value


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
    alpha, beta = -float('inf'), float('inf')

    for move in moves:
        board.makeMove(move, player)
        move_val = board.minimax(board, depth-1, changePlayer(player), alpha, beta)
        board.makeMove(move, " ")  # Undo the move

        if (player == 'O' and move_val > best_val) or (player == 'X' and move_val < best_val):
            best_val = move_val
            best_move = move
            if player == 'O':
                alpha = max(alpha, best_val)
            else:
                beta = min(beta, best_val)

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
