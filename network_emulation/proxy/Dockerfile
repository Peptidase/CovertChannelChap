FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y iproute2 iptables tcpdump && \
    rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["bash"]