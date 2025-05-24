from datetime import timedelta
import discord
from discord import app_commands
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def parse_duration(duration_str: str) -> int:
        units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        try:
            unit = duration_str[-1]
            amount = int(duration_str[:-1])
            return amount * units[unit]
        except (KeyError, ValueError):
            return None


    # Kick command
    @app_commands.command(name="kick", description="Kick a member from the server")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        *,
        reason: str = None,
    ):
        await interaction.response.defer()
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="🔨 Member Kicked",
            description=f"{member.mention} has been kicked.",
            color=discord.Color.orange(),
        )
        embed.add_field(
            name="Reason", value=reason or "No reason provided", inline=False
        )
        embed.add_field(name="Moderator", value=interaction.user.mention, inline=False)
        embed.set_footer(text=f"User ID: {member.id}")
        await interaction.followup.send(embed=embed)

    # Ban command
    @app_commands.command(name="ban", description="Ban a member from the server")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        *,
        reason: str = "No reason provided",
    ):
        await interaction.response.defer()
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="⛔ Member Banned",
            description=f"{member.mention} has been banned.",
            color=discord.Color.red(),
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
                color=discord.Color.green(),
            )
            embed.add_field(name="Moderator", value=interaction.user.mention)
            embed.set_footer(text=f"User ID: {user.id}")
            await interaction.followup.send(embed=embed)
        except discord.NotFound:
            await interaction.followup.send("User not found in the ban list.")
        except discord.Forbidden:
            await interaction.followup.send(
                "I don't have permission to unban that user."
            )
        except discord.HTTPException as e:
            await interaction.followup.send(f"Failed to unban user: {e}")

    # Purge command
    @app_commands.command(name="purge", description="Collectively delete messages")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int = 0):
        await interaction.response.defer()
        await interaction.channel.purge(
            limit=amount + 1
        )  # +1 to include the command message
        # embed = discord.Embed(
        #     title="🧹 Messages Cleared",
        #     description=f"Deleted {amount} messages.",
        #     color=discord.Color.blue(),
        # )
        # embed.add_field(name="Moderator", value=interaction.user.mention)
        # await interaction.followup.send(embed=embed)


    @app_commands.command(name="mute", description="Timeout a member for a specific duration and reason")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def mute(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        duration: str,
        reason: str = "No reason provided"
    ):
        seconds = self.parse_duration(duration)
        if seconds is None:
            embed = discord.Embed(
                title="⏱️ Invalid Duration",
                description="Use formats like `10s`, `10m`, `2h`, `1d`.",
                color=discord.Color.red()
            )
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        try:
            limit = discord.utils.utcnow() + timedelta(seconds=seconds)
            await member.timeout(limit, reason=reason)

            embed = discord.Embed(
                title="🔇 Member Timed Out",
                color=discord.Color.orange()
            )
            embed.add_field(name="User", value=member.mention, inline=True)
            embed.add_field(name="Duration", value=duration, inline=True)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.set_footer(text=f"Muted by {interaction.user}", icon_url=interaction.user.display_avatar.url)

            await interaction.response.send_message(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Permission Denied",
                description="I can't timeout this member. Check my role position and permissions.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        except Exception as e:
            embed = discord.Embed(
                title="⚠️ Mute Failed",
                description=f"Something went wrong:\n```{e}```",
                color=discord.Color.dark_red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="lock", description="Locks the current channel so regular members can't send messages.")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        try:
            await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

            embed = discord.Embed(
                title="🔒 Channel Locked",
                description=f"{ctx.channel.mention} is now locked. Members cannot send messages.",
                color=discord.Color.dark_red()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Failed to Lock",
                description=f"Error: `{e}`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)


    @commands.hybrid_command(name="unlock", description="Unlocks the current channel so members can send messages again.")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        try:
            await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)

            embed = discord.Embed(
                title="🔓 Channel Unlocked",
                description=f"{ctx.channel.mention} is now unlocked. Members can send messages again.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Failed to Unlock",
                description=f"Error: `{e}`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
