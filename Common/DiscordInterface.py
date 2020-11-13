import discord
import asyncio
from base64 import a85encode, a85decode

class Interface(discord.Client):
    messageBlockSize = 1600
    startHeader = "Message"
    lengthHeader = "Length"

    def __init__(self, commChannelId):
        super().__init__()
        self.commChannelId = commChannelId
        self.recvQueue = asyncio.Queue()
        self.incomingQueue = asyncio.Queue()


    async def recv(self):
        """
        Receieve a message.
        Essentialy a helper function for on_message.
        Acts like normal socket recieve, except byte length doesn't need to be specified.
        """

        ## Get message from queue. Messages are received in on_message, then processed in process_messages
        return await self.recvQueue.get()


    async def send(self, message):
        """
        Send a message
        """
        await self.wait_until_ready()
        ## Format message(if message is string, convert to 
        ## bytes, then add message start text and length)
        if type(message) is str:
            message = message.encode()

        formattedMessage = self.startHeader.encode() + b":\n"
        formattedMessage += self.lengthHeader.encode() + b":" + str(len(message)).encode() + b"\n"
        formattedMessage += message

        formattedMessage = a85encode(formattedMessage).decode()

        ## Get communication channel
        commChannel = await self.fetch_channel(self.commChannelId)

        ## Send message
        # Message sent in base64 encoded chunks
        remaining = formattedMessage
        while len(remaining) > self.messageBlockSize:
            await commChannel.send(remaining[:self.messageBlockSize])
            remaining = remaining[self.messageBlockSize:]

        await commChannel.send(remaining)


    async def on_ready(self):
        print(self.user.name + ": Logged in")
        await self.process_messages()


    async def on_message(self, message):
        """
        Bas64 decode incoming messages, and add them to the incoming queue
        """
        if message.author != self.user:
            await self.incomingQueue.put(a85decode(message.content))


    async def process_messages(self):
        """
        Piece messages back together from the incomingQueue, then add them to the recvQueue
        """
        while self.is_ready():
            message = b""

            block = await self.incomingQueue.get()
            if not block.startswith(self.startHeader.encode()):
                continue

            lines = block.split(b"\n")

            length = int(lines[1].split(b":")[1])
            body = b"\n".join(lines[2:])

            while len(body) < length:
                length -= len(body)
                message += body
                body = await self.incomingQueue.get()

            message += body

            await self.recvQueue.put(message)