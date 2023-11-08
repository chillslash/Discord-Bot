import random
import sys
import aiohttp
import Server

class GeneralCaller:

    numbers = {0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}

    def __init__(self, message=None, message_time=None, client=None, discord=None):
        self.message = message
        self.message_time = message_time
        self.client = client
        self.discord = discord

    def help(self):
        helplist = ['General', {'info': ['.info', '', 'Information about this Bot!'], 'ttb': ['.ttb <message>', '', 'Turns your message to blocks'], 'ss': ['.ss <message>', '', 'Turns your message into some numbers'], 'mock': ['.mock <message>', '', 'Turn your message into a mock'], '8ball': ['.8ball <question>', '', 'Answers your question'], 'joke': ['.joke', '', 'Make yourself laugh!'], 'lovecalc': ['.lovecalc <first name> | <second name>', '', 'Calculate chance of two people!'], 'quote': ['.quote', '', 'Listen to a quote or two'], 'choose': ['.choose <choice> | <choice> [...]', '', 'Let me make a decision for you!']}]
        return helplist

    def count_lines(self):
        length = 0
        the_files = ["DiscordBot.py", "Music.py", "Anime.py", "General.py", "Server.py", "Daily.py"]
        for a_file in the_files:
            with open(a_file, encoding='utf-8') as MyFile:
                length+=len(MyFile.readlines())
        return length

    def admin(self, user_id):
        admin_id = "179824176847257600"
        if user_id == admin_id:
            return True
        return False

    async def sorting(self):
        if self.message.content == ".info":
            await self.info()
        elif self.message.content.split(" ")[0] == ".ss" and self.message.author.id != "455541339946221580":
            await self.ss()
        elif self.message.content.split(" ")[0] == ".mock":
            await self.mock()
        elif self.message.content.split(" ")[0] == ".ttb":
            await self.ttb()
        elif self.message.content.startswith(".8ball"):
            await self.eightball()
        elif self.message.content == '.shutdown' or self.message.content == '.sd':
            await self.shutdown()
        elif self.message.content == '.joke':
            await self.joke()
        elif self.message.content.split(" ")[0] == '.lovecalc':
            await self.lovecalc()
        elif self.message.content == '.quote':
            await self.quote()
        elif self.message.content.startswith('.choose'):
            await self.choose()
        else:
            ServerCall = Server.ServerCaller(self.message, self.message_time, self.client, self.discord)
            await ServerCall.sorting()

    async def info(self):
        embed = self.discord.Embed(title="Danki's Bot", colour=0xe74c3c, description='best bot ull ever find ;)')
        embed.add_field(name='Creator', value='Nah#1323')
        embed.add_field(name='Date Born', value='19 ‎August ‎2017, ‏‎11:03PM')
        embed.add_field(name='Number of Servers in', value=len(self.client.servers))
        embed.add_field(name='Number of Lines of Code', value=self.count_lines())
        embed.add_field(name='Link to add to Server', value='http://bit.ly/2Q8hhFi')
        embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/455541339946221580/f194a71678db9e9ca6a2c862f88ab8f3.jpg")
        await self.client.send_message(self.message.channel, embed=embed)
        print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
        
    async def ss(self):
        if self.message.content != ".ss":
            msg = ("".join(self.message.content)).replace(self.message.content.split(" ")[0] + " ", "")
            msg = str(msg).lower()
            msg = msg.replace("a", "4")
            msg = msg.replace("e", "3")
            msg = msg.replace("i", "!")
            msg = msg.replace("l", "1")
            msg = msg.replace("o", "0")
            try:
                await self.client.send_message(self.message.channel, msg)
                print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
    
            except self.discord.errors.HTTPException:
                await self.client.send_message(self.message.channel, "Error: Too many words\nNumber of Letters: {}".format(len(msg)))
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Message too long (Length = {})".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content, len(msg)))
        else:
            await self.client.send_message(self.message.channel, "Hmm, what do I translate :thinking:")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User did not input".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))

    async def mock(self):
        if self.message.content != ".mock":
            msg = self.message.content.lower().split(" ")[1:]
            for word in range(len(msg)):
                starting = 1
                while len(msg[word]) >= starting+1:
                    msg[word] = msg[word].replace(msg[word][starting], msg[word][starting].upper())
                    starting+=2
            await self.client.send_message(self.message.channel, " ".join(msg))
            print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
        else:
            await self.client.send_message(self.message.channel, "Type something to mock")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User did not input".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))

    async def ttb(self):
        if self.message.content != ".ttb":
            msg = self.message.content.replace(".ttb ", "")
            x = ""
            for w in msg:
                if w == " ":
                    x += "   "
                elif w.isdigit():
                    x += ":{}: ".format(self.numbers.get(int(w)))
                elif ord(w) >= 97 and ord(w) <= 122:
                    x += ":regional_indicator_{}: ".format(w)
                else:
                    x = x + w + " "
            if not len(msg) > 50:
                await self.client.send_message(self.message.channel, x)
                print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))

            else:
                await self.client.send_message(self.message.channel,"Error: Text has to be 50 or less letters long\nNumber of Letters: {}".format(len(msg)))
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Message too long (Length = {})".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content, len(msg)))
        else:
            await self.client.send_message(self.message.channel,"Hmm I can't change nothing into blocks. How bout you try entering some words?")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User did not input".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))


    async def eightball(self):
        if self.message.content != ".8ball":
            eightball_number = random.randrange(1, 3)
            if eightball_number == 1:
                eightball_result = "No"
            else:
                eightball_result = "Yes"
            await self.client.send_message(self.message.channel, eightball_result)
            print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
        else:
            await self.client.send_message(self.message.channel, "Well what are you waiting for? Ask something")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User did not input".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))

    async def shutdown(self):
        if self.admin(self.message.author.id):
            await self.client.send_message(self.message.channel, "Bye!")
            for x in self.client.voice_clients:
                if (x.server == self.message.server):
                    await x.disconnect()
                    break
            print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
            self.client.logout()
            sys.exit(1)
        else:
            await self.client.send_message(self.message.channel, "You don't have permissions!")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User has insuffficient permission".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))

    async def joke(self):
        if self.message.channel.permissions_for(self.discord.utils.get(self.message.server.members, id='455541339946221580')).add_reactions and self.message.channel.permissions_for(self.discord.utils.get(self.message.server.members, id='455541339946221580')).manage_messages:
            joke_list = open('D:/Documents/Discord/joke.txt', 'r').read().split("\n")
            joke = joke_list[random.randrange(0, 54)].split(" | ")
            msg = await self.client.send_message(self.message.channel, "**{}**\n\n*Click on the arrow to reveal answer*".format(joke[0]))
            await self.client.add_reaction(msg, "▶")
            await self.client.wait_for_reaction('▶', message=msg, user=self.message.author)
            await self.client.edit_message(msg, "**{}**\n\n{} :laughing:".format(joke[0], joke[1]))
            await self.client.clear_reactions(msg)
            print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
        else:
            await self.client.send_message(self.message.channel, 'I need to have `Add Reactions` and `Manage Messages` Permissions')
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Bot has insuffficient permission".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))

    async def lovecalc(self):
        if self.message.content.startswith('.lovecalc '):
            if " | " in self.message.content:
                msg = self.message.content.replace(self.message.content.split(" ")[0] + " ", '').split(" | ")
                if len(msg) == 2:
                    if '|' not in "".join(msg):
                        name_one = msg[0]
                        name_two = msg[1]
                        lovecalc = open("D:/Documents/Discord/lovecalc.txt", 'r').read()
                        for line in lovecalc.split("\n"):
                            if name_one + " | " + name_two == line.split(" % ")[0]:
                                percentage = int(line.split(" % ")[1])
                                break
                        else:
                            percentage = random.randrange(1, 101)
                            with open("D:/Documents/Discord/lovecalc.txt", 'a') as MyFile:
                                MyFile.write("{} | {} % {}\n".format(name_one, name_two, percentage))
                        if percentage <= 25:
                            quote = "May be better next time"
                        elif 25 < percentage <= 50:
                            quote = "Can choose someone better"
                        elif 50 < percentage <= 75:
                            quote = "All the best!"
                        elif 75 < percentage < 100:
                            quote = "Congratulations! Good choice"
                        else:
                            quote = "Perfect Match!"
                        await self.client.send_message(self.message.channel, "Percentage: `{}%`\n\n{}".format(percentage, quote))
                        print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
                    else:
                        await self.client.send_message(self.message.channel, "Invalid Format. Format: `.lovecalc <first name> | <second name>`")
                        print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Invalid format".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
                else:
                    await self.client.send_message(self.message.channel, "You can't give me more than 2 names. Format: `.lovecalc <first name> | <second name>`")
                    print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Invalid format".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
            else:
                await self.client.send_message(self.message.channel, "Invalid Format. Format: `.lovecalc <first name> | <second name>`")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Invalid format".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
        else:
            await self.client.send_message(self.message.channel, "Try again, this time with names. Format: `.lovecalc <first name> | <second name>`")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Invalid format".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))



    async def quote(self):
        await self.client.send_typing(self.message.channel)
        headers = {"X-Mashape-Key": "DYfZxFhER9mshuwEiyr12xauCGqPp1RFVttjsnLjNh6EFj7cUH","Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get('https://andruxnet-random-famous-quotes.p.mashape.com/?cat=famous') as r:
                js = await r.json()
        await self.client.send_message(self.message.channel,"**{}**\n~ {}".format(js[0].get('quote'), js[0].get('author')))
        print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))

    async def choose(self):
        if self.message.content.startswith('.choose '):
            if " | " in self.message.content:
                msg = self.message.content.replace(self.message.content.split(" ")[0] + " ", '').split(" | ")
                if '|' not in "".join(msg):
                    await self.client.send_message(self.message.channel, "`{}` seems like a good choice".format(msg[random.randrange(0, len(msg))]))
                    print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
                else:
                    await self.client.send_message(self.message.channel, "Invalid format")
                    print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Invalid format".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
            else:
                await self.client.send_message(self.message.channel, "If ya only got one option, then go with that!")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User did not input 2 choices".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
        else:
            await self.client.send_message(self.message.channel, "What do I choose?")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User did not input".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))

        # if message.content.split(" ")[0] == ".w" or message.content.split(" ")[0] == ".weather":
        #     await client.send_typing(message.channel)
        #     if message.content != ".w" and message.content != ".weather":
        #         await client.send(message.channel, "This command is in progress")
        #         print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Command in progress".format(message_time,message.server,message.author,message.id,message.content))
            #     msg = (("".join(message.content)).replace(message.content.split(" ")[0] + " ", "")).replace(" ", "%20")
            #     try:
            #         async with aiohttp.ClientSession() as session:
            #             async with session.get('https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(msg)) as rr:
            #                 rs = await rr.json()
            #         while rs.get("status") == "OVER_QUERY_LIMIT":
            #             async with aiohttp.ClientSession() as session:
            #                 async with session.get(
            #                         'https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(msg)) as rr:
            #                     rs = await rr.json()
            #         if rs.get("status") == "ZERO_RESULTS":
            #             raise Exception
            #         latitude = rs.get("results")[0].get("geometry").get("location").get("lat")
            #         longitude = rs.get("results")[0].get("geometry").get("location").get("lng")
            #         async with aiohttp.ClientSession() as session:
            #             async with session.get(
            #                     'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&APPID=2c800a2c22a77d2bb437cafda1b1eb4b'.format(
            #                             latitude, longitude)) as rr:
            #                 r = await rr.json()
            #         if r.get('message') == 'city not found':
            #             raise Exception
            #     except:
            #         await client.send_message(message.channel, "City not Found")
            #         print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: City not found".format(message_time,message.server,message.author,message.id,message.content))
            #
            #     else:
            #         while True:
            #             try:
            #                 weather = ((r.get('weather')[0]).get('description')).capitalize()
            #                 temperature = (r.get('main')).get('temp')
            #                 temperature1 = int(temperature) - 273.15
            #                 temperature1 = round(temperature1, 2)
            #                 temperature2 = int(temperature) * 9 / 5 - 459.67
            #                 temperature2 = round(temperature2, 2)
            #                 humidity = r.get('main').get('humidity')
            #                 cloud = r.get('clouds').get('all')
            #                 windspeed = r.get('wind').get('speed')
            #                 windspeed = (int(windspeed) * 60 * 60) / 1000
            #                 winddir = r.get('wind').get('deg')
            #                 rainv = r.get('rain')
            #                 snowv = r.get('snow')
            #                 try:
            #                     if winddir > 337.5 or winddir <= 22.5:
            #                         windir = "North"
            #                     elif winddir > 22.5 and winddir <= 67.5:
            #                         windir = "North East"
            #                     elif winddir > 67.5 and winddir <= 112.5:
            #                         windir = "East"
            #                     elif winddir > 112.5 and winddir <= 157.5:
            #                         windir = "South East"
            #                     elif winddir > 157.5 and winddir <= 202.5:
            #                         windir = "South"
            #                     elif winddir > 202.5 and winddir <= 247.5:
            #                         windir = "South West"
            #                     elif winddir > 247.5 and winddir <= 292.5:
            #                         windir = "West"
            #                     elif winddir > 292.5 and winddir <= 337.5:
            #                         windir = "North West"
            #                     winddir = round(winddir, 1)
            #                 except:
            #                     windir = "Unavailable"
            #                 pressure = r.get('main').get('pressure')
            #                 thattime = str(datetime.datetime.fromtimestamp(r.get('dt')))[11:19]
            #                 nowtime = str(datetime.datetime.now())[11:19]
            #                 if int(thattime[0:2]) > int(nowtime[0:2]):
            #                     hr = (int(nowtime[0:2]) + 24) - int(thattime[0:2])
            #                 else:
            #                     hr = int(nowtime[0:2]) - int(thattime[0:2])
            #                 if int(thattime[3:5]) > int(nowtime[3:5]):
            #                     min = (int(nowtime[3:5]) + 60) - int(thattime[3:5])
            #                     hr -= 1
            #                 else:
            #                     min = int(nowtime[3:5]) - int(thattime[3:5])
            #                 if int(thattime[6:8]) > int(nowtime[6:8]):
            #                     sec = (int(nowtime[6:8]) + 60) - int(thattime[6:8])
            #                     min -= 1
            #                 else:
            #                     sec = int(nowtime[6:8]) - int(thattime[6:8])
            #                 if hr == 0:
            #                     if min == 0:
            #                         if sec == 0:
            #                             updatetime = "now"
            #                         else:
            #                             updatetime = "{} seconds ago".format(sec)
            #                     else:
            #                         if sec == 0:
            #                             updatetime = "{} minutes ago".format(min)
            #                         else:
            #                             updatetime = "{} minutes and {} seconds ago".format(min, sec)
            #                 else:
            #                     if min == 0:
            #                         if sec == 0:
            #                             updatetime = "{} hours ago".format(hr)
            #                         else:
            #                             updatetime = "{} hours and {} seconds ago".format(hr, sec)
            #                     else:
            #                         if sec == 0:
            #                             updatetime = "{} hours and {} minutes ago".format(hr, min)
            #                         else:
            #                             updatetime = "{} hours, {} minutes and {} seconds ago".format(hr, min, sec)
            #                 loca = (rs.get("results")[0]).get('formatted_address')
            #                 for i in (rs.get("results")[0]).get('address_components'):
            #                     if 'country' in i.get('types'):
            #                         flag = ":flag_{}:".format(i.get('short_name').lower())
            #
            #                 if latitude == 0 and longitude == 0:
            #                     loca = "Earth"
            #                     flag = ":earth_americas:"
            #
            #                 if latitude != 0 and longitude != 0:
            #                     async with aiohttp.ClientSession() as session:
            #                         async with session.get('https://maps.googleapis.com/maps/api/timezone/json?location={},{}&timestamp=1508828094'.format(latitude, longitude)) as rr:
            #                             re = await rr.json()
            #                     diff = str(int(re.get('rawOffset')) / 60 / 60)
            #                     ddiff = str(int(re.get('dstOffset')) / 60 / 60)
            #                     diff = str(float(ddiff) + float(diff) - 8).split(".")
            #                 else:
            #                     diff = "-8.0".split(".")
            #
            #                 if diff[0][0] == '-':
            #                     sign = "n"
            #                 else:
            #                     sign = "p"
            #                 sunrise = str(datetime.datetime.fromtimestamp(r.get('sys').get('sunrise')))[11:19]
            #                 sunset = str(datetime.datetime.fromtimestamp(r.get('sys').get('sunset')))[11:19]
            #                 # add in the time difference
            #                 if sign == 'p':
            #                     diff1 = int(diff[1]) / 100 * 60
            #                     diff0 = diff[0]
            #                     sunrise = "{}:{}:{}".format(int(sunrise[0:2]) + int(diff[0]),
            #                                                 int(sunrise[3:5]) + int(diff1), sunrise[6:8])
            #                 else:
            #                     diff1 = int(diff[1]) / 100 * 60
            #                     diff0 = diff[0].replace('-', "")
            #                     sunrise = "{}:{}:{}".format(int(sunrise[0:2]) - int(diff0), int(sunrise[3:5]) - int(diff1),
            #                                                 sunrise[6:8])
            #                 if sign == 'p':
            #                     diff1 = int(diff[1]) / 100 * 60
            #                     diff0 = diff[0]
            #                     sunset = "{}:{}:{}".format(int(sunset[0:2]) + int(diff[0]), int(sunset[3:5]) + int(diff1),
            #                                                sunset[6:8])
            #                 else:
            #                     diff1 = int(diff[1]) / 100 * 60
            #                     diff0 = diff[0].replace('-', "")
            #                     sunset = "{}:{}:{}".format(int(sunset[0:2]) - int(diff0), int(sunset[3:5]) - int(diff1),
            #                                                sunset[6:8])
            #
            #                 # change to hours and minutes only, taking out seconds
            #                 if int(sunrise.split(":")[2]) >= 30:
            #                     sunrise = "{}:{}".format(int(sunrise.split(":")[0]), int(sunrise.split(":")[1]) + 1)
            #                 else:
            #                     sunrise = "{}:{}".format(int(sunrise.split(":")[0]), int(sunrise.split(":")[1]))
            #                 if int(sunset.split(":")[2]) >= 30:
            #                     sunset = "{}:{}".format(int(sunset.split(":")[0]), int(sunset.split(":")[1]) + 1)
            #                 else:
            #                     sunset = "{}:{}".format(int(sunset.split(":")[0]), int(sunset.split(":")[1]))
            #
            #                 # if value more than 23, to change it down
            #                 if int(sunrise.split(":")[0]) >= 24:
            #                     sunrise = "{}{}".format("{}:".format(str(int(sunrise.split(":")[0]) - 24)),
            #                                             sunrise.split(":")[1])
            #                 if int(sunset.split(":")[0]) >= 24:
            #                     sunset = "{}{}".format("{}:".format(str(int(sunset.split(":")[0]) - 24)),
            #                                            sunset.split(":")[1])
            #
            #                 if int(sunrise.split(":")[1]) < 10:
            #                     sunrise = "{}:0{}".format(sunrise.split(":")[0], sunrise.split(":")[1])
            #                 if int(sunset.split(":")[1]) < 10:
            #                     sunset = "{}:0{}".format(sunset.split(":")[0], sunset.split(":")[1])
            #
            #                 # change to am pm
            #                 if '-' in sunrise:
            #                     sunrise = "{}:{}".format(str(int(sunrise.split(":")[0]) + 24), sunrise.split(":")[1])
            #                 if '-' in sunset:
            #                     sunset = "{}:{}".format(str(int(sunset.split(":")[0]) + 24), sunset.split(":")[1])
            #
            #                 if int(sunrise.split(":")[0]) > 12:
            #                     sunrise = "{}:{}".format(str(int(sunrise.split(":")[0]) - 12), sunrise.split(":")[1])
            #                     a = "pm"
            #                 elif int(sunrise.split(":")[0]) == 12:
            #                     a = "pm"
            #                 else:
            #                     a = "am"
            #                 if int(sunset.split(":")[0]) > 12:
            #                     sunset = "{}:{}".format(str(int(sunset.split(":")[0]) - 12), sunset.split(":")[1])
            #                     ax = "pm"
            #                 elif int(sunset.split(":")[0]) == 12:
            #                     ax = "pm"
            #                 else:
            #                     ax = "am"
            #                 if a == "pm":
            #                     sunrise = "{} pm".format(sunrise)
            #                 else:
            #                     sunrise = "{} am".format(sunrise)
            #                 if ax == "pm":
            #                     sunset = "{} pm".format(sunset)
            #                 else:
            #                     sunset = "{} am".format(sunset)
            #
            #                 timing = str(datetime.datetime.now())
            #
            #                 await client.send_message(message.channel,"__**Location**__\n{} {}\n\n__**Weather**__\n{}\n\n__**Temperature**__\n{}°C : {}°F\n\n__**Humidity**__\n{}%\n\n__**Cloud Coverage**__\n{}%\n\n__**Wind Speed**__\n{}km/h\n\n__**Wind Direction**__\n{}° ({})\n\n__**Atmospheric Pressure**__\n{}mb\n\n__**Latitude and Longitude**__\n{} (Latitude)\n{} (Longitude)\n\n__**Sunrise and Sunset**__\n{} (Sunrise)\n{} (Sunset)\n\n*Updated {}*".format(flag, loca, weather, temperature1, temperature2, humidity, cloud,windspeed, winddir, windir, pressure, latitude, longitude,sunrise, sunset, updatetime))
            #                 print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(message_time, message.server,message.author, message.id,message.content))
            #                 break
            #             except IndexError as e:
            #                 print("[{}] [{}] [CHECK] {} ({}) executed {}\nReason: {}\n".format(message_time, message.server,message.author, message.id,message.content, e))
            #                 pass
            #                 # except Exception as e:
            #                 #     await client.send_message(message.channel, "An unknown error occurred")
            #                 #     print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: {}".format(message_time, message.server, message.author, message.id, message.content, e))
            #                 #     break
            # else:
            #     await client.send_message(message.channel, "I do not recall a city with no names :thinking:")
            #     print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User did not input".format(message_time,message.server,message.author,message.id,message.content))

        # elif message.content.split(" ")[0] == '.t' or message.content.split(" ")[0] == '.time':
        #     if message.content != '.t' and message.content != '.time':
        #         await client.send(message.channel, "This command is in progress")
        #         print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Command in progress".format(message_time,message.server,message.author,message.id,message.content))
            #     msg = ("".join(message.content)).replace(message.content.split(" ")[0] + " ", "")
            #     try:
            #         while True:
            #             async with aiohttp.ClientSession() as session:
            #                 async with session.get('https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(msg)) as rr:
            #                     rs = await rr.json()
            #             if rs.get("status") == "OVER_QUERY_LIMIT":
            #                 pass
            #             elif rs.get("status") == "ZERO_RESULTS":
            #                 raise Exception
            #             else:
            #                 break
            #     except:
            #         await client.send_message(message.channel, "City not Found")
            #         print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: City not found".format(message_time,message.server,message.author,message.id,message.content))
            #
            #     else:
            #         latitude = rs.get("results")[0].get("geometry").get("location").get("lat")
            #         longitude = rs.get("results")[0].get("geometry").get("location").get("lng")
            #         loca = (rs.get("results")[0]).get('formatted_address')
            #         if latitude != 0 and longitude != 0:
            #             async with aiohttp.ClientSession() as session:
            #                 async with session.get('https://maps.googleapis.com/maps/api/timezone/json?location={},{}&timestamp=1508828094'.format(latitude, longitude)) as rr:
            #                     re = await rr.json()
            #             diff = str(int(re.get('rawOffset')) / 60 / 60)
            #             ddiff = str(int(re.get('dstOffset')) / 60 / 60)
            #             diff = str(float(ddiff) + float(diff) - 8).split(".")
            #         else:
            #             diff = "-8.0".split(".")
            #         nowtime = str(datetime.datetime.now())[11:19]
            #
            #         if diff[0][0] == '-':
            #             sign = "n"
            #         else:
            #             sign = "p"
            #
            #         # add in the time difference
            #         if sign == 'p':
            #             diff1 = int(diff[1]) / 100 * 60
            #             diff0 = diff[0]
            #             nowtime = "{}:{}:{}".format(int(nowtime[0:2]) + int(diff[0]), int(nowtime[3:5]) + int(diff1),nowtime[6:8])
            #         else:
            #             diff1 = int(diff[1]) / 100 * 60
            #             diff0 = diff[0].replace('-', "")
            #             nowtime = "{}:{}:{}".format(int(nowtime[0:2]) - int(diff0), int(nowtime[3:5]) - int(diff1),nowtime[6:8])
            #
            #         # change to hours and minutes only, taking out seconds
            #         if int(nowtime.split(":")[2]) >= 30:
            #             nowtime = "{}:{}".format(int(nowtime.split(":")[0]), int(nowtime.split(":")[1]) + 1)
            #         else:
            #             nowtime = "{}:{}".format(int(nowtime.split(":")[0]), int(nowtime.split(":")[1]))
            #
            #         # if value more than 23, to change it down
            #         if int(nowtime.split(":")[0]) >= 24:
            #             nowtime = "{}{}".format("{}:".format(str(int(nowtime.split(":")[0]) - 24)), nowtime.split(":")[1])
            #
            #         if int(nowtime.split(":")[1]) < 10:
            #             nowtime = "{}:0{}".format(nowtime.split(":")[0], nowtime.split(":")[1])
            #
            #         # change to am pm
            #         if '-' in nowtime:
            #             nowtime = "{}:{}".format(str(int(nowtime.split(":")[0]) + 24), nowtime.split(":")[1])
            #
            #         if int(nowtime.split(":")[0]) > 12:
            #             nowtime = "{}:{}".format(str(int(nowtime.split(":")[0]) - 12), nowtime.split(":")[1])
            #             a = "pm"
            #         elif int(nowtime.split(":")[0]) == 12:
            #             a = "pm"
            #         else:
            #             a = "am"
            #
            #         if a == "pm":
            #             nowtime = "{} pm".format(nowtime)
            #         else:
            #             nowtime = "{} am".format(nowtime)
            #
            #         await client.send_message(message.channel, "The time in **{}** is `{}`".format(loca, nowtime))
            #         print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(message_time, message.server, message.author,message.id, message.content))
            # else:
            #     await client.send_message(message.channel, "Can't tell you the time if you don't provide me with the city name")
            #     print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User did not input".format(message_time,message.server,message.author,message.id,message.content))