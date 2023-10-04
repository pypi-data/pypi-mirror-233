import os, traceback

from discord.ext import commands

from koreanbots.integrations.discord import DiscordpyKoreanbots
from topgg import DBLClient 

from .logging import log


class BotNotReady(Exception):
    def __init__(self):
        """
        Sync 중 봇이 준비되어 있지 않으면 발생합니다.
        """

        super().__init__("The bot is not ready.")

class Bot(commands.Bot):

    def __init__(self, command_prefix=commands.when_mentioned, **options):
        
        self.koreanbots = None

        super().__init__(command_prefix, **options)

    def sync_lists(self, koreanbots: str = None, topgg: str = None):
        """봇 리스트와 봇을 동기화합니다.

        ## Args:
            koreanbots: `str`
                한디리의 토큰이 입력됩니다.

        ## Returns:
            언어의 이름이 리턴됩니다.
        """

        if self.is_ready() == False:
            raise BotNotReady()

        if koreanbots:
            try:
                self.koreanbots = DiscordpyKoreanbots(
                    client=self,
                    api_key=koreanbots, 
                    run_task=True,
                )

            except Exception as e: return log.error(f"koreanbots.dev: {e}")

        if topgg:
            try:
                self.topgg = DBLClient(
                    bot=self,
                    token=topgg, 
                    autopost=True
                )

            except Exception as e: return log.error(f"top.gg: {e}")

        return log.info(f"Sync completed successfully.")

        
    async def cog_load(self, list_dir: str) -> None:

        for i in os.listdir(list_dir):
            if i.endswith(".py") == False:
                continue

            list_dir = list_dir.replace('./', '')
            
            try:
                self.load_extension(f"{list_dir}.{i[:-3]}")
                log.info(f"{list_dir}.{i[:-3]} has been loaded.")
                
            except:
                return log.error(traceback.format_exc())

        await self.sync_commands()
        
        print("")
        return log.info(f"{self.user} has finished loading.\n")