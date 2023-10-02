from jezdzenka.console.interface import initial, interface_handler
from jezdzenka.console.tables import show_single, show_single_verbose


def main():
    interface_handler(initial())


if __name__ == '__main__':
    main()
