# Imports 'n' stuff
import discord
import subprocess as sp
import platform
import shlex


token = "(token here)"

# Commands, root_commands mean only members with Admin can use it
commands = ['whoami', 'ping', 'hostname', 'pwd', 'id', 'echo']
root_commands = ["mkdir", "touch"]

# Setting this to true allows bot to reply to its own echo command
self_reply = False

# Enter allowed channels here
white_list = []


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # Message checks
        if self_reply is False and message.author.id == self.user.id:
            return

        if not message.channel.id in white_list:
            return

        msg_start = message.content.split(' ')[0]
        if msg_start in root_commands and not message.author.guild_permissions.administrator:
            await message.channel.send(message.content + ": Permission denied")

        # Checks for command
        elif msg_start == 'whoami':
            await self.whoami(message)
        elif msg_start == 'ping':
            await self.ping(message)
        elif msg_start == 'hostname':
            await self.hostname(message)
        elif msg_start == 'pwd':
            await self.pwd(message)
        elif msg_start == 'id':
            await self.id(message)
        elif msg_start == 'mkdir':
            await self.mkdir(message)
        elif msg_start == 'touch':
            await self.touch(message)
        elif msg_start == 'echo':
            await self.echo(message)


    async def whoami(self, message):
        if message.author.guild_permissions.administrator:
            await message.channel.send('root')
        else:
            await message.channel.send(message.author.display_name)

    async def ping(self, message):
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

    async def hostname(self, message):
        await message.channel.send(message.guild.name)

    async def pwd(self, message):
        category = '' if message.channel.category is None else message.channel.category.name + '/'
        await message.channel.send(category + message.channel.name)

    async def id(self, message):
        split = message.content.split(' ')
        if len(split) == 2:
            user = message.guild.get_member_named(split[1])
            await self.idout(user, message)
        elif len(split) == 1:
            user = message.author
            await self.idout(user, message)
        else:
            await message.channel.send('Usage: id (username, preferably with the #XXXX)')

    async def idout(self, user, message):
        if not user is None:
            top_role = user.top_role
            await message.channel.send("uid={}({}) gid={}({})".format(str(user.id), user.display_name, str(top_role.id), top_role.name))
        else:
            await message.channel.send('Invalid username')

    async def mkdir(self, message):
        split = message.content.split(' ')
        if len(split) == 2:
            await message.guild.create_category_channel(split[1])
        else:
            await message.channel.send('Usage: mkdir (directory/category name)')

    async def touch(self, message):
        split = shlex.split(message.content)
        if len(split) == 2:
            split = split[1].split('/')
            if len(split) == 1:
                await message.guild.get_channel(message.channel.category_id).create_text_channel(split[0])
            elif len(split) == 2:
                for i in message.guild.by_category():
                    if i[0] is None:
                        continue
                    if i[0].name == split[0]:
                        try:
                            await i[0].create_text_channel(split[1])
                            return
                        except AttributeError:
                            continue
                    else:
                        continue
                channel = await message.guild.create_category_channel(split[0])
                await channel.create_text_channel(split[1])
        else:
            await message.channel.send('Usage: touch (path/channel name)\n path would be in format '
                                       'Category/Channel name or Channel name to put in current category')

    async def echo(self, message):
        await message.channel.send(message.content[4:])


client = MyClient()
client.run(token)
