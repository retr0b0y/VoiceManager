import discord
import os
from dotenv import load_dotenv

load_dotenv()

class MyBot(discord.Bot):
    async def on_ready(self):
        print(f'Logged in as {self.user.name} (id: {self.user.id})')

    def add_commands(self):
        @self.slash_command(name="help", description="Get information about using the bot")
        async def help(ctx):
            embed = discord.Embed(
                title="VoiceManager Bot Help",
                description="",
                color=discord.Colour.blurple(),
            )
            embed.add_field(name="➜ What is it?", value="This is a simple Discord bot for voice channel management.", inline=False)
            embed.add_field(name="➜ Commands", value="", inline=False)
            embed.add_field(name="Command", value="""
            `/ping`
            `/help`
            """, inline=True)
            embed.add_field(name="Description", value="""
            Check the bot's latency
            Get information about using the bot (this message)
            """, inline=True)
 
            logo = discord.File("./static/images/logo.png", filename="logo.png")
            profile = discord.File("./static/images/profile.jpg", filename="profile.jpg")
            embed.set_author(name="Developer: retr0b0y", icon_url="attachment://profile.jpg")
            embed.set_thumbnail(url="attachment://logo.png")
 
            await ctx.respond(files=[logo, profile], embed=embed)

        @self.slash_command(name="ping", description="Check the bot's latency.")
        async def ping(ctx):
            await ctx.respond(f"Pong! Latency is {round(self.latency * 1000)}ms")


def main():
    bot = MyBot()
    bot.add_commands()
    bot.run(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    main()
