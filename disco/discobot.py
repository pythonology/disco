import aiohttp
import os

from discord.ext import commands


class DiscoBot(commands.Bot):
    def __init__(self, command_prefix, formatter=None, description=None,
                 pm_help=False, **options):
        commands.Bot.__init__(self, command_prefix, formatter=formatter,
                              description=description, pm_help=pm_help,
                              **options)

        self.service = None

    async def download_attachment(self, author, attachment):
        path = os.path.join('attachments', author.name)
        if not os.path.exists(path):
            os.makedirs(path)

        url = attachment['url']
        filename = attachment['filename']

        with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                with open(os.path.join(path, filename), 'wb') as f:
                    while True:
                        chunk = await resp.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)

        return 'disco://%s/%s' % (author.name, filename)
