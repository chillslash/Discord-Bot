import asyncio
import datetime
import youtube_dl
from collections import OrderedDict
import math
from urllib import request
import json
import aiohttp
from bs4 import BeautifulSoup

youtube_dl_options = dict(
    noplaylist=True,
    quiet=True,
    skip_download=True,
    retries=True,
    no_warnings=True
)

soundcloud_options = dict(
    noplaylist=True,
    quiet=True,
    skip_download=True,
    retries=True,
    no_warnings=True,
    default_search='scsearch'
)

server_voice = {}
globallist = {}
total = []
blacklist = {}
vote = {}

class Music_Player:

    def __init__(self, voice=None, message=None, message_time=None, player=None, music=None, client=None, discord=None):
        self.voice = voice
        self.message = message
        self.player = player
        self.message_time = message_time
        self.music = music
        self.client = client
        self.discord = discord
        self.MusicCall = MusicCaller(self.message, self.message_time, self.client, self.discord, self.music)

    async def play_details(self, link, ext):
        try:
            if ext == 0:
                players = await self.voice.create_ytdl_player(link,before_options=' -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 1 ',ytdl_options=youtube_dl_options, after=self.playing_next)
            else:
                players = await self.voice.create_ytdl_player(link,before_options=' -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 1 ',ytdl_options=soundcloud_options, after=self.playing_next)
            if not self.client.is_voice_connected(self.message.server):
                await self.MusicCall.play_music(ext)
                raise Exception
        except youtube_dl.utils.DownloadError:
            await self.client.send_message(self.message.channel, "No songs `{}` found :O".format(self.music))
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Song not found".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
        except:
            pass
        else:
            globallist[self.message.server.id][1][players] = [self.message.author, self.message]
            if globallist[self.message.server.id][0]:
                queue = 1
            else:
                queue = 0
            queue += len(globallist[self.message.server.id][1])
            await self.client.send_message(self.message.channel,"**Added [{}]**\n\nTitle: `{}`\nUploaded by: `{}`\nDuration: `{}`".format(queue,players.title,players.uploader, self.MusicCall.format_time(str(datetime.timedelta(seconds=players.duration)), players.is_live)))
            print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server,self.message.author, self.message.id,self.message.content))

    def playing_next(self):
        try:
            self.play_next().send(None)
        except StopIteration:
            pass

    async def play_next(self):
        global blacklist
        if globallist[self.message.server.id][1]:
            if globallist[self.message.server.id][2] == 0:
                globallist[self.message.server.id][0] = []
                await self.play()
            else:
                self.message.author = globallist[self.message.server.id][0][1]
                music_input = 'ytsearch:' + str(globallist[self.message.server.id][0][2].content).replace(str(globallist[self.message.server.id][0][2].content).split(" ")[0] + ' ' + str(globallist[self.message.server.id][0][2].content).split(" ")[1], '').replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
                players = await server_voice[self.message.server.id].create_ytdl_player(music_input, ytdl_options=dict(noplaylist=True, skip_download=True, retries=True))
                globallist[self.message.server.id][1][players] = [globallist[self.message.server.id][0][1], globallist[self.message.server.id][0][2]]
                globallist[self.message.server.id][0] = []
                await self.play()
        else:
            globallist[self.message.server.id][2] = 0
            await self.voice.disconnect()
            del server_voice[self.message.server.id]
            blacklist = {}
            loop = asyncio.get_event_loop()
            loop.create_task(await self.client.send_message(self.message.channel, "Music queue finished, disconnected from voice channel"))

    async def play(self):
        vote[self.message.server.id] = [0, 0, []]
        self.player = list(globallist[self.message.server.id][1])[0]
        globallist[self.message.server.id][0] = [self.player, globallist[self.message.server.id][1][list(globallist[self.message.server.id][1])[0]][0], globallist[self.message.server.id][1][list(globallist[self.message.server.id][1])[0]][1], datetime.datetime.now().timestamp()]
        del globallist[self.message.server.id][1][list(globallist[self.message.server.id][1])[0]]
        self.player.start()

