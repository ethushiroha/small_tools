from Crypto.Cipher import DES
from Crypto.Util.number import long_to_bytes, bytes_to_long

from md4 import MD4


class LM_hash:
    def __init__(self, password=None):
        self.password = password
        self.key = b'KGS!@#$%'

    '''
    def __str__(self):
        return self.password + " ==> " + self.hexdigest()
    '''

    def __str__(self):
        return self.hexdigest()

    def hexdigest(self):
        password = self.password.upper()
        password = password.encode().ljust(14, b'\x00')
        password = hex(bytes_to_long(password))[2:]
        tmp_list = ['0x' + password[:14], '0x' + password[14:]]
        ans = ""
        for i in range(2):
            tmp_key = []
            key = int(tmp_list[i], 16)
            for j in range(8):
                tmp_key.append(hex((key & 0x7f) * 0x2)[2:])
                key = key >> 7

            tmp_key.reverse()
            key = "0x"
            for j in tmp_key:
                if len(j) < 2:
                    j = '0' + j
                key += j
            value = long_to_bytes(int(key, 16))
            val = len(value) % 8
            if val != 0:
                value += b'\x00' * (8 - val)
            des = DES.new(key=value, mode=DES.MODE_ECB)
            ans += des.encrypt(self.key).hex()
        return ans


def main():
    print(LM_hash('hongrisec@2020'))


if __name__ == '__main__':
    main()
