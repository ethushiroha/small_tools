//
// Created by stdout on 2021/4/5.
//

#include "Client/BindConnector.h"

int main() {
    char* ip = "127.0.0.1";
    int port = 8848;

    BindConnector::start(ip, port);

}