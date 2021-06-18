import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context
import datetime
import json

worker_list = list()
counter = 0
current_worker = str()
current_helper = str()
main_channel = 0
global is_starting
client = commands.Bot(command_prefix=["kit ", "Kit ", "KIt ", "KIT ", "kIt ", "kIT ", "kiT "],
                      case_insensitive=True, help_command=None)


def set_day(day: str):
    if day == "mo":
        value = 0
    elif day == "di":
        value = 1
    elif day == "mi":
        value = 2
    elif day == "do":
        value = 3
    elif day == "fr":
        value = 4
    elif day == "sa":
        value = 5
    elif day == "so":
        value = 6
    else:
        value = -1   # Fehler
    return value


def convert_daynumber_to_day(day: int):
    value = ""
    if day == 0:
        value = "Montag"
    elif day == 1:
        value = "Dienstag"
    elif day == 2:
        value = "Mittwoch"
    elif day == 3:
        value = "Donnerstag"
    elif day == 4:
        value = "Freitag"
    elif day == 5:
        value = "Samstag"
    elif day == 6:
        value = "Sonntag"
    return value


def save_json():
    with open("savefile.json", "w") as savefile_write:
        json.dump(save, savefile_write)
        savefile_write.close()


try:
    with open("savefile.json") as savefile_read:
        save = json.load(savefile_read)
        savefile_read.close()
except:
    with open("savefile.json", "w") as savefile_created:
        savefile_created.write("{}")
        save = {}
        savefile_created.close()

with open("token.json") as json_file:
    token = json.load(json_file).get("token")
    json_file.close()


@client.event
async def on_ready():
    global is_starting
    is_starting = True
    print('Bot has logged in as {0.user}'.format(client))
    save.update({"remind": False})
    await service_routine.start()


@tasks.loop(seconds=8)
async def service_routine():
    global save
    global current_worker
    global is_starting
    save_json()

    weekday = datetime.date.today().weekday()
    now = datetime.datetime.now().hour
    if weekday != save["time"][0]:
        save.update({"remind": True})
    if not is_starting:
        if weekday == save["time"][0] and now >= save["time"][1] and save["remind"]:
            save.update({"remind": False})
            print("Neuer Küchendienst wurde mitgeteilt")
            try:
                channel = client.get_channel(main_channel)
                await kit_next(channel)
            except AttributeError:
                print("No text send")
        else:
            print("not notified")
    else:
        is_starting = False
        #print("Bot ist am starten und Küchendienst wird sich nicht ändern")


@client.command(name="setup", pass_context=True)
async def kit_setup(ctx: Context, *users: discord.User):
    if ctx.author == client.user:
        return
    if len(users) >= 2:
        global main_channel
        global worker_list
        global save
        global current_worker
        defined = False
        worker_string = ""

        main_channel = ctx.channel.id
        save.update({"worker": {}, "time": [0, 9], "helper": {}})
        for arg in users:
            save["worker"].update({arg.id: 0})

        for worker in save["worker"]:
            if not defined:
                save["worker"][worker] = 1
                current_worker = worker
                defined = True
            worker_string = worker_string + "- <@" + str(worker) + ">\n"
        embed = discord.Embed(title="Küchendiener:", description=worker_string)
        embed.set_author(name="Küchendienst wurde erstellt")
        print("Küchendienst erstellt mit " + str(save))
        await ctx.send(embed=embed)
        service_routine.cancel()
        service_routine.stop()
        service_routine.start()
        save_json()
    else:
        await ctx.send("Bitte mindestens 2 Personen angeben")


# @client.command(name="start")
# async def kit_start(ctx: Context):
#     if ctx.author == client.user:
#         return
#
#     worker_string = ""
#     global main_channel
#     global worker_list
#     global save
#     global current_worker
#     main_channel = ctx.channel.id
#
#     for worker in save["worker"]:
#         if save["worker"][worker] == 1:
#             current_worker = worker
#         worker_string = worker_string + "- <@" + str(worker) + ">\n"
#     embed = discord.Embed(title="Küchendiener:", description=worker_string)
#     embed.set_author(name="Küchendienst wurde erstellt")
#
#     print("Küchendienst erstellt mit " + str(save))
#     await ctx.send(embed=embed)
#     service_routine.stop()
#     service_routine.start()


@client.command(name="hilfe")
async def kit_hilfe(ctx: Context, arg: discord.User):
    global main_channel
    main_channel = ctx.channel.id
    if arg:
        save.update({"helper": {arg.id: 0}})
        embed = discord.Embed(title="Aushilfe hinzugefügt")
        embed.add_field(name=arg.display_name, value="Ist jetzt eine Aushilfekraft")

        print(str(arg.display_name) + "wurde als Aushilfe hinzugefügt")
        await ctx.send(embed=embed)
    else:
        await ctx.send("Bitte gebe den Helfer an")


@client.command(name="stop")
async def kit_stop(ctx: Context):
    global main_channel
    main_channel = ctx.channel.id
    service_routine.cancel()
    print("Küchendienst gestoppt")
    await ctx.send("Küchendienst gestoppt")


