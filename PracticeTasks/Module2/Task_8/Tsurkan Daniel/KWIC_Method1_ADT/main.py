import sys
from kwic.kwic_processor import KWICProcessor

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Specify text file and keywords file.")
    else:
        text_file, keywords_file = sys.argv[1], sys.argv[2]
        kwic_processor = KWICProcessor(text_file, keywords_file)
        kwic_processor.process()
