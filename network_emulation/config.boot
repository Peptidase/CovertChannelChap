# VyOS configuration file for automatic boot
# Replace this with your actual VyOS config

interfaces {
    ethernet eth0 {
        address 192.168.3.1/24
        description "LAN Interface"
    }
    ethernet eth1 {
        address 172.16.50.1/24
        description "DMZ Interface"
    }
    ethernet eth2 {
        address 10.0.80.1/24
        description "WAN Interface"
    }
}
service {
    dhcp-server {
        shared-network-name LAN {
            subnet 192.168.3.0/24 {
                default-router 192.168.3.1
                name-server 192.168.3.1
                domain-name icorp.internal
            }
        }
    }
    dns {
        forwarding {
            allow-from 192.168.3.0/24
            cache-size 0
            listen-on eth0
            options all-servers
        }
    }
    ntp {
        server pool.ntp.org
    }
}
firewall {
    name LAN {
        default-action drop
        rule 10 {
            action accept
            description "Allow DHCP"
            protocol udp
            destination {
                port 67
            }
        }
        rule 20 {
            action accept
            description "Allow DNS"
            protocol udp
            destination {
                port 53
            }
        }
        rule 30 {
            action accept
            description "Allow NTP"
            protocol udp
            destination {
                port 123
            }
        }
        rule 40 {
            action accept
            description "Allow SSH"
            protocol tcp
            destination {
                port 22
            }
        }
        rule 50 {
            action accept
            description "Allow HTTPS"
            protocol tcp
            destination {
                port 443
            }
        }
        rule 60 {
            action accept
            description "Allow HTTP to proxy"
            protocol tcp
            destination {
                address 192.168.3.201
                port 80
            }
        }
        rule 70 {
            action accept
            description "Allow ICMP"
            protocol icmp
        }
        rule 80 {
            action accept
            description "Allow established connections"
            state {
                established enable
                related enable
            }
        }
    }
    name DMZ {
        default-action drop
        rule 10 {
            action accept
            description "Allow HTTP from proxy"
            protocol tcp
            source {
                address 192.168.3.201
            }
            destination {
                port 80
            }
        }
        rule 20 {
            action accept
            description "Allow HTTPS"
            protocol tcp
            destination {
                port 443
            }
        }
    }
    name WAN {
        default-action drop
        rule 10 {
            action accept
            description "Allow web traffic during working hours"
            protocol tcp
            destination {
                port 80,443
            }
            time {
                starttime 08:00:00
                stoptime 17:00:00
                weekdays Mon,Tue,Wed,Thu,Fri
            }
        }
    }
}
