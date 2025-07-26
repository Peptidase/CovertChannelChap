FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y iproute2 iptables python3 tcpdump && \
    rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
COPY router.py /router.py
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
