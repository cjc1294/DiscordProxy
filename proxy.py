import asyncio
import socket
import sys
from Common.DiscordInterface import Interface


class Endpoint:
    def __init__(self, loop, sock, interface, server=None):
        self.loop = loop
        self.sock = sock
        self.interface = interface
        self.server = server


    async def recvLoop(self):
        await self.interface.wait_until_ready()
        while True:
            incoming = await self.interface.recv()
            print("[<-] Received {} Bytes".format(len(incoming)))
            await self.loop.sock_sendall(self.sock, incoming)


    async def sendLoop(self):
        await self.interface.wait_until_ready()
        while True:
            try:
                outgoing = " "
                while outgoing:
                    outgoing = await self.loop.sock_recv(self.sock, 4096)
                    if len(outgoing) > 0:
                        print("[->] Sent {} Bytes".format(len(outgoing)))
                        await self.interface.send(outgoing)
            except OSError:
                pass

            await self.makeConnection()


    async def makeConnection(self):
        if self.server:
            self.sock = await self.loop.sock_accept(self.server)
            self.sock = self.sock[0]
        else:
            self.sock = socket.socket()
            await self.loop.sock_connect(self.sock, (sys.argv[4], int(sys.argv[5])))


def main():
    global sock
    if len(sys.argv) == 1:
        print("""\
Usage:
    python proxy.py source <token> <channel id> <port>
    python proxy.py dest <token> <channel id> <destination address> <port>\
            """)
        sys.exit(1)

    if len(sys.argv) < 5 or (sys.argv[1] == "dest" and len(sys.argv) < 6):
        if sys.argv[1] == "source":
            print("""\
Usage:
    python proxy.py source <token> <channel id> <port>\
                """)
        elif sys.argv[1] == "dest":
            print("""\
Usage:
    python proxy.py dest <token> <channel id> <destination address> <port>\
                """)
        else:
            print("""\
Usage:
    python proxy.py source <token> <channel id> <port>
    python proxy.py dest <token> <channel id> <destination address> <port>\
                """)
        sys.exit(1)


    if sys.argv[1] == "source":
        token, commChannelId, port = sys.argv[2:5]

        interface = Interface(commChannelId)
        loop = interface.loop

        server = socket.socket()
        server.bind(('', int(port)))
        server.listen(8)

        sock = server.accept()[0]
        sock.setblocking(False)

        server.setblocking(False)

        endpoint = Endpoint(loop, sock, interface, server)

    elif sys.argv[1] == "dest":
        token, commChannelId, destAddr, port = sys.argv[2:6]

        interface = Interface(commChannelId)
        loop = interface.loop

        sock = socket.create_connection((destAddr, int(port)))
        sock.setblocking(False)

        endpoint = Endpoint(loop, sock, interface)

    interface.loop.create_task(endpoint.sendLoop())
    interface.loop.create_task(endpoint.recvLoop())

    interface.run(token)


if __name__ == "__main__":
    main()