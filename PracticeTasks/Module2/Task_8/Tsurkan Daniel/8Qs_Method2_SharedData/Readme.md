# Eight Queens Problem

## Task Description

This program solves the **Eight Queens** problem, a classic combinatorial problem in which the goal is to place eight queens on an 8x8 chessboard such that no two queens threaten each other. This means that no two queens can share the same row, column, or diagonal.

## Project Structure

The project is organized in a modular structure:
```
Method2_Shared_Data/
│
├── main.py                  # Main file to run the application
├── eight_queens.py          # Module that contains the logic to solve the Eight Queens problem
├── output_handler.py        # Module to display results
└── README.md                # Documentation file with project description and usage instructions
```
### Modules

- `eight_queens.py`: Contains the implementation of the backtracking algorithm to solve the Eight Queens problem.
- `output_handler.py`: Formats and displays the solution(s) found.
### Requirements

- Python 3.6 or higher

### Running the Program

1. Clone or download the project repository.
2. Run the program with the following command:
```bash
python main.py
```
### Output Example

**Sample Output**:
```
Solutions for the Eight Queens Problem:

Solution 1:
. Q . . . . . . 
. . . . Q . . . 
. . . . . . Q . 
. . . . . . . Q 
Q . . . . . . . 
. . . Q . . . . 
. . . . . Q . . 
. . Q . . . . . 

Solution 2:
. . Q . . . . . 
. . . . . Q . . 
. . . . . . . Q 
. . . . Q . . . 
. Q . . . . . . 
. . . . . . Q . 
Q . . . . . . . 
. . . Q . . . . 
```
## Explanation

1. The program uses a backtracking algorithm to find all possible solutions for placing eight queens on the chessboard.
2. It explores each row and column, placing queens in valid positions while ensuring that no two queens can attack each other.
3. Once a solution is found, it is displayed in a readable format, showing the positions of the queens on the board (represented as 'Q') and empty spaces (represented as '.').
## Additional Notes

- The program can be modified to solve for a different number of queens by changing the board size in the `eight_queens.py` module.
- The current implementation finds and displays all unique solutions for the standard 8x8 board.