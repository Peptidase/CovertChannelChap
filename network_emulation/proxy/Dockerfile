FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip iproute2 iptables tcpdump && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt ./requirements.txt

RUN pip3 install -r ./requirements.txt

# Create directories for captures and source
RUN mkdir -p /opt/proxy /captures

# Copy entrypoint into the image
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set working directory
WORKDIR /opt/proxy

CMD ["/entrypoint.sh"]
