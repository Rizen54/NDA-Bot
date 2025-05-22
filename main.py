import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

# Load .env token
load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Setup logging
logging.basicConfig(level=logging.INFO)

# Define bot intents
intents = discord.Intents.default()
intents.members = True  # Required for member-related moderation
intents.message_content = True  # Required to read message content

bot = commands.Bot(command_prefix="-", help_command=None, intents=intents)

OWNER_ID = 1244264038117146674
GUILD_IDS = [1244267678831476756]

# To check if command author is the owner before running (for cog commands etc)
def is_owner(ctx):
    return ctx.author.id == OWNER_ID

@bot.event
async def on_ready():
    # Load cogs
    await bot.load_extension("cogs.prep")
    await bot.load_extension("cogs.moderation")  # Load moderation cog

    # Change presence
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.competing,
            name=f"with yall for NDA"
        )
    )

    # Sync slash commands to listed guilds
    for guild_id in GUILD_IDS:
        guild = discord.Object(id=guild_id)
        await bot.tree.sync(guild=guild)
        print(f"✅ Synced commands to guild {guild_id}")
    print("All test guilds synced!")
    print(f"✅ Logged in as {bot.user.name} (ID: {bot.user.id})")

    print("Registered slash commands:")
    for cmd in bot.tree.get_commands():
        print(f"  - {cmd.name}")

# OWNER ONLY COMMANDS
@commands.command(name="sync")
@commands.is_owner()
async def sync(ctx):
    synced_total = 0
    for gid in GUILD_IDS:
        try:
            guild = discord.Object(id=gid)
            synced = await ctx.bot.tree.sync(guild=guild)
            await ctx.send(f"✅ Synced {len(synced)} commands to guild `{gid}`")
            synced_total += len(synced)
        except Exception as e:
            await ctx.send(f"❌ Failed to sync guild `{gid}`: {e}")
    await ctx.send(f"🔁 Done syncing to all listed guilds! `Total commands synced: {synced_total}`")
    print("Registered slash commands:")
    for cmd in bot.tree.get_commands():
        print(f"  - {cmd.name}")

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

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
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
            inline=False
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
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Total: {len(loaded)} cogs")
    await ctx.send(embed=embed)

# Register owner commands to the bot
bot.add_command(sync)
bot.add_command(load_cog)
bot.add_command(unload_cog)
bot.add_command(reload_cog)
bot.add_command(reload_all_cogs)
bot.add_command(list_cogs)

# Error handler for missing permissions and arguments
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to do that.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument.")
    else:
        raise error  # For unexpected errors, raise normally

bot.run(token)
