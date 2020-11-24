import os
import time
import random
import discord
from discord.ext import commands

from load_environment import load_environment
from bot_functions import discord_message_analysis
from bot_functions import bad_word_finder

# TODO: add logger

load_environment()

BOT_TOKEN = os.getenv('BOT_TOKEN')
PREFIX = '!'

bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'{bot.user.name} в сети.')


@bot.event
async def on_member_join(member):
    # TODO: с помощью рандома сделать три вида приветствий

    await member.send(f'Рад тебя видеть, {member.mention}, добро пожаловать! '
                      f'Можешь ознакомиться со списком доступных команд !help и обязательно прочти наши !rules. '
                      f'Мой баннхаммер не знает пощады!')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'{ctx.author.mention}, команда не идентифицирована. Пожалуйста, введите корректную команду.')


@bot.event
async def on_message(message):
    message_author = message.author

    if message_author != bot.user and not message.content.startswith('!'):
        try:
            result = discord_message_analysis(message)
        except UnboundLocalError:
            result = -1

        if result == 'hello':
            await message.channel.send(f'{message_author.mention}, привет!')
        elif result == 'bad':
            bad_word = bad_word_finder(message)
            await message.channel.send(f'Так ты сам, {message_author.mention}, {bad_word} получается.')
        elif result == 'help':
            await message.channel.send(f'{message_author.mention}, придется подождать... Help скоро будет закончен.')

    await bot.process_commands(message)


@bot.command()
async def help(ctx):
    await ctx.channel.purge(limit=1)

    embed = discord.Embed(colour=discord.Color.gold(), title='Навигация по командам:')
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    embed.add_field(name=f'{PREFIX}help', value='Выводит список команд.')
    embed.add_field(name=f'{PREFIX}rules', value='Выводит список правил сервера.')
    embed.add_field(name=f'{PREFIX}duel @target_name', value='Позволяет вызвать на дуэль и испытать удачу. '
                                                             'Проигравший отправляется в мут на 60 секунд.')

    await ctx.send(embed=embed)


@bot.command()
async def rules(ctx):  # TODO: залить мем "МОЖНО СКАЖУ?" на сервер и бот должен её скидывать при этой фразе
    await ctx.channel.purge(limit=1)

    embed = discord.Embed(colour=discord.Color.gold(), title='Правила сервера:')
    embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)
    embed.add_field(name='0.', value='Всегда уважай Великий Разум!', inline=True)
    embed.add_field(name='1.', value='Это сервер друзей для друзей, будь дружелюбнее.', inline=True)
    embed.add_field(name='2.', value='Запрещено быть душным мудилой и говорить "можно скажу?" в голосовом чате.',
                    inline=True)

    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount_to_delete=2):
    await ctx.channel.purge(limit=amount_to_delete)


@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)

    mute_role = discord.utils.get(ctx.message.guild.roles, name='Заключенный')
    await member.add_roles(mute_role)

    await ctx.send(f'Великий Разум пожелал, чтобы {member.mention} немного помолчал.')
    await member.send(f'Фреймы призваны защищать и помогать людям, поэтому я здесь. Тебя забанил {ctx.author.name}.')


@bot.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)

    mute_role = discord.utils.get(ctx.message.guild.roles, name='Заключенный')
    await member.remove_roles(mute_role)

    await ctx.send(f'Великий Разум сжалился над {member.mention} и он снова может говорить.')
    await member.send(f'Ты снова можешь говорить. '
                      f'Пожалуйста, для твоего блага, постарайся больше не раздражать Великий Разум.')


@bot.command()
async def duel(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)

    duelist1 = ctx.author.name
    duelist2 = member.name
    duelists = [duelist1, duelist2]

    mute_role = discord.utils.get(ctx.message.guild.roles, name='Заключенный')

    await ctx.send(f'{duelist1} бросает перчатку вызова {duelist2}. Приготовиться к дуэли! '
                   f'Великий Разум назначил меня вашим секундантом.')
    await ctx.send(f'3!')
    await ctx.send(f'2!')
    await ctx.send(f'1!')
    await ctx.send(f'Начинайте дуэль!')

    winner = random.choice(duelists)
    loser = duelist2 if duelist1 == winner else duelist1

    await ctx.send(f'Победил {winner}! Бездыханное тело {loser} ждет своего призрака. Или он более не достоин Света?!')

    if loser == duelist2:
        await member.add_roles(mute_role)
        time.sleep(60)
        await member.remove_roles(mute_role)
    else:
        await ctx.author.add_roles(mute_role)
        time.sleep(60)
        await ctx.author.remove_roles(mute_role)

    await ctx.send(f'Призрак в очередной раз вдохнул жизнь в {loser}.')


@bot.command()
async def status(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)

    await ctx.send(f'Name = {member.name}, Status = {member.desktop_status}, Role = {member.top_role}')

# Команда '!boobs' - загружает из интернета рандомную фотку сисек и постит её в дискорд-чате.


bot.run(BOT_TOKEN)
