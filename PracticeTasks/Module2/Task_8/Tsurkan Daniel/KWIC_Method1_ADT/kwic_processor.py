from kwic.kwic_input import KwicInput
from kwic.kwic_shifter import KwicShifter
from kwic.kwic_sorter import KwicSorter
from kwic.kwic_output import KwicOutput

class KWICProcessor:
    def __init__(self, text_filename, keywords_filename):
        self.input = KwicInput(text_filename, keywords_filename)
        self.shifter = KwicShifter(self.input)
        self.sorter = KwicSorter(self.shifter)
        self.output = KwicOutput(self.sorter)

    def process(self):
        self.shifter.generate_circular_shifts()
        self.sorter.generate_sorted_list()
        self.output.show_output()
