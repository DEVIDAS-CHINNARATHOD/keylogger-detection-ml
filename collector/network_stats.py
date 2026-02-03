import psutil
import time

class NetworkCollector:
    def __init__(self):
        self.prev = psutil.net_io_counters()
        self.prev_time = time.time()

    def collect(self):
        time.sleep(1)

        current = psutil.net_io_counters()
        now = time.time()

        duration = now - self.prev_time
        if duration <= 0:
            duration = 1

        bytes_sent = current.bytes_sent - self.prev.bytes_sent
        bytes_recv = current.bytes_recv - self.prev.bytes_recv
        packets_sent = current.packets_sent - self.prev.packets_sent
        packets_recv = current.packets_recv - self.prev.packets_recv

        self.prev = current
        self.prev_time = now

        packets_per_sec = (packets_sent + packets_recv) / duration
        bytes_per_sec = (bytes_sent + bytes_recv) / duration

        process_activity_proxy = packets_sent * 2 if packets_sent > 0 else 0
        active_time_mean = duration * 1000 if (packets_sent + packets_recv) > 0 else 0

        return [
            packets_per_sec,        # packets_per_sec
            bytes_per_sec,          # bytes_per_sec
            duration,               # flow_duration
            packets_sent,           # fwd_packets
            bytes_sent,             # fwd_bytes
            bytes_recv,             # bwd_bytes
            process_activity_proxy, # process_activity_proxy
            packets_recv,           # bwd_subflow_packets
            active_time_mean         # active_time_mean
        ]
