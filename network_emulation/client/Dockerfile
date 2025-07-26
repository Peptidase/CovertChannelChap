FROM consol/ubuntu-xfce-vnc

USER root

# Install network tools, tcpdump, curl, and Python 3
RUN apt-get update && \
    apt-get install -y iproute2 tcpdump curl python3 python3-pip net-tools iputils-ping dnsutils && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir -r ./requirements.txt

# Expose VNC/noVNC ports
EXPOSE 5901 6080

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]