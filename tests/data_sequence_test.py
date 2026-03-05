from classes.data_sequence import DataSequence, CombinationMode, merge_unix_time_lists
from classes.data_sequence_plot import plot_sequences

def test_extrapolation_and_plot():
    data_sequence = DataSequence()

    data_sequence.add_value(2000, 10)
    data_sequence.add_value(2005, 15)
    data_sequence.add_value(2010, 20)
    data_sequence.add_value(2020, 40)

    mode = DataSequence.ExtrapolationMode.PREVIOUS
    assert data_sequence.get_value(2000, mode) == 10
    assert data_sequence.get_value(2004, mode) == 10
    assert data_sequence.get_value(2005, mode) == 15
    assert data_sequence.get_value(2009, mode) == 15
    assert data_sequence.get_value(2010, mode) == 20
    assert data_sequence.get_value(2015, mode) == 20

    mode = DataSequence.ExtrapolationMode.INTERPOLATE
    assert data_sequence.get_value(2000, mode) == 10
    assert data_sequence.get_value(2004, mode) == 14
    assert data_sequence.get_value(2005, mode) == 15
    assert data_sequence.get_value(2009, mode) == 19
    assert data_sequence.get_value(2010, mode) == 20
    assert data_sequence.get_value(2015, mode) == 30

    unix_time_list = [unix_time for unix_time in range(2000, 2021)]
    plot_sequences({ "?" : data_sequence }, unix_time_list, DataSequence.ExtrapolationMode.PREVIOUS)
    plot_sequences({ "?" : data_sequence }, unix_time_list, DataSequence.ExtrapolationMode.INTERPOLATE)

def test_merge_unix_time_lists():
    ds1 = DataSequence()
    ds1.add_value(1995, 0)
    ds1.add_value(2000, 0)
    ds1.add_value(2005, 0)
    ds1.add_value(2010, 0)
    ds1.add_value(2015, 0)
    ds2 = DataSequence()
    ds2.add_value(2000, 0)
    ds2.add_value(2004, 0)
    ds2.add_value(2010, 0)
    ds2.add_value(2016, 0)

    unix_time_list = merge_unix_time_lists(ds1, ds2, CombinationMode.UNION)
    assert unix_time_list == [2000, 2004, 2005, 2010, 2015]
    unix_time_list = merge_unix_time_lists(ds1, ds2, CombinationMode.INTERSECTION)
    assert unix_time_list == [2000, 2010]
    unix_time_list = merge_unix_time_lists(ds1, ds2, CombinationMode.FUZZY_INTERSECTION, range=1)
    assert unix_time_list == [2000, 2004, 2010, 2015]

test_extrapolation_and_plot()
test_merge_unix_time_lists()