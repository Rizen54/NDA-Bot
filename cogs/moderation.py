# cogs/moderation.py
import discord
from discord import app_commands
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Kick command
    @app_commands.command(name="kick", description="Kick a member from the server")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, *, reason=None):
        await interaction.response.defer()
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="🔨 Member Kicked",
            description=f"{member.mention} has been kicked.",
            color=discord.Color.orange()
        )
        embed.add_field(name="Reason", value=reason or "No reason provided", inline=False)
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=False)
        embed.set_footer(text=f"User ID: {member.id}")
        await interaction.followup.send(embed=embed)

    # Ban command
    @app_commands.command(name="ban", description="Ban a member from the server")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, *, reason="No reason provided"):
        await interaction.response.defer()
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="⛔ Member Banned",
            description=f"{member.mention} has been banned.",
            color=discord.Color.red()
        )
        embed.add_field(name="Reason:", value=reason, inline=False)
        embed.add_field(name="Moderator:", value=interaction.user.mention, inline=False)
        embed.set_footer(text=f"User ID: {member.id}")
        await interaction.followup.send(embed=embed)

    # Unban command
    @app_commands.command(name="unban", description="Unban a member from the server")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user: discord.User):
        await interaction.response.defer()
        try:
            await interaction.guild.unban(user)
            embed = discord.Embed(
                title="🔓 Member Unbanned",
                description=f"{user.mention} has been unbanned.",
                color=discord.Color.green()
            )
            embed.add_field(name="Moderator", value=interaction.user.mention)
            embed.set_footer(text=f"User ID: {user.id}")
            await interaction.followup.send(embed=embed)
        except discord.NotFound:
            await interaction.followup.send("User not found in the ban list.")
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to unban that user.")
        except discord.HTTPException as e:
            await interaction.followup.send(f"Failed to unban user: {e}")

    # Purge command
    @app_commands.command(name="purge", description="Collectively delete messages")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int = 0):
        await interaction.response.defer()
        await interaction.channel.purge(limit=amount + 1)  # +1 to include the command message
        embed = discord.Embed(
            title="🧹 Messages Cleared",
            description=f"Deleted {amount} messages.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Moderator", value=interaction.user.mention)
        await interaction.followup.send(embed=embed, delete_after=5)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
