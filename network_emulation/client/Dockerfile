FROM consol/ubuntu-xfce-vnc

# Install network tools and tcpdump
USER root
RUN apt-get update && \
    apt-get install -y iproute2 tcpdump curl && \
    rm -rf /var/lib/apt/lists/*

# Expose ports (VNC + noVNC)
EXPOSE 5901 6080

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
