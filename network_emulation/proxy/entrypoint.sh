#!/bin/bash
set -e

echo "[+] Enabling IP forwarding"
echo 1 > /proc/sys/net/ipv4/ip_forward

# Setup NAT for outbound traffic
iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE

# Redirect port 80 traffic to Python proxy running on 8080
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8080

# Start packet captures on both interfaces
TS=$(date +%Y%m%d_%H%M%S)
tcpdump -U -i eth0 -w /captures/proxy_internal_${TS}.pcap &
tcpdump -U -i eth1 -w /captures/proxy_external_${TS}.pcap &

echo "[+] Starting combined transparent proxy and HTTP interceptor"
python3 /opt/proxy/proxy.py
