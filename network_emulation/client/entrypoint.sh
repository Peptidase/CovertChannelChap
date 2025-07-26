#!/bin/bash
set -e

# Configure route to go via proxy
ip route del default || true
ip route add default via 10.200.0.3

# Start tcpdump in background
TS=$(date +%Y%m%d_%H%M%S)
tcpdump -U -i eth0 -w /captures/client_${TS}.pcap &

#echo "[+] Starting client script..."
#python3 /opt/client/client.py

# Keep container alive after script
tail -f /dev/null
