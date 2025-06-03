import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Select, View
from random import choice


class HelpView(View):
    def __init__(self):
        super().__init__(timeout=300)  # Timeout after 5 minutes of inactivity
        self.add_item(HelpSelect())


class HelpSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="General", value="general", emoji="🌟", description="General utility commands"),
            discord.SelectOption(label="Vocab Prep", value="vocab", emoji="📖", description="Vocabulary preparation commands"),
            discord.SelectOption(label="Exam Prep", value="exam", emoji="🎓", description="NDA/CDS exam preparation commands"),
            discord.SelectOption(label="Tools", value="tools", emoji="🛠️", description="Utility tools like timers"),
        ]
        super().__init__(placeholder="Select a category...", options=options)

    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        embed = discord.Embed(
            title=f"Help - {category.capitalize()} Commands",
            description="Here are the commands available in this category. Use `-` as the prefix for hybrid commands (e.g., `-bookmark`). All other commands are slash commands (`/`).",
            color=discord.Color.dark_teal(),
        )

        if category == "general":
            embed.add_field(
                name="🌟 /rule",
                value="Get a specific server rule by number.\n**Usage**: `/rule 1` (for Rule 1)",
                inline=False
            )
            embed.add_field(
                name="🌟 /toss",
                value="Toss a coin to make a decision.\n**Usage**: `/toss`",
                inline=False
            )
            embed.add_field(
                name="🌟 /books",
                value="Get Amazon links to non-academic defence-related books (none sponsored).\n**Usage**: `/books`",
                inline=False
            )
            embed.add_field(
                name="🌟 -bookmark",
                value="DMs you the message you replied to.\n**Usage**: Reply to a message with `-bookmark`",
                inline=False
            )

        elif category == "vocab":
            embed.add_field(
                name="📖 /vocab",
                value="Get hard words for vocabulary prep.\n**Usage**: `/vocab 5` (for 5 words)",
                inline=False
            )
            embed.add_field(
                name="📖 /idioms",
                value="Get idioms for vocabulary prep.\n**Usage**: `/idioms 3` (for 3 idioms)",
                inline=False
            )
            embed.add_field(
                name="📖 /homophones",
                value="Get homophone pairs for vocabulary prep.\n**Usage**: `/homophones 2` (for 2 pairs)",
                inline=False
            )
            embed.add_field(
                name="📖 /synoanto",
                value="Get words with 3 synonyms and antonyms each.\n**Usage**: `/synoanto 4` (for 4 words)",
                inline=False
            )
            embed.add_field(
                name="📖 /vocabfiles",
                value="Get links to the files used for vocab prep commands.\n**Usage**: `/vocabfiles`",
                inline=False
            )
            embed.add_field(
                name="📖 /subscribe",
                value="Subscribe to daily vocab words via DM.\n**Usage**: `/subscribe 10` (for 10 words daily at 6:00 AM IST)",
                inline=False
            )
            embed.add_field(
                name="📖 /unsubscribe",
                value="Unsubscribe from daily vocab DMs.\n**Usage**: `/unsubscribe`",
                inline=False
            )

        elif category == "exam":
            embed.add_field(
                name="🎓 /nda",
                value="Get an in-depth NDA guide.\n**Usage**: `/nda`",
                inline=False
            )
            embed.add_field(
                name="🎓 /cds",
                value="Get an in-depth CDS guide.\n**Usage**: `/cds`",
                inline=False
            )
            embed.add_field(
                name="🎓 /wiki",
                value="Get the r/NDATards official wiki link.\n**Usage**: `/wiki`",
                inline=False
            )
            embed.add_field(
                name="🎓 /mock",
                value="Get links to online NDA mock tests.\n**Usage**: `/mock`",
                inline=False
            )
            embed.add_field(
                name="🎓 /pyqs",
                value="Get links to NDA previous year question papers.\n**Usage**: `/pyqs`",
                inline=False
            )
            embed.add_field(
                name="🎓 /material",
                value="Get Amazon links to NDA prep books (none sponsored).\n**Usage**: `/material`",
                inline=False
            )
            embed.add_field(
                name="🎓 /daysleftto",
                value="Get the number of days remaining to NDA or CDS exam.\n**Usage**: `/daysleftto nda` or `/daysleftto cds`",
                inline=False
            )
            embed.add_field(
                name="🎓 /attemptnda",
                value="Calculate NDA eligibility based on birthdate.\n**Usage**: `/attemptnda 01-07-2008`",
                inline=False
            )
            embed.add_field(
                name="🎓 /attemptcds",
                value="Calculate CDS eligibility based on birthdate.\n**Usage**: `/attemptcds 01-07-2008`",
                inline=False
            )

        elif category == "tools":
            embed.add_field(
                name="🛠️ /timer",
                value="Run a study timer with pause/stop buttons.\n**Usage**: `/timer 25` (for 25 minutes)",
                inline=False
            )

        embed.set_footer(text="Select a category to view more commands. Moderators can use /helpmod for moderation commands.")
        await interaction.response.edit_message(embed=embed, view=self.view)

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
        intro_channel = self.bot.get_channel(1343570812275523639)
        log_channel = self.bot.get_channel(1346165101807403098)
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
            log_channel.send(f"Gave {role.name} role to {member.display_name}")
        except Exception as e:
            log_channel.send(f"Failed to give intro role: {e}")
        
        try:
            async for msg in intro_channel.history(limit=100):
                if msg.author.id == self.bot.user.id and member in msg.mentions:
                    await msg.delete()
                    break
            else:
                # If no message was found, log it but proceed
                await log_channel.send(f"Could not find welcome message for {member.display_name} to delete.")
        except Exception as e:
            await log_channel.send(f"Failed to delete welcome message for {member.display_name}: {e}")


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


    @app_commands.command(name="help", description="Get an interactive help message describing each command")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Help - General Commands",
            description="Here are the commands available in this category. Use `-` as the prefix for hybrid commands (e.g., `-bookmark`). All other commands are slash commands (`/`).",
            color=discord.Color.dark_teal(),
        )
        embed.add_field(
            name="🌟 /rule",
            value="Get a specific server rule by number.\n**Usage**: `/rule 1` (for Rule 1)",
            inline=False
        )
        embed.add_field(
            name="🌟 /toss",
            value="Toss a coin to make a decision.\n**Usage**: `/toss`",
            inline=False
        )
        embed.add_field(
            name="🌟 /books",
            value="Get Amazon links to non-academic defence-related books (none sponsored).\n**Usage**: `/books`",
            inline=False
        )
        embed.add_field(
            name="🌟 -bookmark",
            value="DMs you the message you replied to.\n**Usage**: Reply to a message with `-bookmark`",
            inline=False
        )
        embed.set_footer(text="Select a category to view more commands. Moderators can use /helpmod for moderation commands.")

        view = HelpView()
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="helpmod", description="Get help message describing each moderation command")
    async def helpmod(self, interaction: discord.Interaction):
        await interaction.response.defer()  # Defer the response to avoid timeout

        embed = discord.Embed(
            title="⚠️ Moderation Commands",
            description="These are slash commands (`/`) for server moderation. You need appropriate permissions (e.g., Kick Members, Ban Members, Manage Channels) to use them.",
            color=discord.Color.dark_red(),
        )

        embed.add_field(
            name="👢 /kick",
            value="Kick a user from the server.\n**Usage**: `/kick @user`\n**Example**: `/kick @TroubleMaker`",
            inline=False
        )
        embed.add_field(
            name="🔨 /ban",
            value="Ban a user from the server.\n**Usage**: `/ban @user`\n**Example**: `/ban @Spammer`",
            inline=False
        )
        embed.add_field(
            name="🔓 /unban",
            value="Unban a user by their user ID.\n**Usage**: `/unban user-id`\n**Example**: `/unban 123456789012345678`\n**Note**: Enable Developer Mode in Discord (Settings > Appearance), right-click a banned user in the ban list, and copy their ID.",
            inline=False
        )
        embed.add_field(
            name="🤫 /mute",
            value="Mute a user for a specified time.\n**Usage**: `/mute @user time-limit reason`\n**Example**: `/mute @Noisy 1h Too loud`\n**Time Units**: `s` (seconds), `m` (minutes), `h` (hours), `d` (days)",
            inline=False
        )
        embed.add_field(
            name="🔒 /lock",
            value="Lock the current channel to prevent users from sending messages.\n**Usage**: `/lock`\n**Note**: Requires Manage Channels permission.",
            inline=False
        )
        embed.add_field(
            name="🔓 /unlock",
            value="Unlock the current channel to allow users to send messages again.\n**Usage**: `/unlock`\n**Note**: Requires Manage Channels permission.",
            inline=False
        )

        embed.set_footer(text="For moderators only. Contact an admin if you lack permissions.")
        await interaction.followup.send(embed=embed)  # Send the response after deferring

async def setup(bot):
    await bot.add_cog(Misc(bot))