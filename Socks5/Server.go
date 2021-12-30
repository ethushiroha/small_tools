package main

import (
	"bufio"
	"fmt"
	"io"
	"net"
)

const (
	SOCKS5_VERSION 		byte = 5
	AUTH_COUNT  		byte = 1
	AUTH_METHOD 		byte = 0

	ACCEPT_AUTH 		byte = 0

	COMMAND_CONNECT 	byte = 1
	TYPE_IPV4			byte = 1
	TYPE_DOMAIN			byte = 3
	TYPE_IPV6			byte = 4

	RESULT_SUCCESS		byte = 0
)

type RemoteAddress struct {
	Domain 	string
	Ipv4	[]byte
	Type	byte
	Port	int
}

func Socks5Forward(client net.Conn, remote net.Conn) {
	fmt.Printf("start forward\n")
	forward := func(dst net.Conn, src net.Conn) {
		defer dst.Close()
		defer src.Close()
		io.Copy(src, dst)
	}
	go forward(client, remote)
	go forward(remote, client)
}

func Socks5SendCommand(conn net.Conn, remote *RemoteAddress) net.Conn{
	var address string
	if remote.Type == TYPE_DOMAIN {
		address = remote.Domain
	}
	if remote.Type == TYPE_IPV4 {
		address = fmt.Sprintf("%d.%d.%d.%d",
			remote.Ipv4[0], remote.Ipv4[1], remote.Ipv4[2], remote.Ipv4[3])
	}
	address = fmt.Sprintf("%s:%d", address, remote.Port)
	client, err := net.Dial("tcp", address)
	if err != nil {
		ShowErr(err)
		conn.Close()
		return nil
	}

	var sendBytes = []byte { SOCKS5_VERSION, RESULT_SUCCESS, 0x0, TYPE_IPV4, 0x0,0x0,0x0,0x0, byte(remote.Port >> 8), byte(remote.Port) }
	_, err = conn.Write(sendBytes)
	if err != nil {
		ShowErr(err)
		return nil
	}
	fmt.Printf("send command response\n")

	return client
}

func Socks5RecvCommand(conn net.Conn) *RemoteAddress {
	var remote = new(RemoteAddress)

	reader := bufio.NewReader(conn)
	var buf [128]byte
	n, err := reader.Read(buf[:])
	if err != nil {
		ShowErr(err)
		return nil
	}
	if buf[0] != SOCKS5_VERSION {
		fmt.Printf("command version error: 0x%x\n", buf[0])
		return nil
	}
	if buf[1] != COMMAND_CONNECT {
		fmt.Printf("command connect error: 0x%x\n", buf[1])
		return nil
	}

	remote.Type = buf[3]
	switch remote.Type {
	case TYPE_IPV4:
		remote.Ipv4 = buf[4:8]
	case TYPE_DOMAIN:
		addrBytes := buf[5:n-2]
		remote.Domain = string(addrBytes)
	default:
		return nil
	}

	addrPort := buf[n-2:n]
	remote.Port = int(addrPort[0])*256 + int(addrPort[1])

	return remote
}

func Socks5Command(conn net.Conn) net.Conn {
	remote := Socks5RecvCommand(conn)
	if remote == nil {
		return nil
	}
	var address string
	if remote.Type == TYPE_DOMAIN {
		address = remote.Domain
	}
	if remote.Type == TYPE_IPV4 {
		address = fmt.Sprintf("%d.%d.%d.%d",
			remote.Ipv4[0], remote.Ipv4[1], remote.Ipv4[2], remote.Ipv4[3])
	}
	fmt.Printf("remote address: %s:%d\n", address, remote.Port)

	return Socks5SendCommand(conn, remote)

}

func Socks5Auth(conn net.Conn) bool {
	reader := bufio.NewReader(conn)
	var buf [4]byte
	n, err := reader.Read(buf[:])
	if err != nil {
		ShowErr(err)
		return false
	}
	if n != 3 {
		fmt.Printf("auth length error: %d\n", n)
		return false
	}

	if buf[0] != SOCKS5_VERSION || buf[1] != AUTH_COUNT || buf[2] != AUTH_METHOD {
		fmt.Printf("auth failed, buf: 0x%x, 0x%x, 0x%x\n", buf[0], buf[1], buf[2])
		return false
	}
	fmt.Printf("auth success\n")

	var responseBuf = [] byte {SOCKS5_VERSION, ACCEPT_AUTH}
	conn.Write(responseBuf)

	fmt.Printf("send auth response: 0x%x, 0x%x\n", responseBuf[0], responseBuf[1])
	return true
}

func Process(client net.Conn) {

	if !Socks5Auth(client) {
		return
	}

	remote := Socks5Command(client)
	if remote == nil {
		return
	}

	Socks5Forward(client, remote)

}

func ShowErr(err error) {
	fmt.Printf("Listen failed: %s\n", err)
}

func main() {
	server, err := net.Listen("tcp", ":1080")
	if err != nil {
		ShowErr(err)
		return
	}
	fmt.Printf("listen start\n")
	for {
		client, err := server.Accept()
		if err != nil {
			ShowErr(err)
			return
		}

		go Process(client)

	}
}
