import discord
from dotenv import load_dotenv
import os
load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)
active_members = []
with open("members.csv","r")as f:
    for line in f:
        active_members.append(int(line.strip()))

delete_members = []
@client.event
async def on_ready():
    target_guild:discord.Guild = None
    for guild in client.guilds:
        if guild.name == "デジクリ":
            target_guild = guild
            break
    async for member in target_guild.fetch_members():
        #print(member.name)
        # 既存部員のリストに居ないかつ、OBOGじゃないかつ、Botじゃない人を削除対象者に追加
        if member.id not in active_members and  client.guilds[0].get_role(756079579768291368) not in member.roles and client.guilds[0].get_role(538012097485864961) not in member.roles:
            delete_members.append(f"{member.id}#{member.display_name}")
    for member in delete_members:
        print(member)
    print(f"削除対象者数: {len(delete_members)}")
    key = input("削除しますか？(y/n)")
    if key == "y":
        for member in delete_members:
            id = int(member.split("#")[0])
            await target_guild.kick(discord.Object(id=id), reason="未継続の部員の削除(継続していて削除された場合はMattermostもしくはメール(contact@digicre.net)にてご相談ください)")
            print(f"{member}を削除しました")


client.run(os.getenv("DISCORD_BOT_TOKEN"))