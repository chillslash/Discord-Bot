import discord
import asyncio
import os
import datetime
import Anime
import General
import Music
import Server
import Daily

user = discord.User()
client = discord.Client()
sd = None

@client.event
@asyncio.coroutine
def on_ready():
    yield from client.change_presence(game=discord.Game(name="Anime OP | .help", type=2))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



@client.event
async def on_message(message):
    if message.server != None:
        music_message = message.content
        message_date = "{}".format(str(datetime.datetime.now()).split(" ")[0])
        message_time = "{}{}:{}{}:{}{}".format(str(datetime.datetime.now()).split(" ")[1][0],str(datetime.datetime.now()).split(" ")[1][1], str(datetime.datetime.now()).split(" ")[1][3],str(datetime.datetime.now()).split(" ")[1][4],str(datetime.datetime.now()).split(" ")[1][6],str(datetime.datetime.now()).split(" ")[1][7])

        file_path = "D:/Documents/Discord/"

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        server_file_path = file_path + "Servers/" + str(message.server) + " ([" + str(message.server.id) + "])"
        channel_file_path = server_file_path + '/' + str(message.channel)
        for server_file in os.listdir(file_path + "Servers/"):
            if message.server.id in server_file:
                if file_path + "Servers/" + server_file != server_file_path:
                    os.rename(file_path + "Servers/" + server_file, server_file_path)
                break

        if not os.path.exists(channel_file_path):
            os.makedirs(channel_file_path)

        file_content = "\n({}) ({}): <{}> ({}): {}".format(message_time, message.id, message.author.id, message.author, message.content)

        try:
            with open(channel_file_path + "/" + message_date + ".txt", 'a', encoding='utf8') as MyFile:
                MyFile.write(file_content)
        except:
            print("[{}] [{}] [FAILURE] {} ({}) '{}' has failed to log".format(message_time, message.server, message.author,message.id, message.content))

        if message.content.startswith(".") and message.channel.permissions_for(discord.utils.get(message.server.members, id='455541339946221580')).send_messages:

            message.content = message.content.lower()

            if message.content == ".help" or message.content == ".commands":
                embed = discord.Embed(colour=0xe74c3c)
                embed.set_author(name="Command List")
                lists = [General.GeneralCaller().help(), Server.ServerCaller().help(), Anime.AnimeCaller().help(), Music.MusicCaller().help()]
                for helplist in lists:
                    field = ""
                    for name in helplist[1]:
                        field += '**{}** - {}\n'.format(helplist[1][name][0], helplist[1][name][2])
                    field+='\u200b'
                    embed.add_field(name='{} Commands'.format(helplist[0]), value=field)
                embed.set_footer(text='Type `.help <command>` to find out more! | < > - Required ; [ ] - Optional')
                await client.send_message(message.channel, embed=embed)
                print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(message_time, message.server, message.author,message.id, message.content))

            elif message.content.startswith('.help '):
                args = message.content.replace('.help ', '')
                if len(args.split(' ')) == 2:
                    if args.split(' ')[0] == 'music':
                        helplist = Music.MusicCaller().help()[1]
                        if args.split(' ')[1] in helplist:
                            embed = discord.Embed(title='Command - [{}]'.format(args.split(' ')[1]), description=helplist[args.split(' ')[1]][2], colour=0xe74c3c)
                            embed.add_field(name='Format', value=helplist[args.split(' ')[1]][0])
                            embed.add_field(name='Alias', value=helplist[args.split(' ')[1]][1])
                            await client.send_message(message.channel, embed=embed)
                            print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(message_time, message.server, message.author,message.id, message.content))
                        else:
                            await client.send_message(message.channel, "Unknown Command. Type `.help` to find the list of commands")
                            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Unknown Command".format(message_time,message.server,message.author,message.id,message.content))

                    elif args.split(' ')[0] == 'anime':
                        helplist = Anime.AnimeCaller().help()[1]
                        if args.split(' ')[1] in helplist:
                            embed = discord.Embed(title='Command - [{}]'.format(args.split(' ')[1]), description=helplist[args.split(' ')[1]][2], colour=0xe74c3c)
                            embed.add_field(name='Format', value=helplist[args.split(' ')[1]][0])
                            embed.add_field(name='Alias', value=helplist[args.split(' ')[1]][1])
                            await client.send_message(message.channel, embed=embed)
                            print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(message_time, message.server, message.author,message.id, message.content))
                        else:
                            await client.send_message(message.channel, "Unknown Command. Type `.help` to find the list of commands")
                            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Unknown Command".format(message_time,message.server,message.author,message.id,message.content))
                    else:
                        await client.send_message(message.channel, "Unknown Command. Type `.help` to find the list of commands")
                        print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Unknown Command".format(message_time,message.server,message.author,message.id,message.content))

                elif len(args.split(' ')) == 1:
                    if args in General.GeneralCaller().help()[1]:
                        helplist = General.GeneralCaller().help()[1]
                        embed = discord.Embed(title='Command - [{}]'.format(args), description=helplist[args][2], colour=0xe74c3c)
                        embed.add_field(name='Format', value=helplist[args][0])
                        await client.send_message(message.channel, embed=embed)
                        print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(message_time, message.server, message.author,message.id, message.content))

                    elif args in Server.ServerCaller().help()[1]:
                        helplist = Server.ServerCaller().help()[1]
                        embed = discord.Embed(title='Command - [{}]'.format(args), description=helplist[args][2], colour=0xe74c3c)
                        embed.add_field(name='Format', value=helplist[args][0])
                        await client.send_message(message.channel, embed=embed)
                        print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(message_time, message.server, message.author,message.id, message.content))

                    elif args == 'anime':
                        helplist = Anime.AnimeCaller().help()
                        field = "**Alias:** .a\n\n"
                        for name in helplist[1]:
                            field += '**{}** - {}\n'.format(helplist[1][name][0], helplist[1][name][2])
                        embed = discord.Embed(title='Anime Commands', description=field, colour=0xe74c3c)
                        embed.set_footer(text='Type .help anime <command> to find out more! | < > - Required ; [ ] - Optional')
                        await client.send_message(message.channel, embed=embed)
                        print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(message_time, message.server, message.author,message.id, message.content))

                    elif args == 'music':
                        helplist = Music.MusicCaller().help()
                        field = "**Alias:** .m\n\n"
                        for name in helplist[1]:
                            field += '**{}** - {}\n'.format(helplist[1][name][0], helplist[1][name][2])
                        embed = discord.Embed(title='Music Commands', description=field, colour=0xe74c3c)
                        embed.set_footer(text='Type .help music <command> to find out more! | < > - Required ; [ ] - Optional')
                        await client.send_message(message.channel, embed=embed)
                        print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(message_time, message.server, message.author,message.id, message.content))

                    elif args == 'server':
                        helplist = Server.ServerCaller().help()
                        field = ""
                        for name in helplist[1]:
                            field += '**{}** - {}\n'.format(helplist[1][name][0], helplist[1][name][2])
                        embed = discord.Embed(title='Server Commands', description=field, colour=0xe74c3c)
                        embed.set_footer(text='Type .help <command> to find out more! | < > - Required ; [ ] - Optional')
                        await client.send_message(message.channel, embed=embed)
                        print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(message_time, message.server, message.author,message.id, message.content))

                    elif args == 'general':
                        helplist = General.GeneralCaller().help()
                        field = ""
                        for name in helplist[1]:
                            field += '**{}** - {}\n'.format(helplist[1][name][0], helplist[1][name][2])
                        embed = discord.Embed(title='General Commands', description=field, colour=0xe74c3c)
                        embed.set_footer(text='Type .help <command> to find out more! | < > - Required ; [ ] - Optional')
                        await client.send_message(message.channel, embed=embed)
                        print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(message_time, message.server, message.author,message.id, message.content))

                    elif args == 'help':
                        embed = discord.Embed(title='Command - [help]', colour=0xe74c3c, description='Hmm I think, just maybe, it opens the help list :thinking:')
                        embed.add_field(name='Format', value='.help')
                        await client.send_message(message.channel, embed=embed)
                        print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(message_time, message.server, message.author,message.id, message.content))


                    else:
                        await client.send_message(message.channel, "Unknown Command. Type `.help` to find the list of commands")
                        print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Unknown Command".format(message_time,message.server,message.author,message.id,message.content))
                else:
                    await client.send_message(message.channel, "Unknown Command. Type `.help` to find the list of commands")
                    print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Unknown Command".format(message_time,message.server,message.author,message.id,message.content))



            elif message.content.startswith(".m ") or message.content.startswith(".music "):
                MusicCall = Music.MusicCaller(message, message_time, client, discord, music_message)
                await MusicCall.sorting()

            elif message.content == ".m" or message.content == ".music":
                helplist = Music.MusicCaller().help()
                field = "**Alias:** .m\n\n"
                for name in helplist[1]:
                    field += '**{}** - {}\n'.format(helplist[1][name][0], helplist[1][name][2])
                embed = discord.Embed(title='Music Commands', description=field, colour=0xe74c3c)
                embed.set_footer(text='Type .help music <command> to find out more! | < > - Required ; [ ] - Optional')
                await client.send_message(message.channel, embed=embed)
                print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(message_time, message.server, message.author,message.id, message.content))

            elif message.content.startswith('.anime ') or message.content.startswith('.a '):
                AnimeCall = Anime.AnimeCaller(message, message_time, client, discord)
                await AnimeCall.sorting()

            elif message.content == '.a' or message.content == '.anime':
                helplist = Anime.AnimeCaller().help()
                field = "**Alias:** .a\n\n"
                for name in helplist[1]:
                    field += '**{}** - {}\n'.format(helplist[1][name][0], helplist[1][name][2])
                embed = discord.Embed(title='Anime Commands', description=field, colour=0xe74c3c)
                embed.set_footer(text='Type .help anime <command> to find out more! | < > - Required ; [ ] - Optional')
                await client.send_message(message.channel, embed=embed)
                print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(message_time, message.server, message.author,message.id, message.content))

            elif message.content == '.hello':
                await client.send_message(message.channel, "boi")

            else:
                GeneralCall = General.GeneralCaller(message, message_time, client, discord)
                await GeneralCall.sorting()


@client.event
async def on_server_join(server):
    print("Joined {}".format(server))
    channel = None
    for channels in list(server.channels):
        if str(channels) == 'general':
            channel = channels
            await client.send_message(channels, "Hello! I'm Danki's Bot, type `.help` for more commands :fire:")
            break
    if channel == None:
        for channels in list(server.channels):
            try:
                await client.send_message(channels, "Hello! I'm Danki's Bot, type `.help` for more commands :fire:")
                break
            except:
                pass

client.run("")
