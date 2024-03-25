import socket

def send_data():
    host = '127.0.0.1'  # 服务器主机地址
    port = 8888         # 服务器端口号

    # 创建套接字对象
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 连接到服务器
    client_socket.connect((host, port))
    print("已连接到服务器")

    while True:
        message = input("请输入要发送的数据（输入'exit'退出）: ")

        if message == 'exit':
            break

        # 发送数据到服务器
        client_socket.sendall(message.encode())

        # 接收服务器回显的数据
        data = client_socket.recv(1024)
        print("服务器回显:", data.decode())

    # 关闭连接
    client_socket.close()

send_data()