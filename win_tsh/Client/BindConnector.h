//
// Created by stdout on 2021/4/5.
//

#ifndef BACKDOOR_BINDCONNECTOR_H
#define BACKDOOR_BINDCONNECTOR_H

#include "../Utils/BindUtils.h"

class BindConnector {
public:
    static void start(char* ip, int port);

private:
    static SOCKET Connect(char* ip, int port);

    static void Close(SOCKET socket);

};


#endif //BACKDOOR_BINDCONNECTOR_H
