import discord
from discord.ext import commands
import random
import os

description = '''hola esto te pude ayudar a usar el bot'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def conta(ctx):
    """Te muestra la realidad de la contaminación"""
    img = random.choice ( os.listdir ( 'imagenes' ) )
    with open(f'imagenes/{img}', 'rb') as f:
        # ¡Vamos a almacenar el archivo de la biblioteca Discord convertido en esta variable!
        picture = discord.File(f)
    # A continuación, podemos enviar este archivo como parámetro.
    await ctx.send(file=picture)


@bot.command()
async def tip(ctx):
    list_tip = ["Reduce, Reutiliza y Recicla",
                "Usa transporte sostenible",
                "Ahorra energía", "Reduce el consumo de agua",
                "Consume de forma responsable",
                " No tires basura en la calle o en la naturaleza",
                "Educa y sensibiliza a los demás"]
    tipi = random.choice(list_tip)
    await ctx.send(tipi)


@bot.command()
async def reciclar(ctx,object):
    """te ayuda a reciclar"""
    if object == "papel":
        await ctx.send("https://youtu.be/jTErK7A2XXU")
    elif object == "carton":
        await ctx.send("https://www.youtube.com/watch?v=vSKG6yOGaXs")
    elif object == "botella":
        await ctx.send("https://www.youtube.com/watch?v=wgVhEcMkCiY")
    elif object == "lata":
        await ctx.send("https://www.youtube.com/watch?v=s-8KrN01aVo")
    elif object == "tapas":
        await ctx.send("https://www.youtube.com/watch?v=83qcTV-C1UE")
    elif object == "poliestireno":
        await ctx.send("https://www.youtube.com/watch?v=bZ2QmLdfI_k")
    elif object == "recipiente":
        await ctx.send("https://www.youtube.com/watch?v=FGg2GwuVuSE")


bot.run('token')
