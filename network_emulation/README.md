# Network Emulation Project - Quick Start Guide

This guide provides step-by-step instructions to build, start, and test the network emulation environment using Docker Compose.

## Steps

1. **Cleanup, then Build and Start Services**

    This command will delete all docker containers, if you have any issues with docker and this system not working try running this prior to running the compose command.

    ```
    ./cleanup.sh
    ```
    
    
    Build and start all services in detached mode:

    ```sh
    docker compose up -d --build
    ```

2. **Access Client Container**

    Open an interactive shell inside the `project-client-1` container:

    ```sh
    docker exec -it project-client-1 bash
    ```

3. **Network Connectivity Test**

    Verify connectivity to an external IP (e.g., 8.8.8.8):

    ```sh
    ping -c 2 8.8.8.8
    ```

4. **HTTP Connectivity Test**

    Test HTTP access to an external website (e.g., google.com):

    ```sh
    curl http://google.com
    ```

These commands help ensure the network emulation environment is running correctly and the client container has internet access.