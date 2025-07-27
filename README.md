# Operation Phantom Nexus - Chameleonte

## Quick Start Guide

This project demonstrates a covert channel using HTTP traffic and a transparent proxy.

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/phantom-nexus-chameleonte.git
cd phantom-nexus-chameleonte
```

### 2. Build and Start the Network

```bash
cd network_emulation
docker compose up --build
```

This sets up the client and proxy containers on a virtual network.

### 3. Access the Client VM

Open a shell in the running client container:

```bash
docker exec -it client /bin/bash
```

### 4. Run the Covert Channel Script

Navigate to the client script directory:

```bash
cd /opt/client
python3 client.py
```

Enter your covert message when prompted. The proxy will intercept your Google search, inject a hidden response, and the client will extract it.

### 5. Stopping and Cleaning Up

To stop and clean up the environment:

```bash
docker compose down
./cleanup.sh
```

---




**Note:** PCAP files and extraction scripts are provided for demonstration and analysis.