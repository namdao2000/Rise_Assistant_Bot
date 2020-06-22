import discord
import discord_token
import logging
import re
from random import randint
from time import time
# Start of logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
# End of logging

# Main client object
client = discord.Client()

# Smart Matching shit
how_member = ", go to <#709949282949529713>, and redeem the codes in-game. For further assistance, please go to <#711209371820097566>."
hacker_response = ", suspecting a hacker? Please go to <#711209371820097566> and open a ticket."
glitch_response = ", suspecting a glitcher? Please go to <#711209371820097566> and open a ticket."
vault_response = ", vault wiped? Please go to <#711209371820097566> and open a ticket."
vault_disabled_response = ", vault not working? Please go to <#711209371820097566> and open a ticket."
how_raidalerts = ", need help with setting up Raid Alerts? Please see the tutorial in <#709949282949529713>."
smart_responses = {"how//member": how_member, "where//member": how_member,
                   "can i//member": how_member, "dont//have//member": how_member,
                   "didnt//member": how_member, "someone//is//hack": hacker_response, "help//hack": hacker_response,
                   "got//hack": hacker_response, "think//hack": hacker_response, "vault//my//wipe": vault_response,
                   "there//hacker//in": hacker_response, "there//hacker//on": hacker_response,
                   "how//alert": how_raidalerts, "vault//broken": vault_disabled_response,
                   "vault//not//work": vault_disabled_response, "vault//doesnt": vault_disabled_response,
                   "cant//vault": vault_disabled_response, "vault//disappeared": vault_disabled_response,
                   "lost//stuff//vault": vault_response, "my//vault//clear": vault_response,
                   "vault//disable": vault_disabled_response, "where//code": how_member,
                   "glitch//base": glitch_response, "vault//wipe": vault_response}

# Gif meme list
gif_meme = ["https://tenor.com/view/obi-wan-kenobi-star-wars-hello-there-ewan-mcgregor-gif-16358959",
            "https://tenor.com/view/hey-there-derp-puppy-dog-doggo-gif-13636895",
            "https://tenor.com/view/obi-wan-kenobi-star-wars-hello-there-ewan-mcgregor-gif-16358959",
            "https://tenor.com/view/who-the-fuck-pinged-me-gif-13512602"]


start_time = time()
daily_member_gain = 0


def smartMatch(message, smartResponses):
    match = False
    for key in smartResponses:
        keys = key.split("//")
        for item in keys:
            if not re.search(item, message.lower()):
                match = False
                break
            match = True
        if match:
            return smartResponses[key]
    return False


def filterMessage(message):
    filters = ["?", "'", "@", "#", "%", "$", "^", "*", "(", ")", "<", ">", "/", ":", "[", "]", "{", "}", ".", "|"]
    for filter in filters:
        message = message.replace(filter, "")
    return message


@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))

# Member count shit
@client.event
async def on_member_join(member):
    global daily_member_gain, start_time
    if time() - start_time > 86400:
        daily_member_gain = 0
        start_time = time()

    daily_member_gain += 1

    print("Joined")
    if daily_member_gain >=0:
        channel_name = "User: {} +{}".format(len(member.guild.members) - 11, daily_member_gain)
    if daily_member_gain < 0:
        channel_name = "User: {} -{}".format(len(member.guild.members) - 11, daily_member_gain)
    print(channel_name)
    await client.get_channel(722416312290115657).edit(name=channel_name)


@client.event
async def on_member_remove(member):
    global daily_member_gain, start_time
    if time() - start_time > 86400:
        daily_member_gain = 0
        start_time = time()

    daily_member_gain -= 1
    if daily_member_gain >= 0:
        channel_name = "User: {} +{}".format(len(member.guild.members) - 11, daily_member_gain)
    if daily_member_gain < 0:
        channel_name = "User: {} -{}".format(len(member.guild.members) - 11, daily_member_gain)

    print("Left")
    print(channel_name)
    await client.get_channel(722416312290115657).edit(name=channel_name)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    else:
        response = smartMatch(filterMessage(message.content), smart_responses)
        # General Match Response
        if response and message.channel.id == 303406962312347648:
            await message.channel.send("<@{}>".format(message.author.id) + response)
        # Ticket Tool Response
        elif re.search("Welcome, please wait for", message.content) and message.author.id == 557628352828014614:
            await message.channel.send(gif_meme[randint(0, 3)])
            await message.channel.send("Hello! Go to <#708890609150328952> and tell us which server you are from.")
            await message.channel.send("Example: ★ Risen Heroes ▌SEMI-VANILLA ▌RaidAlerts ▌x2.5▐")


if __name__ == "__main__":
    while True:
        try:
            token = discord_token.token
            client.run(token)
        except Exception:
            continue
