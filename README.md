🚀 INT-Based Security Monitoring in Software Defined Networks

This project demonstrates a programmable network security system using P4, BMv2, and SDN principles, extended with telemetry-driven anomaly detection and automated mitigation.

📌 Overview

Modern networks require real-time visibility and dynamic control. Traditional monitoring systems rely on external collectors and delayed analysis.

This project implements a closed-loop system where:

Network traffic is generated and monitored
Telemetry data is analyzed in real time
Anomalies are detected dynamically
The network automatically enforces mitigation policies
🧠 Key Features
⚙️ Programmable Data Plane (P4)
🔁 SDN-based Dynamic Control
📊 Real-Time Monitoring Dashboard
📡 Telemetry-based Analysis (Latency + Queue Depth)
🚨 Anomaly Detection (Adaptive Threshold)
🔒 Automated Mitigation (Block/Unblock)
📈 Evaluation Metrics (Accuracy, FPR, Detection Latency)
🏗️ System Architecture
Traffic Generator → P4 Switch → Telemetry Log → Dashboard (Analysis) → SDN Control → Mitigation
📂 Project Structure
.
├── simple_router.p4     # P4 data plane program
├── run.sh               # Script to start BMv2 switch
├── send.py              # Traffic generator (Scapy)
├── dashboard.py         # Live monitoring + detection + control + evaluation
├── traffic.log          # Telemetry log (generated at runtime)
├── bmv2/                # BMv2 switch source
⚙️ Requirements
macOS / Linux
Python 3
Scapy
BMv2 (Behavioral Model)
P4 compiler (p4c)
🔧 Installation
1. Install Python dependencies
python3 -m pip install scapy

.
