
# consider making class to avoid passing cli_interface everywhere
def explore_table_metadata(cli_interface, response):
    show_overview(cli_interface, response)

def show_overview(cli_interface, response):
    lines = []
    lines.append(f"Label: {response["label"]}")
    lines.append(f"Variables:")
    for variable in response["id"]:
        lines.append(f"\t{variable}")
    cli_interface.show_lines(*lines)