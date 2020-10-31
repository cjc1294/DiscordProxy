import discord
import asyncio
from base64 import b64encode, b64decode

class Interface(discord.Client):
    messageBlockSize = 1500
    startHeader = "Message"
    lengthHeader = "Length"

    def __init__(self, commChannelId):
        super().__init__()
        self.commChannelId = commChannelId
        self.recvQueue = asyncio.Queue()


    def recv(self):
        """
        Receieve a message.
        Essentialy a helper function for on_message.
        Acts like normal socket recieve, except 
        byte length doesn't need to be specified.
        """

        ## Get message from queue. Messages are processed in on_message
        pass


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

        formattedMessage = b64encode(formattedMessage).decode()

        ## Get communication channel
        commChannel = await self.fetch_channel(self.commChannelId)

        ## Send message
        # Message sent in base64 encoded chunks
        remaining = formattedMessage
        while len(remaining) > self.messageBlockSize:
            await commChannel.send(formattedMessage[:self.messageBlockSize])
            remaining = remaining[self.messageBlockSize:]

        await commChannel.send(remaining)
        print("[->] {}".format(message))


    async def on_ready(self):
        print(self.user.name + ": Logged in")
