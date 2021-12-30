from ...Models/Msg import Msg


class Parser:
    def __init__(msg: Msg):
        self.__getCommand(msg)


    def __getCommand(msg: Msg) -> None:
        raw_msg = msg['raw_message']
        if raw_msg is None:
            self.command = None
            return

        start_index = raw_msg.indexOf()
