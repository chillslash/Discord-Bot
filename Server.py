class ServerCaller:

    def __init__(self, message=None, message_time=None, client=None, discord=None):
        self.message = message
        self.message_time = message_time
        self.client = client
        self.discord = discord

    def help(self):
        helplist = ['Server', {'id': ['.id [username/nickname]', '', 'Find out users ID/Find out your ID'], 'user': ['.user [username/nickname/ID]', '', 'Find out information about a user'], 'serverinfo': ['.serverinfo', '', 'Find out information about the server']}]
        return helplist

    async def user_call(self, member):
        user = member.name
        user_id = member.id
        user_nick = member.nick
        user_game = member.game
        temp_role = sorted(member.roles, reverse=True)
        user_roles = ""
        for role in temp_role: user_roles = user_roles + role.name + ", "
        user_roles = user_roles[:-13]
        if user_roles == "": user_roles = 'None'
        user_icon = member.icon_url
        user_voice = member.voice.voice_channel
        user_perms = self.check_perms(member.server_permissions)
        user_join = str(member.joined_at)[:19]
        if str(member.status) == 'dnd':
            user_status = 'Do not Disturb'
        else:
            user_status = str(member.status).capitalize()
        embed = self.discord.Embed(title="{} [{}]".format(user, user_status), colour=0xe74c3c)
        embed.set_thumbnail(url=user_icon)
        embed.add_field(name='ID', value=user_id, inline=True)
        embed.add_field(name='Nickname', value=user_nick, inline=True)
        embed.add_field(name='Playing now', value=user_game, inline=True)
        embed.add_field(name="Joined Server at (UTC)", value=user_join, inline=True)
        embed.add_field(name='Roles', value=user_roles, inline=False)
        embed.add_field(name='Server Permissions', value=user_perms, inline=False)
        embed.add_field(name='Connected to Voice Channel', value=user_voice, inline=False)
        await self.client.send_message(self.message.channel, embed=embed)
        print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server,self.message.author, self.message.id,self.message.content))

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

    def check_perms(self, permissions):
        global_perms = ""
        if permissions.administrator: global_perms += "Administrator, "
        if permissions.manage_server: global_perms += "Manage Server, "
        if permissions.manage_roles: global_perms += "Manage Roles, "
        if permissions.manage_channels: global_perms += "Manage Channels, "
        if permissions.kick_members: global_perms += "Kick Members, "
        if permissions.ban_members: global_perms += "Ban Members, "
        if permissions.create_instant_invite: global_perms += "Create Instant Invite, "
        if permissions.change_nickname: global_perms += "Change Nickname, "
        if permissions.manage_nicknames: global_perms += "Manage Nicknames, "
        if permissions.manage_emojis: global_perms += "Manage Emojis, "
        if permissions.manage_webhooks: global_perms += "Manage Webhooks, "
        if permissions.read_messages: global_perms += "Read Messages, "
        if permissions.send_messages: global_perms += "Send Messages, "
        if permissions.send_tts_messages: global_perms += "Send TTS Messages, "
        if permissions.manage_messages: global_perms += "Manage Messages, "
        if permissions.embed_links: global_perms += "Embed Links, "
        if permissions.attach_files: global_perms += "Attach Files, "
        if permissions.read_message_history: global_perms += "Read Message History, "
        if permissions.mention_everyone: global_perms += "Mention Everyone, "
        if permissions.external_emojis: global_perms += "Use External Emojis, "
        if permissions.add_reactions: global_perms += "Add Reactions, "
        if permissions.connect: global_perms += "Connect to Voice Channel, "
        if permissions.speak: global_perms += "Speak in Voice Channel, "
        if permissions.mute_members: global_perms += "Mute Members, "
        if permissions.deafen_members: global_perms += "Deafen Members, "
        if permissions.move_members: global_perms += "Move members in Voice Channel, "
        if permissions.use_voice_activation: global_perms += "Use Voice Activation, "
        if not global_perms: return "None"
        return global_perms[:-2]

    async def sorting(self):
        if self.message.content == ".id":
            await self.id()
        elif self.message.content.startswith('.id '):
            await self.id_search()
        elif self.message.content == '.serverinfo':
            await self.serverinfo()
        elif self.message.content.startswith('.user'):
            await self.user()

    async def id(self):
        await self.client.send_message(self.message.channel, "Your ID: ``{}``".format(self.message.author.id))
        print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))

    async def id_search(self):
        try:
            user = str(self.message.content).replace(".id ", "")
            for member in self.message.server.members:
                if (str(user) == str(member.name).lower()) or (str(user) == str(member.nick).lower() and member.nick != None) or (str(user) == member.mention) or (str(user) == str(member.name).lower() + "#" + str(member.discriminator)):
                    if str(user) == str(member.name).lower():
                        for y in self.message.server.members:
                            if (str(member.name).lower() == str(y.name).lower() and member.id != y.id) or (str(member.name).lower() == str(y.nick).lower() and member.id != y.id):
                                raise StopAsyncIteration
                    if str(user) == str(member.nick).lower() and member.nick != None:
                        for y in self.message.server.members:
                            if (str(member.nick).lower() == str(y.name).lower() and member.id != y.id) or (str(member.nick).lower() == str(y.nick).lower() and member.id != y.id):
                                raise StopAsyncIteration
                    user = member.name
                    msgid = member.id
                    nick = member.nick
                    break
            else:
                raise Exception
            if nick:
                await self.client.send_message(self.message.channel, "{} [{}]'s ID: ``{}``".format(user, nick, msgid))
            else:
                await self.client.send_message(self.message.channel, "{}'s ID: ``{}``".format(user, msgid))
            print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author,self.message.id, self.message.content))

        except StopAsyncIteration:
            await self.client.send_message(self.message.channel, "There is more than 1 user with the same name/nickname")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: More than 1 user with same nickname".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))

        except Exception:
            await self.client.send_message(self.message.channel, "User not found")
            print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User not found".format(self.message_time, self.message.server,self.message.author, self.message.id,self.message.content))

    async def serverinfo(self):
        embed = self.discord.Embed(title=self.message.server.name, colour=0xe74c3c)
        embed.add_field(name='ID', value=self.message.server.id, inline=True)
        embed.add_field(name='Date Created', value=self.format_date(str(self.message.server.created_at)[:10].replace('-', '')), inline=True)
        embed.add_field(name='Region', value=str(self.message.server.region).replace("-", " ").title(), inline=True)
        embed.add_field(name='Owner', value=self.message.server.owner, inline=True)
        embed.add_field(name='Members', value="{} Members".format(self.message.server.member_count), inline=True)
        embed.add_field(name='Channels', value="{} Channels".format(len(self.message.server.channels)), inline=True)
        embed.add_field(name='Roles', value="{} Roles".format(len(self.message.server.roles)), inline=True)
        embed.add_field(name='Custom Emojis', value=str(len(self.message.server.emojis)), inline=True)
        embed.set_thumbnail(url=self.message.server.icon_url)
        await self.client.send_message(self.message.channel, embed=embed)
        print("[{}] [{}] [SUCCESS] {} ({}) executed {}".format(self.message_time, self.message.server, self.message.author, self.message.id,self.message.content))

    async def user(self):
        if self.message.content == '.user':
            member = self.message.author
            await self.user_call(member)
        else:
            user = str(self.message.content).replace(".user ", "")
            for member in self.message.server.members:
                if (str(user) == str(member.name).lower()) or (str(user) == str(member.nick).lower() and member.nick != None) or (str(user).replace("!", "") == str(member.mention).replace("!", "")) or (str(user) == member.id) or (str(user) == str(member.name).lower() + "#" + str(member.discriminator)):
                    if str(user) == str(member.name).lower():
                        for y in self.message.server.members:
                            if (str(member.name).lower() == str(y.name).lower() and member.id != y.id) or (str(member.name).lower() == str(y.nick).lower() and member.id != y.id):
                                await self.client.send_message(self.message.channel, "There is more than 1 user with the same name/nickname")
                                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: More than 1 user with same nickname".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
                                return
                    if str(user) == str(member.nick).lower() and member.nick != None:
                        for y in self.message.server.members:
                            if (str(member.nick).lower() == str(y.name).lower() and member.id != y.id) or (str(member.nick).lower() == str(y.nick).lower() and member.id != y.id):
                                await self.client.send_message(self.message.channel, "There is more than 1 user with the same name/nickname")
                                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: More than 1 user with same nickname".format(self.message_time, self.message.server, self.message.author, self.message.id, self.message.content))
                                return
                    await self.user_call(member)
                    break
            else:
                await self.client.send_message(self.message.channel, "User not found")
                print("[{}] [{}] [FAILURE] {} ({}) executed {}\nReason: User not found".format(self.message_time,self.message.server,self.message.author, self.message.id, self.message.content))