#!/bin/bash
set -e

ip route del default || true
ip route add default via 172.30.0.1

echo "Client ready. Default gateway set to 172.30.0.1"
tail -f /dev/null
