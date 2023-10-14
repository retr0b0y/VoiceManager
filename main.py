import discord
import os
from dotenv import load_dotenv

load_dotenv()

class MyBot(discord.Bot):
    async def on_ready(self):
        print(f'Logged in as {self.user.name} (id: {self.user.id})')

    def add_custom_commands(self):
        @self.slash_command(name = "info", description = "Get info about bot")
        async def info(ctx):
            await ctx.respond("--- Coming soon ---")

        @self.slash_command(name = "ping", description = "Ping the bot")
        async def ping(ctx):
            await ctx.respond("Pong (this means that everything is ok)")


def main():
    bot = MyBot()
    bot.add_custom_commands()
    bot.run(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    main()
