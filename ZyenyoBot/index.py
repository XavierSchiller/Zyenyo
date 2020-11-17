import discord, os, json, ast
from discord.ext import commands
from shutil import copyfile
from re import sub
import botconfig

client = commands.Bot(command_prefix = botconfig.PREFIX)

###################
###[DEFINITIONS]###
###################
def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

def zbauto(server_name, channel_name):
    temp = open('../ZBotData/GroupCC/ZBA.json')
    zba = json.loads(temp.readline())
    temp.close()
    entry = f'{server_name} - {channel_name}'
    global file_number
    if entry in zba:
        zba[entry] = zba[entry] + 1
        file_number = zba[entry]
        replace_line("../ZBotData/GroupCC/ZBA.json", 0, json.dumps(zba))
    else:
        zba[entry] = 1
        replace_line("../ZBotData/GroupCC/ZBA.json", 0, json.dumps(zba))
        file_number = 1

temp = open('../ZBotData/char_count_DB.json')
chc = json.loads(temp.readline())
temp.close()

@client.command()
async def load(ctx, extension):
    if ctx.author.id == 642193466876493829:
        client.load_extension(f'cogs.{extension}')
        await ctx.send("Successfully loaded the module.")
    else:
        await ctx.send("Please don't try to break me.")
@client.command()
async def unload(ctx, extension):
    if ctx.author.id == 642193466876493829:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send("Successfully unloaded the module.")
    else:
        await ctx.send("Don't try to break me.")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

####################
#####[COMMANDS]#####
####################

@client.event
async def on_message(message):
    if message.author.bot:
        return
    char_count = len(message.content)
    un = message.author.id
    if f'{un}_tmc' in chc:
        chc[f'{un}'] = chc[f'{un}'] + char_count
        chc[f'{un}_tmc'] = chc[f'{un}_tmc'] + 1
        replace_line("../ZBotData/char_count_DB.json", 0, json.dumps(chc))
    else:
        chc[f'{un}'] = char_count
        chc[f'{un}_tmc'] = 1
        replace_line("../ZBotData/char_count_DB.json", 0, json.dumps(chc))
    await client.process_commands(message)


@client.command()
async def stats(message):
    un = message.author.id
    totalChars = chc[f'{un}']
    totalMsgs = chc[f'{un}_tmc']
    tAvgChar = round(totalChars / totalMsgs, 2)
    await message.channel.send(f'Average character count: . . . . . . . . . . **`{tAvgChar}`**\nTotal character count: . . . . . . . . . . . . . **`{totalChars}`**\nTotal messages sent: . . . . . . . . . . . . . . **`{totalMsgs}`**')



@client.command()
async def cstats(message):
    un = message.author.id
    totalChars = bchc[f'{un}']
    totalMsgs = bchc[f'{un}_tmc']
    tAvgChar = round(totalChars / totalMsgs, 2)
    await message.channel.send(f'Average character count: . . . . . . . . . . **`{tAvgChar}`**\nTotal character count: . . . . . . . . . . . . . **`{totalChars}`**\nTotal messages sent: . . . . . . . . . . . . . . **`{totalMsgs}`**')

## bchc is Big-CHaracter-Count.

@client.command()
async def carch(ctx, arg1, arg2):
    arh = sub("<#|>", "", arg1)
    channel = client.get_channel(int(arh))
    server = ctx.message.guild.name
    copyfile('../ZBotData/cccopy.json', '../ZBotData/c.json')
    temper = open('../ZBotData/c.json')
    global bchc
    bchc = json.loads(temper.readline())
    temper.close()
    async for message in channel.history(limit=int(arg2)):
        if message.author.bot:
            pass
        else:
            char_count = len(message.content)
            un = message.author.id
            if f'{un}_tmc' in bchc:
                bchc[f'{un}'] = bchc[f'{un}'] + char_count
                bchc[f'{un}_tmc'] = bchc[f'{un}_tmc'] + 1
                replace_line("../ZBotData/c.json", 0, json.dumps(bchc))
            else:
                bchc[f'{un}'] = char_count
                bchc[f'{un}_tmc'] = 1
                replace_line("../ZBotData/c.json", 0, json.dumps(bchc))
    zbauto(server, channel)
    os.rename('../ZBotData/c.json', f'../ZBotData/GroupCC/{server} - {channel} ({file_number}).json')
    await ctx.send("Done!")


client.run(botconfig.token)
