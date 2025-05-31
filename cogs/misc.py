import discord
from discord import app_commands
from discord.ext import commands
from random import choice


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = 1343570812275523639
        channel = self.bot.get_channel(channel_id)

        if channel:
            embed = discord.Embed(
                title="Welcome! Please introduce yourself by filling in the details below. You cannot access other channels without putting an intro here.",
                description="```Targeting:\nClass/Grad:\nBirth Year:\nBoard:\nStream:```",
                color=discord.Color.green()
            )
            await channel.send(content=member.mention, embed=embed, allowed_mentions=discord.AllowedMentions(users=True))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return  # Ignore bots

        if message.channel.id != 1343570812275523639:
            return  # Not the intro channel

        guild = message.guild
        member = message.author
        role = guild.get_role(1348380204401168465)

        if role in member.roles:
            return  # They already got the role, skip

        try:
            await member.add_roles(role, reason="Sent message in intro channel")
            self.bot.get_channel(1346165101807403098).send(f"Gave {role.name} role to {member.display_name}")
        except Exception as e:
            self.bot.get_channel(1346165101807403098).send(f"Failed to give intro role: {e}")


    @app_commands.command(name="rule", description="Give a server rule spcified by rule num.")
    async def rule(self, interaction: discord.Interaction, rule_num: int):
        await interaction.response.defer()
        rules = [
            ["NSFW Content is Strictly Prohibited", "Any form of Not Safe For Work (NSFW) content—including explicit images, or sexual discussions—is *not* allowed. Keep it clean and professional."],
            ["No Doxxing or Sharing of Personal Information", "Do not share personal details like names, phone numbers, addresses, or photos of anyone else. Respect privacy at all cost. If you post your own data, you're the one responsible for it."],
            ["No Gore, Shock, or Disturbing Content", "Graphic violence, gore, or any disturbing media is *strictly* banned. This is a space for motivation and growth—not trauma."],
            ["Maintain Respectful Communication", "Healthy debates are welcome, but personal attacks, insults, or aggressive behavior are not. Treat everyone with respect."],
            ["Use Appropriate Language", "Avoid profanity, hate speech, slurs, or any offensive content. You're aiming for the NDA—let your language reflect that."],
            ["Follow Moderator Instructions", "Moderators are here to enforce rules and maintain peace. Follow their directions without argument. And their say is final."],
            ["No Spamming or Self-Promotion", "Do not spam messages, emojis, or links. Unsolicited promotion of YouTube, Instagram, coaching, or other services is prohibited."],
            ["Use Relevant Channels", "Keep discussions in the correct channels. For example, geopolitical talk belongs in #geopolitics, not #general."],
            ["No Politics", "No discussions about political parties, corruption, propagandist sentiments etc will be tolerated."]
        ]

        try:
            rule = rules[rule_num-1]

            embed = discord.Embed(
                title = f"Rule {rule_num}: {rule[0]}",
                description = rule[1],
                color = discord.Color.red(),
            )
        except:
            embed = discord.Embed(
                title = "⚠️ Invalid format! Put in a number (1-9)",
                color = discord.Color.red(),
            )
            

        await interaction.followup.send(embed=embed)


    @app_commands.command(name="toss", description="Let the bot make your decision by tossing a coin.")
    async def toss(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        embed = discord.Embed(
            title = choice(["Heads!", "Tails!"]),
            color = discord.Color.teal(),
        )

        await interaction.followup.send(embed=embed)
    

    @commands.hybrid_command(name="bookmark", description="Sends replied msg to you in DM")
    async def bookmark(self, ctx: commands.Context):
        ref = ctx.message.reference
        if ref:
            replied_msg = await ctx.channel.fetch_message(ref.message_id)
            author_name = replied_msg.author.name

            try:
                await ctx.author.send(f"> {replied_msg.content}\n*By {author_name}*")
            except discord.Forbidden:
                embed = discord.Embed(
                    title="❌ I couldn't DM you! Check your settings.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                    title="❗ Reply to a message to use this command. Use this as prefix or wont work.",
                    color=discord.Color.red()
                )
            await ctx.send(embed=embed)

    
    @app_commands.command(name="books", description="List of amazon links to non academic defence books (none sponsored)")
    async def books(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📚 Books",
            color=discord.Color.gold(),

        )

        embed.add_field(
            name="🔗 Links:",
            value=(
                "[The Mental Inertia *by Ace Bravo Sierra*](https://amzn.in/d/2HXIySY)\n"
                "[Balidan](https://amzn.in/d/fZBY0am)\n"
                "[Kargil: Untold Stories from the War](https://amzn.in/d/6SDBlFo)\n"
                "[The Kargil Story](https://amzn.in/d/dwGzTI4)\n"
                "[Field Marshal Sam Manekshaw biography](https://amzn.in/d/bPBFRKj)\n"
                "[Rambo: The true account of a Special Forces Officer](https://amzn.in/d/9GUSWu4)\n"
                "[Air Warriors](https://amzn.in/d/fIMrMcU)\n"
                "[The Brave Param Vir Chakra Stories](https://amzn.in/d/g4i1GRj)\n"
                "[In Her Defence](https://amzn.in/d/ayxrKdO)\n"
                "[Boots Belts Berets](https://amzn.in/d/1Nr6lAI)\n"
                "[Hero of The Tiger Hill](https://amzn.in/d/fz2BTnq)\n"
            ),
            inline=False,
        )
        embed.set_footer(text="Suggest more books in #suggestions\nIf a link is broken DM Light-Weeny\nIf book is out of stock nothing can be done just search the name up for other links.")

        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="help", description="Get help msg describing each command")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Help",
            description="prefix is `-` though its useful only for `-bookmark` all other commands are slash only for technical reasons",
            color=discord.Color.dark_grey(),
        )

        embed.add_field(name="`nda`", value="Get an in-depth nda guide.", inline=True)
        embed.add_field(name="`cds`", value="Get an in-depth cds guide.", inline=True)
        embed.add_field(name="`wiki`", value="Get link to r/NDATards official wiki.", inline=True)
        embed.add_field(name="`mock`", value="Get links to online nda mock tests.", inline=True)
        embed.add_field(name="`pyqs`", value="Get links to online nda pyq tests.", inline=True)
        embed.add_field(name="`material`", value="Get amazon links to books for nda prep (none sponsored).", inline=True)
        embed.add_field(name="`books`", value="Get amazon links to non academic defence related books (none sponsored).", inline=True)
        embed.add_field(name="daysleftto", value="Get number of days remaining to either cds or nda exam. Usage: `/daysleftto nda` or `/daysleftto cds`", inline=True)
        embed.add_field(name="attemptnda", value="Get number of attempts remaining to nda exam by birthdate. Usage: `/attemptnda DD-MM-YYYY`", inline=True)
        embed.add_field(name="attemptcds", value="Get number of attempts remaining to cds exam by birthdate. Usage: `/attemptcds DD-MM-YYYY`", inline=True)
        embed.add_field(name="timer", value="Run a study timer. Usage: `/timer number-of-minutes`", inline=True)
        embed.add_field(name="rule", value="Get a specific server rule by rule number. Usage: `/rule number(1-9)`", inline=True)
        embed.add_field(name="bookmark", value="**Can only be run using `-` prefix**. DMs you the msg you replied to. Usage: reply to a msg with `-bookmark`", inline=True)
        embed.add_field(name="toss", value="Toss a coin.", inline=True)
    
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="helpmod", description="Get help msg describing each moderation command.")
    async def helpmod(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Helpmod",
            description="All commands are slash only. Can only be run by people with adequate perms.",
            color=discord.Color.red(),
        )

        embed.add_field(name="`kick`", value="`/kick @user`", inline=True)
        embed.add_field(name="`ban`", value="`/ban @user`", inline=True)
        embed.add_field(name="`unban`", value="`/unban user-id` Get user-id by enabling discord dev features in your profile settings then right click on user to unban and get the user id.", inline=True)
        embed.add_field(name="`mute`", value="`/mute @user time-limit reason` time limit can be `10m`, `2h`, `1d`, etc.", inline=True)
        embed.add_field(name="`lock`", value="locks a channel `/lock`", inline=True)
        embed.add_field(name="`unlock`", value="unlocks a channel `/lock`", inline=True)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Misc(bot))