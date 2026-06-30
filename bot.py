import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import utils

# Dotenv
load_dotenv('conf/.env')

token = os.getenv('token')

# Intents
intents = discord.Intents.default()
intents.message_content = True


# Bot object
bot = commands.Bot(command_prefix="!", intents=intents)

# Commands
@bot.command()
async def lista(ctx):
    complete_list = utils.read_movie_list()
    template_filled = utils.template_list(complete_list)

    await ctx.send(template_filled)


@bot.command()
async def pelicula(ctx, movie):
    movie_data = utils.read_movie_list()[int(movie) - 1]
    embed = discord.Embed(
        title=f"{movie_data['title']} ({movie_data['rating']} :star:)",
        description=movie_data['synopsis']
    )

    embed.set_author(name='https://github.com/zsendokame/mobot')
    embed.set_image(url=movie_data['poster'])

    await ctx.send(embed=embed)


@bot.command()
async def buscar(ctx, movie):
    query_results = utils.imdb_search(movie)
    template_filled = utils.template_query(query_results)

    await ctx.send(template_filled)


@bot.command()
async def agregar(ctx, imdb_id):
    title = utils.add_movie(imdb_id, ctx.author.id)

    await ctx.send(f'Se añadio {title}')


@bot.command()
async def limpiar(ctx):
    utils.clear_movie_list()

    await ctx.send('Se ha limpiado la lista de películas')


bot.run(token)
