//
// Created by stdout on 2021/4/5.
//

#include "Bind.h"

SOCKET Bind::listen(int port) {
    // init has None connection
    WORD version = MAKEWORD(2,2);
    WSADATA  wsaData;
    if (WSAStartup(version, &wsaData) != 0) {
        // raise Exception
        return INVALID_SOCKET;
    }
    // start a tcp link
    SOCKET server = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (server == INVALID_SOCKET) {
        // raise Exception
        return INVALID_SOCKET;
    }

    // set listen params
    sockaddr_in sockAddr;
    sockAddr.sin_family = AF_INET;
    sockAddr.sin_port = htons(port);
    sockAddr.sin_addr.S_un.S_addr = INADDR_ANY;

    if (bind(server, (sockaddr*)&sockAddr, sizeof(sockAddr)) == SOCKET_ERROR) {
        // raise exception
        return INVALID_SOCKET;
    }

    if (::listen(server, 10) == SOCKET_ERROR) {
        // raise exception
        return INVALID_SOCKET;
    }
    return server;
}

int Bind::NewConnection(SOCKET client) {
    // malloc a buf to write ans

    if (client == INVALID_SOCKET) {
        // raise exception
        return 0;
    }

    char signal1[] = "cmd >\x00";
    dktb::BUFFER send_cmd;
    send_cmd.size = strlen(signal1);
    send_cmd.buf = (unsigned char *)signal1;

    while (true) {
        dktb::SendData(client, &send_cmd);

        dktb::BUFFER *recv = dktb::RecvData(client);

        if (recv->size > 0) {
            recv->buf[recv->size] = '\0';
            if (recv->buf[recv->size - 1] == '\n') {
                recv->buf[recv->size - 1] = 0;
            }

            char *cmd = strtok((char *)recv->buf, " ");
            RET ret = PreDealCommand(cmd);
            if (ret.model == STOP_MODEL) {
                const char *exit = "exit";
                dktb::SendData(client, dktb::Char2Buffer((char *)exit));
                return ret.ret;
            }

            dktb::BUFFER *result;

            try {
                int length = strlen(cmd);
                char *args = (char *)&recv->buf[length + 1];

                result = CommandExecutor::dealWithCommand(cmd, args);
                dktb::DeleteBuffer(recv);
            } catch (std::exception &e) {
                result->buf = (unsigned char*)malloc(sizeof(unsigned char) * 0x20);
                strncpy((char *)result->buf, "command error\n\x00", 14);
                result->size = strlen("command error\n");
            }
            dktb::SendData(client, result);
            dktb::DeleteBuffer(result);

            dktb::BUFFER *ok = dktb::RecvData(client);
            if (!strncmp((char *)ok->buf, "ok", 2)) {
                continue;
            } else{
                const char *exit = "exit";
                dktb::SendData(client, dktb::Char2Buffer((char *)exit));
                return CLOSE_CONNECTION;
            }
        }
    }


}

SOCKET Bind::AcceptConnection(SOCKET server) {
    SOCKET client;
    sockaddr client_sin;
    int len = sizeof(client_sin);

    client = accept(server, (sockaddr *) &client_sin, &len);
    if (client == INVALID_SOCKET) {
        // raise exception
        return INVALID_SOCKET;
    }
    return client;
}

bool Bind::start(int port) {

    SOCKET server = Bind::listen(port);
    // set up client
    SOCKET clientSocket;

    // flag ==> has connection?
    int flag = 0;
    while (true) {
        if (!flag) {
            clientSocket = AcceptConnection(server);

            // if return a STOP_MODEL
            int ret = Bind::NewConnection(clientSocket);

            // for "exit"
            if (ret == CLOSE_CONNECTION) {
                Bind::CloseSocket(clientSocket);
                break;
            }
            // for "back"
            else if (ret == WAIT_FOR_OTHOR) {
                Bind::CloseSocket(clientSocket);
                flag = 0;
            }
        }
    }
    Bind::CloseSocket(server);
    WSACleanup();

    return true;
}

void Bind::CloseSocket(SOCKET socket) {
    closesocket(socket);
}

RET Bind::PreDealCommand(char* cmd) {
    RET result;
    if (!strncmp(cmd, "exit", 4)) {
        result.model = STOP_MODEL;
        result.ret = WAIT_FOR_OTHOR;
    }
    if (!strncmp(cmd, "back", 4)) {
        result.model = STOP_MODEL;
        result.ret = WAIT_FOR_OTHOR;
    }
    if (!strncmp(cmd, "exec", 4)) {
        result.model = CONTINUE_MODEL;
        result.ret = EXECUTE_COMMAND;
    }
    if (!strncmp(cmd, "stop", 4)) {
        result.model = STOP_MODEL;
        result.ret = CLOSE_CONNECTION;
    }
    return result;
}


