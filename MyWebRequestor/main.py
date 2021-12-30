from MyWebRequestor.Utils.MySender import Sender


def test():
    sender: Sender = Sender.getFromJson("./Poc/test.json")
    res = sender.send()


if __name__ == '__main__':
    test()
