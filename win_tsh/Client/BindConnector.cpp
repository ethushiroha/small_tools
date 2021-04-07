//
// Created by stdout on 2021/4/5.
//

#include <iostream>
#include "BindConnector.h"

void BindConnector::start(char *ip, int port) {
    SOCKET client = BindConnector::Connect(ip, port);

    char buf[1024] = {0};
    dktb::BUFFER *result;

    while (true) {
        result = dktb::RecvData(client);
        dktb::PrintBuffer(result);
        if (!strncmp((char *)result->buf, "exit", 4)) {
            break;
        }
        dktb::DeleteBuffer(result);

        fgets(buf, 1000, stdin);

        result = dktb::Char2Buffer(buf);

        dktb::SendData(client, result);
        dktb::DeleteBuffer(result);

        result = dktb::RecvData(client);
        dktb::PrintBuffer(result);

        if (!strncmp((char *)result->buf, "exit", 4)) {
            break;
        }
        dktb::DeleteBuffer(result);

        dktb::SendData(client, dktb::Char2Buffer("ok"));
    }

    BindConnector::Close(client);
}

SOCKET BindConnector::Connect(char *ip, int port) {
    WORD sockVersion = MAKEWORD(2, 2);
    WSADATA data;
    if (WSAStartup(sockVersion, &data) != 0) {
        return INVALID_SOCKET;
    }

    SOCKET clientSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (clientSocket == INVALID_SOCKET) {
        return INVALID_SOCKET;
    }
    sockaddr_in sock_in;
    sock_in.sin_family = AF_INET;
    sock_in.sin_port = htons(port);
    sock_in.sin_addr.S_un.S_addr = inet_addr(ip);
    if (connect(clientSocket, (sockaddr *) &sock_in, sizeof(sock_in)) == SOCKET_ERROR) {
        return INVALID_SOCKET;
    }

    return clientSocket;


}

void BindConnector::Close(SOCKET socket) {
    closesocket(socket);
}


