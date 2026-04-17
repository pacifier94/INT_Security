# 🚀 INT-Based Security Monitoring in Software Defined Networks

This project demonstrates a **programmable network security system** using **P4**, **BMv2**, and **SDN principles**, extended with **telemetry-driven anomaly detection and automated mitigation**.

---

## 📌 Overview

Modern networks require **real-time visibility and dynamic control**. Traditional monitoring systems rely on external collectors and delayed analysis.

This project implements a **closed-loop system** where:

- Network traffic is generated and monitored
- Telemetry data is analyzed in real time
- Anomalies are detected dynamically
- The network automatically enforces mitigation policies

---

## 🧠 Key Features

- ⚙️ Programmable Data Plane (P4)
- 🔁 SDN-based Dynamic Control
- 📊 Real-Time Monitoring Dashboard
- 📡 Telemetry-based Analysis (Latency + Queue Depth)
- 🚨 Anomaly Detection (Adaptive Threshold)
- 🔒 Automated Mitigation (Block/Unblock)
- 📈 Evaluation Metrics (Accuracy, FPR, Detection Latency)

---

## 🏗️ System Architecture

Traffic Generator → P4 Switch → Telemetry Log → Dashboard (Analysis) → SDN Control → Mitigation

---

## 📂 Project Structure

.
├── simple_router.p4     # P4 data plane program  
├── run.sh               # Script to start BMv2 switch  
├── send.py              # Traffic generator (Scapy)  
├── dashboard.py         # Monitoring + detection + control + evaluation  
├── traffic.log          # Telemetry log (generated at runtime)  
├── bmv2/                # BMv2 switch source  

---

## ⚙️ Requirements

- macOS / Linux
- Python 3
- Scapy
- BMv2 (Behavioral Model)
- P4 compiler (p4c)

---

## 🔧 Installation

Install Scapy:
python3 -m pip install scapy

(Optional) Build BMv2:
cd bmv2  
make -j$(sysctl -n hw.ncpu)

---

## 🚀 Running the Project

### 1. Clean start
rm -f traffic.log  
pkill simple_switch 2>/dev/null  

---

### 2. Start the switch
sudo ./run.sh  

---

### 3. Open control plane (new terminal)
bmv2/tools/bm_CLI  

Add rule:
table_add ipv4_lpm set_nhop 10.0.0.2/32 => 10.0.0.2 1  

---

### 4. Start dashboard (new terminal)
python3 dashboard.py  

---

### 5. Generate traffic (new terminal)
sudo python3 send.py  

---

## 📊 Output

The dashboard displays:

- Packet count per IP
- Queue depth (traffic intensity)
- Average latency
- Anomaly detection status
- Blocked / Unblocked IPs
- Evaluation metrics:
  - Detection Accuracy
  - False Positive Rate
  - Detection Latency

---

## 🧠 Detection Logic

- Queue Depth → approximated using packet count  
- Latency → measured per packet  
- Dynamic Threshold → adapts based on traffic  

An IP is marked anomalous if:
- Traffic exceeds threshold, OR  
- Latency exceeds threshold  

---

## 🔒 Mitigation Strategy

Suspicious IPs are blocked dynamically using SDN:

table_add ipv4_lpm _drop IP/32 =>  

After cooldown, rules are updated to restore normal behavior.

---

## 📈 Evaluation Metrics

- Detection Accuracy  
- False Positive Rate  
- Detection Latency  

---

## ⚠️ Limitations

- Full INT (queue depth, latency from switch) is simulated  
- Mininet topology not included (macOS limitation)  
- Not deployed on hardware switches  

---

## 🔮 Future Work

- Full INT implementation  
- Mininet-based multi-switch topology  
- ML-based anomaly detection  
- Performance benchmarking  

---

## 📚 References

- P4: Programming Protocol-Independent Packet Processors (SIGCOMM 2014)  
- In-band Network Telemetry (Barefoot Networks)  
- NetSight, FlowRadar, Sonata  

---

## 👨‍💻 Authors

- Astitwa Saxena  
- Abhishek Gupta  

---

## 🏁 Final Note

This project demonstrates how programmable networks can monitor, analyze, and react to threats in real time, forming the foundation for intelligent network security systems.
