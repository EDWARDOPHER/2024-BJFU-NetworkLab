"""
    client
    run on host os
"""
import socket
import sys
import select
import time
import math

"""
    引用包的作用：
    socket 用来构造套接字对象实现udp编程
    sys 用来从命令行接收参数
    select 监听规定时间内是否响应，未响应则超时重传
    time 计算RTT
"""

ip, port = sys.argv[1], int(sys.argv[2])
# ip, port = '127.0.0.1', 1200
# ip, port = '192.168.243.129', 1200

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # 构建一个udp套接字对象


# 连接建立方法
def start_connections():
    while 1:
        message = 'connect'
        client.sendto(message.encode(), (ip, port))
        try:
            response, _ = client.recvfrom(2024)
            if response.decode() == 'ACK':
                print("connection established")
                return True
        except socket.timeout:
            print("connection timeout")


# 关闭连接方法
def stop_connections():
    while True:
        message = 'disconnect'
        client.sendto(message.encode(), (ip, port))
        try:
            response, _ = client.recvfrom(2024)
            if response.decode() == 'ACK':
                print("\nconnection closed")
                client.close()
                return
        except ConnectionResetError:
            print("connection closed timeout")


# 传输数据方法
def data_trans():
    # 报文首部信息，seq no, ver
    sequence_number = 0
    version = 2

    rtt_total = []  # 记录所有的RTT数据
    udp_packets = 0  # 记录接收到的udp packet数量
    loss = 0.00  # 丢包率
    server_response_time = 0.00  # server 响应时间
    cnt = 0  # 发送的udp packets数量

    # 开始十二次request发送
    while sequence_number < 12:
        # 报文内容
        sequence_number += 1
        content = "nothing in the content:client -> server"
        message = f"{sequence_number}:{version}:{content}"  # 报文内容封装

        rtt_start = time.time() * 1000  # 用来计算RTT
        client.sendto(message.encode(), (ip, port))     # 发送消息
        cnt += 1  # 记录发送次数

        retries = 0     # 重传次数
        while 1:
            # 监听在100ms内是否接收到回传消息
            ready = select.select([client], [], [], 0.1)
            # 成功接收回传数据
            if ready[0]:
                rtt_end = time.time() * 1000
                rtt = rtt_end - rtt_start  # RTT时间计算
                try:
                    back_data, addr = client.recvfrom(2024)
                    udp_packets += 1  # udp packets + 1
                    data = back_data.decode().split(':')  # 回传的数据
                    print('sequence number: ', data[0], ' | server IP: ', addr[0], ' | server Port:', addr[1],
                          ' | RTT: ', rtt, 'ms')  # 打印内容
                    rtt_total.append(rtt)  # 将计算的RTT记录在RTT_TOTAL中
                    if data[0] == '1':  # 记录第一次server系统时间
                        server_response_time = float(data[3]) * 60 + float(data[4])
                    elif data[0] == '12':  # 计算server的整体响应时间
                        server_response_time = float(data[3]) * 60 + float(data[4]) - server_response_time
                except OSError:
                    print('传输数据大于接收范围')
                break
            # 发生丢包
            else:
                retries += 1
                print(f"sequence no: {sequence_number}, request time out")
                if retries == 3:    # 已重传两次
                    break
                message = f"{sequence_number}:{version}:{content}"
                rtt_start = time.time() * 1000
                client.sendto(message.encode(), (ip, port))  # 尝试重传
                cnt += 1

    loss = (1 - udp_packets / cnt) * 100  # 计算丢包率
    # 打印汇总信息
    print('汇总信息：\nreceived UDP packets: ', udp_packets, '\nloss: ', loss, '%', '\nserver response: ', server_response_time, 's'
          '\nRTT max: ', rtt_max(rtt_total), ' | min: ', rtt_min(rtt_total), ' | avg: ', rtt_avg(rtt_total),
          ' | standard deviation: ', rtt_std_deviation(rtt_total), sep='')


# 计算标准差
def rtt_std_deviation(elem: list):
    avg = rtt_avg(elem)
    ret = 0
    for i in elem:
        ret += pow(i - avg, 2)
    ret /= len(elem)
    ret = math.sqrt(ret)
    return ret


# 计算平均值
def rtt_avg(elem: list):
    ret = 0
    for i in elem:
        ret += i
    ret /= len(elem)
    return ret


# 最小值
def rtt_min(elem: list):
    ret = 9999
    for i in elem:
        ret = min(ret, i)
    return ret


# 最大值
def rtt_max(elem: list):
    ret = 0.0
    for i in elem:
        ret = max(ret, i)
    return ret


# main
if __name__ == '__main__':
    if start_connections():
        data_trans()
        stop_connections()













