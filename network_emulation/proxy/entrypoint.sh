#!/bin/bash
set -e

echo "[+] Enabling IP forwarding"
echo 1 > /proc/sys/net/ipv4/ip_forward

# Show current DNS configuration for debugging
echo "[+] Current DNS configuration:"
cat /etc/resolv.conf

# Flush old rules to avoid duplicates
iptables -F
iptables -t nat -F

# Masquerade outbound traffic for internet access
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Accept forwarding between interfaces
iptables -A FORWARD -i eth0 -j ACCEPT
iptables -A FORWARD -o eth0 -j ACCEPT

# Redirect all port 80 traffic to local Python proxy
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 80

echo "[+] Starting covert channel transparent proxy"
python3 /opt/proxy/proxy.py