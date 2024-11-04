# Key Word in Context (KWIC)

## Task Description

This program implements the **Key Word in Context (KWIC)** task. It allows users to find a keyword within a given text and outputs sentences that contain the keyword, showing its context.

## Project Structure

The project is organized in a modular structure:

```
Method2_Shared_Data/
│
├── main.py                  # Main file to run the application
├── input_handler.py         # Module to handle input
├── kwic_processor.py        # Module to search for the keyword and its context
├── output_handler.py        # Module to display results
└── README.md                # Documentation file with project description and usage instructions
```

### Modules

- `input_handler.py`: Handles text and keyword input.
- `kwic_processor.py`: Processes the text and identifies the keyword's context.
- `output_handler.py`: Formats and displays the search results.

## How to Run

### Requirements

- Python 3.6 or higher

### Running the Program

1. Clone or download the project repository.
2. Run the program with the following command:

```bash
python main.py
```

### Input and Output Example

**Sample Input** (entered during program execution):

```
Enter text:
The quick brown fox jumps over the lazy dog. The fox is quick and clever.
Enter keyword:
fox
```

**Sample Output**:

```
Search results for the keyword "fox":

1. 'The quick brown fox jumps over the lazy dog' at position 16
2. 'The fox is quick and clever.' at position 4
```

## Explanation

1. The program prompts the user for a text and a keyword to search for.
2. It then identifies all sentences containing the keyword and stores them.
3. The program displays each sentence that includes the keyword, highlighting its context within the text.
