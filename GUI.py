import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit
import socket
import struct
import random

class PacketSenderWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("网络发包器")
        self.setGeometry(1200, 200, 600, 500)
        
        self.source_ip_label = QLabel("源IP地址:", self)
        self.source_ip_label.move(50, 50)
        self.source_ip_entry = QLineEdit("10.181.23.245",self)
        self.source_ip_entry.move(150, 50)
        self.source_ip_entry.setFixedWidth(200)
        
        self.destination_ip_label = QLabel("目标IP地址:", self)
        self.destination_ip_label.move(50, 90)
        self.destination_ip_entry = QLineEdit(self)
        self.destination_ip_entry.move(150, 90)
        self.destination_ip_entry.setFixedWidth(200)
        
        self.source_port_label = QLabel("源端口号:", self)
        self.source_port_label.move(50, 130)
        self.source_port_entry = QLineEdit(str(find_available_port()),self)
        self.source_port_entry.move(150, 130)
        self.source_port_entry.setFixedWidth(200)
        
        self.destination_port_label = QLabel("目标端口号:", self)
        self.destination_port_label.move(50, 170)
        self.destination_port_entry = QLineEdit(self)
        self.destination_port_entry.move(150, 170)
        self.destination_port_entry.setFixedWidth(200)
        
        self.payload_label = QLabel("报文数据:", self)
        self.payload_label.move(50, 210)
        self.payload_entry = QTextEdit(self)
        self.payload_entry.move(150, 210)
        self.payload_entry.setFixedSize(300, 200)
        
        self.send_button = QPushButton("发送", self)
        self.send_button.move(150, 420)
        self.send_button.clicked.connect(self.send_packet)
        
    def send_packet(self):
        source_ip = self.source_ip_entry.text()
        destination_ip = self.destination_ip_entry.text()
        source_port = int(self.source_port_entry.text())
        destination_port = int(self.destination_port_entry.text())
        payload = self.payload_entry.toPlainText()
        

        # 在这里添加发送报文的逻辑
        send_udp_packet(source_ip, destination_ip, source_port, destination_port, payload)
        send_tcp_packet(source_ip, destination_ip, source_port, destination_port, payload)

        # # 发送IP报文
        # send_ip_packet(source_ip, destination_ip, payload)

        # # 发送ARP报文
        # send_arp_packet(source_ip, destination_ip)

        # # 发送ICMP报文
        # send_icmp_packet(source_ip, destination_ip)

        print("发送报文")
        print("源IP地址:", source_ip)
        print("目标IP地址:", destination_ip)
        print("源端口号:", source_port)
        print("目标端口号:", destination_port)
        print("有效载荷:", payload)

def find_available_port():
    # 创建一个临时套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))  # 绑定到任意IP地址和空闲端口号
    _, port = sock.getsockname()  # 获取分配的端口号
    sock.close()  # 关闭临时套接字
    return port

def send_tcp_packet(source_ip, destination_ip, source_port, destination_port, payload):
    # 创建TCP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 绑定源IP和端口号
    sock.bind((source_ip, source_port))
    
    # 连接到目标IP和端口号
    sock.connect((destination_ip, destination_port))
    
    # 发送数据
    sock.sendall(payload.encode())
    
    # 接收响应
    response = sock.recv(1024)
    
    # 打印响应
    print("TCP Response:", response.decode())
    
    # 关闭套接字
    sock.close()

def send_udp_packet(source_ip, destination_ip, source_port, destination_port, payload):
    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # 绑定源IP和端口号
    sock.bind((source_ip, source_port))
    
    # 发送数据
    sock.sendto(payload.encode(), (destination_ip, destination_port))
    
    # 接收响应
    response, addr = sock.recvfrom(1024)
    
    # 打印响应
    print("UDP Response:", response.decode())
    
    # 关闭套接字
    sock.close()

def send_ip_packet(source_ip, destination_ip, payload):
    # 创建原始套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

    # 构建IP报文头
    ip_header = create_ip_header(source_ip, destination_ip, payload)

    # 发送IP报文
    sock.sendto(ip_header + payload.encode(), (destination_ip, 0))

    # 关闭套接字
    sock.close()

