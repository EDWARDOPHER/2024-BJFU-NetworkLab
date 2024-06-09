解释器：python3.11
guest os: Ubuntu 22.04.4 LTS
host os: Windows11

ASCII.txt文件为client用于读取的英文文本

运行：
server.py： 运行在guest os(虚拟机)上，在终端输入 'python/python3/python2 server.py' 即可，python, python3, python2根据您系统安装的解释器版本选择，例如在ubuntu系统下我安装了python3.11，那么输入 'python3 server.py' 。

client.py：运行在host os下，在终端输入'python client.py 192.168.243.129 1200 128 512', 这几个参数分别是server IP, server Port, min, max, server IP 根据你的server来选择，端口为1200， 例如我的server IP为192.168.243.129，那么我的ip=192.168.243.129， min, max则是块大小区间，min 必须小于max, 同时max不能大于1024