@client.command(name="time")
async def kit_set_time(ctx: Context, *args):
    global main_channel
    main_channel = ctx.channel.id
    if not args:
        await ctx.send("Gebe Tag(mo,di,mi,do,fr,sa,so) und Uhrzeit(0-23) für die Erinnerung an")
    else:
        global save
        if set_day(args[0]) == -1 or int(args[1]) not in range(0, 24):
            await ctx.send("Bitte halte dich ans Format")
        else:
            save["remind"] = True
            save["time"][0] = set_day(args[0])
            day = convert_daynumber_to_day(save["time"][0])
            save["time"][1] = int(args[1])
            await ctx.send(f"Küchendienst wechselt am {day} um {args[1]} Uhr")
            print(f"Wechselzeit wurde auf {day}-{args[1]} umgestellt")
            save_json()


@client.command(name="check")
async def kit_check(ctx: Context):
    global main_channel
    global save
    global current_helper
    await service_routine()

    main_channel = ctx.channel.id
    worker_string = ""

    embed = discord.Embed(title="Küchendiener", color=0xffffff)
    embed.set_author(name="Küchendienst")
    try:
        for worker in save["worker"]:
            if save["worker"][worker] == 1:
                value = "- <@"+str(worker)+">"
                if current_helper:
                    value += "\n- <@" + str(current_helper) + ">  `Aushilfe`"

                embed.add_field(name="momentaner Küchendienst", value=value, inline=False)
            else:
                worker_string = worker_string + "- <@" + str(worker) + ">\n"
        if not current_helper:
            for helper in save["helper"]:
                worker_string += "- <@" + str(helper) + ">  `Aushilfe`"
        embed.add_field(name="Pause", value=worker_string, inline=False)

    except AttributeError:
        await ctx.send("Kein Küchendienst eingerichtet!")
    else:
        embed.add_field(name="Wechselzeit", value="Am " + convert_daynumber_to_day(save["time"][0]) + " um " +
                                                  str(save["time"][1]) + "Uhr", inline=False)
        print("Küchendienst-Check wurde angefordert")
        print("Save: " + str(save))
        await ctx.send(embed=embed)


@client.command(name="next")
async def kit_next(channel):
    for i, key in enumerate(save["worker"]):
        if save["worker"][key] == 1:
            save["worker"][key] = 0
            if i == len(save["worker"])-1:
                save["worker"][list(save["worker"])[0]] = 1
            else:
                save["worker"][list(save["worker"])[i + 1]] = 1
            break

    global current_worker
    global current_helper
    for worker in save["worker"]:
        if save["worker"][worker] == 1:
            current_worker = worker

    description = "<@" + str(current_worker) + ">" + " hat Küchendienst!"

    for helper in save["helper"]:
        save["helper"][helper] += 1
        if save["helper"][helper] == len(save["worker"])+1:
            save["helper"][helper] = 0
            description = description + "\n<@" + str(helper) + ">" + " hilft diese Woche aus!"
            current_helper = helper
        else:
            current_helper = None

    save_json()
    print("Küchendienst wurde aktualisiert")
    if current_helper:
        print(str(current_worker) + " arbeitet und " + str(current_helper) + "hilft")
    else:
        print(str(current_worker) + " arbeitet und niemand hilft")
    embed = discord.Embed(title="Küchendienst wurde aktualisiert", description=description)
    await channel.send(embed=embed)


@client.command(name="help")
async def kit_help(ctx: Context):
    global main_channel
    main_channel = ctx.channel.id
    embed = discord.Embed(title="Küchendienst Bot Commands", color=0xffffff)
    embed.add_field(name="`kit help`", value="Ruft diese Nachricht auf", inline=False)
    embed.add_field(name="`kit setup [@user, ...]`", value="Richtet den Küchendienst ein! Reihenfolge der "
                                                           "angegebenen Benutzer bestimmt "
                                                           "die Küchendienst Reihenfolge", inline=False)
    embed.add_field(name="`kit start`", value="Startet den Bot wenn setup schonmal ausgeführt wurde", inline=False)
    embed.add_field(name="`kit check`", value="Zeigt wer diese Woche mit Küchendienst an der Reihe ist", inline=False)
    embed.add_field(name="`kit stop`", value="Stoppt die Küchendienst Benachrichtigung. "
                                             "Danach erneut kit setup/start", inline=False)
    embed.add_field(name="`kit next`", value="Küchendienst wird an nächste Person gereicht")
    embed.add_field(name="`kit time [day] [hour]`", value="Stelle ein wann Küchendienst wechseln soll\n [day] = "
                                                          "mo,di,mi,do,fr,sa,so \n [hour] = 0 - 23", inline=False)
    embed.add_field(name="`kit hilfe [@user]`", value="Fügt den User als Aushilfe hinzu")

    print("Küchendienst Hilfe wurde angefordert")
    await ctx.send(embed=embed)

client.run(token)
