import discord
from discord.ext import commands
from discord_secrets import dc_token, uploadChannel,imageRequests

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

imageFolder = "discord_bot/images"

class Button(discord.ui.View):
    def __init__(self, *, timeout = 180,message,picture):
        super().__init__(timeout=timeout)
        self.user_message = message
        self.picture = picture
    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green)
    async def approve_callback(self,interaction: discord.Interaction, button):
        print(f"Upload: {self.picture.filename} | {self.picture.content_type}")
        await self.picture.save(fp=f"{imageFolder}/{self.picture.filename}")
        await self.user_message.clear_reactions()
        await self.user_message.add_reaction("✅")
        approval_message = f"Der Upload der Datei **[{self.picture.filename}](https://discord.com/channels/{self.user_message.guild.id}/{self.user_message.channel.id}/{self.user_message.id})** wurde von {interaction.user.mention} angenommen"
        await interaction.response.send_message(approval_message)
    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red)
    async def deny_callback(self,interaction: discord.Interaction, button):
        await self.user_message.clear_reactions()
        await self.user_message.add_reaction("❎")
        denial_message = f"Der Upload der Datei **[{self.picture.filename}](https://discord.com/channels/{self.user_message.guild.id}/{self.user_message.channel.id}/{self.user_message.id})** wurde von {interaction.user.mention} abgelehnt"
        await interaction.response.send_message(denial_message)


@bot.listen()
async def on_message(message: discord.Message):
    if message.author.id != bot.user.id:
        pass
    if message.channel.id == uploadChannel:
        print(f"Correct Channel: {message.channel}")
        for picture in message.attachments:
            if not picture.content_type[0:5] == "image":
                await message.add_reaction("❎")
                await message.reply(f"Anhang {picture.filename} | {picture.content_type} ist nicht im unterstützten Dateinformat (jpeg/png) | Dateiformat: {picture.content_type}")
            else:
                await message.add_reaction("📨")
                requestChannel = bot.get_channel(imageRequests)
                request_message = f"**{message.author}** will die Datei **[{picture.filename}](https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id})** mit **~{round(picture.size/1000000),2}mb** hochladen"
                await requestChannel.send(request_message,view=Button(message=message,picture=picture))
            
@bot.listen()
async def on_ready():
    print("Online")
    
bot.run(dc_token)