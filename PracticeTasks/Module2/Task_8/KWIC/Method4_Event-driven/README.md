# Key Word in Context - Event-Driven Solution

## Task Description

This program implements the **Key Word in Context (KWIC)** system, designed to process a text input and generate contexts for each word based on a specified keyword. The program uses an event-driven (implicit invocation) approach to handle the flow of events and manage context creation and display.

## Project Structure

The project is organized in a modular structure:
```
Method4_Event_Driven/
├── main.py                  # Main file with the logic to process text input and manage events
├── event_manager.py         # Module for managing event subscriptions and firing events
└── README.md                # Documentation file with project description and usage instructions
```
### Modules

- `event_manager.py`: Manages event subscriptions, allowing actions in `main.py` to be triggered by specific events.

### Requirements

- Python 3.6 or higher

## Running the Program

1. Clone or download the project repository.
2. Run the program with the following command:
```
python main.py
```
### Input Example

**Sample Input** (entered during program execution):
```
Input: This is an example of the Key Word in Context system
```
### Output Example

**Sample Output**:
```
Result:
This                | example    | of the Key Word in Context    
is                  | example    | of the Key Word in Context    
an                  | example    | of the Key Word in Context    
```
## Explanation

1. **Event-Driven Approach**: The program leverages events to process text input, create contexts for keywords, and display results.
2. **Event Flow**:
    - The program starts by reading text input from the user.
    - It splits the text into words and generates contexts for each word based on the keyword.
    - Upon constructing contexts, the program fires an event to display the sorted contexts in a structured format.

### Additional Notes

- The program is designed to handle various text inputs and generates contexts dynamically.
- The event-driven approach allows for easy modifications or extensions of functionality by subscribing new actions to specific events in `event_manager.py`.