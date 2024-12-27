import nextcord
import asyncio
from nextcord.ext import commands

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

admin_id = 
TOKEN = ""

@bot.event
async def on_ready():
    print(f'로그인 완료: {bot.user}')

@bot.slash_command(name='리뷰', description="리뷰를 작성합니다.")
async def review(interaction: nextcord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        embed = nextcord.Embed(
            title="권한 없음",
            description="이 명령어는 관리자만 사용할 수 있습니다.",
            color=nextcord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    embed = nextcord.Embed(
        title="리뷰", 
        description="아래 버튼을 눌러 리뷰를 작성해주세요.", 
        color=nextcord.Color.green()
    )
    await interaction.response.send_message(embed=embed, view=RvButton(interaction))

class RvButton(nextcord.ui.View):
    def __init__(self, interaction):
        super().__init__(timeout=None)
        self.interaction = interaction

    async def send_to_channel(self, number, message):
        channel_id = 1219612683381375036
        channel = self.interaction.guild.get_channel(channel_id)
        if channel:
            stars = "⭐" * number
            embed = nextcord.Embed(
                title="리뷰", 
                description=f"평점: {stars}\n리뷰 내용: {message}", 
                color=nextcord.Color.green()
            )
            await channel.send(embed=embed)

    @nextcord.ui.button(label="⭐", style=nextcord.ButtonStyle.primary, row=0)
    async def first_button_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("1점을 선택하셨습니다.", ephemeral=True)
        await self.collect_review(1)

    @nextcord.ui.button(label="⭐⭐", style=nextcord.ButtonStyle.primary, row=0)
    async def second_button_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("2점을 선택하셨습니다.", ephemeral=True)
        await self.collect_review(2)

    @nextcord.ui.button(label="⭐⭐⭐", style=nextcord.ButtonStyle.primary, row=0)
    async def third_button_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("3점을 선택하셨습니다.", ephemeral=True)
        await self.collect_review(3)

    @nextcord.ui.button(label="⭐⭐⭐⭐", style=nextcord.ButtonStyle.primary, row=1)
    async def fourth_button_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("4점을 선택하셨습니다.", ephemeral=True)
        await self.collect_review(4)

    @nextcord.ui.button(label="⭐⭐⭐⭐⭐", style=nextcord.ButtonStyle.primary, row=1)
    async def fifth_button_callback(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.response.send_message("5점을 선택하셨습니다.", ephemeral=True)
        await self.collect_review(5)

    async def collect_review(self, number):
        await self.interaction.followup.send("리뷰 내용을 입력해주세요. (10분 이내)", ephemeral=True)
        try:
            response = await bot.wait_for(
                'message', 
                check=lambda m: m.author == self.interaction.user, 
                timeout=600
            )
        except asyncio.TimeoutError:
            await self.interaction.followup.send("시간 초과로 리뷰 작성이 취소되었습니다.", ephemeral=True)
        else:
            await self.send_to_channel(number, response.content)


bot.run(TOKEN)
