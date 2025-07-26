#!/bin/bash
set -e

TS=$(date +%Y%m%d_%H%M%S)

# Flush old rules and enable forwarding
iptables -F
iptables -t nat -F

# Allow forwarding
iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# Start tcpdump on both interfaces
tcpdump -U -i eth0 -w /captures/proxy_internal_${TS}.pcap &
tcpdump -U -i eth1 -w /captures/proxy_external_${TS}.pcap &

echo "[+] Proxy capturing on eth0 (internal) and eth1 (external)"
python3 /router.py