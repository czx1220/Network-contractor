from scapy.all import IP, TCP, UDP, send

def send_tcp_packet(source_ip, destination_ip, source_port, destination_port, payload):
    packet = IP(src=source_ip, dst=destination_ip) / TCP(sport=source_port, dport=destination_port) / payload
    send(packet)

def send_udp_packet(source_ip, destination_ip, source_port, destination_port, payload):
    packet = IP(src=source_ip, dst=destination_ip) / UDP(sport=source_port, dport=destination_port) / payload
    send(packet)

# 示例用法
source_ip = "192.168.0.100"
destination_ip = "192.168.0.200"
source_port = 1234
destination_port = 5678
payload = "Hello, server!"

send_tcp_packet(source_ip, destination_ip, source_port, destination_port, payload)
send_udp_packet(source_ip, destination_ip, source_port, destination_port, payload)