class MusicCaller:

    def __init__(self, message=None, message_time=None, client=None, discord=None, music_message=None):
        self.message = message
        self.message_time = message_time
        self.client = client
        self.discord = discord
        self.music_message = music_message

    def help(self):
        helplist = ['Music', {'play': ['.music play <song>', '.m p', 'Play a song from Youtube!'], 'playsoundcloud': ['.music playsoundcloud <song>', '.m psc', 'Play a song from Soundcloud!'], 'info': ['.music info [queue number]', '.m i', 'Find out details about the song in the queue'], 'queue': ['.music queue [page number]', '.m q', 'Find the list of songs in queue'], 'skip':['.music skip', '.m s', 'Skip the song'], 'skipsong': ['.music skipsong <queue number>', '.m ss', 'Remove a song in the queue'], 'voteskip': ['.music voteskip', '.m vs', 'Vote to skip the song'], 'movetop': ['.music movetop <queue number>', '.m mt', 'Move songs up to the top of the queue'], 'lyrics': ['.music lyrics [song]', '.m ly', 'Search up lyrics of a song/Find lyrics of a music playing']}]
        return helplist

    def format_date(self, date):
        year, month, date = date[0:4], date[4:6], date[6:]
        if month == '01': month = 'January'
        elif month == '02': month = 'February'
        elif month == '03': month = 'March'
        elif month == '04': month = 'April'
        elif month == '05': month = 'May'
        elif month == '06': month = 'June'
        elif month == '07': month = 'July'
        elif month == '08': month = 'August'
        elif month == '09': month = 'September'
        elif month == '10': month = 'October'
        elif month == '11': month = 'November'
        elif month == '12': month = 'December'
        return "{} {} {}".format(date, month, year)

    def admin(self, user_id):
        admin_id = "179824176847257600"
        if user_id == admin_id:
            return True
        return False


    def format_number(self, number):
        if number >= 1000000000:
            number = "{}B".format(round(number / 1000000000, 2))
        elif number >= 1000000:
            number = "{}M".format(round(number / 1000000, 2))
        elif number >= 1000:
            number = "{}K".format(round(number / 1000, 2))
        return number


    def format_time(self, time, live=None):
        if live and time == "0:00:00": return "Livestream"
        if time[0:2] == '0:':
            return time[2:]
        else:
            return time

    def vote_command(self, reaction, user):
        number = int(round((len(server_voice[reaction.message.server.id].channel.voice_members)-1) * 0.75, 0))
        if user.voice.voice_channel == server_voice[reaction.message.server.id].channel and user.id not in vote[user.server.id][2]:
            vote[user.server.id][1]+=1
            vote[user.server.id][2].append(user.id)
            if vote[user.server.id][1] >= number:
                return True
            else:
                loop = asyncio.get_event_loop()
                if globallist[reaction.message.server.id][0][0].is_live:
                    loop.create_task(self.client.edit_message(reaction.message, "**VoteSkip**\nClick the arrow to vote\n\nSong: `{}` [Livestream]\n\nNo. of Votes required remaining: {}".format(globallist[reaction.message.server.id][0][0].title, number-vote[user.server.id][1])))
                elif globallist[reaction.message.server.id][0][0].is_playing():
                    loop.create_task(self.client.edit_message(reaction.message, "**VoteSkip**\nClick the arrow to vote\n\nSong: `{}` [`{}`/`{}`]\n\nNo. of Votes required remaining: {}".format(globallist[reaction.message.server.id][0][0].title,self.format_time(str(datetime.timedelta(seconds=(int(round(datetime.datetime.now().timestamp() - globallist[reaction.message.server.id][0][3], 0)))))),self.format_time(str(datetime.timedelta(seconds=globallist[reaction.message.server.id][0][0].duration))), number-vote[user.server.id][1])))
                else:
                    loop.create_task(self.client.edit_message(reaction.message, "**VoteSkip**\nClick the arrow to vote\n\nSong: `{}` [`{}`/`{}`]\n\nNo. of Votes required remaining: {}".format(globallist[reaction.message.server.id][0][0].title,self.format_time(str(datetime.timedelta(seconds=(int(round(blacklist[reaction.message.server.id] - globallist[reaction.message.server.id][0][3], 0)))))),self.format_time(str(datetime.timedelta(seconds=globallist[reaction.message.server.id][0][0].duration))), number-vote[user.server.id][1])))
                return False
        else:
            if vote[user.server.id][1] >= number:
                return True
            else:
                loop = asyncio.get_event_loop()
                loop.create_task(self.client.remove_reaction(reaction.message, "▶", user))
                return False

    async def play_music(self, ext):
        await self.client.send_typing(self.message.channel)
        real_music_input = str(self.music_message).replace(str(self.music_message).split(" ")[0] + ' ' + str(self.music_message).split(" ")[1] + " ", '')
        music_input = real_music_input
        if ext == 0:
            music_input = real_music_input.replace("[", "")
            music_input = music_input.replace("]", "")
            music_input = music_input.replace("'", "")
            music_input = music_input.replace(" ", "")
        if str(self.music_message).replace(str(self.music_message).split(" ")[0] + ' ' + str(self.music_message).split(" ")[1], '') != "":
            if ext == 0:
                music_input = 'ytsearch:' + music_input
            vc = self.message.author.voice.voice_channel
            if str(vc) != 'None':
                try:
                    if self.message.server.id in server_voice or self.client.is_voice_connected(self.message.server):
                        voice = server_voice[self.message.server.id]
                        if voice.channel != vc:
                            await self.client.send_message(self.message.channel, "You are not in the same channel as the bot")
                            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User not in the same voice channel as Bot".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
                            raise ValueError
                        else:
                            music = Music_Player(voice=voice, message=self.message, message_time=self.message_time, music=real_music_input, client=self.client, discord=self.discord)
                            await music.play_details(music_input, ext)
                    else:
                        if not vc.permissions_for(self.message.server.get_member('455541339946221580')).connect:
                            await self.client.send_message(self.message.channel,"I can't join the voice channel. Song `{}` was not registered".format(real_music_input))
                            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Bot cannot join channel".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
                            raise ValueError
                        if not vc.permissions_for(self.message.server.get_member('455541339946221580')).speak:
                            await self.client.send_message(self.message.channel,"I can't speak in the voice channel. Song `{}` was not registered".format(real_music_input))
                            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Bot cannot speak in the channel".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
                            raise ValueError
                        else:
                            voice = await self.client.join_voice_channel(vc)
                            server_voice[self.message.server.id] = voice
                            vote[self.message.server.id] = [0, 0, []]
                            globallist[self.message.server.id] = [[], OrderedDict(), 0]
                            self.client.loop.create_task(self.check_voice_channel(self.message.server.id))
                            music = Music_Player(voice=voice, message=self.message, message_time=self.message_time, music=real_music_input, client=self.client, discord=self.discord)
                            await music.play_details(music_input, ext)
                            await music.play_next()
                except asyncio.TimeoutError:
                    await self.client.send_message(self.message.channel,"You're adding songs too fast. Song `{}` was not registered".format(real_music_input))
                    print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User inputted songs too fast".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
                except ValueError:
                    pass

            else:
                await self.client.send_message(self.message.channel, "You're not in a voice channel")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User not in voice channel".format(self.message_time, self.message.server, self.message.author, self.message.id,self.message.content))

        else:
            await self.client.send_message(self.message.channel, "Play something :/")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User did not input".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))

    async def check_voice_channel(self, server_id):
        while server_id in server_voice:
            if len(server_voice[server_id].channel.voice_members) == 1:
                if (server_id in blacklist and blacklist[server_id][1] == 0) or server_id not in blacklist:
                    try:
                        await self.client.send_message(globallist[server_id][0][2].channel, "No one is in the voice channel, music has been paused!\nThe queue will be cleared in 60s")
                        globallist[server_id][0][0].pause()
                        await self.check_disconnect_channel(server_id)
                    except: pass
            await asyncio.sleep(5)


    async def check_disconnect_channel(self, x):
        global blacklist
        if x in blacklist:
            blacklist[x][1] = 1
        else:
            blacklist[x] = [datetime.datetime.now().timestamp(), 1]
        for countdown in range(60):
            if x not in blacklist:
                return None
            elif len(server_voice[x].channel.voice_members) <= 1:
                pass
            else:
                globallist[x][0][3] = globallist[x][0][3] + datetime.datetime.now().timestamp() - blacklist[x][0]
                globallist[x][0][0].resume()
                del blacklist[x]
                await self.client.send_message(globallist[x][0][2].channel, "Music Resumed!")
                return None
            await asyncio.sleep(1)
        globallist[x][1] = OrderedDict()
        globallist[x][0][0].stop()
        del blacklist[x]
        await self.client.send_message(globallist[x][0][2].channel, "Music has stopped!")

    async def check_loop(self, message):
        while globallist[message.server.id][2] == 1:
            if len(server_voice[message.server.id].channel.voice_members) <= 2:
                await asyncio.sleep(1)
            else:
                globallist[message.server.id][2] = 0
                await self.client.send_message(message.channel, "Someone has joined the channel\nLoop has been turned off")
                break

    async def sorting(self):
        if "".join(str(self.message.content)).split(" ")[1] == "play" or "".join(str(self.message.content)).split(" ")[1] == "p":
            await self.play()
        elif "".join(str(self.message.content)).split(" ")[1] == "playsoundcloud" or "".join(str(self.message.content)).split(" ")[1] == "psc":
            await self.playsoundcloud()
        elif "".join(str(self.message.content)).split(" ")[1] == "info" or "".join(str(self.message.content)).split(" ")[1] == "i":
            await self.info()
        elif "".join(str(self.message.content)).split(" ")[1] == "skip" or "".join(str(self.message.content)).split(" ")[1] == "s":
            await self.skip()
        elif "".join(str(self.message.content)).split(" ")[1] == "queue" or "".join(str(self.message.content)).split(" ")[1] == "q":
            await self.queue()
        elif "".join(str(self.message.content)).split(" ")[1] == "skipsong" or "".join(str(self.message.content)).split(" ")[1] == "ss":
            await self.skipsong()
        elif "".join(str(self.message.content)).split(" ")[1] == "movetop" or "".join(str(self.message.content)).split(" ")[1] == "mt":
            await self.movetop()
        elif "".join(str(self.message.content)).split(" ")[1] == "stop" or "".join(str(self.message.content)).split(" ")[1] == "st":
            await self.stop()
        elif "".join(str(self.message.content)).split(" ")[1] == "pause":
            await self.pause()
        elif "".join(str(self.message.content)).split(" ")[1] == "resume" or "".join(str(self.message.content)).split(" ")[1] == "r":
            await self.resume()
        elif "".join(str(self.message.content)).split(" ")[1] == "voteskip" or "".join(str(self.message.content)).split(" ")[1] == "vs":
            await self.voteskip()
        elif "".join(str(self.message.content)).split(" ")[1] == "loop" or "".join(str(self.message.content)).split(" ")[1] == "l":
            await self.loop()
        elif "".join(str(self.message.content)).split(" ")[1] == "lyrics" or "".join(str(self.message.content)).split(" ")[1] == "ly":
            await self.lyrics()
        else:
            helplist = self.help()
            field = "**Alias:** .m\n\n"
            for name in helplist[1]:
                field += '**{}** - {}\n'.format(helplist[1][name][0], helplist[1][name][2])
            embed = self.discord.Embed(title='Music Commands', description=field, colour=0xe74c3c)
            embed.set_footer(text='Type .help music <command> to find out more! | < > - Required ; [ ] - Optional')
            await self.client.send_message(self.message.channel, embed=embed)
            print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))

    async def play(self):
        await self.play_music(0)

    async def playsoundcloud(self):
        await self.play_music(1)

    async def info(self):
        if self.message.server.id in server_voice and globallist[self.message.server.id][0]:
            try:
                song_number = int("".join(str(self.message.content)).split(" ")[2])
            except:
                song_number = 1
            finally:
                if len(globallist[self.message.server.id][1])+1 >= song_number and song_number > 0:
                    if song_number == 1: player = globallist[self.message.server.id][0][0]
                    else: player = list(globallist[self.message.server.id][1])[song_number-2]
                    embed = self.discord.Embed(title="{} [{}]".format(player.title, str(song_number)), colour=0xe74c3c)
                    embed.add_field(name='Requested by', value=globallist[self.message.server.id][0][1], inline=True)
                    embed.add_field(name='Uploaded by', value=player.uploader, inline=True)
                    if song_number == 1:
                        if player.is_live:
                            embed.add_field(name='Duration', value="Livestream", inline=True)
                        elif player.is_playing():
                            embed.add_field(name='Duration', value="{}/{}".format(self.format_time(str(datetime.timedelta(seconds=(int(round(datetime.datetime.now().timestamp() - globallist[self.message.server.id][0][3], 0)))))), self.format_time(str(datetime.timedelta(seconds=player.duration)))), inline=True)
                        else:
                            embed.add_field(name='Duration', value="{}/{}".format(self.format_time(str(datetime.timedelta(seconds=(int(round(blacklist[self.message.server.id][0] - globallist[self.message.server.id][0][3], 0)))))), self.format_time(str(datetime.timedelta(seconds=player.duration)))), inline=True)
                    else:
                        embed.add_field(name='Duration', value="{}".format(self.format_time(str(datetime.timedelta(seconds=player.duration)), player.is_live)), inline=True)
                    embed.add_field(name='Upload Date', value=self.format_date(player.date), inline=True)
                    if player.ext == 'youtube':
                        embed.add_field(name='Views', value=self.format_number(player.views), inline=True)
                        embed.add_field(name='Likes | Dislikes', value="{} | {}".format(self.format_number(player.likes), self.format_number(player.dislikes)), inline=True)
                    embed.add_field(name='Link', value=player.utube_url, inline=True)
                    embed.set_image(url=player.thumbnail)
                    await self.client.send_message(self.message.channel, embed=embed)
                    print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))

                else:
                    await self.client.send_message(self.message.channel, "There is no queue page number as `{}`".format(song_number))
                    print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Invalid queue number".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
        else:
            await self.client.send_message(self.message.channel, "There is no song currently playing")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: No songs currently playing".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))

    async def skip(self):
        if self.message.server.id in server_voice and globallist[self.message.server.id][0]:
            player, artist = globallist[self.message.server.id][0][0], globallist[self.message.server.id][0][1]
            if artist == self.message.author or self.admin(self.message.author.id):
                field = ""
                if globallist[self.message.server.id][1]:
                    playerr = list(globallist[self.message.server.id][1])[0]
                    field = "\nNext Song: `{}` [`{}`]".format(playerr.title, self.format_time(str(datetime.timedelta(seconds=playerr.duration))))
                try:
                    player.stop()
                except OSError:
                    pass
                await self.client.send_message(self.message.channel, "Music successfully skipped{}".format(field))
                print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server,self.message.author, self.message.id,self.message.content))
            else:
                await self.client.send_message(self.message.channel, "You weren't the one who added this song")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User did not add this song".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
        else:
            await self.client.send_message(self.message.channel, "There is no song currently playing")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: No songs currently playing".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))

    async def queue(self):
        try:
            page = int("".join(str(self.message.content)).split(" ")[2])
        except:
            page = 1
        finally:
            if self.message.server.id in server_voice and globallist[self.message.server.id][0]:
                total_page = math.ceil((len(globallist[self.message.server.id][1])+1)/10)
                if total_page == 0: total_page = 1
                if page > total_page or page <= 0:
                    await self.client.send_message(self.message.channel, "There is no queue number as `{}`".format(page))
                    print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Invalid page number".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
                else:
                    if page == total_page and page == 1:
                        queue_range = list(globallist[self.message.server.id][1].items())
                        queue_counter = 2
                    elif page == total_page:
                        queue_range = list(globallist[self.message.server.id][1].items())[(page*10)-11:]
                        queue_counter = 1
                    elif page == 1:
                        queue_range = list(globallist[self.message.server.id][1].items())[0:9]
                        queue_counter = 2
                    else:
                        queue_range = list(globallist[self.message.server.id][1].items())[(page*10)-11:(page*10)-1]
                        queue_counter = 1
                    embed = self.discord.Embed(title="**Page [{}/{}]**".format(page, total_page), colour=0xe74c3c)
                    # queue_message = "**Page [{}/{}]**\nMusic queue of `{}` songs:\n\n".format(page, total_page, 1 + len(globallist[self.message.server.id][1]))
                    if globallist[self.message.server.id][0][0].is_live:
                        embed.add_field(name="Playing now", value="**{}** added by `{}` [Livestream]".format(globallist[self.message.server.id][0][0].title, globallist[self.message.server.id][0][1]), inline=False)
                        # queue_message += "Playing now: `{}` added by `{}` [Livestream]\n\n".format(globallist[self.message.server.id][0][0].title, globallist[self.message.server.id][0][1])
                        total_time = 0
                    elif globallist[self.message.server.id][0][0].is_playing():
                        embed.add_field(name="Playing now", value="**{}** added by `{}` [{}/{}]".format(globallist[self.message.server.id][0][0].title, globallist[self.message.server.id][0][1],self.format_time(str(datetime.timedelta(seconds=(int(round(datetime.datetime.now().timestamp() - globallist[self.message.server.id][0][3], 0)))))),self.format_time(str(datetime.timedelta(seconds=globallist[self.message.server.id][0][0].duration)))), inline=False)
                        # queue_message += "Playing now: `{}` added by `{}` [{}/{}]\n\n".format(globallist[self.message.server.id][0][0].title, globallist[self.message.server.id][0][1],self.format_time(str(datetime.timedelta(seconds=(int(round(datetime.datetime.now().timestamp() - globallist[self.message.server.id][0][3], 0)))))),self.format_time(str(datetime.timedelta(seconds=globallist[self.message.server.id][0][0].duration))))
                        total_time = globallist[self.message.server.id][0][0].duration - int(round(datetime.datetime.now().timestamp() - globallist[self.message.server.id][0][3], 0))
                    else:
                        embed.add_field(name="Playing now", value="**{}** added by `{}` [{}/{}]".format(globallist[self.message.server.id][0][0].title, globallist[self.message.server.id][0][1],self.format_time(str(datetime.timedelta(seconds=(int(round(blacklist[self.message.server.id][0] - globallist[self.message.server.id][0][3], 0)))))),self.format_time(str(datetime.timedelta(seconds=globallist[self.message.server.id][0][0].duration)))), inline=False)
                        # queue_message += "Playing now: `{}` added by `{}` [{}/{}]\n\n".format(globallist[self.message.server.id][0][0].title, globallist[self.message.server.id][0][1],self.format_time(str(datetime.timedelta(seconds=(int(round(blacklist[self.message.server.id][0] - globallist[self.message.server.id][0][3], 0)))))),self.format_time(str(datetime.timedelta(seconds=globallist[self.message.server.id][0][0].duration))))
                        total_time = globallist[self.message.server.id][0][0].duration - int(round(blacklist[self.message.server.id][0] - globallist[self.message.server.id][0][3], 0))
                    queue_message = ""
                    for player, author in queue_range:
                        queue_message+="{}) **{}** added by `{}` [{}]\n".format(queue_counter + (page - 1) * 10,player.title, author[0],self.format_time(str(datetime.timedelta(seconds=player.duration)), player))
                        # queue_message += "{}) `{}` added by `{}` [{}]\n".format(queue_counter + (page - 1) * 10,player.title, author[0],self.format_time(str(datetime.timedelta(seconds=player.duration)), player))
                        queue_counter += 1
                    if queue_message:
                        embed.add_field(name='Queue', value=queue_message, inline=False)
                    for player, author in globallist[self.message.server.id][1].items():
                        total_time += player.duration
                    # queue_message += '\nTotal Time Remaining: `{}`'.format(self.format_time(str(datetime.timedelta(seconds=total_time)), True))
                    if total_page > page:
                        embed.set_footer(text="{} Songs | Total Time Remaining: {} | Type `.music queue {}` to go to the next page".format(1 + len(globallist[self.message.server.id][1]), self.format_time(str(datetime.timedelta(seconds=total_time)), True), page+1))
                        # queue_message += '\n\n| Type `.music queue {}` to go to the next page |'.format(page+1)
                    else:
                        embed.set_footer(text="{} Songs | Total Time Remaining: {}".format(1 + len(globallist[self.message.server.id][1]), self.format_time(str(datetime.timedelta(seconds=total_time)), True)))
                    await self.client.send_message(self.message.channel, embed=embed)
                    print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server,self.message.author, self.message.id,self.message.content))
            else:
                await self.client.send_message(self.message.channel, "There is no song currently playing")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: No songs currently playing".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))

    async def skipsong(self):
        try:
            song_number = int("".join(str(self.message.content)).split(" ")[2])
        except IndexError:
            await self.client.send_message(self.message.channel, "Hmm which song do I skip?")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User did not input".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
        except ValueError:
            await self.client.send_message(self.message.channel, "That's not a number")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Invalid number".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
        else:
            try:
                if song_number == 1:
                    await self.client.send_message(self.message.channel, "Use `.music skip` to skip the song that is currently playing")
                    print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User used skipsong instead of skip".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
                elif list(globallist[self.message.server.id][1].items())[song_number - 2][1][0] == self.message.author or self.admin(self.message.author.id):
                    title = list(globallist[self.message.server.id][1])[song_number - 2].title
                    del globallist[self.message.server.id][1][list(globallist[self.message.server.id][1])[song_number - 2]]
                    await self.client.send_message(self.message.channel, "Successfully skipped `{}`".format(title))
                    print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server,self.message.author, self.message.id,self.message.content))
                else:
                    await self.client.send_message(self.message.channel, "You weren't the one who added this song")
                    print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User did not add the song".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
            except IndexError:
                await self.client.send_message(self.message.channel,"There is no queue number as `{}`".format(song_number))
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Invalid queue number".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
            except KeyError:
                await self.client.send_message(self.message.channel, "There is no song currently playing!")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: No songs currently playing".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))

    async def movetop(self):
        if self.message.server.id in server_voice and globallist[self.message.server.id][0]:
            if self.message.author.voice.voice_channel == server_voice[self.message.server.id].channel:
                if self.admin(self.message.author.id) or len(server_voice[self.message.server.id].channel.voice_members) == 2:
                    try:
                        song_number = int("".join(str(self.message.content)).split(" ")[2])
                    except:
                        await self.client.send_message(self.message.channel, "Specify a queue number to move")
                        print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User did not input queue number".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
                    else:
                        if song_number == 1:
                            await self.client.send_message(self.message.channel, "Music is already playing")
                            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Song was already playing".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
                        elif song_number == 2:
                            await self.client.send_message(self.message.channel, "Bro, it's already at the top of the queue")
                            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Song was already at the top of the queue".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
                        else:
                            try:
                                player = list(globallist[self.message.server.id][1])[song_number - 2]
                                title = player.title
                            except:
                                await self.client.send_message(self.message.channel,"There is no queue number `{}`".format(song_number))
                                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Invalid queue number".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
                            else:
                                globallist[self.message.server.id][1].move_to_end(list(globallist[self.message.server.id][1].items())[song_number - 2][0], last=False)
                                await self.client.send_message(self.message.channel, "`{}` has been moved to the top of the queue".format(title))
                                print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server,self.message.author, self.message.id,self.message.content))
                else:
                    await self.client.send_message(self.message.channel, "You have to be in the voice channel by yourself")
                    print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User not alone in channel".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
            else:
                await self.client.send_message(self.message.channel, "You are not in the same channel as the bot")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User not in the same voice channel as Bot".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
        else:
            await self.client.send_message(self.message.channel, "There is no song currently playing!")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: No songs currently playing".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))

    async def stop(self):
        if self.message.server.id in server_voice and globallist[self.message.server.id][0]:
            if self.admin(self.message.author.id):
                globallist[self.message.server.id][1] = OrderedDict()
                globallist[self.message.server.id][0][0].stop()
                await self.client.send_message(self.message.channel, "Music has stopped!")
                print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
            else:
                await self.client.send_message(self.message.channel, "You don't have permissions!")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User has insufficient permissions".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
        else:
            await self.client.send_message(self.message.channel, "There is no song currently playing!")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: No songs currently playing".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))

    async def pause(self):
        if self.message.server.id in server_voice and globallist[self.message.server.id][0]:
            if self.admin(self.message.author.id):
                if globallist[self.message.server.id][0][0].is_playing():
                    globallist[self.message.server.id][0][0].pause()
                    if self.message.server.id not in blacklist:
                        blacklist[self.message.server.id] = [datetime.datetime.now().timestamp(), 0]
                    await self.client.send_message(self.message.channel, "Music is paused!")
                    print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
                else:
                    await self.client.send_message(self.message.channel, "Music is already paused!")
                    print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Music already paused".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
            else:
                await self.client.send_message(self.message.channel, "You don't have permissions!")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User has insufficient permissions".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
        else:
            await self.client.send_message(self.message.channel, "There is no song currently playing!")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: No songs currently playing".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))

    async def resume(self):
        if self.message.server.id in server_voice and globallist[self.message.server.id][0]:
            if self.admin(self.message.author.id):
                if not globallist[self.message.server.id][0][0].is_playing():
                    globallist[self.message.server.id][0][0].resume()
                    globallist[self.message.server.id][0][3] = globallist[self.message.server.id][0][3] + datetime.datetime.now().timestamp() - blacklist[self.message.server.id][0]
                    del blacklist[self.message.server.id]
                    await self.client.send_message(self.message.channel, "Music resumed!")
                    print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
                else:
                    await self.client.send_message(self.message.channel, "Music is already playing!")
                    print("[{}] [{}] [Failure] {} ({}) executed {}\nReason: Music already paused".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
            else:
                await self.client.send_message(self.message.channel, "You don't have permissions!")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User has insufficient permissions".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
        else:
            await self.client.send_message(self.message.channel, "There is no song currently playing!")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: No songs currently playing".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))

    async def voteskip(self):
        if self.message.channel.permissions_for(self.discord.utils.get(self.message.server.members, id='455541339946221580')).add_reactions and self.message.channel.permissions_for(self.discord.utils.get(self.message.server.members, id='455541339946221580')).manage_messages:
            if self.message.server.id in server_voice and globallist[self.message.server.id][0]:
                if self.message.author.voice.voice_channel == server_voice[self.message.server.id].channel:
                    if vote[self.message.server.id][0] == 0:
                        vote[self.message.server.id][0] = 1
                        number = int(round((len(server_voice[self.message.server.id].channel.voice_members)-1) * 0.75, 0))
                        vote[self.message.server.id][1] = -1
                        if globallist[self.message.server.id][0][0].is_live:
                            msg = await self.client.send_message(self.message.channel, "**VoteSkip**\nClick the arrow to vote\n\nSong: `{}` [Livestream]\n\nNo. of Votes required remaining: {}".format(globallist[self.message.server.id][0][0].title,self.format_time(str(datetime.timedelta(seconds=(int(round(datetime.datetime.now().timestamp() - globallist[self.message.server.id][0][3], 0)))))), number))
                        elif globallist[self.message.server.id][0][0].is_playing():
                            msg = await self.client.send_message(self.message.channel, "**VoteSkip**\nClick the arrow to vote\n\nSong: `{}` [`{}`/`{}`]\n\nNo. of Votes required remaining: {}".format(globallist[self.message.server.id][0][0].title,self.format_time(str(datetime.timedelta(seconds=(int(round(datetime.datetime.now().timestamp() - globallist[self.message.server.id][0][3], 0)))))),self.format_time(str(datetime.timedelta(seconds=globallist[self.message.server.id][0][0].duration))), number))
                        else:
                            msg = await self.client.send_message(self.message.channel, "**VoteSkip**\nClick the arrow to vote\n\nSong: `{}` [`{}`/`{}`]\n\nNo. of Votes required remaining: {}".format(globallist[self.message.server.id][0][0].title,self.format_time(str(datetime.timedelta(seconds=(int(round(blacklist[self.message.server.id][0] - globallist[self.message.server.id][0][3], 0)))))),self.format_time(str(datetime.timedelta(seconds=globallist[self.message.server.id][0][0].duration))), number))
                        await self.client.add_reaction(msg, "▶")
                        await self.client.wait_for_reaction('▶', message=msg, check=self.vote_command)
                        await self.client.edit_message(msg, "Votes has reached the required quota, skipping song...")
                        await self.client.clear_reactions(msg)
                        vote[self.message.server.id] = [0, 0, []]
                        globallist[self.message.server.id][0][0].stop()
                        print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author, self.message.id,self.message.content))
                    else:
                        await self.client.send_message(self.message.channel, "There is already an ongoing vote!")
                        print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Vote is ongoing already".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))

                else:
                    await self.client.send_message(self.message.channel, "You are not in the same channel as the bot")
                    print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User not in the same voice channel as Bot".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
            else:
                await self.client.send_message(self.message.channel, "There is no song currently playing!")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: No songs currently playing".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
        else:
            await self.client.send_message(self.message.channel, 'I need to have `Add Reactions` and `Manage Messages` Permissions')
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Bot has insuffficient permission".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))

    async def loop(self):
        if self.message.server.id in server_voice and globallist[self.message.server.id][0] and self.admin(self.message.author.id):
            if self.message.author.voice.voice_channel == server_voice[self.message.server.id].channel:
                if len(server_voice[self.message.server.id].channel.voice_members) == 2:
                    if globallist[self.message.server.id][2] == 0:
                        globallist[self.message.server.id][2] = 1
                        await self.client.send_message(self.message.channel, "Loop has been turned on")
                        await self.check_loop(self.message)
                    else:
                        globallist[self.message.server.id][2] = 0
                        await self.client.send_message(self.message.channel, "Loop has been turned off")
                    print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
                else:
                    await self.client.send_message(self.message.channel, "You have to be in the voice channel by yourself")
                    print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User not alone in channel".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
            else:
                await self.client.send_message(self.message.channel, "You are not in the same channel as the bot")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User not in the same voice channel as Bot".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
        else:
            await self.client.send_message(self.message.channel, "This command is in progress")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Command in progress".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))

    async def lyrics(self):
        if self.message.content.replace(" ".join(self.message.content.split(" ")[0:2]), "") == '' and self.message.server.id not in server_voice:
            await self.client.send_message(self.message.channel, "Enter a song to search")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User did not input".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
        else:
            await self.client.send_typing(self.message.channel)
            if self.message.content.replace(" ".join(self.message.content.split(" ")[0:2]), "") != '':
                lyrics_search = self.message.content.replace(" ".join(self.message.content.split(" ")[0:2])+' ', "")
            else:
                if globallist[self.message.server.id][0][0].music:
                    lyrics_search = globallist[self.message.server.id][0][0].music
                else: lyrics_search = globallist[self.message.server.id][0][0].title
            try:
                headers = {"Authorization": "Bearer rBCS0HmU8eMV1elHOqErx8TZhIdjxtAAwESw5JzQuu4o3nUZ5H1vPTb-S-ndu4nI","User-Agent": ""}
                async with aiohttp.ClientSession(headers=headers) as session:
                    async with session.get('https://api.genius.com/search?q={}'.format(request.quote(lyrics_search))) as r:
                        js = await r.json()
                async with aiohttp.ClientSession() as session:
                    async with session.get(js.get('response').get('hits')[0].get('result').get('url')) as r:
                        jss = await r.text()
                html = BeautifulSoup(jss, "html.parser")
                lyrics = html.find("div", class_="lyrics").get_text()
                album = html.find("script", attrs={'type': 'application/ld+json'})
                if album and json.loads(album.get_text()).get('inAlbum'): album = json.loads(album.get_text()).get('inAlbum')[0].get('name')
                else: album = None
                date = html.find_all("div", attrs={'class', 'metadata_unit metadata_unit--table_row'})
                if date:
                    for x in date:
                        if 'Release Date' in x.get_text():
                            date = x.get_text().split("\n")[2]
                            break
                    else: date = None
                else: date = None
                song = js.get('response').get('hits')[0].get('result').get('title')
                artist = js.get('response').get('hits')[0].get('result').get('primary_artist').get('name')
                url = js.get('response').get('hits')[0].get('result').get('url')
                icon = js.get('response').get('hits')[0].get('result').get('header_image_url')
            except:
                await self.client.send_message(self.message.channel, "No song found")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Song not found".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
            else:
                total_length_lyrics = len(str(song)) + len(str(artist)) + len(str(lyrics)) + len(str(url))
                number_of_page = int(math.ceil(((total_length_lyrics - 1986) / 1990) + 1))
                if number_of_page > 5:
                    await self.client.send_message(self.message.channel, "The lyrics is too long, but here's the link\n{}".format(url))
                    print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Lyrics too long".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
                else:
                    starting_number = 0
                    extra_lyrics = ""
                    lyrics_format_counter = 0
                    for page_number in range(1, number_of_page):
                        if lyrics_format_counter == 0:
                            cut_off = 2000 - len(extra_lyrics) - len(song) - len(artist) - 10
                        else:
                            cut_off = starting_number + 2000 - len(extra_lyrics)
                        new_lyrics = extra_lyrics + str(lyrics)[starting_number:cut_off]
                        starting_number = cut_off
                        lyrics_counter = 1
                        while True:
                            if new_lyrics[-lyrics_counter] == "\n":
                                break
                            else:
                                lyrics_counter += 1
                        extra_lyrics = new_lyrics[:-lyrics_counter:-1][::-1]
                        new_lyrics = new_lyrics[:-lyrics_counter]
                        if lyrics_format_counter == 0:
                            embed = self.discord.Embed(title="Lyrics", description=str(new_lyrics), color=0xe74c3c, url=url)
                            embed.set_author(name="{} by {}".format(song, artist))
                            lyrics_format_counter = 1
                        else:
                            embed = self.discord.Embed(description=str(new_lyrics), color=0xe74c3c)
                        if page_number == 1:
                            embed.set_thumbnail(url=icon)
                        await self.client.send_message(self.message.channel, embed=embed)
                    new_lyrics = extra_lyrics + str(lyrics)[starting_number:]
                    if lyrics_format_counter == 0:
                        embed = self.discord.Embed(title="Lyrics", description=str(new_lyrics), color=0xe74c3c, url=url)
                        embed.set_thumbnail(url=icon)
                        embed.set_author(name="{} by {}".format(song, artist))
                    else:
                        embed = self.discord.Embed(description=str(new_lyrics), color=0xe74c3c)
                    if album: embed.add_field(name="Album", value=album, inline=True)
                    if date: embed.add_field(name="Released Date", value=date, inline=True)
                    embed.set_footer(text="Genius.com")
                    await self.client.send_message(self.message.channel, embed=embed)
                    print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))

