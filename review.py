import nextcord
import asyncio
from nextcord.ext import commands
from nextcord.ui import Button, View, Modal, TextInput

intents = nextcord.Intents.default()
intents.message_content = True

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

admin_id = #관리자 아이디
TOKEN = " " #봇 토큰

@bot.event
async def on_ready():
    print(f'로그인 완료: {bot.user}')

def is_admin(user):
    return user.id == admin_id

@bot.slash_command(name="리뷰", description="리뷰를 작성합니다.")
async def review(interaction: nextcord.Interaction):
    if not is_admin(interaction.user):
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
    await interaction.response.send_message(embed=embed, view=ReviewButton())

class ReviewButton(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="⭐", style=nextcord.ButtonStyle.primary, row=0)
    async def one_star(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.collect_review(interaction, 1)

    @nextcord.ui.button(label="⭐⭐", style=nextcord.ButtonStyle.primary, row=0)
    async def two_star(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.collect_review(interaction, 2)

    @nextcord.ui.button(label="⭐⭐⭐", style=nextcord.ButtonStyle.primary, row=0)
    async def three_star(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.collect_review(interaction, 3)

    @nextcord.ui.button(label="⭐⭐⭐⭐", style=nextcord.ButtonStyle.primary, row=1)
    async def four_star(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.collect_review(interaction, 4)

    @nextcord.ui.button(label="⭐⭐⭐⭐⭐", style=nextcord.ButtonStyle.primary, row=1)
    async def five_star(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await self.collect_review(interaction, 5)

    async def collect_review(self, interaction: nextcord.Interaction, stars: int):
        await interaction.response.send_message(f"{stars}점을 선택하셨습니다. 리뷰 내용을 입력해주세요. (10분 이내)", ephemeral=True)

        def check(message: nextcord.Message):
            return message.author == interaction.user and message.channel == interaction.channel

        try:
            message = await bot.wait_for("message", timeout=600, check=check)
        except asyncio.TimeoutError:
            await interaction.followup.send("시간 초과로 리뷰 작성이 취소되었습니다.", ephemeral=True)
            return

        await self.send_review_to_channel(interaction, stars, message.content)

    async def send_review_to_channel(self, interaction: nextcord.Interaction, stars: int, review_content: str):
        channel_id = #리뷰를 보낼 채널 아이디
        channel = interaction.guild.get_channel(channel_id)

        if not channel:
            await interaction.followup.send("리뷰 채널을 찾을 수 없습니다.", ephemeral=True)
            return

        stars_display = "⭐" * stars
        embed = nextcord.Embed(
            title="새로운 리뷰",
            description=f"작성자: {interaction.user.mention}\n평점: {stars_display}\n리뷰: {review_content}",
            color=nextcord.Color.green()
        )
        await channel.send(embed=embed)
        await interaction.followup.send("리뷰가 성공적으로 등록되었습니다.", ephemeral=True)

bot.run(TOKEN)
