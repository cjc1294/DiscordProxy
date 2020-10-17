import discord

class Interface:
    def __init__(self, token):
        self.token = token
        self.client = discord.Client()


    def run(self):
        pass


    def recv(self):
        pass


    def send(self, message):
        pass