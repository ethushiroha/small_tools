//
// Created by stdout on 2021/4/5.
//

#include "Server/Bind.h"

int CommandExecutor::BufferSize = 1024;

int main() {

    int port = 8848;
    Bind::start(port);


    return 0;
}