def create_ip_header(source_ip, destination_ip, payload):
    # 构建IP报文头
    version = 4  # IPv4
    ihl = 5  # IP报文头长度（单位：32位字）
    tos = 0  # 服务类型
    total_length = 0  # 总长度，待计算
    identification = 54321  # 标识
    flags = 0  # 标志位
    fragment_offset = 0  # 分片偏移
    ttl = 64  # 存活时间
    protocol = socket.IPPROTO_TCP  # 上层协议类型
    checksum = 0  # 校验和，待计算
    source_address = socket.inet_aton(source_ip)  # 源IP地址
    destination_address = socket.inet_aton(destination_ip)  # 目标IP地址

    # 计算IP报文头的总长度
    total_length = 20 + len(payload)

    # 构建IP报文头
    ip_header = struct.pack("!BBHHHBBH4s4s",
                            (version << 4) + ihl,
                            tos,
                            total_length,
                            identification,
                            (flags << 13) + fragment_offset,
                            ttl,
                            protocol,
                            checksum,
                            source_address,
                            destination_address)

    # 计算IP报文头的校验和
    checksum = calculate_checksum(ip_header)
    ip_header = struct.pack("!BBHHHBBH4s4s",
                            (version << 4) + ihl,
                            tos,
                            total_length,
                            identification,
                            (flags << 13) + fragment_offset,
                            ttl,
                            protocol,
                            socket.htons(checksum),
                            source_address,
                            destination_address)

    return ip_header

def calculate_checksum(data):
    # 计算校验和
    checksum = 0

    if len(data) % 2 == 1:
        data += b'\x00'

    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        checksum += word

    while checksum >> 16:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    checksum = ~checksum & 0xFFFF

    return checksum

def send_arp_packet(source_ip, source_mac, destination_ip, destination_mac):
    # 创建原始套接字
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0806))

    # 构建ARP报文
    arp_packet = create_arp_packet(source_ip, source_mac, destination_ip, destination_mac)

    # 发送ARP报文
    sock.send(arp_packet)

    # 关闭套接字
    sock.close()

def create_arp_packet(source_ip, source_mac, destination_ip, destination_mac):
    # 构建ARP报文
    hardware_type = 1  # 以太网类型
    protocol_type = 0x0800  # 上层协议类型（IPv4）
    hardware_size = 6  # MAC地址长度
    protocol_size = 4  # IP地址长度
    opcode = 1  # ARP请求
    source_mac = mac_to_bytes(source_mac)  # 源MAC地址
    source_ip = socket.inet_aton(source_ip)  # 源IP地址
    destination_mac = mac_to_bytes(destination_mac)  # 目标MAC地址
    destination_ip = socket.inet_aton(destination_ip)  # 目标IP地址

    arp_packet = struct.pack("!HHBBH6s4s6s4s",
                             hardware_type,
                             protocol_type,
                             hardware_size,
                             protocol_size,
                             opcode,
                             source_mac,
                             source_ip,
                             destination_mac,
                             destination_ip)

    return arp_packet

def mac_to_bytes(mac_address):
    # 将MAC地址转换为字节数组
    mac_bytes = []

    # 将MAC地址字符串分割为16进制数值
    mac_parts = mac_address.split(':')

    # 将每个16进制数值转换为字节，并添加到字节数组中
    for part in mac_parts:
        mac_bytes.append(int(part, 16))

    return bytes(mac_bytes)

def send_icmp_packet(source_ip, destination_ip, data):
    # 创建原始套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    # 构建ICMP报文
    icmp_packet = create_icmp_packet(data)

    # 发送ICMP报文
    sock.sendto(icmp_packet, (destination_ip, 0))

    # 关闭套接字
    sock.close()

def create_icmp_packet(data):
    # 构建ICMP报文
    icmp_type = 8  # ICMP Echo Request
    icmp_code = 0  # 0 for Echo Request and Echo Reply
    icmp_checksum = 0  # 校验和，待计算
    icmp_identifier = random.randint(0, 65535)  # 标识符
    icmp_sequence_number = 1  # 序列号

    # 构建ICMP头部
    icmp_header = struct.pack("!BBHHH",
                              icmp_type,
                              icmp_code,
                              icmp_checksum,
                              icmp_identifier,
                              icmp_sequence_number)

    # 计算ICMP头部的校验和
    icmp_checksum = calculate_checksum(icmp_header + data.encode())
    icmp_header = struct.pack("!BBHHH",
                              icmp_type,
                              icmp_code,
                              socket.htons(icmp_checksum),
                              icmp_identifier,
                              icmp_sequence_number)

    # 构建ICMP报文
    icmp_packet = icmp_header + data.encode()

    return icmp_packet

if __name__=="__main__":
    # 创建应用程序对象
    app = QApplication(sys.argv)

    # 创建主窗口对象
    window = PacketSenderWindow()

    # 显示主窗口
    window.show()

    # 运行应用程序的消息循环
    sys.exit(app.exec_())