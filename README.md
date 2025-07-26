# Operation Phantom Nexus - Chameleonte

The following repository contains the solution to the challenge problem.

## Covert Channel Overview

This project implements a proof-of-concept covert channel using HTTP traffic. The channel leverages a transparent proxy positioned inline with network traffic to intercept Google search requests and responses. When the proxy detects a search request matching predefined trigger conditions, it modifies the server’s HTTP response in-flight and embeds an encoded message inside the `<DOCTYPE>` tag of the returned HTML page. The modified page is then delivered to the client without disrupting normal browsing behavior.

## Methods Used

1. **Transparent HTTP Proxy**  
   A custom proxy operates inline with outbound and inbound HTTP traffic. It inspects each request and response without requiring client-side configuration.

2. **Trigger Detection**  
   The proxy monitors all HTTP requests to the Google domain. When a search request matches specific keywords or patterns, it flags the session for covert message injection.

3. **Payload Injection**  
   The proxy intercepts the corresponding HTTP response and parses the HTML. It encodes a covert message and embeds it within the `<DOCTYPE>` declaration. This approach avoids altering visible page content and minimizes detection risk.

4. **Message Extraction**  
   A separate decoding script reads the modified HTML, parses the `<DOCTYPE>` tag, and extracts the covert message. This can be run on the client side or by an operator collecting returned pages.

5. **Traffic Camouflage**  
   The covert channel hides within normal web browsing patterns, using HTTP’s ubiquity to blend with legitimate network traffic and avoid triggering simple anomaly-based detection.

## Requirements

- Python 3.10+
- Docker For testing

## Deliverables

- Proof-of-concept code for the HTTP covert channel
- README describing setup and operation
- PCAP demonstrating message injection and extraction
