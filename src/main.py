from modules.api_wrapper import ApiWrapper
from modules.cli_interface import CliInterface

from curses import wrapper

from explore_table_metadata import explore_table_metadata


def print_tables(response):
    for table in response["tables"]:
        print("Label:", table["label"])
        print("Id:", table["id"])
        print("Variables")
        for variable_name in table["variableNames"]:
            print("\t", variable_name)
        print("")
        # yooo jag borde hämta metadata istället, det ger dimension-storlekar o grejor



def search_for_table(cli_interface, api_wrapper):
    query = cli_interface.get_input("Query: ")
    response = api_wrapper.get_tables_by_query(query)
    choices = []
    for table in response["tables"]:
        choice = (table["label"], table["id"])
        choices.append(choice)
    table_id = cli_interface.get_choice(choices)

    response = api_wrapper.get_table_metadata(table_id)
    explore_table_metadata(cli_interface, response)


def main(stdscr):
    cli_interface = CliInterface(stdscr)
    api_wrapper = ApiWrapper()
    while True:
        search_for_table(cli_interface, api_wrapper)


if __name__ == "__main__":
    wrapper(main)
