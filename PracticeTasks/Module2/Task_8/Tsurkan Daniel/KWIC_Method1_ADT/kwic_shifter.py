from kwic.circular_shift import CircularShift

class KwicShifter:
    def __init__(self, kwic_input):
        self.kwic_input = kwic_input
        self.circular_shifts = []

    def generate_circular_shifts(self):
        for line in self.kwic_input.get_lines():
            words = line.split()
            for i, word in enumerate(words):
                if self._is_significant_word(word):
                    self.circular_shifts.append(CircularShift(line, i))

    def _is_significant_word(self, word):
        clean_word = ''.join(char for char in word if char.isalnum()).lower()
        return clean_word not in self.kwic_input.get_keywords()

    def get_circular_shifts(self):
        return self.circular_shifts
