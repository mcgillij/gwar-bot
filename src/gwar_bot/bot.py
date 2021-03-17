""" Gwar Bot """
import os
import sqlite3
from random import choices
from twitchio.ext import commands

DB_CONNECTION = sqlite3.connect("deaths.db")

IRC_TOKEN = os.getenv('IRC_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
NICK = os.getenv('NICK')
PREFIX = os.getenv('PREFIX')
INITIAL_CHANNELS = [os.getenv('INITIAL_CHANNELS')]

GWAR_FACTS = [
        """The stage show is not for the faint of heart. "If your idea of fun is watching The 700 Club, if you enjoy going to church, if you're a Mormon, if you're a social conservative, then you probably aren't going to enjoy a GWAR show. But if you're somebody who enjoys naughty fun, which is probably about 98 percent of the human race, you're going to f---ing love GWAR."  """,
        """But GWAR is totally in on the joke. "Sure, we do violent things on stage. We do sexual things on stage. But it's a parody of people's violent, sexual attitudes. When we do racist humor or sexual humor or violent humor, we're making jokes of people that are racist, sexist or violent. We're in no way advocating rape, murder or racism in any way. GWAR is all about satire, GWAR is all about sarcasm, GWAR is all about freedom, and really, GWAR is all about love." """,
        """The first few rows will get slimed. "It wouldn't be a GWAR show without blood and slime and all that kind of stuff. Anybody within about 30, 40 feet of the stage should be prepared to get s--- all over them. But it's completely nontoxic, biodegradeable, green. In all the years we've been doing GWAR, we've never had any problems with the spew. It's no worse than having a beer thrown in your face." """,
        """You are safe in GWAR's hands. "We're pros. There's a security barrier; there's a bunch of goons in that security barrier ready to control the crowd physically, if that's what it takes. But generally speaking, GWAR crowds are no more violent than any other typical mosh-pit experience. They're not out there to clobber the s--- out of people." """,
        """Remember: GWAR are fictional characters. "If you condemn GWAR for what they do and say, you run the risk of making a complete fool of yourself. You might as well get mad at Homer Simpson for being a dumbass." """,
        """Please do not throw dead animals at the band. Brockie's blog lists the nastiest things to be hurled onstage at a GWAR show, including dead chickens, armadillos and a cat with an eyeball hanging from its socket: "Yeah, we've attracted some weirdos. We do get the occasional dead cat thrown at us, but that just comes with the terrain." """,
        """Bring the kids! "Recently at a show, we had three generations of GWAR fans in one family - grandma, her kid, and her kid's kid, all there, all together, all in the front row, wearing their GWAR T-shirts, all covered in slime and blood. Going to a GWAR show has become a rite of passage, like having sex for the first time, or smoking crack. Well, not that you have to smoke crack. But going to a GWAR show is something that pretty much every teenager is going to do sooner or later." """,
]

bot = commands.Bot(
    irc_token=IRC_TOKEN,
    client_id=CLIENT_ID,
    nick=NICK,
    prefix=PREFIX,
    initial_channels=INITIAL_CHANNELS
)


@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{NICK} is online!")
    cursor = DB_CONNECTION.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS deaths (reason TEXT)")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(INITIAL_CHANNELS[0], "/me bursts through the wall!")


@bot.command(name='hi')
async def test(ctx):
    await ctx.send('die puny humans!')


@bot.command(name='gwarfacts')
async def gwarfacts(ctx):
    await ctx.send(choices(GWAR_FACTS))


@bot.command(name='death')
async def death(ctx):
    cursor = DB_CONNECTION.cursor()
    reason = ctx.content.lower().removeprefix('$death ')
    cursor.execute("INSERT INTO deaths VALUES (?)", (reason,))
    await ctx.send(f'Death recorded for {reason}')


@bot.command(name='totaldeaths')
async def totaldeaths(ctx):
    cursor = DB_CONNECTION.cursor()
    results = cursor.execute("SELECT count(*) FROM deaths")
    await ctx.send(f'Death {results.fetchall()}')


@bot.command(name='squidler')
async def squidler(ctx):
    await ctx.send('https://clips.twitch.tv/ProtectivePatientTardigradeOSsloth-t6BFoebSlSYhOfzV')


@bot.command(name='love')
async def love(ctx):
    await ctx.send("/me doesn't know how to love!")


@bot.command(name='help')
async def help(ctx):
    await ctx.send('Commands available: $hi, $gwarfacts, $death <reason>, $totaldeaths, $squidler, $love, $help')


# Need actual streamers permissions to access stream statistics
# @bot.command(name='info')
# async def info(ctx):
#     await ctx.send(await ctx.get_stream())

if __name__ == "__main__":
    bot.run()
