
# consider making class to avoid passing cli_interface everywhere
def explore_table_metadata(cli_interface, metadata_response):
    show_overview(cli_interface, metadata_response)


def show_overview(cli_interface, metadata_response):
    lines = []
    lines.append(f"Label: {metadata_response["label"]}")
    lines.append(f"Variables:")
    dimension_label_list = metadata_response["id"]
    dimension_size_list = metadata_response["size"]
    assert len(dimension_label_list) == len(dimension_size_list)
    for dimension_index in range(len(dimension_label_list)):
        label = dimension_label_list[dimension_index]
        size = dimension_size_list[dimension_index]
        lines.append(
            f"\t{label}, {size}")
        category_index_dict = metadata_response["dimension"][label]["category"]["label"]
        for category_index in category_index_dict:
            category_label = category_index_dict[category_index]
            lines.append(f"\t\t{category_label}")
    cli_interface.show_lines(lines)
