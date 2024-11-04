def solve_eight_queens(N):
    """ Main function to solve the Eight Queens problem. """
    solutions = []
    board = [['.'] * N for _ in range(N)]  # Create an empty N x N board
    backtrack(board, 0, solutions)
    return solutions

def backtrack(board, row, solutions):
    """ Recursive backtracking function to place queens. """
    if row == len(board):
        # All queens are placed, save the solution
        solutions.append([''.join(r) for r in board])
        return

    for col in range(len(board)):
        if is_safe(board, row, col):
            board[row][col] = 'Q'  # Place queen
            backtrack(board, row + 1, solutions)  # Recur to place next queen
            board[row][col] = '.'  # Remove queen (backtrack)

def is_safe(board, row, col):
    """ Check if placing a queen is safe. """
    # Check column and diagonals for conflicts
    for i in range(row):
        if board[i][col] == 'Q':
            return False
        if col - (row - i) >= 0 and board[i][col - (row - i)] == 'Q':
            return False
        if col + (row - i) < len(board) and board[i][col + (row - i)] == 'Q':
            return False
    return True
