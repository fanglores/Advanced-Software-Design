class PrintPositionImpl:
    @staticmethod
    def print(queens):
        print("\n┏━━━━━━━━━━━━━━┓")
        print("┃   SOLVED!    ┃")
        print("┗━━━━━━━━━━━━━━┛\n")
        print("Final state:")
        print("-" + "-".join(str(q + 1) for q in queens) + "-")
