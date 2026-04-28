from config import *
from logic import *
import discord
from discord.ext import commands
from config import TOKEN

# Veri tabanı yöneticisini başlatma
manager = DB_Map("database.db")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot başlatıldı!")

@bot.command()
async def start(ctx: commands.Context):
    await ctx.send(f"Merhaba, {ctx.author.name}. Mevcut komutların listesini keşfetmek için !help_me yazın.")

@bot.command()
async def help_me(ctx: commands.Context):
    await ctx.send(
        "Kullanılabilir komutlar:\n"
        "!start → Botu başlatır\n"
        "!help_me → Komutları listeler\n"
        "!show_city <şehir> → Belirtilen şehri haritada gösterir\n"
        "!show_my_cities → Kaydettiğin şehirleri haritada gösterir\n"
        "!remember_city <şehir> → Şehri kaydeder"
    )

@bot.command()
async def show_city(ctx: commands.Context, *, city_name=""):
    if not city_name:
        await ctx.send("Şehir İsmini Unuttunuz!")
        return
    manager.create_graph(f'{ctx.author.id}.png', [city_name])
    await ctx.send(file=discord.File(f'{ctx.author.id}.png'))

    # Belirtilen şehirle birlikte haritayı gösterecek komutu yazın.

@bot.command()
async def show_my_cities(ctx: commands.Context):
    cities = manager.select_cities(ctx.author.id)  # Kullanıcının kaydettiği şehirlerin listesini alma
    if cities:
        manager.create_graph(f'{ctx.author.id}_cities.png', cities)
        await ctx.send(file=discord.File(f'{ctx.author.id}_cities.png'))
    else:
        await ctx.send("Hiç Şehir Kaydetmediniz!")    

    # Kullanıcının şehirleriyle birlikte haritayı gösterecek komutu yazın

@bot.command()
async def remember_city(ctx: commands.Context, *, city_name=""):
    if manager.add_city(ctx.author.id, city_name):  # Şehir adının format uygunluğunu kontrol etme. Başarılıysa şehri kaydet!
        await ctx.send(f'{city_name} şehri başarıyla kaydedildi!')
    else:
        await ctx.send("Hatalı format. Lütfen şehir adını İngilizce olarak ve komuttan sonra bir boşluk bırakarak girin.")

if __name__ == "__main__":
    bot.run(TOKEN)
