import discord
import subprocess as sp
import platform

token = "(Token Here)"
white_list = [(Channel ID here)]


def run_command(command):
    out = sp.run(command, capture_output=True)
    if out.returncode == 0:
        return str(out.stdout, 'utf-8')
    else:
        return str(out.stderr, 'utf-8')


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if not message.channel.id in white_list:
            return

        if message.content.startswith("ping"):
            print(message.author.name + ": " + message.content)
            split = message.content.split(' ')
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            if len(split) == 2:
                out = sp.run(['ping', param, '1', split[1]], capture_output=True)
                if out.returncode == 0:
                    await message.channel.send(str(out.stdout, 'utf-8'))
                else:
                    await message.channel.send('Error: ' + str(out.stderr, 'utf-8'))
            else:
                await message.channel.send('Usage: ping (IP address)')


client = MyClient()
client.run(token, bot=False)
