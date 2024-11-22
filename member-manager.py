import discord
from dotenv import load_dotenv
import os
from typing import List
load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
active_members: List[int] = []
delete_members: List[discord.Member] = []

with open("members.csv", "r")as f:
    for line in f:
        active_members.append(int(line.strip()))


@client.event
async def on_ready():
    target_guild: discord.Guild = None
    for guild in client.guilds:
        if guild.name == "デジクリ":
            target_guild = guild
            break
    async for member in target_guild.fetch_members():
        # 既存部員のリストに居ないかつ、OBOGじゃないかつ、Botじゃない人を削除対象者に追加
        if (
            member.id not in active_members and
            client.guilds[0].get_role(756079579768291368) not in member.roles and
            client.guilds[0].get_role(538012097485864961) not in member.roles
        ):
            # オブジェクトのままで扱います。
            delete_members.append(member)

    print(f"削除対象者数: {len(delete_members)}")
    print([f"{member.id}#{member.display_name}\n" for member in delete_members])

    key = input("削除しますか？(y/n)")
    if key == "y":
        for member in delete_members:
            # reasonは監査ログに残るもので、キックした本人に対しては理由が見えません。
            # キックした理由を伝えたい場合はDMで伝えるなどしてください。
            await target_guild.kick(
                discord.Object(id=member.id),
                reason="未継続の部員の削除"
            )
            print(f"{member}を削除しました")


client.run(os.getenv("DISCORD_BOT_TOKEN"))
