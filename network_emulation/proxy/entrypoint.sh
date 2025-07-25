#!/bin/bash
set -e

# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# NAT traffic from internal_net (eth0) to internet (eth1)
iptables -t nat -A POSTROUTING -o eth1 -j MASQUERADE
iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# Start tcpdump capturing all packets
tcpdump -i any -w /captures/network_dump.pcap &
echo "Proxy ready. Tcpdump writing to /captures/network_dump.pcap"

tail -f /dev/null