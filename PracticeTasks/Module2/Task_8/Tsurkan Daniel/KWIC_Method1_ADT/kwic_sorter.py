class KwicSorter:
    def __init__(self, shifter):
        self.shifter = shifter
        self.sorted_shifts = []

    def generate_sorted_list(self):
        self.sorted_shifts = sorted(self.shifter.get_circular_shifts(), key=lambda shift: shift.get_shifted_line().lower())

    def get_sorted_shifts(self):
        return self.sorted_shifts
