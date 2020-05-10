import discord
from gtts import gTTS
import os


token = "(Token Here)"
channels = ["(Channel ID here)"]


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.channel.id in channels:
            await self.tts_read(message)

    def tts_read(self, message):
        filename = "test.mp3"
        text = message.author.display_name + " has said " + message.content
        language = 'en'
    
        speech = gTTS(text=text, lang=language, slow=False)
    
        speech.save(filename)
    
        os.system("afplay " + filename)
        os.remove("test.mp3")


client = MyClient()
client.run(token)
