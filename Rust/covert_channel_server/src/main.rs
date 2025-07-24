use pnet::datalink::{self, Channel::Ethernet, Config, NetworkInterface};
use pnet::packet::ethernet::{EthernetPacket, EtherTypes};
use pnet::packet::Packet;
use std::str;

fn main() {
    let interface_name_one = "lo"; // Internal facing Interface
    let interface_name_two = "wlp0s20f3"; // External facing Interface

    let mut interface_one: Option<NetworkInterface> = None;
    let mut interface_two: Option<NetworkInterface> = None;

    let interfaces = datalink::interfaces();
    for iface in &interfaces {
        println!("Name: {}", iface.name);

        if iface.name == interface_name_one {
            interface_one = Some(iface.clone());
        }
        if iface.name == interface_name_two {
            interface_two = Some(iface.clone());
        }
    }

    let interface_one = interface_one.expect("Interface one not found");
    let interface_two = interface_two.expect("Interface two not found");

    let mut config = Config::default();
    config.read_timeout = None;

    // Create receiver on interface_one
    let (_, mut rx) = match datalink::channel(&interface_one, config.clone()) {
        Ok(Ethernet(_tx, rx)) => (_tx, rx),
        Ok(_) => panic!("Unhandled channel type"),
        Err(e) => panic!("Failed to create datalink channel: {}", e),
    };

    // Create transmitter on interface_two
    let (mut tx, _) = match datalink::channel(&interface_two, config) {
        Ok(Ethernet(tx, _rx)) => (tx, _rx),
        Ok(_) => panic!("Unhandled channel type"),
        Err(e) => panic!("Failed to create datalink channel: {}", e),
    };

    println!("Forwarding packets from {} to {}", interface_one.name, interface_two.name);

    loop {
        match rx.next() {
            Ok(packet) => {
                if filter_packet(packet) {
                    println!("Forwarding IPv4 packet!");
                    // Forward the packet to interface_two
                    tx.send_to(packet, None).unwrap();
                }
            }
            Err(e) => {
                eprintln!("An error occurred while reading: {}", e);
            }
        }
    }
}

fn filter_packet(packet: &[u8]) -> bool {
    if let Some(eth_pkt) = EthernetPacket::new(packet) {
        if eth_pkt.get_ethertype() == EtherTypes::Ipv4 {
            return true;
        }
    }
    false
}