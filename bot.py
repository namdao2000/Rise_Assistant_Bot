import discord
import discord_token

client = discord.Client()


@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('penis'):
        await message.channel.send('Yes Daddy I do 😩💧')
    else:
        print("{}: {}".format(message.author, message.content))
        await message.channel.send(message.content)


if __name__ == "__main__":
    token = discord_token.token
    client.run(token)
