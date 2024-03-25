import sys
import socket
import struct
import random
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, \
    QPushButton, QTextEdit, QStackedWidget, QWidget, QVBoxLayout,QHBoxLayout


class PacketSenderWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("网络发包器")
        self.setGeometry(1200, 200, 600, 500)

        # 创建按钮页面
        self.button_widget = QWidget()
        self.button_layout = QVBoxLayout()
        self.button_widget.setLayout(self.button_layout)

        # 创建按钮
        self.tcp_button = QPushButton("发送TCP报文")
        self.udp_button = QPushButton("发送UDP报文")
        self.icmp_button = QPushButton("发送ICMP报文")
        self.ip_button = QPushButton("发送IP报文")
        self.arp_button = QPushButton("发送ARP报文")

        # 将按钮添加到布局中
        self.button_layout.addWidget(self.tcp_button)
        self.button_layout.addWidget(self.udp_button)
        self.button_layout.addWidget(self.icmp_button)
        self.button_layout.addWidget(self.ip_button)
        self.button_layout.addWidget(self.arp_button)

        # 创建页面堆栈
        self.page_stack = QStackedWidget()
        self.page_stack.addWidget(self.button_widget)  # 添加按钮页面

        # 设置堆栈为主窗口的中心部件
        self.setCentralWidget(self.page_stack)

        # 连接按钮的点击事件到相应的槽函数
        self.tcp_button.clicked.connect(self.show_tcp_page)
        self.udp_button.clicked.connect(self.show_udp_page)
        self.icmp_button.clicked.connect(self.show_icmp_page)
        self.ip_button.clicked.connect(self.show_ip_page)
        self.arp_button.clicked.connect(self.show_arp_page)

        self.back_button = QPushButton("返回")
        self.back_button.clicked.connect(self.show_button_page)

    def show_button_page(self):
        # 切换回按钮页面
        self.page_stack.setCurrentWidget(self.button_widget)

    def show_tcp_page(self):
        # TCP标识
        self.symbol = "tcp"

        # 创建TCP页面
        tcp_widget = QWidget()
        tcp_layout = QVBoxLayout()
        tcp_widget.setLayout(tcp_layout)

        # 创建TCP页面的具体内容，例如IP地址、端口号和报文数据的输入框等
        self.source_ip_label = QLabel("源IP地址:", tcp_widget)
        self.source_ip_entry = QLineEdit("10.181.23.245", tcp_widget)
        source_ip_layout = QHBoxLayout()
        source_ip_layout.addWidget(self.source_ip_label)
        source_ip_layout.addWidget(self.source_ip_entry)
        tcp_layout.addLayout(source_ip_layout)

        self.destination_ip_label = QLabel("目标IP地址:", tcp_widget)
        self.destination_ip_entry = QLineEdit("192.168.1.104",tcp_widget)
        destination_ip_layout = QHBoxLayout()
        destination_ip_layout.addWidget(self.destination_ip_label)
        destination_ip_layout.addWidget(self.destination_ip_entry)
        tcp_layout.addLayout(destination_ip_layout)

        self.source_port_label = QLabel("源端口号:", tcp_widget)
        self.source_port_entry = QLineEdit(str(find_available_port()), tcp_widget)
        source_port_layout = QHBoxLayout()
        source_port_layout.addWidget(self.source_port_label)
        source_port_layout.addWidget(self.source_port_entry)
        tcp_layout.addLayout(source_port_layout)

        self.destination_port_label = QLabel("目标端口号:", tcp_widget)
        self.destination_port_entry = QLineEdit("8080",tcp_widget)
        destination_port_layout = QHBoxLayout()
        destination_port_layout.addWidget(self.destination_port_label)
        destination_port_layout.addWidget(self.destination_port_entry)
        tcp_layout.addLayout(destination_port_layout)

        self.payload_label = QLabel("报文数据:", tcp_widget)
        self.payload_entry = QTextEdit(tcp_widget)
        payload_layout = QHBoxLayout()
        payload_layout.addWidget(self.payload_label)
        payload_layout.addWidget(self.payload_entry)
        tcp_layout.addLayout(payload_layout)

        self.send_button = QPushButton("发送", tcp_widget)
        self.send_button.clicked.connect(self.send_packet)
        tcp_layout.addWidget(self.send_button)
        
        # 将返回按钮添加到TCP页面
        tcp_layout.addWidget(self.back_button)

        # 将TCP页面添加到堆栈中
        self.page_stack.addWidget(tcp_widget)

        # 切换到TCP页面
        self.page_stack.setCurrentWidget(tcp_widget)

    def show_udp_page(self):
        # UDP标识
        self.symbol = "udp"

        # 创建UDP页面
        udp_widget = QWidget()
        udp_layout = QVBoxLayout()
        udp_widget.setLayout(udp_layout)

        # 创建UDP页面的具体内容，例如IP地址、端口号和报文数据的输入框等
        self.source_ip_label = QLabel("源IP地址:", udp_widget)
        self.source_ip_entry = QLineEdit("10.181.23.245", udp_widget)
        source_ip_layout = QHBoxLayout()
        source_ip_layout.addWidget(self.source_ip_label)
        source_ip_layout.addWidget(self.source_ip_entry)
        udp_layout.addLayout(source_ip_layout)

        self.destination_ip_label = QLabel("目标IP地址:", udp_widget)
        self.destination_ip_entry = QLineEdit("192.168.1.104",udp_widget)
        destination_ip_layout = QHBoxLayout()
        destination_ip_layout.addWidget(self.destination_ip_label)
        destination_ip_layout.addWidget(self.destination_ip_entry)
        udp_layout.addLayout(destination_ip_layout)

        self.source_port_label = QLabel("源端口号:", udp_widget)
        self.source_port_entry = QLineEdit(str(find_available_port()), udp_widget)
        source_port_layout = QHBoxLayout()
        source_port_layout.addWidget(self.source_port_label)
        source_port_layout.addWidget(self.source_port_entry)
        udp_layout.addLayout(source_port_layout)

        self.destination_port_label = QLabel("目标端口号:", udp_widget)
        self.destination_port_entry = QLineEdit("8080",udp_widget)
        destination_port_layout = QHBoxLayout()
        destination_port_layout.addWidget(self.destination_port_label)
        destination_port_layout.addWidget(self.destination_port_entry)
        udp_layout.addLayout(destination_port_layout)

        self.payload_label = QLabel("报文数据:", udp_widget)
        self.payload_entry = QTextEdit(udp_widget)
        payload_layout = QHBoxLayout()
        payload_layout.addWidget(self.payload_label)
        payload_layout.addWidget(self.payload_entry)
        udp_layout.addLayout(payload_layout)

        self.send_button = QPushButton("发送", udp_widget)
        self.send_button.clicked.connect(self.send_packet)
        udp_layout.addWidget(self.send_button)
        
        # 将返回按钮添加到UDP页面
        udp_layout.addWidget(self.back_button)
        # 将UDP页面添加到堆栈中
        self.page_stack.addWidget(udp_widget)

        # 切换到UDP页面
        self.page_stack.setCurrentWidget(udp_widget)

    def show_icmp_page(self):
        # ICMP标识
        self.symbol = "icmp"

        # 创建ICMP页面
        icmp_widget = QWidget()
        icmp_layout = QVBoxLayout()
        icmp_widget.setLayout(icmp_layout)

        # 创建ICMP页面的具体内容，例如IP地址、端口号和报文数据的输入框等
        self.source_ip_label = QLabel("源IP地址:", icmp_widget)
        self.source_ip_entry = QLineEdit("10.181.23.245", icmp_widget)
        source_ip_layout = QHBoxLayout()
        source_ip_layout.addWidget(self.source_ip_label)
        source_ip_layout.addWidget(self.source_ip_entry)
        icmp_layout.addLayout(source_ip_layout)

        self.destination_ip_label = QLabel("目标IP地址:", icmp_widget)
        self.destination_ip_entry = QLineEdit("192.168.1.104",icmp_widget)
        destination_ip_layout = QHBoxLayout()
        destination_ip_layout.addWidget(self.destination_ip_label)
        destination_ip_layout.addWidget(self.destination_ip_entry)
        icmp_layout.addLayout(destination_ip_layout)

        self.payload_label = QLabel("报文数据:", icmp_widget)
        self.payload_entry = QTextEdit(icmp_widget)
        payload_layout = QHBoxLayout()
        payload_layout.addWidget(self.payload_label)
        payload_layout.addWidget(self.payload_entry)
        icmp_layout.addLayout(payload_layout)

        self.send_button = QPushButton("发送", icmp_widget)
        self.send_button.clicked.connect(self.send_packet)
        icmp_layout.addWidget(self.send_button)
        
        # 将返回按钮添加到ICMP页面
        icmp_layout.addWidget(self.back_button)

        # 将ICMP页面添加到堆栈中
        self.page_stack.addWidget(icmp_widget)

        # 切换到ICMP页面
        self.page_stack.setCurrentWidget(icmp_widget)

    def show_ip_page(self):
        # IP标识
        self.symbol = "ip"

        # 创建IP页面
        ip_widget = QWidget()
        ip_layout = QVBoxLayout()
        ip_widget.setLayout(ip_layout)

        # 创建IP页面的具体内容，例如IP地址、端口号和报文数据的输入框等
        self.source_ip_label = QLabel("源IP地址:", ip_widget)
        self.source_ip_entry = QLineEdit("10.181.23.245", ip_widget)
        source_ip_layout = QHBoxLayout()
        source_ip_layout.addWidget(self.source_ip_label)
        source_ip_layout.addWidget(self.source_ip_entry)
        ip_layout.addLayout(source_ip_layout)

        self.destination_ip_label = QLabel("目标IP地址:", ip_widget)
        self.destination_ip_entry = QLineEdit("192.168.1.104",ip_widget)
        destination_ip_layout = QHBoxLayout()
        destination_ip_layout.addWidget(self.destination_ip_label)
        destination_ip_layout.addWidget(self.destination_ip_entry)
        ip_layout.addLayout(destination_ip_layout)

        self.payload_label = QLabel("报文数据:",ip_widget)
        self.payload_entry = QTextEdit(ip_widget)
        payload_layout = QHBoxLayout()
        payload_layout.addWidget(self.payload_label)
        payload_layout.addWidget(self.payload_entry)
        ip_layout.addLayout(payload_layout)

        self.send_button = QPushButton("发送", ip_widget)
        self.send_button.clicked.connect(self.send_packet)
        ip_layout.addWidget(self.send_button)
        
        # 将返回按钮添加到IP页面
        ip_layout.addWidget(self.back_button)

        # 将IP页面添加到堆栈中
        self.page_stack.addWidget(ip_widget)

        # 切换到IP页面
        self.page_stack.setCurrentWidget(ip_widget)

    def show_arp_page(self):
        # ARP标识
        self.symbol = "arp"

        # 创建ARP页面
        arp_widget = QWidget()
        arp_layout = QVBoxLayout()
        arp_widget.setLayout(arp_layout)

        # 创建ARP页面的具体内容，例如IP地址、端口号和报文数据的输入框等
        self.source_ip_label = QLabel("源IP地址:", arp_widget)
        self.source_ip_entry = QLineEdit("10.181.23.245", arp_widget)
        source_ip_layout = QHBoxLayout()
        source_ip_layout.addWidget(self.source_ip_label)
        source_ip_layout.addWidget(self.source_ip_entry)
        arp_layout.addLayout(source_ip_layout)

        self.destination_ip_label = QLabel("目标IP地址:", arp_widget)
        self.destination_ip_entry = QLineEdit("192.168.1.104",arp_widget)
        destination_ip_layout = QHBoxLayout()
        destination_ip_layout.addWidget(self.destination_ip_label)
        destination_ip_layout.addWidget(self.destination_ip_entry)
        arp_layout.addLayout(destination_ip_layout)

        self.source_mac_label = QLabel("源物理地址:", arp_widget)
        self.source_mac_entry = QLineEdit("38-FC-98-F8-8D-74",arp_widget)
        source_mac_layout = QHBoxLayout()
        source_mac_layout.addWidget(self.source_mac_label)
        source_mac_layout.addWidget(self.source_mac_entry)
        arp_layout.addLayout(source_mac_layout)

        self.destination_mac_label = QLabel("目标物理地址:", arp_widget)
        self.destination_mac_entry = QLineEdit(arp_widget)
        destination_mac_layout = QHBoxLayout()
        destination_mac_layout.addWidget(self.destination_mac_label)
        destination_mac_layout.addWidget(self.destination_mac_entry)
        arp_layout.addLayout(destination_mac_layout)

        self.payload_label = QLabel("报文数据:", arp_widget)
        self.payload_entry = QTextEdit(arp_widget)
        payload_layout = QHBoxLayout()
        payload_layout.addWidget(self.payload_label)
        payload_layout.addWidget(self.payload_entry)
        arp_layout.addLayout(payload_layout)

        self.send_button = QPushButton("发送", arp_widget)
        self.send_button.clicked.connect(self.send_packet)
        arp_layout.addWidget(self.send_button)
        
        # 将返回按钮添加到ARP页面
        arp_layout.addWidget(self.back_button)

        # 将ARP页面添加到堆栈中
        self.page_stack.addWidget(arp_widget)

        # 切换到ARP页面
        self.page_stack.setCurrentWidget(arp_widget)

    def send_packet(self):

        try:
            # 在这里添加发送报文的逻辑

            # 发送TCP报文
            if self.symbol == "tcp":
                print("发送arp报文")
                source_ip = self.source_ip_entry.text()
                destination_ip = self.destination_ip_entry.text()
                source_port = int(self.source_port_entry.text())
                destination_port = int(self.destination_port_entry.text())
                payload = self.payload_entry.toPlainText()

                send_tcp_packet(source_ip, destination_ip, source_port, destination_port, payload)

            # 发送UDP报文
            if self.symbol == "udp":
                print("发送udp报文")
                source_ip = self.source_ip_entry.text()
                destination_ip = self.destination_ip_entry.text()
                source_port = int(self.source_port_entry.text())
                destination_port = int(self.destination_port_entry.text())
                payload = self.payload_entry.toPlainText()

                send_udp_packet(source_ip, destination_ip, source_port, destination_port, payload)

            # 发送ICMP报文
            if self.symbol == "icmp":
                print("发送icmp报文")
                source_ip = self.source_ip_entry.text()
                destination_ip = self.destination_ip_entry.text()
                payload = self.payload_entry.toPlainText()
                send_icmp_packet(source_ip, destination_ip, payload)

            # 发送IP报文
            if self.symbol == "ip":
                print("发送ip报文")
                source_ip = self.source_ip_entry.text()
                destination_ip = self.destination_ip_entry.text()
                payload = self.payload_entry.toPlainText()
                send_ip_packet(source_ip, destination_ip, payload)

            # 发送ARP报文
            if self.symbol == "arp":
                print("发送arp报文")
                source_ip = self.source_ip_entry.text()
                destination_ip = self.destination_ip_entry.text()
                source_mac = self.source_mac_entry.text()
                destination_mac = self.destination_mac_entry.text()
                send_arp_packet(source_ip, source_mac, destination_ip, destination_mac)

        except Exception as e:
            print("发生异常:", str(e))

        # 执行其他操作或返回原来界面的代码
        print("执行了return_to_previous_screen")
        self.return_to_previous_screen()
        print("执行了return_to_previous_screen")


        # print("发送报文")
        # print("源IP地址:", source_ip)
        # print("目标IP地址:", destination_ip)
        # print("源端口号:", source_port)
        # print("目标端口号:", destination_port)
        # print("有效载荷:", payload)

    def return_to_previous_screen(self):

        print("执行了return_to_previous_screen")
        # 在这里添加返回到之前界面的逻辑
        self.show_button_page()
        # 例如，可以清除输入字段或隐藏发送按钮

        # 清除输入字段
        # self.source_ip_entry.clear()
        # self.destination_ip_entry.clear()
        # self.source_port_entry.clear()
        # self.destination_port_entry.clear()
        self.payload_entry.clear()

        # 隐藏发送按钮
        self.send_button.hide()

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
    sock.settimeout(5)
    try:
        response = sock.recv(1024)
        print("ARP Response:", response.decode())
    except socket.timeout:
        print("No response received within the specified timeout period.")
        
    # 关闭套接字
    sock.close()

