import monitor
from monitor.JsonParser import compress_plot_save

# Entry point to run the monitor (and optionally compress data)

m = monitor.Monitor()
# compress_plot_save(m.websites)
m.run_monitor()
