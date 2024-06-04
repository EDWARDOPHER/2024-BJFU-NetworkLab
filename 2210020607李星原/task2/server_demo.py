"""
    - guest os start
    - 模拟tcp连接过程，建立连接后才传输数据
    - client发送12个request, server采用随机不响应模拟丢包

"""
import socket
import random
import time

ip, port = ['127.0.0.1', 1200]
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # 先声明一个对象
serverSocket.bind((ip, port))

while 1:
    print('udp server start.....')
    sock, addr = serverSocket.recvfrom(1024)    # recvfrom 接收数据和客户端的地址、端口
    message = sock.decode()
    print('message: ', message, '   address: ', addr)
    if message == 'exit':
        break

    flag = random.randint(0, 1)     # 丢包率设定为50%
    if flag == 0:
        print("sending back.....")
        ret = "server message: " + message
        serverSocket.sendto(ret.encode(), addr)
    else:
        print('data loss.....')
serverSocket.close()
