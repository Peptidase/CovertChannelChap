# README

This directory contains all the python files and the logic for the protocol. IT IS VERY MESSY.

The chunked versions of this protocol are used for testing file transmission.
The non_chunked versions just send a simple string to and from the scripts. `client.py` sends a string to `proxy_NSQUEUE.py` which always sends a `pong!` message back.

## Docker Compose Volumes

Both `covert_proxy` and `covert_client` folders are mounted as volumes in the Docker Compose setup. This allows containers to access and manipulate these files directly, supporting various covert channel experiments and file handling operations.