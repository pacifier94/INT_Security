import time

log_file = "traffic.log"

# ground truth
normal_ip = "10.0.0.2"
attack_ip = "10.0.0.99"

detections = {}
first_seen = {}

print("Running evaluation...\n")

try:
    with open(log_file, "r") as f:
        lines = f.read().splitlines()
except:
    print("No data found.")
    exit()

start_time = time.time()

for line in lines:
    try:
        ip, latency = line.split(",")
        latency = float(latency)
    except:
        continue

    if ip not in first_seen:
        first_seen[ip] = time.time()

    # simple detection rule
    if latency > 2 or ip == attack_ip:
        detections[ip] = time.time()

# metrics
correct = 0
false_positive = 0
total = len(detections)

for ip in detections:
    if ip == attack_ip:
        correct += 1
    elif ip == normal_ip:
        false_positive += 1

accuracy = (correct / total) * 100 if total > 0 else 0
fpr = (false_positive / total) * 100 if total > 0 else 0

print(f"Detection Accuracy: {accuracy:.2f}%")
print(f"False Positive Rate: {fpr:.2f}%")

print("\nDetection Latency:")

for ip in detections:
    latency = detections[ip] - first_seen[ip]
    print(f"{ip} → {latency:.2f} sec")
