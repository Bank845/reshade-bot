import discord
from discord import app_commands, ui
import os

import os
TOKEN = os.environ.get("TOKEN")
SLIP_CHANNEL_ID = 123456789  # ID ช่อง #หลักฐานการโอน

PRODUCTS = {
    "basic":  {"name": "Reshade Basic",  "price": 20,  "desc": "preset เริ่มต้นสวยๆ"},
    "pro":    {"name": "Reshade Pro",    "price": 59,  "desc": "full pack + อัพเดตฟรี"},
    "bundle": {"name": "Reshade Bundle", "price": 99,  "desc": "ครบทุก preset + support"},
}

class ProductSelect(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=p["name"], value=k,
                description=f'{p["desc"]} — ฿{p["price"]}')
            for k, p in PRODUCTS.items()
        ]
        super().__init__(placeholder="✨ เลือก Reshade ที่ต้องการซื้อ",
                         options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        p = PRODUCTS[self.values[0]]
        embed = discord.Embed(
            title="📋 ยืนยันการสั่งซื้อ",
            description=(f"**สินค้า:** {p['name']}\n"
                         f"**ราคา:** ฿{p['price']}\n\n"
                         f"โอนเงิน ฿{p['price']} แล้วส่งสลิปใน <#{SLIP_CHANNEL_ID}>"),
            color=0x5865F2
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

class ShopView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ProductSelect())

class ShopBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"✅ บอทออนไลน์: {self.user}")

bot = ShopBot()

@bot.tree.command(name="shop", description="เปิดร้านค้าซื้อ Reshade")
async def shop(interaction: discord.Interaction):
    embed = discord.Embed(title="📢 ซื้อ Reshade อัตโนมัติ", color=0x57F287)
    embed.add_field(name="📢 วิธีการซื้อ", inline=False, value=(
        "› เลือก Reshade จากเมนูด้านล่าง\n"
        f"⬇ ส่งสลิปที่ <#{SLIP_CHANNEL_ID}>\n"
        "✅ รับลิ้งก์ดาวน์โหลดทาง DM ทันที"
    ))
    embed.add_field(name="🎀 ข้อควรระวัง", inline=False, value=(
        "• ตรวจสอบยอดเงินให้ถูกต้องก่อนโอน\n"
        "• ส่งเฉพาะไฟล์รูปภาพที่ชัดเจนเท่านั้น\n"
        "• สลิปแต่ละใบใช้ได้เพียง 1 ครั้งเท่านั้น\n"
        "• คิวหมดอายุใน 30 นาที หากไม่ส่งสลิป"
    ))
    await interaction.response.send_message(embed=embed, view=ShopView())

bot.run(TOKEN)