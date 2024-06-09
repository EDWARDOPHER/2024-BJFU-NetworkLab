"""
    server
"""
import socket
import threading


# 定义一个处理客户端请求的函数
def handle_client(client_socket, client_address):
    msg_type = [1, 2, 3, 4, ]
    print(f"Accepted connection from {client_address}")
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                print(f"Connection closed by {client_address}")
                break
            else:
                data = message.decode('utf-8')
                data = data.split(':')
                if int(data[0]) is msg_type[0]:
                    message = f"{msg_type[1]}"
                elif int(data[0]) is msg_type[2]:
                    message = f"{msg_type[3]}:{data[1]}:{data[2][::-1]}"
                client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error: {client_socket}: {e}")
    client_socket.close()


def main():
    # 定义服务器地址和端口
    server_ip = '127.0.0.1'
    server_port = 65432

    # 创建TCP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print(f"Server listening on {server_ip}:{server_port}")

    while True:
        # 接受客户端连接
        client_socket, client_address = server_socket.accept()
        # 为每个客户端连接创建一个新线程
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()


if __name__ == "__main__":
    main()
