import discord
import discord_token
import logging
import re

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
how_member = "Go to #:computer:wiki, and redeem the codes in-game. For further assistance, please go to #📩support."
smart_responses = {"how//member": how_member, "where//member": how_member,
                   "can i//member": how_member, "dont//have//member": how_member,
                   "didnt//member": how_member}


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
    print(client.users[1].name)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    else:
        respond = smartMatch(filterMessage(message.content), smart_responses)
        if respond:
            await message.channel.send(respond)



if __name__ == "__main__":
    token = discord_token.token
    client.run(token)
