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
    _, table_id = cli_interface.get_choice(choices)
    response = api_wrapper.get_table_metadata(table_id)
    explore_table_metadata(cli_interface, response)
    return (table_id, response["label"])


def accumulate_tables(cli_interface, api_wrapper):
    table_data_list = []
    while True:
        choices = []
        for table_data in table_data_list:
            table_id, label = table_data
            choice = (f"{table_id}: {label}", table_id)
            choices.append(choice)
        choices.append("(+) Add new table")
        choice_index, value = cli_interface.get_choice(choices)
        if choice_index == len(choices) - 1:
            table_data = search_for_table(cli_interface, api_wrapper)
            table_data_list.append(table_data)
        else:
            cli_interface.show_lines(
                "Not implemented, but would do something with", value)


def main(stdscr):
    cli_interface = CliInterface(stdscr)
    api_wrapper = ApiWrapper()
    accumulate_tables(cli_interface, api_wrapper)


if __name__ == "__main__":
    wrapper(main)
    # api_wrapper = ApiWrapper()
    # table_id = "TAB1136"
    # response = api_wrapper.get_table_metadata(table_id)
    # import json
    # print(json.dumps(response, indent=2))
