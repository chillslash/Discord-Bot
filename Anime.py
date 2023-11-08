from urllib import request
import aiohttp
import math
import datetime
import calendar

page_list = {}

class AnimeCaller:

    def __init__(self, message=None, message_time=None, client=None, discord=None):
        self.message = message
        self.message_time = message_time
        self.client = client
        self.discord = discord

    def help(self):
        helplist = ['Anime', {'search': ['.anime search <anime>', '.a s', 'Search up any Anime'], 'manga': ['.anime manga <manga>', '.a m', 'Search up any Manga'], 'character':['.anime character <character>', '.a c', 'Search up any anime characters'], 'trending': ['.anime trending [page number]', '.a t', 'Find out the seasonal animes'], 'animetop': ['.anime animetop [page number]', '.a at', 'Find out the top Animes'], 'mangatop':['.anime mangatop [page number]', '.a mt', 'Find out the top Mangas'], 'schedule':['.anime schedule [day]', '.a sc', 'Find out the Anime Schedule today or any day'], 'user': ['.anime user <profile | stats> <username>', '.a u', 'Search up any MyAnimeList Users']}]
        return helplist

    async def page_list_add(self, author, number):
        page_list[author] = number

    async def page_list_delete(self, author):
        del page_list[author]

    def format_number(self, number):
        if number >= 1000000000:
            number = "{}B".format(round(number / 1000000000, 2))
        elif number >= 1000000:
            number = "{}M".format(round(number / 1000000, 2))
        elif number >= 1000:
            number = "{}K".format(round(number / 1000, 2))
        return number

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

    def check_anime(self, message):
        number = page_list[message.author.id]
        for x in range(1, number+1):
            if message.content == str(x):
                return True
        else:
            if message.content.lower() == 'exit':
                return True
            return False

    async def sorting(self):
        if self.message.content.split(" ")[1] == 'search' or self.message.content.split(" ")[1] == 's':
            await self.anime_search()
        elif self.message.content.split(" ")[1] == 'manga' or self.message.content.split(" ")[1] == 'm':
            await self.manga_search()
        elif self.message.content.split(" ")[1] == 'animetop' or self.message.content.split(" ")[1] == 'at':
            await self.anime_top()
        elif self.message.content.split(" ")[1] == 'mangatop' or self.message.content.split(" ")[1] == 'mt':
            await self.manga_top()
        elif self.message.content.split(" ")[1] == 'trending' or self.message.content.split(" ")[1] == 't':
            await self.trending()
        elif self.message.content.split(" ")[1] == 'schedule' or self.message.content.split(" ")[1] == 'sc':
            await self.schedule()
        elif self.message.content.split(" ")[1] == 'user' or self.message.content.split(" ")[1] == 'u':
            await self.user()
        elif self.message.content.split(" ")[1] == 'character' or self.message.content.split(" ")[1] == 'c':
            await self.character_search()
        else:
            helplist = self.help()
            field = "**Alias:** .a\n\n"
            for name in helplist[1]:
                field += '**{}** - {}\n'.format(helplist[1][name][0], helplist[1][name][2])
            embed = self.discord.Embed(title='Anime Commands', description=field, colour=0xe74c3c)
            embed.set_footer(text='Type .help anime <command> to find out more! | < > - Required ; [ ] - Optional')
            await self.client.send_message(self.message.channel, embed=embed)
            print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
        


    async def anime_search(self):
        if not self.message.author.id in page_list:
            if self.message.content != '.anime search' and self.message.content != '.a s' and self.message.content != '.anime s' and self.message.content != '.a search':
                await self.client.send_typing(self.message.channel)
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://api.jikan.moe/v3/search/anime?q={}&limit=10'.format(request.quote(str(self.message.content).replace(str(self.message.content).split(" ")[0] + " " +str(self.message.content).split(" ")[1] + " ", '')))) as r:
                        js = await r.json()
                if not 'error' in js:
                    page_preview = "**Searching:** {}\n".format(str(self.message.content).replace(str(self.message.content).split(" ")[0] + " " +str(self.message.content).split(" ")[1] + " ",''))
                    for number in range(0, len(js.get('results'))):
                        page_preview+="\n{}) `{}`".format(str(number+1), str(js.get('results')[number].get('title')))
                    page_preview+="\n\nType the index number of the anime you want, or type `exit` to delete your request"
                    await self.page_list_add(self.message.author.id, len(js.get('results')))
                    msg1 = await self.client.send_message(self.message.channel, page_preview)
                    msg = await self.client.wait_for_message(author=self.message.author, check=self.check_anime, timeout=20)
                    await self.page_list_delete(self.message.author.id)
                    if msg != None: page_number = msg.content
                    else: page_number = None
                    if page_number != None and page_number.isdigit():
                        await self.client.delete_message(msg1)
                        await self.client.send_typing(self.message.channel)
                        async with aiohttp.ClientSession() as session:
                            async with session.get('https://api.jikan.moe/v3/anime/{}'.format(js.get('results')[int(page_number)-1].get('mal_id'))) as r:
                                js = await r.json()
                        title = js.get('title')
                        result = ' [#{} Result]'.format(int(page_number))
                        description = js.get('synopsis')
                        if js.get('aired').get('from'): start = self.format_date(js.get('aired').get('from')[:10].replace('-', ''))
                        else: start = "None"
                        if js.get('aired').get('to'): end = self.format_date(js.get('aired').get('to')[:10].replace('-', ''))
                        else: end = "None"
                        if js.get('type').islower():
                            type_ = js.get('type').capitalize()
                        else:
                            type_ = js.get('type')
                        episodes = js.get('episodes')
                        en = js.get('title_english')
                        if 'title_japanese' in js: ja_jp = js.get('title_japanese')
                        else: ja_jp = "None"
                        if en == None: en = 'None'
                        genre = ""
                        for genres in js.get('genres'):
                            genre = genre + genres.get('name') + ", "
                        genre = genre[:-2]
                        status = js.get('status')
                        rating = js.get('rating')
                        if status == 'Finished Airing':
                            status = 'Completed'
                        elif status == 'Currently Airing':
                            status = 'Airing'
                        elif status == 'Not yet aired':
                            status = 'Not aired yet'
                        image = js.get('image_url')
                        if js.get('trailer_url'): trailer = "https://youtube.com/watch?v={}".format(js.get('trailer_url').split("/")[4].split("?")[0])
                        else: trailer = None
                        averateRating = js.get('score')
                        popularityRank = js.get('popularity')
                        if js.get('rank'): ratingRank = js.get('rank')
                        else: ratingRank = 'None'
                        broadcast = js.get('broadcast')
                        embed = self.discord.Embed(title=title + result, description=description, colour=0xe74c3c, url=js.get('url'))
                        members = self.format_number(js.get('members'))
                        embed.add_field(name='Titles (English/Japanese)',value=en + "/" + ja_jp, inline=False)
                        embed.add_field(name='Start Date', value=start, inline=True)
                        embed.add_field(name='End Date', value=end, inline=True)
                        embed.add_field(name='Type', value=type_, inline=True)
                        embed.add_field(name='Status', value=status, inline=True)
                        embed.add_field(name='Broadcast', value=broadcast, inline=True)
                        embed.add_field(name='Parental Rating', value=rating, inline=True)
                        embed.add_field(name='Episodes', value=episodes, inline=True)
                        embed.add_field(name='Anime Rating', value=averateRating, inline=True)
                        embed.add_field(name='Popularity Ranking', value="#{}".format(popularityRank), inline=True)
                        embed.add_field(name='Rating Ranking', value="#{}".format(ratingRank), inline=True)
                        if str(genre):
                            embed.add_field(name='Genres', value=genre, inline=False)
                        if trailer:
                            embed.add_field(name='Trailer', value=trailer, inline=False)
                        embed.set_thumbnail(url=image)
                        embed.set_footer(text='myanimelist.net | {} Members'.format(members))
                        try:
                            await self.client.send_message(self.message.channel, embed=embed)
                        except self.discord.errors.HTTPException:
                            description = description[:1900] + "..."
                            embed.description = description
                            await self.client.send_message(self.message.channel, embed=embed)
                        finally:
                            print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server,self.message.author,self.message.id,self.message.content))
                    elif page_number != None:
                        await self.client.edit_message(msg1, "*Request Deleted*")
                        print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Request deleted".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
                    else:
                        await self.client.edit_message(msg1, page_preview+"\n\n*Request timeout*")
                        print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Timeout".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
                else:
                    await self.client.send_message(self.message.channel, "Anime not found")
                    print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Anime not found".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))

            else:
                await self.client.send_message(self.message.channel, "Enter a anime to search")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User did not input".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))

        else:
            await self.client.send_message(self.message.channel, "You're already requesting for an Anime Command! Finish that request before trying again")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User has ongoing request".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))

    async def manga_search(self):
        if not self.message.author.id in page_list:
            if self.message.content != '.anime manga' and self.message.content != '.a m' and self.message.content != '.anime m' and self.message.content != '.a manga':
                await self.client.send_typing(self.message.channel)
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://api.jikan.moe/v3/search/manga?q={}&limit=10'.format(request.quote(str(self.message.content).replace(str(self.message.content).split(" ")[0] + " " +str(self.message.content).split(" ")[1] + " ", '')))) as r:
                        js = await r.json()
                if not 'error' in js:
                    page_preview = "**Searching:** {}\n".format(str(self.message.content).replace(str(self.message.content).split(" ")[0] + " " +str(self.message.content).split(" ")[1] + " ",''))
                    for number in range(0, len(js.get('results'))):
                        page_preview+="\n{}) `{}`".format(str(number+1), str(js.get('results')[number].get('title')))
                    page_preview+="\n\nType the index number of the manga you want, or type `exit` to delete your request"
                    await self.page_list_add(self.message.author.id, len(js.get('results')))
                    msg1 = await self.client.send_message(self.message.channel, page_preview)
                    msg = await self.client.wait_for_message(author=self.message.author, check=self.check_anime, timeout=20)
                    await self.page_list_delete(self.message.author.id)
                    if msg != None: page_number = msg.content
                    else: page_number = None
                    if page_number != None and page_number.isdigit():
                        await self.client.delete_message(msg1)
                        await self.client.send_typing(self.message.channel)
                        async with aiohttp.ClientSession() as session:
                            async with session.get('https://api.jikan.moe/v3/manga/{}'.format(js.get('results')[int(page_number)-1].get('mal_id'))) as r:
                                js = await r.json()
                        title = js.get('title')
                        result = ' [#{} Result]'.format(int(page_number))
                        description = js.get('synopsis')
                        if js.get('published').get('from'): start = self.format_date(js.get('published').get('from')[:10].replace('-', ''))
                        else: start = "None"
                        if js.get('published').get('to'): end = self.format_date(js.get('published').get('to')[:10].replace('-', ''))
                        else: end = "None"
                        if js.get('type').islower():
                            type_ = js.get('type').capitalize()
                        else:
                            type_ = js.get('type')
                        chapters = js.get('chapters')
                        volumes = js.get('volumes')
                        en = js.get('title_english')
                        if 'title_japanese' in js: ja_jp = js.get('title_japanese')
                        else: ja_jp = "None"
                        if en == None: en = 'None'
                        genre = ""
                        for genres in js.get('genres'):
                            genre = genre + genres.get('name') + ", "
                        genre = genre[:-2]
                        status = js.get('status')
                        rating = js.get('rating')
                        image = js.get('image_url')
                        averateRating = js.get('score')
                        popularityRank = js.get('popularity')
                        if js.get('rank'): ratingRank = js.get('rank')
                        else: ratingRank = 'None'
                        members = self.format_number(js.get('members'))
                        embed = self.discord.Embed(title=title + result, description=description, colour=0xe74c3c, url=js.get('url'))
                        embed.add_field(name='Titles (English/Japanese)',value=en + "/" + ja_jp, inline=False)
                        embed.add_field(name='Start Date', value=start, inline=True)
                        embed.add_field(name='End Date', value=end, inline=True)
                        embed.add_field(name='Type', value=type_, inline=True)
                        embed.add_field(name='Status', value=status, inline=True)
                        embed.add_field(name='Parental Rating', value=rating, inline=True)
                        embed.add_field(name='Chapters', value=chapters, inline=True)
                        embed.add_field(name='Volumes', value=volumes, inline=True)
                        embed.add_field(name='Manga Rating', value=averateRating, inline=True)
                        embed.add_field(name='Popularity Ranking', value="#{}".format(popularityRank), inline=True)
                        embed.add_field(name='Rating Ranking', value="#{}".format(ratingRank), inline=True)
                        if str(genre):
                            embed.add_field(name='Genres', value=genre, inline=False)
                        embed.set_thumbnail(url=image)
                        embed.set_footer(text='myanimelist.net | {} Members'.format(members))
                        try:
                            await self.client.send_message(self.message.channel, embed=embed)
                        except self.discord.errors.HTTPException:
                            description = description[:1900] + "..."
                            embed.description = description
                            await self.client.send_message(self.message.channel, embed=embed)
                        finally:
                            print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server,self.message.author,self.message.id,self.message.content))
                    elif page_number != None:
                        await self.client.edit_message(msg1, "*Request Deleted*")
                        print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Request deleted".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
                    else:
                        await self.client.edit_message(msg1, page_preview+"\n\n*Request timeout*")
                        print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Timeout".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
                else:
                    await self.client.send_message(self.message.channel, "Manga not found")
                    print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Manga not found".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))

            else:
                await self.client.send_message(self.message.channel, "Enter a manga to search")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User did not input".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
        else:
            await self.client.send_message(self.message.channel, "You're already requesting for an Anime Command! Finish that request before trying again")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User has ongoing request".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))

    async def anime_top(self):
        try:
            try:
                page_number = int(str(self.message.content).split(" ")[2])
                if page_number > 1500 or page_number <= 0: raise EnvironmentError
            except IndexError:
                page_number = 1
            except ValueError:
                raise EnvironmentError
        except EnvironmentError:
            await self.client.send_message(self.message.channel, "Enter a number between 1 - 1500")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Invalid page number".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
        else:
            await self.client.send_typing(self.message.channel)
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.jikan.moe/v3/top/anime/{}'.format(math.ceil(page_number/5))) as r:
                    js = await r.json()
            if 'error' in js:
                await self.client.send_message(self.message.channel, "The page does not go this far")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Invalid page number".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
            embed = self.discord.Embed(title='Top Anime', colour=0xe74c3c, url='https://myanimelist.net/topanime.php')
            for number in range(((page_number-1)*10)-int(math.ceil(page_number/5)-1)*50, 10+((page_number-1)*10)-int(math.ceil(page_number/5)-1)*50):
                title = js.get('top')[number].get('title')
                type_ = js.get('top')[number].get('type')
                score = js.get('top')[number].get('score')
                episodes = js.get('top')[number].get('episodes')
                embed.add_field(name="{}) {} [{}]".format((int(math.ceil(page_number/5)-1)*50)+number+1, title, type_), value="Score: **{}** | Episodes: **{}**".format(score, episodes), inline=False)
            embed.set_footer(text='myanimelist.net | Page {}/1500'.format(page_number))
            embed.set_thumbnail(url=js.get('top')[(page_number%5-1)*10].get('image_url'))
            await self.client.send_message(self.message.channel, embed=embed)
            print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server,self.message.author, self.message.id,self.message.content))


    async def manga_top(self):
        try:
            try:
                page_number = int(str(self.message.content).split(" ")[2])
                if page_number > 1500 or page_number <= 0: raise EnvironmentError
            except IndexError:
                page_number = 1
            except ValueError:
                raise EnvironmentError
        except EnvironmentError:
            await self.client.send_message(self.message.channel, "Enter a number between 1 - 1500")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Invalid page number".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
        else:
            await self.client.send_typing(self.message.channel)
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.jikan.moe/v3/top/manga/{}'.format(math.ceil(page_number/5))) as r:
                    js = await r.json()
            if 'error' in js:
                await self.client.send_message(self.message.channel, "The page does not go this far")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Invalid page number".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
            embed = self.discord.Embed(title='Top Manga', colour=0xe74c3c, url='https://myanimelist.net/topmanga.php')
            for number in range(((page_number-1)*10)-int(math.ceil(page_number/5)-1)*50, 10+((page_number-1)*10)-int(math.ceil(page_number/5)-1)*50):
                title = js.get('top')[number].get('title')
                score = js.get('top')[number].get('score')
                volumes = js.get('top')[number].get('volumes')
                embed.add_field(name="{}) {}".format((int(math.ceil(page_number/5)-1)*50)+number+1, title), value="Score: **{}** | Volumes: **{}**".format(score, volumes), inline=False)
            embed.set_footer(text='myanimelist.net | Page {}/1500'.format(page_number))
            embed.set_thumbnail(url=js.get('top')[(page_number%5-1)*10].get('image_url'))
            await self.client.send_message(self.message.channel, embed=embed)
            print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server,self.message.author, self.message.id,self.message.content))

    async def trending(self):
        try:
            try:
                page_number = int(str(self.message.content).split(" ")[2])
                if page_number <= 0: raise EnvironmentError
            except IndexError:
                page_number = 1
            except ValueError:
                raise EnvironmentError
        except EnvironmentError:
            await self.client.send_message(self.message.channel, "Enter a number from 1")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Invalid page number".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
        else:
            await self.client.send_typing(self.message.channel)
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.jikan.moe/v3/season') as r:
                    js = await r.json()
            if page_number < int(len(js.get('anime'))/5):
                embed = self.discord.Embed(title='Trending Anime [{} {}]'.format(js.get('season_name'), js.get('season_year')), colour=0xe74c3c, url='https://myanimelist.net/anime/season')
                for number in range((page_number*5)-5, page_number*5):
                    title = js.get('anime')[number].get('title')
                    type_ = js.get('anime')[number].get('type')
                    if len(js.get('anime')[number].get('synopsis')) > 199: desc = str(js.get('anime')[number].get('synopsis'))[:200] + "..."
                    else: desc = js.get('anime')[number].get('synopsis')
                    score = js.get('anime')[number].get('score')
                    episodes = js.get('anime')[number].get('episodes')
                    if js.get('anime')[number].get('genres'):
                        genres = ""
                        for genre in js.get('anime')[number].get('genres'):
                            genres = genres + genre.get('name') + ', '
                        genres = genres[:-2]
                    else: genres = 'None'
                    embed.add_field(name='{}) {} [{}]'.format(number+1, title, type_), value="{}\n\nScore: **{}** | Episodes: **{}** | Genres: **{}**\n\u200b".format(desc,score, episodes, genres), inline=False)
                embed.set_footer(text='myanimelist.net | Page {}/{}'.format(page_number, int(len(js.get('anime'))/5)-1))
                embed.set_thumbnail(url=js.get('anime')[(page_number*5)-5].get('image_url'))
                await self.client.send_message(self.message.channel, embed=embed)
                print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server,self.message.author, self.message.id,self.message.content))
            else:
                await self.client.send_message(self.message.channel, "Enter a number between 1 - {}".format(int(len(js.get('anime'))/5)-1))
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Invalid page number".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))

    async def schedule(self):
        if len(self.message.content.split(' ')) == 3:
            if self.message.content.split(' ')[2] == 'monday' or self.message.content.split(' ')[2] == 'tuesday' or self.message.content.split(' ')[2] == 'wednesday' or self.message.content.split(' ')[2] == 'thursday' or self.message.content.split(' ')[2] == 'friday' or self.message.content.split(' ')[2] == 'saturday' or self.message.content.split(' ')[2] == 'sunday':
                day = self.message.content.split(' ')[2].capitalize()
        elif len(self.message.content.split(' ')) == 2:
            day = calendar.day_name[(datetime.datetime.now() + datetime.timedelta(hours=1)).weekday()]
        if not 'day' in locals():
            await self.client.send_message(self.message.channel, "Invalid Day. Enter a day from Monday - Sunday")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Invalid day".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
        else:
            await self.client.send_typing(self.message.channel)
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.jikan.moe/v3/schedule/{}'.format(day)) as r:
                    js = await r.json()
            desc = ""
            for number in range(0, len(js.get(day.lower()))):
                if js.get(day.lower())[number].get('airing_start'):
                    timing = str(datetime.timedelta(hours=int(js.get(day.lower())[number].get('airing_start').split('T')[1].split(':')[0])-15, minutes=int(js.get(day.lower())[number].get('airing_start').split('T')[1].split(':')[1])))
                    if len(timing.split(', ')) == 2: timing = ":".join(timing.split(', ')[1].split(':')[0:2])
                    else: timing = ":".join(timing.split(':')[0:2])
                    desc = desc + "{}) **{}** [{}]\n\n".format(number+1, js.get(day.lower())[number].get('title'), timing)
                else:
                    desc = desc + "{}) **{}**\n\n".format(number+1, js.get(day.lower())[number].get('title'))
            embed = self.discord.Embed(title='Schedule for {}'.format(day), description=desc, colour=0xe74c3c, url='https://myanimelist.net/anime/season/schedule')
            embed.set_footer(text='myanimelist.net | JST Timing')
            await self.client.send_message(self.message.channel, embed=embed)
            print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))

    async def user(self):
        try:
            argument = str(self.message.content).split(" ")[2]
            username = " ".join(str(self.message.content).split(" ")[3:])
            if not (argument == 'profile' or argument == 'stats') or len(self.message.content.split(" ")) < 4:
                raise Exception
        except:
            await self.client.send_message(self.message.channel, "Invalid format. Try `.anime user <profile | stats> <username>`")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Invalid format".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
        else:
            await self.client.send_typing(self.message.channel)
            if argument == 'profile':
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://api.jikan.moe/v3/user/{}/profile'.format(request.quote(username))) as r:
                        js = await r.json()
                if not 'error' in js:
                    async with aiohttp.ClientSession() as session:
                        async with session.get('https://api.jikan.moe/v3/user/{}/friends'.format(request.quote(username))) as r:
                            jss = await r.json()
                    embed = self.discord.Embed(title=js.get('username'), colour=0xe74c3c, url=js.get('url'))
                    if js.get('about'): embed.description = js.get('about').replace('<br>', "\n").replace('</br>', '').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace("&#39", "'")
                    if js.get('image_url'): embed.set_thumbnail(url=js.get('image_url'))
                    else: embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/926302376738377729/SMlpasPv_400x400.jpg")
                    embed.add_field(name='Joined at', value=self.format_date(js.get('joined').split('T')[0].replace('-', "")), inline=True)
                    embed.add_field(name='Last Online', value=self.format_date(js.get('last_online').split('T')[0].replace('-', '')), inline=True)
                    if js.get('favorites').get('anime'):
                        if len(js.get('favorites').get('anime')[0].get('name').split(' ')) > 3:
                            embed.add_field(name='Favourite Anime', value=" ".join(js.get('favorites').get('anime')[0].get('name').split(' ')[:3])+ '\n' + " ".join(js.get('favorites').get('anime')[0].get('name').split(' ')[3:]))
                        else:
                            embed.add_field(name='Favourite Anime', value=js.get('favorites').get('anime')[0].get('name'))
                    if js.get('favorites').get('manga'):
                        if len(js.get('favorites').get('manga')[0].get('name').split(' ')) > 3:
                            embed.add_field(name='Favourite Anime', value=" ".join(js.get('favorites').get('manga')[0].get('name').split(' ')[:3])+ '\n' + " ".join(js.get('favorites').get('manga')[0].get('name').split(' ')[3:]))
                        else:
                            embed.add_field(name='Favourite Manga', value=js.get('favorites').get('manga')[0].get('name'))
                    if not 'error' in jss: embed.add_field(name='Friends', value=str(len(jss.get('friends'))), inline=True)
                    else: embed.add_field(name='Friends', value="0", inline=True)
                    if js.get('gender'): embed.add_field(name='Gender', value=js.get('gender'), inline=True)
                    if js.get('location'):
                        if len(js.get('location').split(" ")) > 3:
                            embed.add_field(name='Location', value=" ".join(js.get('location').split(" ")[:3]) + "\n" + " ".join(js.get('location').split(' ')[3:]), inline=True)
                        else:
                            embed.add_field(name='Location', value=js.get('location'), inline=True)
                    if js.get('birthday'): embed.add_field(name='Birthday', value=self.format_date(js.get('birthday').split('T')[0].replace('-', '')), inline=True)
                    embed.set_footer(text='myanimelist.net')
                    await self.client.send_message(self.message.channel, embed=embed)
                    print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
                else:
                    await self.client.send_message(self.message.channel, "User not found")
                    print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User not found".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
            elif argument == 'stats':
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://api.jikan.moe/v3/user/{}/profile'.format(username)) as r:
                        js = await r.json()
                if not 'error' in js:
                    if js.get('anime_stats').get('total_entries') == 0 and js.get('manga_stats').get('total_entries') == 0:
                        embed = self.discord.Embed(title="{} Anime & Manga Stats".format(js.get('username')), description='Non Existent', colour=0xe74c3c)
                        embed.set_footer(text='myanimelist.net')
                        await self.client.send_message(self.message.channel, embed=embed)
                    else:
                        if js.get('anime_stats').get('total_entries') != 0:
                            embed = self.discord.Embed(title="{} Anime Stats".format(js.get('username')), colour=0xe74c3c, url=js.get('url'))
                            embed.set_thumbnail(url=js.get('image_url'))
                            embed.add_field(name="Days Watched", value=js.get('anime_stats').get('days_watched'), inline=True)
                            embed.add_field(name="Mean Score", value=js.get('anime_stats').get('mean_score'), inline=True)
                            embed.add_field(name="Watching", value=js.get('anime_stats').get('watching'), inline=True)
                            embed.add_field(name="Completed", value=js.get('anime_stats').get('completed'), inline=True)
                            embed.add_field(name="On Hold", value=js.get('anime_stats').get('on_hold'), inline=True)
                            embed.add_field(name="Dropped", value=js.get('anime_stats').get('dropped'), inline=True)
                            embed.add_field(name="Plan To Watch", value=js.get('anime_stats').get('plan_to_watch'), inline=True)
                            embed.add_field(name="Total Entries", value=js.get('anime_stats').get('total_entries'), inline=True)
                            embed.add_field(name="Rewatched", value=js.get('anime_stats').get('rewatched'), inline=True)
                            embed.add_field(name="Episodes Watched", value=js.get('anime_stats').get('episodes_watched'), inline=True)
                            embed.set_footer(text='myanimelist.net')
                            await self.client.send_message(self.message.channel, embed=embed)
                        if js.get('manga_stats').get('total_entries') != 0:
                            embedd = self.discord.Embed(title="{} Manga Stats".format(js.get('username')), colour=0xe74c3c, url=js.get('url'))
                            embedd.set_thumbnail(url=js.get('image_url'))
                            embedd.add_field(name="Days Read", value=js.get('manga_stats').get('days_read'), inline=True)
                            embedd.add_field(name="Mean Score", value=js.get('manga_stats').get('mean_score'), inline=True)
                            embedd.add_field(name="Reading", value=js.get('manga_stats').get('reading'), inline=True)
                            embedd.add_field(name="Completed", value=js.get('manga_stats').get('completed'), inline=True)
                            embedd.add_field(name="On Hold", value=js.get('manga_stats').get('on_hold'), inline=True)
                            embedd.add_field(name="Dropped", value=js.get('manga_stats').get('dropped'), inline=True)
                            embedd.add_field(name="Plan To Read", value=js.get('manga_stats').get('plan_to_read'), inline=True)
                            embedd.add_field(name="Total Entries", value=js.get('manga_stats').get('total_entries'), inline=True)
                            embedd.add_field(name="Reread", value=js.get('manga_stats').get('reread'), inline=True)
                            embedd.add_field(name="Chapter Watched", value=js.get('manga_stats').get('chapters_read'), inline=True)
                            embedd.add_field(name="Volumes Watched", value=js.get('manga_stats').get('volumes_read'), inline=True)
                            embedd.set_footer(text='myanimelist.net')
                            await self.client.send_message(self.message.channel, embed=embedd)
                    print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))
                else:
                    await self.client.send_message(self.message.channel, "User not found")
                    print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User not found".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))

    async def character_search(self):
        if not self.message.author.id in page_list:
            if self.message.content != '.anime character' and self.message.content != '.a c' and self.message.content != '.anime c' and self.message.content != '.a character':
                await self.client.send_typing(self.message.channel)
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://api.jikan.moe/v3/search/character?q={}&limit=10'.format(request.quote(str(self.message.content).replace(str(self.message.content).split(" ")[0] + " " +str(self.message.content).split(" ")[1] + " ", '')))) as r:
                        js = await r.json()
                if not 'error' in js:
                    page_preview = "**Searching:** {}\n".format(str(self.message.content).replace(str(self.message.content).split(" ")[0] + " " +str(self.message.content).split(" ")[1] + " ",''))
                    for number in range(0, len(js.get('results'))):
                        page_preview+="\n{}) `{}`".format(str(number+1), str(js.get('results')[number].get('name')))
                    page_preview+="\n\nType the index number of the character you want, or type `exit` to delete your request"
                    await self.page_list_add(self.message.author.id, len(js.get('results')))
                    msg1 = await self.client.send_message(self.message.channel, page_preview)
                    msg = await self.client.wait_for_message(author=self.message.author, check=self.check_anime, timeout=20)
                    await self.page_list_delete(self.message.author.id)
                    if msg != None: page_number = msg.content
                    else: page_number = None
                    if page_number != None and page_number.isdigit():
                        await self.client.delete_message(msg1)
                        await self.client.send_typing(self.message.channel)
                        async with aiohttp.ClientSession() as session:
                            async with session.get('https://api.jikan.moe/v3/character/{}'.format(js.get('results')[int(page_number)-1].get('mal_id'))) as r:
                                js = await r.json()
                        title = js.get('name')
                        result = ' [#{} Result]'.format(int(page_number))
                        description = js.get('about')
                        en = js.get('name')
                        if 'name_kanji' in js: ja_jp = js.get('name_kanji')
                        else: ja_jp = "None"
                        if en == None: en = 'None'
                        if js.get('nicknames'):
                            nickname = ''
                            for nicknames in js.get('nicknames'):
                                nickname = nickname + nicknames + ', '
                            nickname = nickname[:-2]
                        else: nickname = 'None'
                        if 'animeography' in js:
                            anime = "{} ({})".format(js.get('animeography')[0].get('name'), js.get('animeography')[0].get('role'))
                        else: anime = 'None'
                        if 'mangaography' in js:
                            manga = "{} ({})".format(js.get('mangaography')[0].get('name'), js.get('mangaography')[0].get('role'))
                        else: manga = 'None'
                        image = js.get('image_url')
                        embed = self.discord.Embed(title=title + result, description=description, colour=0xe74c3c, url=js.get('url'))
                        embed.add_field(name='Names (English/Japanese)',value=en + "/" + ja_jp, inline=True)
                        embed.add_field(name='Nicknames', value=nickname, inline=True)
                        embed.add_field(name='Anime', value=anime, inline=True)
                        embed.add_field(name='Manga', value=manga, inline=True)
                        embed.set_thumbnail(url=image)
                        embed.set_footer(text='myanimelist.net')
                        try:
                            await self.client.send_message(self.message.channel, embed=embed)
                        except self.discord.errors.HTTPException:
                            description = description[:1900] + "..."
                            embed.description = description
                            await self.client.send_message(self.message.channel, embed=embed)
                        finally:
                            print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server,self.message.author,self.message.id,self.message.content))
                    elif page_number != None:
                        await self.client.edit_message(msg1, "*Request Deleted*")
                        print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Request deleted".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
                    else:
                        await self.client.edit_message(msg1, page_preview+"\n\n*Request timeout*")
                        print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Timeout".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
                else:
                    await self.client.send_message(self.message.channel, "Character not found")
                    print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: Character not found".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))

            else:
                await self.client.send_message(self.message.channel, "Enter a character to search")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User did not input".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))
        else:
            await self.client.send_message(self.message.channel, "You're already requesting for an Anime Command! Finish that request before trying again")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User has ongoing request".format(self.message_time,self.message.server,self.message.author,self.message.id,self.message.content))