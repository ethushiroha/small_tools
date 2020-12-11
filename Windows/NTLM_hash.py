from Windows.md4 import MD4


class NTLM_hash:
    def __init__(self, password=None):
        self.password = password

    def set_password(self, password):
        self.password = password

    def __str__(self):
        return self.password + " ==> " + self.hexdigest()

    def __eq__(self, other):
        return self.hexdigest() == other.hexdigest()

    def hexdigest(self):
        # FE FF 表示UTF-16
        tmp_byte = self.password.encode('utf-16')[2:]
        return MD4(tmp_byte).hexdigest()


def main():
    password = input("input your password: ")
    ntlm = NTLM_hash(password)
    print(ntlm)


if __name__ == '__main__':
    main()
