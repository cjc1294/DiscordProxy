import discord

class Interface:
    def __init__(self, token, commChannelId):
        self.token = token
        self.commChannelId = commChannelId
        self.client = discord.Client()


    def run(self):
        self.client.run(self.token)


    def recv(self):
        pass


    def send(self, message):
        pass