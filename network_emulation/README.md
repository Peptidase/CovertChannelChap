# Docker Test Range Guide

## Quick Start

1. Build and start the environment:

    ```bash
    cd network_emulation
    docker compose up --build
    ```

2. Access the client container:

    ```bash
    docker exec -it network_emulation /bin/bash
    ```

3. Run the client script:

    ```bash
    cd /opt/client
    python3 client.py
    ```

4. To stop and clean up:

    ```bash
    docker compose down
    ./cleanup.sh
    ```

---

- All captures and files are saved in the `captures/` directory.
- The proxy intercepts and modifies HTTP traffic as described in the main README.