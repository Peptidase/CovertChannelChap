#!/bin/bash
set -e

TS=$(date +%Y%m%d_%H%M%S)

# Configure route via proxy
ip route del default || true
ip route add default via 10.200.0.3

# Start tcpdump capture
tcpdump -U -i eth0 -w /captures/client_traffic_${TS}.pcap &

# Start XFCE + VNC stack (preconfigured in base image)
echo "[+] Starting XFCE desktop with noVNC"
exec /usr/bin/vnc_startup &
tail -f /dev/null
