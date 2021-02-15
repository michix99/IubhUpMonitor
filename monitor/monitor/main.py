import monitor
from monitor.JsonParser import compress_plot_save

m = monitor.Monitor()
# compress_plot_save(m.websites)
m.run_monitor()
