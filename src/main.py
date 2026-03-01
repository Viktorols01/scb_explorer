from modules.api_wrapper import ApiWrapper

api_wrapper = ApiWrapper()


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


def main():
    response = api_wrapper.get_tables_by_query("polis")
    print_tables(response)


if __name__ == "__main__":
    main()
