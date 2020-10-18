import discord

class Interface:
    def __init__(self, token, commChannelId):
        self.token = token
        self.commChannelId = commChannelId
        self.client = discord.Client()


    def run(self):
        pass


    def recv(self):
        pass


    def send(self, message):
        pass