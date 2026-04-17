import time
import os
from collections import defaultdict

log_file = "traffic.log"

BASE_THRESHOLD = 5
LATENCY_THRESHOLD = 2.0   # ms
COOLDOWN = 10

blocked_ips = {}

def clear():
    os.system("clear")

while True:
    clear()
    print("=== INT-BASED SECURITY MONITORING DASHBOARD ===\n")

    data = defaultdict(list)
    first_seen = {}
    detected_time = {}

    try:
        with open(log_file, "r") as f:
            lines = f.read().splitlines()
    except:
        print("No traffic data yet...")
        time.sleep(2)
        continue

    current_time = time.time()

    # ---------------- DATA COLLECTION ----------------
    for line in lines:
        try:
            ip, latency = line.split(",")
            latency = float(latency)
        except:
            continue

        data[ip].append(latency)

        if ip not in first_seen:
            first_seen[ip] = current_time

    if not data:
        print("No traffic observed")
        time.sleep(2)
        continue

    # ---------------- THRESHOLD ----------------
    total_packets = sum(len(v) for v in data.values())
    avg = total_packets / len(data)
    threshold = max(BASE_THRESHOLD, int(avg * 1.5))

    print(f"Dynamic Packet Threshold: {threshold}")
    print(f"Latency Threshold: {LATENCY_THRESHOLD} ms\n")

    print("---- TRAFFIC ANALYSIS ----\n")

    correct = 0
    false_positive = 0
    total_detected = 0

    # ground truth
    normal_ip = "10.0.0.2"
    attack_ip = "10.0.0.99"

    for ip, latencies in data.items():
        count = len(latencies)
        avg_latency = sum(latencies) / count
        queue_depth = count

        status = "NORMAL"

        # detection condition
        if count > threshold or avg_latency > LATENCY_THRESHOLD:
            status = "ANOMALY"
            total_detected += 1

            if ip == attack_ip:
                correct += 1
            elif ip == normal_ip:
                false_positive += 1

            if ip not in blocked_ips:
                cmd = f'echo "table_add ipv4_lpm _drop {ip}/32 =>" | ~/Desktop/ACN/Project2/bmv2/tools/bm_CLI'
                os.system(cmd)
                blocked_ips[ip] = current_time
                detected_time[ip] = current_time

        print(f"{ip}")
        print(f"  packets: {count}")
        print(f"  queue_depth: {queue_depth}")
        print(f"  avg_latency: {avg_latency:.2f} ms")
        print(f"  status: {status}\n")

    # ---------------- BLOCK STATUS ----------------
    print("---- MITIGATION STATUS ----\n")

    for ip in list(blocked_ips.keys()):
        if current_time - blocked_ips[ip] > COOLDOWN:
            cmd = f'echo "table_add ipv4_lpm set_nhop {ip}/32 => {ip} 1" | ~/Desktop/ACN/Project2/bmv2/tools/bm_CLI'
            os.system(cmd)
            del blocked_ips[ip]
            print(f"{ip} → UNBLOCKED")
        else:
            print(f"{ip} → BLOCKED")

    # ---------------- EVALUATION ----------------
    print("\n---- EVALUATION METRICS ----\n")

    accuracy = (correct / total_detected) * 100 if total_detected > 0 else 0
    fpr = (false_positive / total_detected) * 100 if total_detected > 0 else 0

    print(f"Detection Accuracy: {accuracy:.2f}%")
    print(f"False Positive Rate: {fpr:.2f}%")

    print("\nDetection Latency:")

    for ip in detected_time:
        latency = detected_time[ip] - first_seen.get(ip, detected_time[ip])
        print(f"{ip} → {latency:.2f} sec")

    print("\nRefreshing in 2 seconds...")
    time.sleep(2)