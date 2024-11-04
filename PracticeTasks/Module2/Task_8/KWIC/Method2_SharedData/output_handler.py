def display_results(context):
    # Output of results
    for line, position in context:
        print(f"Keyword found in: '{line}' at position {position}")