def find_available_port():
    # 创建一个临时套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", 0))  # 绑定到任意IP地址和空闲端口号
    _, port = sock.getsockname()  # 获取分配的端口号
    sock.close()  # 关闭临时套接字
    return port

def send_udp_packet(source_ip, destination_ip, source_port, destination_port, payload):
    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # 绑定源IP和端口号
    sock.bind((source_ip, source_port))
    
    # 发送数据
    sock.sendto(payload.encode(), (destination_ip, destination_port))
    
    # 接收响应
    sock.settimeout(5)
    try:
        response, addr = sock.recvfrom(1024)
        print("UDP Response:", response.decode())
    except socket.timeout:
        print("No response received within the specified timeout period.")
    
    # 关闭套接字
    sock.close()

def send_ip_packet(source_ip, destination_ip, payload):
    # 创建原始套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

    # 构建IP报文头
    ip_header = create_ip_header(source_ip, destination_ip, payload)

    # 发送IP报文
    sock.sendto(ip_header + payload.encode(), (destination_ip, 0))

    # 接收响应
    sock.settimeout(5)
    try:
        response, addr = sock.recvfrom(1024)
        print("IP Response:", response.decode())
    except socket.timeout:
        print("No response received within the specified timeout period.")
    
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
                            socket.htons(checksum),
                            source_address,
                            destination_address)

    # 计算IP报文头的校验和
    checksum = calculate_checksum(ip_header)

    # 构建IP报文头
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
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.htons(0x0806))

    # 构建ARP报文
    arp_packet = create_arp_packet(source_ip, source_mac, destination_ip, destination_mac)

    # 发送ARP报文
    sock.send(arp_packet)

    # 接收响应
    sock.settimeout(5)
    try:
        response, addr = sock.recvfrom(1024)
        print("ARP Response:", response.decode())
    except socket.timeout:
        print("No response received within the specified timeout period.")
    
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

    # 等待响应
    sock.settimeout(5)
    try:
        response, addr = sock.recvfrom(1024)
        print("ICMP Response:", response.decode())
    except socket.timeout:
        print("No response received within the specified timeout period.")

    # 关闭套接字
    sock.close()

