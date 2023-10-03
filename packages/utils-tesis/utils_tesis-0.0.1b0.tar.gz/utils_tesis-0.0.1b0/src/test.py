import utils_tesis.integration as itg
from utils_tesis.signalload import CSV_pandas

signal_info = {}
signal_info["window_length"] = 64
signal_info["step"] = 4
signals = CSV_pandas()
signals.relay_list()
signal_info["signals"] = signals
signal_info["signal_name"] = "I: X0023A-R1A"
t, trip = itg.img_trip(signal_info)
import matplotlib.pyplot as plt

plt.stem(t, trip)
plt.show()
