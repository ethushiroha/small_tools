from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Cipher import DES

des_key = b'KGS!@#$%'


def main():
    password = 'hongrisec@2020'.upper()
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
        print(key)
        value = long_to_bytes(int(key, 16))
        val = len(value) % 8
        if val != 0:
            value += b'\x00' * (8 - val)
        print("value ==> ", type(value), value)

        des = DES.new(key=value, mode=DES.MODE_ECB)
        ans += des.encrypt(des_key).hex()
    print(ans)


if __name__ == '__main__':
    main()
