import socket
import threading
import signal
import sys

running = True  # 控制服务器运行状态的全局变量

def handle_tcp_client(client_socket):
    while running:
        data = client_socket.recv(1024)
        if not data:
            break
        client_socket.sendall(data)
    client_socket.close()

def handle_udp_client(data, client_address, server_socket):
    server_socket.sendto(data, client_address)


def signal_handler(signum, frame):
    stop_servers()

def stop_servers():
    global running  # 使用全局变量
    running = False
    print("服务器已停止")
    sys.exit()

def start_servers():
    host = '127.0.0.1'
    tcp_port = 8888
    udp_port = 9999

    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind((host, tcp_port))
    tcp_server_socket.listen(2)

    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_server_socket.bind((host, udp_port))



    print("等待连接和数据...")

    tcp_thread = threading.Thread(target=start_tcp_server, args=(tcp_server_socket,))
    tcp_thread.start()

    udp_thread = threading.Thread(target=start_udp_server, args=(udp_server_socket,))
    udp_thread.start()

    # 主线程继续执行其他操作
    while True:
        signal.signal(signal.SIGINT, signal_handler)
        pass


def start_tcp_server(tcp_server_socket):
    while running:
        client_socket, client_address = tcp_server_socket.accept()
        print("TCP连接来自:", client_address)
        client_thread = threading.Thread(target=handle_tcp_client, args=(client_socket,))
        client_thread.start()

def start_udp_server(udp_server_socket):
    while running:
        data, client_address = udp_server_socket.recvfrom(1024)
        print("UDP连接来自:", client_address)
        udp_thread = threading.Thread(target=handle_udp_client, args=(data, client_address, udp_server_socket))
        udp_thread.start()

start_servers()