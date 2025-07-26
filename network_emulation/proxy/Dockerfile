FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip iproute2 iptables tcpdump net-tools iputils-ping dnsutils libnfnetlink-dev libnetfilter-queue-dev && \
    rm -rf /var/lib/apt/lists/*



COPY requirements.txt ./requirements.txt

RUN pip3 install --no-cache-dir -r ./requirements.txt

# Create directories for captures and source
RUN mkdir -p /opt/proxy /captures

# Copy entrypoint into the image
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set working directory
WORKDIR /opt/proxy

CMD ["/entrypoint.sh"]
