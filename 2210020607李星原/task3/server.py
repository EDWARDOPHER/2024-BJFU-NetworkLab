"""
    server
"""

import socket
import select

HOST = '127.0.0.1'  # 本地地址
PORT = 65432        # 端口


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 这句话的作用

    server_socket.bind((HOST, PORT))
    server_socket.listen()
    server_socket.setblocking(False)  # 设置为非阻塞模式

    sockets_list = [server_socket]
    clients = {}
    msg_type = [1, 2, 3, 4, ]

    print(f"Server listening on {HOST}:{PORT}")

    while True:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

        for conn_socket in read_sockets:
            if conn_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                client_socket.setblocking(False)
                sockets_list.append(client_socket)
                clients[client_socket] = client_address
                print(f"new connection: {client_address[0]}:{client_address[1]}")
            else:
                try:
                    message = conn_socket.recv(1024)
                    if not message:
                        print(f"Closed connection from {clients[conn_socket][0]}:{clients[conn_socket][1]}")
                        sockets_list.remove(conn_socket)
                        del clients[conn_socket]
                    else:
                        print(f"Received message: {clients[conn_socket][0]}:{clients[conn_socket][1]}:{message.decode('utf-8')}")
                        data = message.decode('utf-8')
                        data = data.split(':')
                        if int(data[0]) is msg_type[0]:
                            message = f"{msg_type[1]}"
                        elif int(data[0]) is msg_type[2]:
                            message = f"{msg_type[3]}:{data[1]}:{data[2][::-1]}"
                        conn_socket.send(message.encode('utf-8'))
                except Exception as e:
                    print(f"Error: {clients[conn_socket][0]}:{clients[conn_socket][1]}: {e}")
                    sockets_list.remove(conn_socket)
                    del clients[conn_socket]

        for notified_socket in exception_sockets:
            sockets_list.remove(notified_socket)
            del clients[notified_socket]


if __name__ == "__main__":
    main()