def create_icmp_packet(data):
    # 构建ICMP报文
    icmp_type = 8  # ICMP Echo Request
    icmp_code = 0  # 0 for Echo Request and Echo Reply
    icmp_checksum = 0  # 校验和，待计算
    icmp_identifier = random.randint(0, 65535)  # 标识符
    icmp_sequence_number = 1  # 序列号

    # 构建ICMP报文头
    icmp_header = struct.pack("!BBHHH",
                              icmp_type,
                              icmp_code,
                              socket.htons(icmp_checksum),
                              icmp_identifier,
                              icmp_sequence_number)


    # 计算ICMP头部的校验和
    icmp_checksum = calculate_checksum(icmp_header + data.encode())

    # 构建ICMP报文头
    icmp_header = struct.pack("!BBHHH",
                              icmp_type,
                              icmp_code,
                              socket.htons(icmp_checksum),
                              icmp_identifier,
                              icmp_sequence_number)

    # 构建ICMP报文
    icmp_packet = icmp_header + data.encode()

    return icmp_packet


if __name__ == "__main__":
    # 创建应用程序对象
    app = QApplication(sys.argv)

    # 创建主窗口对象
    window = PacketSenderWindow()

    # 显示主窗口
    window.show()

    # 运行应用程序的消息循环
    sys.exit(app.exec_())