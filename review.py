import discord
import asyncio
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

admin_id = 1218194406147096580
TOKEN = "" #님 토큰
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.slash_command(name='리뷰')
async def review(ctx):
    embed = discord.Embed(title="리뷰", description="아래 버튼을 눌러 리뷰를 해주세요.", color=discord.Color.green())
    await ctx.respond(embed=embed, view=RvButton(ctx))

class RvButton(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx

    async def send_to_channel(self, number, message):
        channel_id = #리뷰 내용 전송할 채널 아이디
        channel = self.ctx.guild.get_channel(channel_id)
        if channel:
            stars = "⭐" * number
            embed =  discord.Embed(title="리뷰", description=f"평점: {stars}\n리뷰 내용: {message}",color=discord.Color.green())
            await channel.send(embed=embed)

    @discord.ui.button(label="⭐", style=discord.ButtonStyle.primary, row=0)
    async def first_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("1점을 선택하셨습니다.")
        await self.collect_review(1)

    @discord.ui.button(label="⭐⭐", style=discord.ButtonStyle.primary, row=0)
    async def second_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("2점을 선택하셨습니다.")
        await self.collect_review(2)

    @discord.ui.button(label="⭐⭐⭐", style=discord.ButtonStyle.primary, row=0)
    async def third_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("3점을 선택하셨습니다.")
        await self.collect_review(3)

    @discord.ui.button(label="⭐⭐⭐⭐", style=discord.ButtonStyle.primary, row=1)
    async def fourth_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("4점을 선택하셨습니다.")
        await self.collect_review(4)

    @discord.ui.button(label="⭐⭐⭐⭐⭐", style=discord.ButtonStyle.primary, row=1)
    async def fifth_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("5점을 선택하셨습니다.")
        await self.collect_review(5)

    async def collect_review(self, number):
        message = await self.ctx.send("리뷰 내용을 입력하세요.")
        try:
            response = await bot.wait_for('message', check=lambda m: m.author == self.ctx.author, timeout=60)
        except asyncio.TimeoutError:
            await message.delete()
            await self.ctx.send("시간이 초과되었습니다. 리뷰를 작성할 수 없습니다.")
        else:
            await message.delete()
            await self.send_to_channel(number, response.content)


bot.run(TOKEN)
