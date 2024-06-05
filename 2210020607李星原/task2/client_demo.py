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

ip, port = '127.0.0.1', 1200
# ip, port = '192.168.243.255', 1200

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def start_connections():
    while 1:
        message = 'connect'
        client.sendto(message.encode(), (ip, port))
        try:
            response, _ = client.recvfrom(2024)
            if response.decode() == 'ACK':
                print("connection established")
                return True
        except ConnectionResetError:
            print("connection timeout")


def stop_connections():
    while True:
        message = 'disconnect'
        client.sendto(message.encode(), (ip, port))
        try:
            response, _ = client.recvfrom(2024)
            if response.decode() == 'ACK':
                print("connection closed")
                client.close()
                return
        except ConnectionResetError:
            print("connection closed timeout")


def data_trans():
    sequence_number = 0
    version = 2

    rtt_total = []  # 每一次的RTT数据
    udp_packets = 0  # 接收到的udp packet
    loss = 0.00  # 丢包率
    server_response_time = 0.00  # server 响应时间
    cnt = 0  # 发送的udp packets
    while sequence_number < 12:
        systime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        # 报文内容
        sequence_number += 1
        content = f"{systime} : client -> server"
        message = f"{sequence_number}:{version}:{content}"  # 报文内容封装
        rtt_start = time.time() * 1000  # 用来计算RTT
        client.sendto(message.encode(), (ip, port))     # 发送消息
        cnt += 1
        retries = 0     # 两次重传记录

        # 是否丢包
        while retries < 2:
            ready = select.select([client], [], [], 0.1)
            # 如果接收到了回传数据
            if ready[0]:
                rtt_end = time.time() * 1000
                rtt = rtt_end - rtt_start  # RTT时间计算
                try:
                    back_data, addr = client.recvfrom(2024)
                    udp_packets += 1
                    data = back_data.decode().split(':')
                    print('sequence number: ', data[0], ' | server IP: ', addr[0], ' | server Port:', addr[1],
                          ' | RTT: ', rtt, 'ms')
                    rtt_total.append(rtt)
                    if sequence_number == '1':
                        server_response_time = float(data[2])
                    elif data[0] == '12':
                        server_response_time = float(data[2]) - server_response_time
                except OSError:
                    print('传输数据大于接收范围')

                break
            else:
                retries += 1
                print(f"sequence no:{sequence_number}, request time out")
                message = f"{sequence_number}:{version}:{content}"
                client.sendto(message.encode(), (ip, port))
                cnt += 1
                rtt_start = time.time() * 1000

    loss = (1 - udp_packets / cnt) * 100
    print('汇总信息：\nreceived UDP packets: ', udp_packets, '\nloss: ', loss, '%', '\nserver response: ', server_response_time,
          '\nRTT max: ', rtt_max(rtt_total), ' | min: ', rtt_min(rtt_total), ' | avg: ', rtt_avg(rtt_total),
          ' | standard deviation: ', rtt_std_deviation(rtt_total), sep='')


def rtt_std_deviation(elem: list):
    avg = rtt_avg(elem)
    ret = 0
    for i in elem:
        ret += pow(i - avg, 2)
    ret /= len(elem)
    return ret


def rtt_avg(elem: list):
    ret = 0
    for i in elem:
        ret += i
    ret /= len(elem)
    return ret


def rtt_min(elem: list):
    ret = 9999
    for i in elem:
        ret = min(ret, i)
    return ret


def rtt_max(elem: list):
    ret = 0.0
    for i in elem:
        ret = max(ret, i)
    return ret


if __name__ == '__main__':
    if start_connections():
        print("connected")
        data_trans()
        stop_connections()













