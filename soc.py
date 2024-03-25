import socket

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

# 示例用法
source_ip = "192.168.0.100"
destination_ip = "192.168.0.200"
source_port = find_available_port()  # 动态选择未被占用的端口号
destination_port = 5678
payload = "Hello, server!"

send_tcp_packet(source_ip, destination_ip, source_port, destination_port, payload)
send_udp_packet(source_ip, destination_ip, source_port, destination_port, payload)