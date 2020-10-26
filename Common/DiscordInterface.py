import discord

class Interface:
    def __init__(self, token, commChannelId):
        self.token = token
        self.commChannelId = commChannelId
        self.client = discord.Client()


    def run(self):
        self.client.run(self.token)


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