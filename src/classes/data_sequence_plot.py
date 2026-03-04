import matplotlib.pyplot as plt


def plot_sequences(data_sequence_map, unix_time_list, mode):
    for title in data_sequence_map:
        values = data_sequence_map[title].get_value_list(unix_time_list, mode)
        plt.plot(unix_time_list, values, 'o', label=title)
        plt.xlabel("Unix time")
        plt.show()
