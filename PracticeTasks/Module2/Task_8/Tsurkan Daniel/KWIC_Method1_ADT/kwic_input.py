import os

class KwicInput:
    def __init__(self, text_filename, keywords_filename):
        self.lines = self._read_file(text_filename)
        self.keywords = set(self._read_file(keywords_filename)[0].strip().lower().split())

    def _read_file(self, filename):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File '{filename}' not found.")
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]

    def get_lines(self):
        return self.lines

    def get_keywords(self):
        return self.keywords
