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
    sock, addr = serverSocket.recvfrom(2024)    # 是否需要添加分片处理机制
    # 用来模拟TCP连接建立和释放
    if sock.decode() == 'connect':
        print(addr, 'connected')
        message = 'ACK'
        serverSocket.sendto(message.encode(), addr)
        continue
    elif sock.decode() == 'disconnect':
        message = 'ACK'
        serverSocket.sendto(message.encode(), addr)
        break

    sequence_number, version, *last = sock.decode().split(':')
    server_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
    content = f"{server_time}:server -> client"
    flag = random.randint(0, 1)     # 丢包率设定为50%
    if flag == 0:
        print("sending back.....")
        ret = f"{sequence_number}:{version}:{content}"
        serverSocket.sendto(ret.encode(), addr)
    else:
        print('data loss.....')
serverSocket.close()
