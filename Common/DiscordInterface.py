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


    def send(self, message):
        ## Format message(if message is string, convert to 
        ## bytes, then add message start text and length)

        ## Get communication channel

        ## Send message
        # Message sent in base64 encoded chunks
        pass