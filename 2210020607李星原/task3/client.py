"""
    client
"""
import socket
import random
import sys


HOST = sys.argv[1]      # 服务端地址
PORT = int(sys.argv[2])     # 服务端端口
lmin = int(sys.argv[3])
lmax = int(sys.argv[4])

if lmin > lmax or lmax > 1024:
    print("min 大于 max， 或者max 大于1024，请修改后重新尝试")
    sys.exit()

FILE_PATH = 'ASCII.txt'  # 需要发送的文本文件路径

segment_size_range = (lmin, lmax)  # 分块大小区间

segment_message = list()

msg_type = [1, 2, 3, 4, ]
length = 0

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


def main():
    try:
        with open(FILE_PATH, 'r', encoding='utf-8') as file:
            while True:
                seg_size = random.randint(*segment_size_range)
                message = file.read(seg_size)
                if not message:
                    break
                segment_message.append(message)

        # initialization
        init_msg = f"{msg_type[0]}: {len(segment_message)}"
        client_socket.send(init_msg.encode())
        try:
            response = client_socket.recv(1024)
            if int(response.decode()) != msg_type[1]:
                print('server doesnt agree')
            else:
                # 开始发送消息
                idx = 0
                for data in segment_message:
                    # flag = input('If you want to continue, type "c"')
                    # if flag != 'c':
                    #     break
                    msg = f"{msg_type[2]}:{len(data)}:{data}"
                    client_socket.sendall(msg.encode('utf-8'))
                    try:
                        data = client_socket.recv(1024)
                        idx += 1
                        data = data.decode('utf-8').split(':')
                        print(f"{idx}: {data[2]}")
                    except Exception as e:
                        print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()

