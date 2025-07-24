# Operation Phantom Nexus - Chameleonte

The following repo contains the solution to the challenge problem  


## Network Emulation Guide

In order to begin the network emulation you must have docker installed. The `network_emulation` contains a docker compose file which you must use `docker compose up` to start and `docker compose down` to stop. This will turn on several docker images which connect a DMZ network LAN to a router to another network share which acts as the internal enterprise network. 
The docker compose file is essentially multiple dockerfiles container together. Following the `services:` section, we have the names of the different systems which we can see as the indented names `router`, `dmz_srv`, `internal_srv`. We can observe that under these services we have an `image:` flag. This is similar to what you could imagine an `iso` or `vbox` file for virtual box is but contains a state of the machine as well. It also isnt virtualised to the hardware and only on the operating system level. [`alpine`](https://hub.docker.com/_/alpine) is a super lightweight "iso" which just contains the bare minimum for a linux system to run (its 5MB lmao) which lets you install specifically what you want and then expand functionality on that. We can see in the different containers we all have `alpine` as the specific base image. We specify a name for the container. `priviledged` gives the machine access to sudo on the host machine which is required on the `router` container to be able to connect to the internet. We can also run commands when they start which we see with `router` when we specify `iptables` command to add the routing option to filter DMZ network traffic from other portions of the network. Lastly, **the `network:` tag within a container specifies how this container connects to that network. This means the address the container has in that network!** We can see the router container gives itself the `xxx.xxx.xxx.1` ip on both networks. 
We can see something similar on the `dmz_srv` container which runs similar commands. We can also see we dont define an ip for this container on the `internal_net` meaning the only way to access this machine is on the `dmz_net`. This is how we define our network layout with these verbose definitions in the `networks:` section on each container.
Finally, at the end of the file we see the network configurations occur. This is adding a custom docker network. The `driver:` detail just states how the network will communicate as a virtualised connection. We could make this more realistic by not having them be a bridge. Bridges are layer 3 virtualised connections so it can lose some flexability that a different driver type may have but that comes with increased overheads. 


## Covert Channel Ideas

The following protocols have been observed within the network.
1.  
