import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

# Load .env token
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

# Setup logging
logging.basicConfig(level=logging.INFO)

# Define bot intents
intents = discord.Intents.default()
intents.members = True  # Required for member-related moderation
intents.message_content = True  # Required to read message content

bot = commands.Bot(command_prefix="-", help_command=None, intents=intents)

OWNER_ID = 1244264038117146674


# To check if command author is the owner before running (for cog commands etc)
def is_owner(ctx):
    return ctx.author.id == OWNER_ID


async def load_all_cogs(bot: commands.Bot):
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            if f"cogs.{filename[:-3]}" not in bot.extensions:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ {filename[:-3]}")


@bot.event
async def on_ready():
    print("Currently loaded cogs:")
    for cog in bot.extensions:  
        print(f" - {cog}")

    print(f"✅ Logged in as {bot.user.name} (ID: {bot.user.id})")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.competing,
            name="with yall for NDA"
        )
    )


@bot.event
async def setup_hook():
    print("Loading cogs...")
    await load_all_cogs(bot)


# OWNER ONLY COMMANDS
@commands.command(name="sync")
@commands.is_owner()
async def sync(ctx):
    await bot.tree.sync()
    await ctx.reply("Syncing commands now...")


@commands.command(name="load")
@commands.check(is_owner)
async def load_cog(ctx, extension: str):
    try:
        await ctx.bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"✅ Loaded `cogs.{extension}` successfully.")
    except Exception as e:
        await ctx.send(f"⚠️ Failed to load cog:\n```{e}```")


@commands.command(name="unload")
@commands.check(is_owner)
async def unload_cog(ctx, extension: str):
    try:
        await ctx.bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"✅ Unloaded `cogs.{extension}` successfully.")
    except Exception as e:
        await ctx.send(f"⚠️ Failed to unload cog:\n```{e}```")


@commands.command(name="reload")
@commands.check(is_owner)
async def reload_cog(ctx, extension: str):
    try:
        await ctx.bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"♻️ Reloaded `cogs.{extension}` successfully.")
    except Exception as e:
        await ctx.send(f"⚠️ Failed to reload cog:\n```{e}```")


@commands.command(name="reloadall")
@commands.check(is_owner)
async def reload_all_cogs(ctx):
    import os

    reloaded = []
    failed = []

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog = f"cogs.{filename[:-3]}"
            try:
                await ctx.bot.reload_extension(cog)
                reloaded.append(cog)
            except Exception as e:
                failed.append((cog, str(e)))

    embed = discord.Embed(title="♻️ Reloaded Cogs", color=discord.Color.gold())
    if reloaded:
        embed.add_field(name="✅ Success", value="\n".join(reloaded), inline=False)
    if failed:
        embed.add_field(
            name="❌ Failed",
            value="\n".join(f"{name} - `{err}`" for name, err in failed),
            inline=False,
        )

    await ctx.send(embed=embed)


@commands.command(name="listcogs", aliases=["cogs", "loaded"])
@commands.check(is_owner)
async def list_cogs(ctx):
    loaded = list(ctx.bot.extensions.keys())
    if not loaded:
        await ctx.send("⚠️ No cogs are currently loaded.")
        return

    embed = discord.Embed(
        title="🧠 Loaded Cogs",
        description="\n".join(f"✅ `{cog}`" for cog in loaded),
        color=discord.Color.green(),
    )
    embed.set_footer(text=f"Total: {len(loaded)} cogs")
    await ctx.send(embed=embed)


owner_commands = [sync, load_cog, unload_cog, reload_cog, reload_all_cogs, list_cogs]
for cog in owner_commands:
    bot.add_command(cog)


# Error handler for missing permissions and arguments
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to do that.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument.")
    else:
        raise error  # For unexpected errors, raise normally


try:
    bot.run(token)
except (discord.ConnectionClosed, discord.HTTPException, asyncio.TimeoutError) as e:
    print(f"Bot crashed due to connection issue: {e}")
    sys.exit(1)  # This triggers systemd to restart it
