"""
    server
    run on guest os
"""
import socket
import random
import time

"""
    random: 用来获取随机数，模拟丢包
    time: 获取系统时间
"""

ip, port = ['0.0.0.0', 1200]
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    # 先声明一个udp套接字对象
serverSocket.bind((ip, port))  # 配置ip, port

print('udp server start.....')
while 1:
    try:
        sock, addr = serverSocket.recvfrom(2024)
        # 用来模拟TCP连接建立和释放
        if sock.decode() == 'connect':  # 连接建立
            print(addr, 'connected')
            message = 'ACK'
            serverSocket.sendto(message.encode(), addr)
            continue
        elif sock.decode() == 'disconnect':  # 连接释放
            message = 'ACK'
            serverSocket.sendto(message.encode(), addr)
            print(addr, 'disconnected')
            continue

        # 数据处理
        sequence_number, version, *last = sock.decode().split(':')  # 获取seq no, ver
        server_time = time.strftime('%H:%M:%S', time.localtime(time.time()))  # 系统时间
        content = f"{server_time}:server -> client"
        flag = random.randint(0, 1)  # 丢包率设定为50%
        if flag == 0:
            print("sending back.....")
            ret = f"{sequence_number}:{version}:{content}"
            time.sleep(0.0001)  # RTT响应时间基本都太快了，给一个0.1ms的人为延时
            serverSocket.sendto(ret.encode(), addr)
        else:
            print('data loss.....')
    except OSError:
        print('接收数据超出范围')

serverSocket.close()