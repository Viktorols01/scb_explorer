from modules.api_wrapper import ApiWrapper
from modules.cli_interface import CliInterface

from curses import wrapper


def print_tables(response):
    for table in response["tables"]:
        print("Label:", table["label"])
        print("Id:", table["id"])
        print("Variables")
        for variable_name in table["variableNames"]:
            print("\t", variable_name)
        print("")
        # yooo jag borde hämta metadata istället, det ger dimension-storlekar o grejor


def iterate_over_tables():
    page_number = 1
    while True:
        response, is_last_page = api_wrapper.get_table_page(page_number)

        print_tables(response)

        if is_last_page:
            break
        page_number += 1


def main(stdscr):
    cli_interface = CliInterface(stdscr)
    api_wrapper = ApiWrapper()
    choices = [f"{i}" for i in range(25)]
    choice = cli_interface.get_choice(choices)
    cli_interface.show_lines("Selected choice:", choice)


if __name__ == "__main__":
    wrapper(main)
