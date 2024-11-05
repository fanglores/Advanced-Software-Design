from search_position_impl import SearchPositionImpl
from print_position_impl import PrintPositionImpl

def main():
    search_position = SearchPositionImpl()
    result = search_position.search()
    PrintPositionImpl.print(result)

if __name__ == "__main__":
    main()
