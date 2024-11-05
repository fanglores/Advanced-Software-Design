class KwicOutput:
    def __init__(self, sorter):
        self.sorter = sorter

    def show_output(self):
        for shift in self.sorter.get_sorted_shifts():
            print(shift)
