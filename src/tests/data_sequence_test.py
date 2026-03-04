from classes.data_sequence import DataSequence
from classes.data_sequence_plot import plot_sequences

data_sequence = DataSequence()

data_sequence.add_value(2000, 10)

assert data_sequence.get_value(2000) == 10
# workaround
throws_error = False
try:
    assert data_sequence.get_value(1999) == 10
except:
    throws_error = True
assert throws_error


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