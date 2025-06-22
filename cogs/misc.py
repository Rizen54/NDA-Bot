import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Select, View
from random import choice
from typing import Union


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
            description="Here are the commands available in this category. Use `-` as the prefix for commands (e.g., `-bookmark`). All commands also support slash (`/`).",
            color=discord.Color.dark_teal(),
        )

        if category == "general":
            embed.add_field(
                name="🌟 rule",
                value="Get a specific server rule by number.\n**Usage**: `/rule 1` or `-rule 1`",
                inline=False
            )
            embed.add_field(
                name="🌟 toss",
                value="Toss a coin to make a decision.\n**Usage**: `/toss` or `-toss`",
                inline=False
            )
            embed.add_field(
                name="🌟 books",
                value="Get Amazon links to non-academic defence-related books (none sponsored).\n**Usage**: `/books` or `-books`",
                inline=False
            )
            embed.add_field(
                name="🌟 bookmark",
                value="DMs you the message you replied to.\n**Usage**: Reply to a message with `/bookmark` or `-bookmark`",
                inline=False
            )
            embed.add_field(
                name="🌟 quote",
                value="Sends a quote to fill you with josh!\n**Usage**: `/quote` or `-quote`",
                inline=False
            )

        elif category == "vocab":
            embed.add_field(
                name="📖 vocab",
                value="Get hard words for vocabulary prep.\n**Usage**: `/vocab 5` or `-vocab 5` (for 5 words)",
                inline=False
            )
            embed.add_field(
                name="📖 idioms",
                value="Get idioms for vocabulary prep.\n**Usage**: `/idioms 3` or `-idioms 3` (for 3 idioms)",
                inline=False
            )
            embed.add_field(
                name="📖 homophones",
                value="Get homophone pairs for vocabulary prep.\n**Usage**: `/homophones 2` or `-homophones 2` (for 2 pairs)",
                inline=False
            )
            embed.add_field(
                name="📖 synoanto",
                value="Get words with 3 synonyms and antonyms each.\n**Usage**: `/synoanto 4` or `-synoanto 4` (for 4 words)",
                inline=False
            )
            embed.add_field(
                name="📖 vocabfiles",
                value="Get links to the files used for vocab prep commands.\n**Usage**: `/vocabfiles` or `-vocabfiles`",
                inline=False
            )
            embed.add_field(
                name="📖 subscribe",
                value="Subscribe to daily vocab words via DM.\n**Usage**: `/subscribe 10` or `-subscribe 10` (for 10 words daily at 6:00 AM IST)",
                inline=False
            )
            embed.add_field(
                name="📖 unsubscribe",
                value="Unsubscribe from daily vocab DMs.\n**Usage**: `/unsubscribe` or `-unsubscribe`",
                inline=False
            )

        elif category == "exam":
            embed.add_field(
                name="🎓 nda",
                value="Get an in-depth NDA guide.\n**Usage**: `/nda` or `-nda`",
                inline=False
            )
            embed.add_field(
                name="🎓 cds",
                value="Get an in-depth CDS guide.\n**Usage**: `/cds` or `-cds`",
                inline=False
            )
            embed.add_field(
                name="🎓 wiki",
                value="Get the r/NDATards official wiki link.\n**Usage**: `/wiki` or `-wiki`",
                inline=False
            )
            embed.add_field(
                name="🎓 mock",
                value="Get links to online NDA mock tests.\n**Usage**: `/mock` or `-mock`",
                inline=False
            )
            embed.add_field(
                name="🎓 pyqs",
                value="Get links to NDA previous year question papers.\n**Usage**: `/pyqs` or `-pyqs`",
                inline=False
            )
            embed.add_field(
                name="🎓 material",
                value="Get Amazon links to NDA prep books (none sponsored).\n**Usage**: `/material` or `-material`",
                inline=False
            )
            embed.add_field(
                name="🎓 daysleftto",
                value="Get the number of days remaining to NDA or CDS exam.\n**Usage**: `/daysleftto nda` or `-daysleftto nda`",
                inline=False
            )
            embed.add_field(
                name="🎓 attemptnda",
                value="Calculate NDA eligibility based on birthdate.\n**Usage**: `/attemptnda 01-07-2008` or `-attemptnda 01-07-2008`",
                inline=False
            )
            embed.add_field(
                name="🎓 attemptcds",
                value="Calculate CDS eligibility based on birthdate.\n**Usage**: `/attemptcds 01-07-2008` or `-attemptcds 01-07-2008`",
                inline=False
            )

        elif category == "tools":
            embed.add_field(
                name="🛠️ timer",
                value="Run a study timer with pause/stop buttons.\n**Usage**: `/timer 25` or `-timer 25` (for 25 minutes)",
                inline=False
            )

        embed.set_footer(text="Select a category to view more commands. Moderators can use /helpmod or -helpmod for moderation commands.")
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

    @commands.hybrid_command(name="rule", description="Get a server rule specified by rule number")
    async def rule(self, interaction_or_ctx: Union[discord.Interaction, commands.Context], rule_num: str):
        # Convert rule_num to int
        try:
            rule_num = int(rule_num)
        except ValueError:
            embed = discord.Embed(
                title="⚠️ Invalid format! Put in a number (1-9)",
                color=discord.Color.red(),
            )
            if isinstance(interaction_or_ctx, discord.Interaction):
                await interaction_or_ctx.response.defer()
                await interaction_or_ctx.followup.send(embed=embed)
            else:
                await interaction_or_ctx.reply(embed=embed)
            return

        # Defer if slash command
        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.response.defer()

        rules = [
            ["NSFW Content is Prohibited", "Any form of Not Safe For Work (NSFW) content—including explicit images, or sexual discussions—is *not* allowed. Keep it clean and professional."],
            ["No Doxxing or Sharing of Personal Information", "Do not share personal details like names, phone numbers, addresses, or photos of anyone else. Respect privacy at all cost. If you post your own data, you're responsible for it."],
            ["No Gore or Disturbing Content", "Graphic violence, gore, or any disturbing media is *strictly* banned. This is a space for motivation and growth—not trauma."],
            ["Maintain Respectful Communication", "Healthy debates are welcome, but personal attacks, insults, or aggressive behavior are not. Treat everyone with respect."],
            ["Use Appropriate Language", "Avoid profanity, slurs, or any offensive content. You're aiming for the NDA—let your language reflect that."],
            ["Follow Moderator Instructions", "Moderators are here to enforce rules and maintain peace. Follow their directions without argument. Their say is final."],
            ["No Spamming or Self-Promotion", "Do not spam messages, emojis, or links. Unsolicited promotion of YouTube, services, etc., is prohibited."],
            ["Use Relevant Channels", "Keep discussions in the correct channels. For example, geopolitical talk belongs in #geopolitics, not #general."],
            ["No Politics", "No discussions about political parties, corruption, etc., will be tolerated."]
        ]

        try:
            rule = rules[rule_num - 1]
            embed = discord.Embed(
                title=f"Rule {rule_num}: {rule[0]}",
                description=rule[1],
                color=discord.Color.red(),
            )
        except IndexError:
            embed = discord.Embed(
                title="⚠️ Invalid format! Put in a number (1-9)",
                color=discord.Color.red(),
            )

        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.followup.send(embed=embed)
        else:
            await interaction_or_ctx.reply(embed=embed)
    
    @commands.hybrid_command(name="quote", description="Gives a quote to fill you with josh!")
    async def quote(self, interaction_or_ctx: Union[discord.Interaction, commands.Context]):
        # Defer if slash command
        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.response.defer()

        quotes = [
            "Which other academy gives you such a great life without blowing a mars sized hole in your dad's pocket?",
            "Comfort is a civilian's luxury. We trade it for glory.",
            "We don't wait for chances. We train till we earn them.",
            "Sleep is a weapon - and we choose when to reload.",
            "Pain is a visitor. Pride is permanent.",
            "You don't become a warrior by shouting loud. You become one by showing up when others back down.",
            "In the land of the brave, medals aren't given - they're taken.",
            "You have two choices every morning: stay in bed and dream, or wake up and chase that damn dream down.",
            "Discipline: doing what needs to be done, even when no one is watching, and you're dead tired.",
            "When you pass the NDA gate, you don't enter a campus - you step into history.",
            "While others party on weekends, warriors are forged in sweat.",
            "We don't fear the storm. We are the reason the storm changes course.",
            "Train like hell. So your enemy meets heaven faster.",
            "This isn't for everyone. That's exactly why you're doing it.",
            "Your body will scream to stop. That's when your soul will answer - 'not yet.'",
            "Excuses don't get saluted. Effort does.",
            "If you're scared of a 5 AM wake-up, you're not ready for a 0500 strike.",
            "No backup plan. No plan B. Only mission accomplished.",
            "You either break records, or you break yourself trying.",
            "Not everyone gets to wear the tricolor on their chest. Some of us earn that right.",
            "We do more before sunrise than most people do in a day.",
            "It's not just training. It's war with the weaker version of yourself.",
            "You don't need motivation when you've got a mission.",
            "While others fear the dark, we operate in it.",
            "Some train for the mirror. We train for the battlefield.",
            "The only easy day was yesterday - and even that wasn't easy.",
            "Fall in love with the grind, or fall behind.",
            "Failure isn't falling down. It's staying down.",
            "There are no shortcuts to the parade ground.",
            "We don't quit when we're tired. We quit when we're done.",
            "In NDA, your limits aren't broken—they're redefined.",
            "When your legs give up, march with your mind.",
            "You don't get chosen. You become undeniable.",
            "Weakness checked in. Strength checked out.",
            "You want comfort? Join a club. You want glory? Join the forces.",
            "The road to the uniform is paved with broken egos and forged wills.",
            "You won't just earn a rank. You'll earn a legacy."
        ]

        embed = discord.Embed(
            title=choice(quotes),
            color=discord.Color.red(),
            )

        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.followup.send(embed=embed)
        else:
            await interaction_or_ctx.reply(embed=embed)

    @commands.hybrid_command(name="toss", description="Let the bot make your decision by tossing a coin")
    async def toss(self, interaction_or_ctx: Union[discord.Interaction, commands.Context]):
        # Defer if slash command
        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.response.defer()

        embed = discord.Embed(
            title=choice(["Heads!", "Tails!"]),
            color=discord.Color.teal(),
        )

        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.followup.send(embed=embed)
        else:
            await interaction_or_ctx.reply(embed=embed)

    @commands.hybrid_command(name="bookmark", description="Sends replied message to you in DM")
    async def bookmark(self, ctx: commands.Context):
        # Already a hybrid command; no changes needed since it doesn't need to handle Interaction
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
                title="❗ Reply to a message to use this command.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="books", description="List of Amazon links to non-academic defence books (none sponsored)")
    async def books(self, interaction_or_ctx: Union[discord.Interaction, commands.Context]):
        # Defer if slash command
        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.response.defer()

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
                "[The Brave Param Vir Chakra Stories](https://amn.in/d/g4i1GRj)\n"
                "[In Her Defence](https://amzn.in/d/ayxrKdO)\n"
                "[Boots Belts Berets](https://amzn.in/d/1Nr6lAI)\n"
                "[Hero of The Tiger Hill](https://amzn.in/d/fz2BTnq)\n"
            ),
            inline=False,
        )
        embed.set_footer(text="Suggest more books in #suggestions\nIf a link is broken DM Light-Weeny\nIf book is out of stock, search the name for other links.")

        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.followup.send(embed=embed)
        else:
            await interaction_or_ctx.reply(embed=embed)

    @commands.hybrid_command(name="help", description="Get an interactive help message describing each command")
    async def help(self, interaction_or_ctx: Union[discord.Interaction, commands.Context]):
        # Defer if slash command
        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.response.defer()

        embed = discord.Embed(
            title="Help - General Commands",
            description="Here are the commands available in this category. Use `-` as the prefix for commands (e.g., `-bookmark`). All commands also support slash (`/`).",
            color=discord.Color.dark_teal(),
        )
        embed.add_field(
            name="🌟 rule",
            value="Get a specific server rule by number.\n**Usage**: `/rule 1` or `-rule 1`",
            inline=False
        )
        embed.add_field(
            name="🌟 toss",
            value="Toss a coin to make a decision.\n**Usage**: `/toss` or `-toss`",
            inline=False
        )
        embed.add_field(
            name="🌟 books",
            value="Get Amazon links to non-academic defence-related books (none sponsored).\n**Usage**: `/books` or `-books`",
            inline=False
        )
        embed.add_field(
            name="🌟 bookmark",
            value="DMs you the message you replied to.\n**Usage**: Reply to a message with `/bookmark` or `-bookmark`",
            inline=False
        )
        embed.set_footer(text="Select a category to view more commands. Moderators can use /helpmod or -helpmod for moderation commands.")

        view = HelpView()
        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.followup.send(embed=embed, view=view)
        else:
            await interaction_or_ctx.reply(embed=embed, view=view)

    @commands.hybrid_command(name="helpmod", description="Get help message describing each moderation command")
    async def helpmod(self, interaction_or_ctx: Union[discord.Interaction, commands.Context]):
        # Defer if slash command
        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.response.defer()

        embed = discord.Embed(
            title="⚠️ Moderation Commands",
            description="These are commands for server moderation. Use as `/command` or `-command`. You need appropriate permissions (e.g., Kick Members, Ban Members, Manage Channels) to use them.",
            color=discord.Color.dark_red(),
        )

        embed.add_field(
            name="👢 kick",
            value="Kick a user from the server.\n**Usage**: `/kick @user` or `-kick @user`\n**Example**: `/kick @TroubleMaker`",
            inline=False
        )
        embed.add_field(
            name="🔨 ban",
            value="Ban a user from the server.\n**Usage**: `/ban @user` or `-ban @user`\n**Example**: `/ban @Spammer`",
            inline=False
        )
        embed.add_field(
            name="🔓 unban",
            value="Unban a user by their user ID.\n**Usage**: `/unban user-id` or `-unban user-id`\n**Example**: `/unban 123456789012345678`\n**Note**: Enable Developer Mode in Discord (Settings > Appearance), right-click a banned user in the ban list, and copy their ID.",
            inline=False
        )
        embed.add_field(
            name="🤫 mute",
            value="Mute a user for a specified time.\n**Usage**: `/mute @user time-limit reason` or `-mute @user time-limit reason`\n**Example**: `/mute @Noisy 1h Too loud`\n**Time Units**: `s` (seconds), `m` (minutes), `h` (hours), `d` (days)",
            inline=False
        )
        embed.add_field(
            name="🔒 lock",
            value="Lock the current channel to prevent users from sending messages.\n**Usage**: `/lock` or `-lock`\n**Note**: Requires Manage Channels permission.",
            inline=False
        )
        embed.add_field(
            name="🔓 unlock",
            value="Unlock the current channel to allow users to send messages again.\n**Usage**: `/unlock` or `-unlock`\n**Note**: Requires Manage Channels permission.",
            inline=False
        )

        embed.set_footer(text="For moderators only. Contact an admin if you lack permissions.")
        if isinstance(interaction_or_ctx, discord.Interaction):
            await interaction_or_ctx.followup.send(embed=embed)
        else:
            await interaction_or_ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Misc(bot))