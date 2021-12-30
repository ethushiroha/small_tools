from LM_hash import LM_hash
from NTLM_hash import NTLM_hash
from optparse import OptionParser
import sys

def tests():
    password = "hello"
    print("{}:{}".format(LM_hash(password), NTLM_hash(password)))


def main():
    if len(sys.argv) != 2:
        print("Usage: python {} password".format(sys.argv[0]))
        print("Returns: lm:ntml")

    else:
        password = sys.argv[1]
        print("password: ", password)
        print("{}:{}".format(LM_hash(password), NTLM_hash(password)))


if __name__ == '__main__':
#     tests()
    main()
