# Eight Queens Problem - Event-Driven Solution

## Task Description

This program solves the **Eight Queens** problem, where the goal is to place eight queens on an 8x8 chessboard so that no two queens threaten each other. This means no two queens can share the same row, column, or diagonal. The solution is implemented using an event-driven (implicit invocation) approach.

## Project Structure

The project is organized in a modular structure:
```
Method4_Event_Driven/
├── main.py                  # Main file with the logic to solve the Eight Queens problem and manage events
├── event_manager.py         # Module for managing event subscriptions and firing events
└── README.md                # Documentation file with project description and usage instructions
```
### Modules

-  `event_manager.py`: Manages event subscriptions, allowing actions in `main.py` to be triggered by specific events.

### Requirements

- Python 3.6 or higher

## Running the Program

1. Clone or download the project repository.
2. Run the program with the following command:
```bash
python main.py
```
### Input and Output Example

**Sample Input** (entered during program execution):
```
Initial position (x y): 0 0
```

**Sample Output**:
```
Solution:
Q - - - - - - -
- - - Q - - - -
- - - - - Q - -
- Q - - - - - -
- - - - - - Q -
- - Q - - - - -
- - - - Q - - -
- - - - - - - Q
```
## Explanation

1. **Event-Driven Approach**: The program uses events to manage queen placements and solution display.
2. **Event Flow**:
    - The program starts by placing the initial queen based on user input.
    - An event-driven backtracking algorithm then places each subsequent queen, checking that no two queens threaten each other.
    - Upon finding a complete solution, the program fires an event to display the result.

### Additional Notes

- The program outputs all unique solutions for the 8x8 board.
- The event-driven approach makes it easy to modify or extend functionality by subscribing new actions to specific events in `event_manager.py`.