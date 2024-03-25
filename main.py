import discord
from discord.ext import commands
import yaml

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='start')
async def start_command(ctx):
    file_path = 'sas.yml'
    desired_encoding = 'UTF-8'

    try:
        with open(file_path, encoding=desired_encoding) as file:
            data = yaml.safe_load(file)
    except FileNotFoundError:
        await ctx.send("Файл не найден!")
        return
    except UnicodeDecodeError:
        await ctx.send("Ошибка декодирования файла!")
        return

    embed = discord.Embed(description='Нажмите на кнопку "Начать"')

    message = await ctx.send(embed=embed)

    async def button_callback(interaction):
        text = ''
        for item in data:
            text += f'{item["id"]}. {item["text"]} :\n\n'

        await interaction.response.send_message(text)

    view = discord.ui.View()
    button = discord.ui.Button(label='Начать', style=discord.ButtonStyle.blurple, custom_id='show_text_button')
    button.callback = button_callback
    view.add_item(button)

    await message.edit(embed=embed, view=view)

bot.run('Secret')
