import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv

load_dotenv()

description = '''Hola, soy un bot que te ayuda a concientizar sobre la contaminación y cómo reducirla.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', description=description, intents=intents, help_command=None)

TOKEN = os.getenv('DISCORD_TOKEN')

image_folder = 'contaminacion'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def adivina(ctx):
    """Juego visual: Adivina la imagen relacionada con la contaminación"""
    # Elegir una imagen al azar de la carpeta 'contaminacion'
    image_files = os.listdir(image_folder)
    image = random.choice(image_files)
    
    # Enviar la imagen
    image_path = f'{image_folder}/{image}'
    picture = discord.File(image_path)
    await ctx.send("¡Adivina qué es esta imagen relacionada con la contaminación!", file=picture)
    
    # Dar tiempo para que los usuarios adivinen
    def check(msg):
        return msg.author == ctx.author  # Solo el que inició el comando puede participar
    
    # Esperamos que el usuario adivine
    await ctx.send("Escribe tu adivinanza.")
    
    try:
        msg = await bot.wait_for('message', check=check, timeout=30.0)
        
        # Aquí puedes agregar las respuestas correctas, por ejemplo: "Basura", "Contaminación del aire", etc.
        # Vamos a asumir que el nombre del archivo es la respuesta correcta (sin la extensión).
        correct_answer = os.path.splitext(image)[0].lower()
        
        # Verificar la respuesta
        if msg.content.lower() == correct_answer:
            await ctx.send(f"¡Correcto! 🎉 La respuesta era: {correct_answer}. ¡Bien hecho!")
        else:
            await ctx.send(f"¡Incorrecto! 😞 La respuesta correcta era: {correct_answer}. ¡Inténtalo nuevamente!")
    
    except discord.ext.commands.errors.CommandInvokeError:
        await ctx.send("¡Oops! Se acabó el tiempo para adivinar. ¡Intenta nuevamente!")


questions = [
    {
        "question": "¿Cuánto de la basura plástica mundial se recicla?",
        "options": ["a) 50%", "b) 10%", "c) 91%", "d) 1%"],
        "answer": "b"
    },
    {
        "question": "¿Qué porcentaje de las emisiones globales de CO2 provienen de la deforestación?",
        "options": ["a) 5%", "b) 15%", "c) 20%", "d) 35%"],
        "answer": "c"
    },
    {
        "question": "¿Cuántas toneladas de residuos plásticos llegan al océano cada año?",
        "options": ["a) 5 millones", "b) 10 millones", "c) 15 millones", "d) 8 millones"],
        "answer": "d"
    },
    {
        "question": "¿Qué animal está en peligro de extinción debido a la contaminación de los océanos?",
        "options": ["a) Delfín", "b) Ballena azul", "c) Tortuga marina", "d) León marino"],
        "answer": "c"
    },
    {
        "question": "¿Cuál es el mayor productor de dióxido de carbono (CO2) en el mundo?",
        "options": ["a) Estados Unidos", "b) China", "c) India", "d) Rusia"],
        "answer": "b"
    }
]
puntaje = 0

@bot.command()
async def trivia(ctx):
    """Inicia un juego de trivia ecológica"""
    question = random.choice(questions)
    await ctx.send(f"**Pregunta de trivia ecológica**: {question['question']}")
    
    # Enviar las opciones
    options = '\n'.join(question['options'])
    await ctx.send(options)
    
    def check(msg):
        return msg.author == ctx.author and msg.content.lower() in ['a', 'b', 'c', 'd']

    # Esperamos la respuesta del jugador de manera sincrónica
    try:
        msg = await bot.wait_for('message', check=check, timeout=15.0)
        if msg.content.lower() == question['answer']:
            await ctx.send(f"¡Correcto! La respuesta es {msg.content.upper()}. 🎉")
            puntaje == puntaje + 1
        else:
            await ctx.send(f"¡Incorrecto! La respuesta correcta era {question['answer'].upper()}. 😞")
            puntaje == puntaje - 1
    except discord.ext.commands.errors.CommandInvokeError:
        await ctx.send("¡Oops! Hubo un error al procesar la trivia. Intenta nuevamente.")
        await ctx.send(puntaje)

@bot.command()
async def conta(ctx):
    """Te muestra la realidad de la contaminación"""
    img = random.choice(os.listdir('imagenes'))
    with open(f'imagenes/{img}', 'rb') as f:
        picture = discord.File(f)
    await ctx.send(file=picture)


@bot.command()
async def tip(ctx):
    """Te da un consejo para ayudar al medio ambiente"""
    list_tip = [
        "Reduce, Reutiliza y Recicla",
        "Usa transporte sostenible",
        "Ahorra energía",
        "Reduce el consumo de agua",
        "Consume de forma responsable",
        "No tires basura en la calle o en la naturaleza",
        "Educa y sensibiliza a los demás"
    ]
    tipi = random.choice(list_tip)
    await ctx.send(tipi)


@bot.command()
async def reciclar(ctx, object):
    """Te ayuda a reciclar de forma correcta"""
    reciclaje_info = {
        "papel": "https://youtu.be/jTErK7A2XXU",
        "carton": "https://www.youtube.com/watch?v=vSKG6yOGaXs",
        "botella": "https://www.youtube.com/watch?v=wgVhEcMkCiY",
        "lata": "https://www.youtube.com/watch?v=s-8KrN01aVo",
        "tapas": "https://www.youtube.com/watch?v=83qcTV-C1UE",
        "poliestireno": "https://www.youtube.com/watch?v=bZ2QmLdfI_k",
        "recipiente": "https://www.youtube.com/watch?v=FGg2GwuVuSE"
    }

    link = reciclaje_info.get(object.lower())
    if link:
        await ctx.send(link)
    else:
        await ctx.send("Lo siento, no tengo información sobre cómo reciclar ese objeto. Intenta con papel, cartón, botella, lata, tapas, poliestireno o recipiente.")


@bot.command()
async def help(ctx):
    """Muestra un mensaje de ayuda personalizado"""
    help_message = """
    **🌎 ¡Hola, soy tu bot ecológico! Vamos a salvar el planeta juntos, ¿listo? 🌱💪**

    **🦸‍♂️ Aquí tienes algunos de mis superpoderes (comandos):**

    ➡️ **/adivina** - ¡Un juego visual! Te mostraremos una imagen relacionada con la contaminación y tendrás que adivinar qué es. 🌍🧐 Tienes 30 segundos para dar tu respuesta. ¡Diviértete y aprende! 🎉💡

    ➡️ **/conta**: Te muestra una imagen impactante sobre la contaminación. ¡No te hagas el distraído! 🧹🗑️🚯

    ➡️ **/tip**: Te doy un consejo para cuidar la Tierra. ¡Hazlo por el futuro! 🌍💚🌞

    ➡️ **/reciclar <objeto>**: ¿No sabes si un objeto es reciclable? ¡Yo te ayudo a descifrarlo! Ejemplo: **/reciclar papel** ♻️📄

    ➡️ **/estadisticas**: ¡Datos escalofriantes sobre la contaminación global! 😱🌐📉

    ➡️ **/curiosidades**: ¡Datos curiosos sobre el medio ambiente que te dejarán con la boca abierta! 🤯🌳🦋

    ➡️ **/reto**: ¡Un desafío ecológico del día! 💪🌱 ¡Hazlo y el planeta te lo agradecerá! 🌏✨

    ➡️ **/huellacarbono**: Consejos para reducir tu huella de carbono. ¡Un pequeño cambio puede hacer una gran diferencia! 🌿🌍🚶‍♀️

    ➡️ **/frase**: Citas inspiradoras que te motivarán a cuidar el planeta. 💬🌟 "La Tierra no es una herencia de nuestros padres, sino un préstamo de nuestros hijos." – Proverbio indígena 👶

    ➡️ **/trivia**: ¡Pon a prueba tus conocimientos ecológicos con este juego de trivia! 🧠🎉🌎 ¿Te atreves a ganar? 🏆

    **🌱 ¡Recuerda! Cada acción cuenta, y juntos podemos lograr un mundo más verde y saludable. ¡Tú puedes ser parte del cambio!**

    **⚡️ Usa estos comandos y transforma tu huella en una huella verde. ¡Vamos a cambiar el mundo! 🌍💚**
    """
    await ctx.send(help_message)


@bot.command()
async def estadisticas(ctx):
    """Muestra estadísticas sobre el medio ambiente"""
    stats = [
        "El 91% de la basura plástica mundial no se recicla.",
        "Cada año, se pierden 18.7 millones de hectáreas de bosques.",
        "Se estima que hay más de 5 billones de piezas de plástico en los océanos.",
        "La deforestación contribuye al 20% de las emisiones globales de CO2."
    ]
    stat = random.choice(stats)
    await ctx.send(stat)


@bot.command()
async def curiosidades(ctx):
    """Muestra curiosidades sobre el medio ambiente"""
    curiosidades = [
        "Las ballenas jorobadas cantan canciones que pueden durar 30 minutos y viajar a través de miles de kilómetros.",
        "El 80% de la biodiversidad mundial se encuentra en los bosques tropicales.",
        "Los árboles en las ciudades pueden reducir las temperaturas hasta 10°C durante los días calurosos.",
        "En promedio, cada persona consume alrededor de 500 gramos de plástico cada semana sin saberlo."
    ]
    curiosidad = random.choice(curiosidades)
    await ctx.send(curiosidad)


@bot.command()
async def reto(ctx):
    """Desafío ecológico del día"""
    retos = [
        "Hoy no uses plástico de un solo uso. ¡Adiós a las bolsas plásticas!",
        "Planta una planta o árbol hoy para ayudar al medio ambiente.",
        "Apaga las luces cuando no las estés usando, ¡ahorra energía!",
        "Usa transporte público o camina para reducir tu huella de carbono."
    ]
    reto_del_dia = random.choice(retos)
    await ctx.send(f"¡Reto ecológico del día! {reto_del_dia}")


@bot.command()
async def huellacarbono(ctx):
    """Consejos para reducir tu huella de carbono"""
    consejos = [
        "Consume más alimentos vegetales y reduce el consumo de carne.",
        "Usa electrodomésticos y bombillas de bajo consumo energético.",
        "Recicla y reutiliza lo máximo posible.",
        "Prefiere el transporte público o el uso de bicicletas a los autos."
    ]
    consejo = random.choice(consejos)
    await ctx.send(f"Consejo para reducir tu huella de carbono: {consejo}")


@bot.command()
async def frase(ctx):
    """Envia una cita inspiradora sobre el medio ambiente"""
    frases = [
        "La Tierra no es una herencia de nuestros padres, sino un préstamo de nuestros hijos. – Proverbio indígena",
        "El medio ambiente no es un problema, es una solución. – Anónimo",
        "Lo que hacemos con la tierra, lo hacemos con nosotros mismos. – Chief Seattle",
        "La mejor forma de predecir el futuro es crearlo. – Abraham Lincoln"
    ]
    cita = random.choice(frases)
    await ctx.send(cita)



bot.run('token')
