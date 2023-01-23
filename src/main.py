import discord
import os

# 自分のBotのアクセストークンに置き換えてください
TOKEN = os.environ['DISTOKEN']

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=discord.Intents.all())

# 起動時に動作する処理
@client.event
async def on_ready():

	ch_name = "bottest"

	for channel in client.get_all_channels():
		if channel.name == ch_name:
			await channel.send("起動しました")

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '!test':
        await message.channel.send('test')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)