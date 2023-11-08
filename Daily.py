import datetime

class DailyCaller:

    def __init__(self, message=None, message_time=None, client=None, discord=None):
        self.message = message
        self.message_time = message_time
        self.client = client
        self.discord = discord
        self.file = open('D:/Documents/Discord/daily.txt', 'a', encoding='utf8')
        self.file_read = open('D:/Documents/Discord/daily.txt', 'r', encoding='utf8')

    async def sorting(self):
        if str(datetime.datetime.now())[:10] in self.file_read.read():
            self.file.write(' '+self.message.content)
            mgs = []
            async for x in self.client.logs_from(self.message.channel, limit=10):
                mgs.append(x)
            try:
                await self.client.delete_messages(mgs)
            except self.discord.errors.ClientException:
                await self.client.delete_message(self.message)
            self.file.close()
            self.file_read = open('D:/Documents/Discord/daily.txt', 'r', encoding='utf8')
            msg = '```\n' + str(datetime.datetime.now())[:10] + '\n' + (self.file_read.read().split(str(datetime.datetime.now())[:10])[1])[-1980:] + '```'
            await self.client.send_message(self.message.channel, msg)
            self.file.close()

        else:
            self.file.write('\n\n'+str(datetime.datetime.now())[:10]+'\n'+self.message.content)
            mgs = []
            async for x in self.client.logs_from(self.message.channel, limit=10):
                mgs.append(x)
            try:
                await self.client.delete_messages(mgs)
            except self.discord.errors.ClientException:
                await self.client.delete_message(self.message)
            self.file.close()
            self.file_read = open('D:/Documents/Discord/daily.txt', 'r', encoding='utf8')
            msg = '```\n' + str(datetime.datetime.now())[:10] + '\n' + (self.file_read.read().split(str(datetime.datetime.now())[:10])[1])[-1980:] + '```'
            await self.client.send_message(self.message.channel, msg)
            self.file.close()