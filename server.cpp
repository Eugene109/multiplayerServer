#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <cassert>
#include <iostream>
// #include <thread>
#include <string>
#include <vector>

using namespace std;

#define PORT 8080

void threaded_client(int socket)
{
    //
    char *hello = "Hello from server";
    send(socket, hello, strlen(hello), 0);
    char buffer[1024] = {0};
    int valread;
    while (true)
    {
        valread = read(socket, buffer, 1024);
        if (valread <= 0)
        {
            printf("Disconnected");
            break;
        }
        else
        {
            printf("Received: %p\n", buffer);
            printf("Sending: %p\n", buffer);
        }
        send(socket, buffer, strlen(buffer), 0);
    }
    printf("Lost connection");
    close(socket);
}

int main(int argc, char const *argv[])
{
    // string server = "10.202.224.101";
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    int server_fd, new_socket, valread;
    int opt = 1;
    char buffer[1024] = {0};
    char *hello = "Hello from server";
    printf("hello there");

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        perror("socket failed");
        // exit(EXIT_FAILURE);
        assert(0);
    }
    printf("hello there");
    if (setsockopt(server_fd, SOL_SOCKET,
                   SO_REUSEADDR | SO_REUSEPORT, &opt,
                   sizeof(opt)))
    {
        perror("setsockopt");
        // exit(EXIT_FAILURE);
        assert(0);
    }
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Forcefully attaching socket to the port 8080
    if (bind(server_fd, (struct sockaddr *)&address,
             sizeof(address)) < 0)
    {
        perror("bind failed");
        // exit(EXIT_FAILURE);
        assert(0);
    }
    if (listen(server_fd, 3) < 0)
    {
        perror("listen");
        // exit(EXIT_FAILURE);
        assert(0);
    }
    printf("Waiting for a connection, Server Started");

    //
    //
    //
    //

    // thread
    while (true)
    {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address,
                                 (socklen_t *)&addrlen)) < 0)
        {
            perror("accept");
            // exit(EXIT_FAILURE);
            assert(0);
        }
        // thread newThread(threaded_client, new_socket);
        // newThread.join();
        threaded_client(new_socket);
    }
    // closing the listening socket
    shutdown(server_fd, SHUT_RDWR);
    return 0;
}