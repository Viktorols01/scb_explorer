import bisect


class DataSequence:
    class ExtrapolationMode:
        INTERPOLATE = 0
        PREVIOUS = 1
        NEXT = 2

    def __init__(self, title):
        self.title = title
        self.sorted_values = []
        self.min_unix_time = 2**32 - 1
        self.max_unix_time = 0

    def add_value(self, unix_time, value):
        if unix_time < self.min_unix_time:
            self.min_unix_time = unix_time
        if unix_time > self.max_unix_time:
            self.max_unix_time = unix_time
        element = unix_time, value
        bisect.insort_right(self.sorted_values, element, key=lambda x: x[0])

    def get_value(self, unix_time, mode=ExtrapolationMode.PREVIOUS):
        if unix_time < self.min_unix_time or unix_time > self.max_unix_time:
            raise Exception("Provided unix time outside of existing interval")

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
                return 0

    def get_previous_or_same_index(self, unix_time):
        return bisect.bisect_right(self.sorted_values, unix_time, key=lambda x: x[0]) - 1
