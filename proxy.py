import asyncio
import socket
import sys
from Common.DiscordInterface import Interface


class Endpoint:
    def __init__(self, interface, *connectionArgs):
        self.loop = asyncio.get_event_loop()
        self.interface = interface

        if type(connectionArgs[0]) is socket.socket:
            self.server = connectionArgs[0]
        else:
            self.server = None
            self.destAddr = connectionArgs[0]
            self.destPort = connectionArgs[1]

        if self.server:
            self.server.setblocking(True)
            self.sock = self.server.accept()
            self.sock = self.sock[0]
            self.sock.setblocking(False)
            self.server.setblocking(False)
        else:
            self.sock = socket.create_connection((self.destAddr, self.destPort))
            self.sock.setblocking(False)


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
            self.sock.setblocking(False)
            await self.loop.sock_connect(self.sock, (self.destAddr, self.destPort))


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

    token = sys.argv[2] 
    commChannelId = sys.argv[3]
    interface = Interface(commChannelId)
    loop = asyncio.get_event_loop()

    if sys.argv[1] == "source":
        port = sys.argv[4]
        port = int(port)

        server = socket.socket()
        server.bind(('', port))
        server.listen(8)

        endpoint = Endpoint(interface, server)

    elif sys.argv[1] == "dest":
        destAddr, port = sys.argv[4:6]
        port = int(port)

        endpoint = Endpoint(interface, destAddr, port)

    loop.create_task(endpoint.sendLoop())
    loop.create_task(endpoint.recvLoop())

    interface.run(token)


if __name__ == "__main__":
    main()