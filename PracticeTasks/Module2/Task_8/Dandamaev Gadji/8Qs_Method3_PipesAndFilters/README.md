# Eight Queens Problem - Pipes-and-Filters Solution

## Task Description

This program solves the Eight Queens problem, a well-known combinatorial puzzle. The objective is to place eight queens on an 8x8 chessboard in such a way that no two queens threaten each other. This requires ensuring that no two queens are in the same row, column, or diagonal.

## Project Structure

The project is organized in a modular structure:
```
Method3_Pipes_and_Filters/
├── main.py                  # Main file to initialize filters and manage data flow between them
├── board.py                 # Module representing the chessboard, handling queen placements and safety checks
├── input_filter.py          # Filter to initialize the board and send it to the pipeline
├── placement_filter.py      # Filter to apply backtracking for queen placement
├── solution_filter.py       # Filter to format and forward complete solutions
├── output_filter.py         # Filter to display formatted solutions
└── README.md                # Documentation file with project description and usage instructions
```
### Modules

- `board.py`: Represents the chessboard, handling queen placements and safety checks.
- `input_filter.py`: Filter to initialize the board and send it to the pipeline.
- `placement_filter.py`: Filter that applies backtracking for queen placement.
- `solution_filter.py`: Filter that formats and forwards complete solutions.
- `output_filter.py`: Filter that displays formatted solutions.
- `event_manager.py`: Manages event subscriptions, allowing actions in `main.py` to be triggered by specific events.
### Requirements

- Python 3.6 or higher

## Running the Program

1. Clone or download the project repository.
2. Run the program with the following command:
```
python main.py
```
### Output Example

**Sample Output**:
```
Solution: [0, 4, 7, 5, 2, 6, 1, 3]
Solution: [0, 5, 7, 2, 6, 3, 1, 4]
...
```
Each solution list indicates where queens are positioned on the board: the index in the list is the row, and the integer at each index represents the column of the queen in that row.
## Explanation

1. **Pipes-and-Filters Approach**: The program utilizes a pipes-and-filters architecture to efficiently process solutions for the Eight Queens problem, where each filter performs a specific task in the solution workflow.
2. **Data Flow**:
    - The program begins by initializing the board size and setting up inter-process communication pipes for data transfer between filters.
    - The `input_filter` creates a `Board` object and sends it to the `placement_filter`.
    - The `placement_filter` applies backtracking to place queens on the board, sending complete solutions to the `solution_filter`.
    - The `solution_filter` formats the solutions for readability and forwards them to the `output_filter`.
    - Finally, the `output_filter` displays the formatted solutions to the user, showing all valid arrangements of the queens on the chessboard.

### Additional Notes

- The Pipes-and-Filters approach used here enables flexibility and modularity. Each filter can be modified or extended without affecting other parts of the program. This program currently solves the classic 8x8 board problem, but you can adjust the board size by changing the `size` parameter in `main.py`.