# Docker Test Range Guide

## Quick Start

0. Ensure the correct file is selected in the entrypoint file for the proxt server.

    Check `network_emulation/proxy/entrypoint.sh` for the last line.

    The last line runs the proxy file.

    ```
    python3 /opt/proxy/proxy_NSQUEUE_chunked.py
    
    ```
    This can be changed to a file located within the `python/covert_proxy/*.py` to start the other proxy server version. The difference is detailed within the `README.md` within the python directory.

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