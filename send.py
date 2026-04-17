from scapy.all import *
import time

log_file = "traffic.log"

def log(ip, latency):
    with open(log_file, "a") as f:
        f.write(f"{ip},{latency}\n")

print("Sending NORMAL traffic...")

for _ in range(5):
    pkt = Ether()/IP(dst="10.0.0.2")/TCP()
    start = time.time()
    sendp(pkt, iface="lo0", verbose=False)
    end = time.time()

    latency = (end - start) * 1000  # ms
    log("10.0.0.2", latency)

print("Sending SUSPICIOUS traffic...")

for _ in range(12):
    pkt = Ether()/IP(dst="10.0.0.99")/TCP()
    start = time.time()
    sendp(pkt, iface="lo0", verbose=False)
    end = time.time()

    latency = (end - start) * 1000
    log("10.0.0.99", latency)

print("Traffic sent and logged.")