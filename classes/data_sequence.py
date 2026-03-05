import bisect
import numpy as np


class DataSequence:
    class ExtrapolationMode:
        INTERPOLATE = 0
        PREVIOUS = 1
        NEXT = 2

    def __init__(self):
        self.sorted_values = []

    def add_value(self, unix_time, value):
        element = unix_time, value
        bisect.insort_right(self.sorted_values, element, key=lambda x: x[0])

    def get_value(self, unix_time, mode=ExtrapolationMode.PREVIOUS):
        previous_element_index = self.get_previous_or_same_index(unix_time)
        previous_unix_time, previous_value = self.sorted_values[previous_element_index]
        if previous_unix_time == unix_time:
            return previous_value

        next_unix_time, next_value = self.sorted_values[previous_element_index + 1]

        match mode:
            case self.ExtrapolationMode.INTERPOLATE:
                t = (unix_time - previous_unix_time) / \
                    (next_unix_time - previous_unix_time)
                return previous_value * (1 - t) + next_value * t
            case self.ExtrapolationMode.PREVIOUS:
                return previous_value
            case self.ExtrapolationMode.NEXT:
                return next_value
            case _:
                return

    def get_value_list(self, unix_time_list, mode=ExtrapolationMode.PREVIOUS):
        values = []
        for unix_time in unix_time_list:
            value = self.get_value(unix_time, mode)
            values.append(value)
        return values

    def get_unix_time_list(self):
        unix_time_list = []
        for element in self.sorted_values:
            unix_time, _ = element
            unix_time_list.append(element)
        return unix_time_list

    def get_unix_time(self, index):
        unix_time, _ = self.sorted_values[index]
        return unix_time

    def get_previous_or_same_index(self, unix_time):
        return bisect.bisect_right(self.sorted_values, unix_time, key=lambda x: x[0]) - 1

    def length(self):
        return len(self.sorted_values)


class CombinationMode:
    # add all distinct times
    UNION = 0
    # add only distinct times that exist in both sequences
    INTERSECTION = 1
    # add only distinct times that exist in both sequences (fuzzy equal using range)
    # only the smallest time is added - we don't want doubled fuzzy equal points
    FUZZY_INTERSECTION = 2


def merge_unix_time_lists(ds1, ds2, mode=CombinationMode.UNION, range=0):
    """
    Creates a unix_time_list from two data sequences.
    Only collects samples from the overlapping time interval.
    """
    unix_time_list = []

    if ds1.get_unix_time(0) < ds2.get_unix_time(0):
        first_common_unix_time = ds2.get_unix_time(0)
        i1 = ds1.get_previous_or_same_index(first_common_unix_time)
        i2 = 0
    elif ds1.get_unix_time(0) > ds2.get_unix_time(0):
        first_common_unix_time = ds1.get_unix_time(0)
        i1 = 0
        i2 = ds2.get_previous_or_same_index(first_common_unix_time)
    else:
        i1 = 0
        i2 = 0

    while i1 < ds1.length() and i2 < ds2.length():
        unix_time_1 = ds1.get_unix_time(i1)
        unix_time_2 = ds2.get_unix_time(i2)
        unix_time = None
        match mode:
            case CombinationMode.UNION:
                if unix_time_1 < unix_time_2:
                    unix_time = unix_time_1
                    i1 += 1
                elif unix_time_1 > unix_time_2:
                    unix_time = unix_time_2
                    i2 += 1
                else:
                    unix_time = unix_time_1
                    i1 += 1
                    i2 += 1
            case CombinationMode.INTERSECTION:
                if unix_time_1 == unix_time_2:
                    unix_time = unix_time_1
                    i1 += 1
                    i2 += 1
                else:
                    if unix_time_1 < unix_time_2:
                        i1 += 1
                    else:
                        i2 += 1
                    continue  # don't append
            case CombinationMode.FUZZY_INTERSECTION:
                if np.abs(unix_time_1 - unix_time_2) <= range:
                    unix_time = min(unix_time_1, unix_time_2)
                    i1 += 1
                    i2 += 1
                else:
                    if unix_time_1 < unix_time_2:
                        i1 += 1
                    else:
                        i2 += 1
                    continue  # don't append
            case _:
                pass

        unix_time_list.append(unix_time)
    return unix_time_list
