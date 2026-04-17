from collections import Counter
import os
import time

log_file = "traffic.log"

BASE_THRESHOLD = 5
COOLDOWN = 10   # seconds

blocked_ips = {}

print("Analyzing traffic...\n")

try:
    with open(log_file, "r") as f:
        ips = f.read().splitlines()
except:
    print("No traffic data found.")
    exit()

counts = Counter(ips)

# dynamic threshold (based on avg traffic)
avg = sum(counts.values()) / len(counts) if counts else 0
threshold = max(BASE_THRESHOLD, int(avg * 1.5))

print(f"Dynamic threshold set to: {threshold}\n")

for ip, count in counts.items():
    print(f"IP: {ip} → Packets: {count}")

    if count > threshold and ip not in blocked_ips:
        print(f"Anomaly detected for {ip}")

        # BLOCK
        cmd = f'echo "table_add ipv4_lpm _drop {ip}/32 =>" | ~/Desktop/ACN/Project2/bmv2/tools/bm_CLI'
        os.system(cmd)

        blocked_ips[ip] = time.time()

        print(f"Blocking {ip}\n")

    elif ip in blocked_ips:
        print(f"Already blocked: {ip}\n")

    else:
        print(f"✓ Normal traffic\n")

# AUTO UNBLOCK LOGIC
print("Checking for cooldown expiration...\n")

current_time = time.time()

for ip in list(blocked_ips.keys()):
    if current_time - blocked_ips[ip] > COOLDOWN:
        print(f"🔓 Unblocking {ip}")

        # NOTE: BMv2 doesn't support delete easily → simulate by overwriting rule
        cmd = f'echo "table_add ipv4_lpm set_nhop {ip}/32 => {ip} 1" | ~/Desktop/ACN/Project2/bmv2/tools/bm_CLI'
        os.system(cmd)

        del blocked_ips[ip]