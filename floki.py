import discord
from discord.ext import tasks
from pycoingecko import CoinGeckoAPI

gc = CoinGeckoAPI()
# perms: 2147616768
client = discord.Client()
global CURRENT_PRICE,CURRENT_VALUE


def api():
    api_return = gc.get_price(ids='shiba-inu', vs_currencies='usd')
    return format(float(api_return["shiba-inu"]["usd"]), '.8f'), float(api_return["shiba-inu"]["usd"])

def returnMessage():
    return f"@everyone current Shiba Inu price is `${api()[0]}`"

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$shib'):
        await message.channel.send(returnMessage())

@tasks.loop(minutes=5)
async def timerMessage():
    global CURRENT_PRICE, CURRENT_VALUE
    temp_price, temp_value = api()

    if CURRENT_VALUE * 1.05 < temp_value:
        CURRENT_PRICE = temp_price
        CURRENT_VALUE = temp_value
        message = f"@everyone PRICE INCREASE! Current price of Shiba Inu: ${temp_price}"
        channel = client.get_channel(YOUR CHANNEL HERE)
        await channel.send(message)

    elif CURRENT_VALUE * .95 > temp_value:
        CURRENT_PRICE = temp_price
        CURRENT_VALUE = temp_value
        message = f"@everyone PRICE DECREASE. Current price of Shib: ${temp_price}"
        channel = client.get_channel(YOUR CHANNEL HERE)
        await channel.send(message)


@client.event
async def on_ready():
    global CURRENT_PRICE, CURRENT_VALUE
    CURRENT_PRICE, CURRENT_VALUE = api()
    timerMessage.start()


client.run("YOUR TOKEN HERE")
