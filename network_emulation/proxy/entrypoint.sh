#!/bin/bash
set -e

echo "[+] Enabling IP forwarding"
echo 1 > /proc/sys/net/ipv4/ip_forward

echo "[+] Current DNS config:"
cat /etc/resolv.conf

# Flush rules
iptables -F
iptables -t nat -F

# Masquerade for internet access
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Send HTTP packets to NFQUEUE instead of redirecting to a local socket
iptables -I FORWARD -p tcp --dport 80 -j NFQUEUE --queue-num 1
iptables -I FORWARD -p tcp --sport 80 -j NFQUEUE --queue-num 1


# Start tcpdump in background
TS=$(date +%Y%m%d_%H%M%S)
tcpdump -U -i eth0 -w /captures/proxy_${TS}.pcap &


echo "[+] Starting NFQUEUE-based transparent proxy"
python3 /opt/proxy/proxy_NSQUEUE_chunked.py