import optparse
import socket
import threading
import sys


def check_ip(ip: str) -> bool:
    tmp_ip_list = ip.split('.')
    # check length
    if len(tmp_ip_list) != 4:
        return False
    # check range
    for i in tmp_ip_list:
        if int(i) > 255:
            return False
    return True


def check_port(port_list: list) -> bool:
    for port in port_list:
        if int(port) > 65535 or int(port) < 0:
            return False
    return True


def setThreadNumber(number: int) -> int:
    if number < 0:
        return 0
    elif number > 10:
        return 10
    else:
        return number


def set_ip(ip: str, mode: int) -> list:
    tmp_ip_list = ip.split(".")
    ans_ip_list = []
    if mode == 0:
        ans_ip_list.append(ip)
    # 0.0.0.0/24
    elif mode == 24:
        for i in range(255):
            tmp_ip = tmp_ip_list[0] + '.' + tmp_ip_list[1] + '.' + tmp_ip_list[2] + '.' + str(i)
            ans_ip_list.append(tmp_ip)
    return ans_ip_list


def split_ip(ip: str) -> set:
    mode = 0
    if "/" in ip:
        tmp_ip_list = ip.split("/")
        ip = tmp_ip_list[0]
        mode = int(tmp_ip_list[1])
    return ip, mode


def test_connection(ip, port):
    try:
        s = socket.socket()
        # 2 秒没连通就说没开
        s.settimeout(2)
        s.connect((ip, port))
        print("[+] port: {0} is open".format(port))
    except:
        # print("[-] port: {0} is close".format(port))
        pass


def start_scan(ip_list: list, port_list: list):
    print("[+] scan start.....")
    for ip in ip_list:
        for port in port_list:
            thread = threading.Thread(target=test_connection, args=(ip, port))
            thread.start()


def set_port(port: str) -> list:
    ans_port_list = []
    if ',' in port:
        tmp_port_list = port.split(",")
        for ports in tmp_port_list:
            ans_port_list.append(int(ports))
    elif '-' in port:
        tmp_port_list = port.split('-')
        if (0 < int(tmp_port_list[0]) < 65535) and (0 < int(tmp_port_list[1]) < 65535):
            if int(tmp_port_list[0]) < int(tmp_port_list[1]):
                for ports in range(int(tmp_port_list[0]), int(tmp_port_list[1]) + 1):
                    ans_port_list.append(ports)

    return ans_port_list


def set_parser() -> set:
    parser = optparse.OptionParser()
    parser.add_option("-i", "--ip", dest="ip", type='string', help="scan ip")
    parser.add_option("-p", "--port", type="string", dest="port", help="scan port")
    parser.add_option("-o", "--outfile", type='string', dest='filename', help='write result to file')

    # parser.add_option("-t", "--threads", dest='threads', type='int', help="the thread of process")

    (option, arg) = parser.parse_args()
    return option, arg


def main():
    option, arg = set_parser()
    ip, mode = split_ip(option.ip)
    port = option.port
    file_name = option.filename
    if file_name is not None:
        sys.stdout = open(file_name, 'w+')
    # thread_number = option.threads
    if check_ip(ip):
        # thread_number = setThreadNumber(thread_number)
        # if thread_number != 0:
        ip_list = set_ip(ip=ip, mode=mode)
        # print(ip_list)
        port_list = set_port(port=port)
        # print(port_list)
        if check_port(port_list):
            start_scan(ip_list, port_list)
            print("[-] scan ends")


if __name__ == '__main__':
    main()
