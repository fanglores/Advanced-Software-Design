def display_solutions(solutions):
    """ Display the found solutions for the Eight Queens problem. """
    print("Solutions for the Eight Queens Problem:\n")
    for i, solution in enumerate(solutions):
        print(f"Solution {i + 1}:")
        for row in solution:
            print(row)
        print()  # Print a newline for better readability
