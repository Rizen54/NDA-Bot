from datetime import timedelta
import discord
from discord.ext import commands
from typing import Union  # Added for hybrid command type hints

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
    @commands.hybrid_command(name="kick", description="Kick a member from the server")
    @commands.has_permissions(kick_members=True)
    async def kick(
        self,
        interaction_or_ctx: Union[discord.Interaction, commands.Context],
        member: discord.Member,
        *,
        reason: str = None,
    ):
        # Defer if slash command
        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.response.defer()

        await member.kick(reason=reason)
        embed = discord.Embed(
            title="🔨 Member Kicked",
            description=f"{member.mention} has been kicked.",
            color=discord.Color.orange(),
        )
        embed.add_field(
            name="Reason", value=reason or "No reason provided", inline=False
        )
        embed.add_field(
            name="Moderator",
            value=interaction_or_ctx.user.mention if isinstance(interaction_or_ctx, discord.Interaction) else interaction_or_ctx.author.mention,
            inline=False
        )
        embed.set_footer(text=f"User ID: {member.id}")

        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.followup.send(embed=embed)
        else:
            await interaction_or_ctx.reply(embed=embed)

    # Ban command
    @commands.hybrid_command(name="ban", description="Ban a member from the server")
    @commands.has_permissions(ban_members=True)
    async def ban(
        self,
        interaction_or_ctx: Union[discord.Interaction, commands.Context],
        member: discord.Member,
        *,
        reason: str = "No reason provided",
    ):
        # Defer if slash command
        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.response.defer()

        await member.ban(reason=reason)
        embed = discord.Embed(
            title="⛔ Member Banned",
            description=f"{member.mention} has been banned.",
            color=discord.Color.red(),
        )
        embed.add_field(name="Reason:", value=reason, inline=False)
        embed.add_field(
            name="Moderator:",
            value=interaction_or_ctx.user.mention if isinstance(interaction_or_ctx, discord.Interaction) else interaction_or_ctx.author.mention,
            inline=False
        )
        embed.set_footer(text=f"User ID: {member.id}")

        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.followup.send(embed=embed)
        else:
            await interaction_or_ctx.reply(embed=embed)

    # Unban command
    @commands.hybrid_command(name="unban", description="Unban a member from the server")
    @commands.has_permissions(ban_members=True)
    async def unban(
        self,
        interaction_or_ctx: Union[discord.Interaction, commands.Context],
        user: discord.User
    ):
        # Defer if slash command
        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.response.defer()

        guild = interaction_or_ctx.guild
        try:
            await guild.unban(user)
            embed = discord.Embed(
                title="🔓 Member Unbanned",
                description=f"{user.mention} has been unbanned.",
                color=discord.Color.green(),
            )
            embed.add_field(
                name="Moderator",
                value=interaction_or_ctx.user.mention if isinstance(interaction_or_ctx, discord.Interaction) else interaction_or_ctx.author.mention
            )
            embed.set_footer(text=f"User ID: {user.id}")

            if isinstance(interaction_or_ctx, discord.Interaction):
                await interaction_or_ctx.followup.send(embed=embed)
            else:
                await interaction_or_ctx.reply(embed=embed)
        except discord.NotFound:
            message = "User not found in the ban list."
            if isinstance(interaction_or_ctx, discord.Interaction):
                await interaction_or_ctx.followup.send(message)
            else:
                await interaction_or_ctx.reply(message)
        except discord.Forbidden:
            message = "I don't have permission to unban that user."
            if isinstance(interaction_or_ctx, discord.Interaction):
                await interaction_or_ctx.followup.send(message)
            else:
                await interaction_or_ctx.reply(message)
        except discord.HTTPException as e:
            message = f"Failed to unban user: {e}"
            if isinstance(interaction_or_ctx, discord.Interaction):
                await interaction_or_ctx.followup.send(message)
            else:
                await interaction_or_ctx.reply(message)

    # Purge command
    @commands.hybrid_command(name="purge", description="Collectively delete messages")
    @commands.has_permissions(manage_messages=True)
    async def purge(
        self,
        interaction_or_ctx: Union[discord.Interaction, commands.Context],
        amount: int = 0
    ):
        # Defer if slash command
        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.response.defer()

        channel = interaction_or_ctx.channel
        await channel.purge(limit=amount + 1)  # +1 to include the command message

        embed = discord.Embed(
            title="🧹 Messages Cleared",
            description=f"Deleted {amount} messages.",
            color=discord.Color.blue(),
        )
        embed.add_field(
            name="Moderator",
            value=interaction_or_ctx.user.mention if isinstance(interaction_or_ctx, discord.Interaction) else interaction_or_ctx.author.mention
        )

        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.followup.send(embed=embed)
        else:
            await interaction_or_ctx.reply(embed=embed)

    # Mute command
    @commands.hybrid_command(name="mute", description="Timeout a member for a specific duration and reason")
    @commands.has_permissions(moderate_members=True)
    async def mute(
        self,
        interaction_or_ctx: Union[discord.Interaction, commands.Context],
        member: discord.Member,
        duration: str,
        reason: str = "No reason provided"
    ):
        # Defer if slash command
        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.response.defer(ephemeral=True)

        seconds = self.parse_duration(duration)
        if seconds is None:
            embed = discord.Embed(
                title="⏱️ Invalid Duration",
                description="Use formats like `10s`, `10m`, `2h`, `1d`.",
                color=discord.Color.red()
            )
            if isinstance(interaction_or_ctx, discord.Interaction):
                await interaction_or_ctx.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction_or_ctx.reply(embed=embed)
            return

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
            embed.set_footer(
                text=f"Muted by {interaction_or_ctx.user if isinstance(interaction_or_ctx, discord.Interaction) else interaction_or_ctx.author}",
                icon_url=(interaction_or_ctx.user.display_avatar.url if isinstance(interaction_or_ctx, discord.Interaction) else interaction_or_ctx.author.display_avatar.url)
            )

            if isinstance(interaction_or_ctx, discord.Interaction):
                await interaction_or_ctx.followup.send(embed=embed)
            else:
                await interaction_or_ctx.reply(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Permission Denied",
                description="I can't timeout this member. Check my role position and permissions.",
                color=discord.Color.red()
            )
            if isinstance(interaction_or_ctx, discord.Interaction):
                await interaction_or_ctx.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction_or_ctx.reply(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="⚠️ Mute Failed",
                description=f"Something went wrong:\n```{e}```",
                color=discord.Color.dark_red()
            )
            if isinstance(interaction_or_ctx, discord.Interaction):
                await interaction_or_ctx.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction_or_ctx.reply(embed=embed)

    # Lock command (already hybrid, but adjust response for consistency)
    @commands.hybrid_command(name="lock", description="Locks the current channel so regular members can't send messages.")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, interaction_or_ctx: Union[discord.Interaction, commands.Context]):
        # Defer if slash command
        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.response.defer()

        channel = interaction_or_ctx.channel
        guild = interaction_or_ctx.guild
        overwrite = channel.overwrites_for(guild.default_role)
        overwrite.send_messages = False
        try:
            await channel.set_permissions(guild.default_role, overwrite=overwrite)

            embed = discord.Embed(
                title="🔒 Channel Locked",
                description=f"{channel.mention} is now locked. Members cannot send messages.",
                color=discord.Color.dark_red()
            )
            if isinstance(interaction_or_ctx, discord.Interaction):
                await interaction_or_ctx.followup.send(embed=embed)
            else:
                await interaction_or_ctx.reply(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Failed to Lock",
                description=f"Error: `{e}`",
                color=discord.Color.red()
            )
            if isinstance(interaction_or_ctx, discord.Interaction):
                await interaction_or_ctx.followup.send(embed=embed)
            else:
                await interaction_or_ctx.reply(embed=embed)

    # Unlock command (already hybrid, but adjust response for consistency)
    @commands.hybrid_command(name="unlock", description="Unlocks the current channel so members can send messages again.")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, interaction_or_ctx: Union[discord.Interaction, commands.Context]):
        # Defer if slash command
        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.response.defer()

        channel = interaction_or_ctx.channel
        guild = interaction_or_ctx.guild
        overwrite = channel.overwrites_for(guild.default_role)
        overwrite.send_messages = True
        try:
            await channel.set_permissions(guild.default_role, overwrite=overwrite)

            embed = discord.Embed(
                title="🔓 Channel Unlocked",
                description=f"{channel.mention} is now unlocked. Members can send messages again.",
                color=discord.Color.green()
            )
            if isinstance(interaction_or_ctx, discord.Interaction):
                await interaction_or_ctx.followup.send(embed=embed)
            else:
                await interaction_or_ctx.reply(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Failed to Unlock",
                description=f"Error: `{e}`",
                color=discord.Color.red()
            )
            if isinstance(interaction_or_ctx, discord.Interaction):
                await interaction_or_ctx.followup.send(embed=embed)
            else:
                await interaction_or_ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))