from input_handler import read_input
from kwic_processor import find_keyword_context
from output_handler import display_results

def main():
    text, keyword = read_input()
    results = find_keyword_context(text, keyword)
    display_results(results)

if __name__ == "__main__":
    main()
