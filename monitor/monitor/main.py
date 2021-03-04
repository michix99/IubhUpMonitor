import monitor
import time

from monitor import Website
from monitor.Utils import plot_data, get_sec, get_past_utc, create_json, create_status_json, create_rest_json

# Entry point to run the monitor (and optionally compress data)


m = monitor.Monitor()
m.run_monitor()
