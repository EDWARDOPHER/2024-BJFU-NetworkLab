"""
    - client 在100ms内
        - 接收到server的响应：计算本次交互的RTT和 server的系统时间（hh-mm-ss）
        - 没接收到则认为丢包，丢包重传，两次重传失败，则放弃重传
"""

import socket
import sys
import select
import time

"""
    select 外部包可以实现对数据丢包的检测
    
    time 用作计算RTT， 实现逻辑为：当Client发送到接收这段时间代码运行的时间
"""

# ip, port = sys.argv[1], int(sys.argv[2])

# ip, port = '127.0.0.1', 1200
ip, port = '192.168.243.255', 1200

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# client.connect((ip, port))    # 本次实验要求要先模仿tcp建立连接这一步骤暂时没看懂

while True:
    message = input("message you want to send: ")
    RTT_start = time.time() * 1000
    client.sendto(message.encode(), (ip, port))
    retries = 0
    while retries < 2:
        ready = select.select([client], [], [], 0.1)
        if ready[0]:
            RTT_end = time.time() * 1000
            RTT = RTT_end - RTT_start  # RTT时间计算
            backData, addr = client.recvfrom(1024)
            print('server back data: ', backData.decode(), ' | address: ', addr, ' | RTT: ', RTT, 'ms')
            break
        else:
            retries += 1
            print("未接受到server回传数据, 进行第%d次回传" % retries)
            client.sendto(message.encode(), (ip, port))
            RTT_start = time.time() * 1000
            if retries == 2:
                print("2次重传失败，放弃本次重传\n")


client.close()
