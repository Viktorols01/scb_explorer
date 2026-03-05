
# consider making class to avoid passing cli_interface everywhere
def explore_table_metadata(cli_interface, response):
    show_overview(cli_interface, response)


def show_overview(cli_interface, response):
    lines = []
    lines.append(f"Label: {response["label"]}")
    lines.append(f"Variables:")
    dimension_label_list = response["id"]
    dimension_size_list = response["size"]
    assert len(dimension_label_list) == len(dimension_size_list)
    for dimension_index in range(len(dimension_label_list)):
        lines.append(
            f"\t{dimension_label_list[dimension_index]}, {dimension_size_list[dimension_index]}")
    cli_interface.show(*lines)
