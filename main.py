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

# Define bot command prefix
intents = discord.Intents.default()
intents.members = True  # Required for member-related moderation
intents.message_content = True # Required to read msg content

bot = commands.Bot(command_prefix="-", help_command=None, intents=intents)


OWNER_ID = 1244264038117146674
TEST_GUILD_IDS = [1244267678831476756]


#To check if command author is rizen before running (for cog commands etc)
def is_owner(ctx):
    return ctx.author.id == OWNER_ID

@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.competing,
            name=f"with yall for NDA"
        )
    )

    for guild_id in TEST_GUILD_IDS:
        guild = discord.Object(id=guild_id)
        await bot.tree.sync(guild=guild)
        print(f"✅ Synced commands to guild {guild_id}")
    print("All test guilds synced!")
    print(f"✅ Logged in as {bot.user.name} (ID: {bot.user.id})")


# OWNER ONLY COMMANDS
# Load cog
@commands.command(name="load")
@commands.check(is_owner)
async def load_cog(ctx, extension: str):
    try:
        await ctx.bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"✅ Loaded `cogs.{extension}` successfully.")
    except Exception as e:
        await ctx.send(f"⚠️ Failed to load cog:\n```{e}```")


# Unload cog
@commands.command(name="unload")
@commands.check(is_owner)
async def unload_cog(ctx, extension: str):
    try:
        await ctx.bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"✅ Unloaded `cogs.{extension}` successfully.")
    except Exception as e:
        await ctx.send(f"⚠️ Failed to unload cog:\n```{e}```")


# Reload cog
@commands.command(name="reload")
@commands.check(is_owner)
async def reload_cog(ctx, extension: str):
    try:
        await ctx.bot.reload_extension(f"cogs.{extension}")
        await ctx.send(f"♻️ Reloaded `cogs.{extension}` successfully.")
    except Exception as e:
        await ctx.send(f"⚠️ Failed to reload cog:\n```{e}```")


# Reload all cogs
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


# Command: Kick a member
@commands.hybrid_command(name="kick", description="Kick a member from the server")
@commands.has_permissions(kick_members=True)
async def kick(ctx: commands.Context, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)

    embed = discord.Embed(
        title="🔨 Member Kicked",
        description=f"{member.mention} has been kicked.",
        color=discord.Color.orange()
    )
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
    embed.set_footer(text=f"User ID: {member.id}")

    await ctx.send(embed=embed)


# Command: Ban
@commands.hybrid_command(name="ban", description="Ban a member from the server")
@commands.has_permissions(ban_members=True)
async def ban(ctx: commands.Context, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)

    embed = discord.Embed(
        title="⛔ Member Banned",
        description=f"{member.mention} has been banned.",
        color=discord.Color.red()
    )
    embed.add_field(name="Reason:", value=reason, inline=False)
    embed.add_field(name="Moderator:", value=ctx.author.mention, inline=False)
    embed.set_footer(text=f"User ID: {member.id}")

    await ctx.send(embed=embed)


# Command: Unban
@commands.hybrid_command(name="unban", description="Unban a member from the server")
@commands.has_permissions(ban_members=True)
async def unban(ctx: commands.Context, user: discord.User):
    try:
        await ctx.guild.unban(user)

        embed = discord.Embed(
            title="🔓 Member Unbanned",
            description=f"{user.mention} has been unbanned.",
            color=discord.Color.green()
        )
        embed.add_field(name="Moderator", value=ctx.author.mention)
        embed.set_footer(text=f"User ID: {user.id}")
        await ctx.send(embed=embed)

    except discord.NotFound:
        await ctx.send("User not found in the ban list.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to unban that user.")
    except discord.HTTPException as e:
        await ctx.send(f"Failed to unban user: {e}")


# Command: purge
@commands.hybrid_command(name="purge", description="collectively delete msgs")
@commands.has_permissions(manage_messages=True)
async def purge(ctx: commands.Context, amount=0):
    await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message
    embed = discord.Embed(
        title="🧹 Messages Cleared",
        description=f"Deleted {amount} messages.",
        color=discord.Color.blue()
    )
    embed.add_field(name="Moderator", value=ctx.author.mention)
    await ctx.send(embed=embed, delete_after=5)


# Command: Help
@commands.hybrid_command(name="help", description="Show commands list")
async def helpcomm(ctx: commands.Context):
    embed = discord.Embed(
        title="📖 Help Book",
        description=f"Here's a list of all commands of the nda bot.\nPrefixes: slash command or `-`",
        color=discord.Color.blue()
    )
    embed.add_field(name="Purge", value="Deletes a set amount of msgs.\n`Usage: /purge \{amount of msgs\}`\nNeeds manage messages perms.")
    embed.add_field(name="Kick", value="Removes a member from server.\n`Usage: /kick \{mention user\}`\nNeeds kick member perms.")
    embed.add_field(name="Ban", value="Removes a member from server and they cannot rejoin.\n`Usage: /ban \{mention user\}`\nNeeds ban member perms.")
    embed.add_field(name="Unban", value="Allows member to join server.\nUsage: `/unban \{mention user\}`\nNeeds ban member perms.")
    await ctx.send(embed=embed)


# Error handler for missing permissions
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don’t have permission to do that.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing required argument.")
    else:
        raise error  # Let unexpected errors propagate for debugging


# Run the bot
bot.add_command(kick)
bot.add_command(ban)
bot.add_command(unban)
bot.add_command(purge)
bot.add_command(helpcomm)
bot.add_command(load_cog)
bot.add_command(unload_cog)
bot.add_command(reload_all_cogs)
bot.run(token)