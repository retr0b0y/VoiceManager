import discord
import os
from dotenv import load_dotenv

version = "0.1 (beta)"

load_dotenv()

class MyBot(discord.Bot):
    def __init__(self):
        discord.Bot.__init__(self)
        self.lobby_channel = {
            "id": None,
            "category_id": None
        }
        self.temp_channels = []
        self.last_text_channel = None


    async def on_ready(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="use /help for info"))
        print(f'Logged in as {self.user.name} (id: {self.user.id})')

    async def on_voice_state_update(self, member, before, after):
        if after.channel and self.lobby_channel["id"]:
            if after.channel.id == self.lobby_channel["id"]:
                channel_name = f"{member.name}`s channel"
                if not any(elem['channel_name'] == channel_name for elem in self.temp_channels):
                    new_temp_channel = await after.channel.guild.create_voice_channel(channel_name, category=self.get_channel(self.lobby_channel["category_id"]))
                    self.temp_channels.append({"channel_name": channel_name, "channel_obj": new_temp_channel})
                    await member.move_to(new_temp_channel)
                else:
                    await self.last_text_channel.send(f"Sorry, but your channel already exists!")
                    print("Channel exist already")
        if before.channel:
            for temp_channel in self.temp_channels:
                if before.channel.name == temp_channel["channel_obj"].name and len(before.channel.members) < 1:
                    await before.channel.delete()

    def set_last_text_channel(self, channel):
        self.last_text_channel = channel

    def add_commands(self):
        @self.slash_command(name="help", description="Get information about using the bot")
        async def help(ctx):
            embed = discord.Embed(
                title="VoiceManager Bot Help",
                description="",
                color=discord.Colour.blurple(),
            )
            embed.add_field(name="➜ What is it?", value="This is a simple Discord bot for voice channel management", inline=False)
            embed.add_field(name="➜ Commands", value="", inline=False)
            embed.add_field(name="Command", value="""
            `/create_lobby_channel`
            `/delete_lobby_channel`
            `/ping`
            `/version`
            `/help`
            """, inline=True)
            embed.add_field(name="Description", value="""
            Create a lobby channel, joining which will create a temporary channel
            Delete a lobby channel
            Check the bot's latency
            Check the bot's version
            Get information about using the bot (this message)
            """, inline=True)
 
            logo = discord.File("./static/images/logo.png", filename="logo.png")
            profile = discord.File("./static/images/profile.jpg", filename="profile.jpg")
            embed.set_author(name="retr0b0y (github)\nretr0b0y73 (discord)", icon_url="attachment://profile.jpg")
            embed.set_thumbnail(url="attachment://logo.png")
 
            await ctx.respond(files=[logo, profile], embed=embed)
            self.set_last_text_channel(ctx.channel)

        @self.slash_command(name="version", description="Check the bot's version")
        async def ping(ctx):
            await ctx.respond(f"Current bot version is {version}.")
            self.set_last_text_channel(ctx.channel)

        @self.slash_command(name="ping", description="Check the bot's latency")
        async def ping(ctx):
            await ctx.respond(f"Pong! Latency is {round(self.latency * 1000)}ms (server - {ctx.guild.name}).")
            self.set_last_text_channel(ctx.channel)

        @self.slash_command(name="create_lobby_channel", description="Create a lobby channel, joining which will create a temporary channel")
        async def create_lobby(ctx, lobby_channel_name: discord.Option(str, description="Enter the name of the channel lobby", required=True), 
                                    category_name: discord.Option(discord.CategoryChannel, description="Specify the category in which you want to create a lobby channel, if you need", required=False)):
            new_lobby_channel = await ctx.guild.create_voice_channel(lobby_channel_name, category=category_name if category_name else None) #, user_limit=members2move)
            self.lobby_channel["id"] = new_lobby_channel.id
            respond = f'Creating a lobby channel ___***{self.get_channel(self.lobby_channel["id"])}***___'
            if category_name:
                self.lobby_channel["category_id"] = new_lobby_channel.category_id
                respond += f' in the category ___***{self.get_channel(self.lobby_channel["category_id"])}***___'
            await ctx.respond(f'{respond}, please wait ...')
            self.set_last_text_channel(ctx.channel)

        @self.slash_command(name="delete_lobby_channel", description="Delete a lobby channel")
        async def delete_lobby(ctx):
            if self.lobby_channel["id"]:
                channel = self.get_channel(self.lobby_channel["id"])
                await channel.delete()
                self.lobby_channel["id"] = None
                self.lobby_channel["category_id"] = None
                await ctx.respond(f'The lobby channel has been successfully deleted!')
            self.set_last_text_channel(ctx.channel)

def main():
    bot = MyBot()
    bot.add_commands()
    bot.run(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    main()
