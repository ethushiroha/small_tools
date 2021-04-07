cmake_minimum_required(VERSION 3.17)
project(backdoor)

set(CMAKE_CXX_STANDARD 14)

link_libraries(ws2_32)
add_executable(server Server/Bind.cpp Server/Bind.h CommandExecutor/CommandExecutor.cpp CommandExecutor/CommandExecutor.h Utils/BindUtils.h server.cpp)
add_executable(client Utils/BindUtils.h client.cpp Client/BindConnector.cpp Client/BindConnector.h)