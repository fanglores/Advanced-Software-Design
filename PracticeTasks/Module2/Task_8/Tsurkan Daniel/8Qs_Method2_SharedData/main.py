from eight_queens import solve_eight_queens
from output_handler import display_solutions

def main():
    N = 8  # Set the size of the chessboard
    solutions = solve_eight_queens(N)
    display_solutions(solutions)

if __name__ == "__main__":
    main()
