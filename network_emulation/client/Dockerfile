FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y iproute2 iputils-ping curl && \
    rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["bash"]