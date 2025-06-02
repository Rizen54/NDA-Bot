from random import sample
from datetime import datetime, date
import discord
from discord import app_commands, Interaction, ui
from discord.ext import commands, tasks
import asyncio


class Prep(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        #Read files for english
        with open("english/vocab.txt", "r") as f:
            self.vocab = f.readlines()
        with open("english/homophones.txt", "r") as f:
            self.homophones = f.readlines()
        with open("english/idioms.txt", "r") as f:
            self.idioms = f.readlines()
        with open("english/synoanto.txt", "r") as f:
            self.synoanto = f.readlines()

        # Load subscriptions from file
        self.subscriptions = {}  # Maps user_id (int) to word_count (int)
        self.subscriptions_file = "subscriptions.txt"
        self.load_subscriptions()

        # Start the background task for sending daily DMs
        self.last_sent_date = None  # Track the last date we sent messages to avoid duplicates
        self.send_daily_vocab.start()

    def load_subscriptions(self):
        """Load subscription data from subscriptions.txt into self.subscriptions."""
        try:
            with open(self.subscriptions_file, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
            for line in lines:
                if line.strip():  # Ignore empty lines
                    user_id, word_count = map(int, line.split(","))
                    self.subscriptions[user_id] = word_count
        except FileNotFoundError:
            # If the file doesn't exist, create it
            with open(self.subscriptions_file, "w", encoding="utf-8") as f:
                pass
        except Exception as e:
            print(f"Error loading subscriptions: {e}")
    

    def save_subscriptions(self):
        """Save subscription data from self.subscriptions to subscriptions.txt."""
        with open(self.subscriptions_file, "w", encoding="utf-8") as f:
            for user_id, word_count in self.subscriptions.items():
                f.write(f"{user_id},{word_count}\n")

    @app_commands.command(name="subscribe", description="Subscribe to daily vocab words in DM")
    async def subscribe(self, interaction: discord.Interaction, number: int = 10):
        # Validate the number of words
        if number < 1:
            await interaction.response.send_message("Please request at least 1 word.", ephemeral=True)
            return
        if number > 20:
            await interaction.response.send_message("Max limit is 20 words!", ephemeral=True)
            return

        # Add user to subscriptions
        user_id = interaction.user.id
        self.subscriptions[user_id] = number
        self.save_subscriptions()

        embed = discord.Embed(
                title="Subscription Successful",
                description=f"You'll receive {number} vocab words every morning at 6:00 AM IST via DM.",
                color=discord.Color.green(),
            )
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="unsubscribe", description="Unsubscribe from daily vocab DMs")
    async def unsubscribe(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        if user_id in self.subscriptions:
            del self.subscriptions[user_id]
            self.save_subscriptions()
            await interaction.response.send_message(
                "Unsubscribed! You will no longer receive daily vocab DMs.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "You are not subscribed to daily vocab DMs.", ephemeral=True
            )

    @tasks.loop(minutes=10)  # Check every minutes
    async def send_daily_vocab(self):
        # Get current local time (assumed to be IST)
        now = datetime.now()
        current_hour = now.hour
        current_date = now.date()

        # Check if it's 6:00 AM
        if current_hour != 6:
            return

        # Ensure we only send once per day
        if self.last_sent_date == current_date:
            return
        self.last_sent_date = current_date

        # Send vocab words to each subscribed user
        for user_id, word_count in self.subscriptions.items():
            try:
                user = await self.bot.fetch_user(user_id)
                if not user:
                    continue  # Skip if user can't be found

                # Select random words
                if not self.vocab:
                    await user.send("Sorry, the vocabulary list is empty!")
                    continue
                selected_words = sample(self.vocab, k=min(word_count, len(self.vocab)))

                # Create an embed with the selected words
                embed = discord.Embed(
                    title=f"Your Daily Vocabulary - {word_count} Words",
                    description="\n".join(selected_words),
                    color=discord.Color.blue(),
                )

                await user.send(embed=embed)
            except Exception as e:
                print(f"Error sending DM to user {user_id}: {e}")

    @send_daily_vocab.before_loop
    async def before_send_daily_vocab(self):
        await self.bot.wait_until_ready()  # Wait for the bot to be ready before starting the task


    @app_commands.command(name="vocab", description="Get hard words for vocab prep")
    async def vocabulary(self, interaction: discord.Interaction, number: int=1):
        await interaction.response.defer()

        if number>20:
            embed = discord.Embed(
                title=f"❌ Max limit is 20 words!",
                color=discord.Color.red(),
            )

        elif number<=0:
            embed = discord.Embed(
                title=f"❌ Ask for at least 1 word!",
                color=discord.Color.red(),
            )

        else:
            returnlist = sample(self.vocab, number)

            embed = discord.Embed(
                title=f"Here are {number} words",
                description="\n".join(returnlist),
                color=discord.Color.blue(),
            )

        await interaction.followup.send(embed=embed)

    
    @app_commands.command(name="idioms", description="Get idioms for vocab prep")
    async def give_idioms(self, interaction: discord.Interaction, number: int=1):
        await interaction.response.defer()

        if number>20:
            embed = discord.Embed(
                title=f"❌ Max limit is 20 idioms!",
                color=discord.Color.red(),
            )
            await interaction.followup.send(embed=embed)
            return
        elif number<=0:
            embed = discord.Embed(
                title=f"❌ Ask for at least 1 idiom!",
                color=discord.Color.red(),
            )

        else:
            returnlist = sample(self.idioms, number)

            embed = discord.Embed(
                title=f"Here are {number} idioms",
                description="\n".join(returnlist),
                color=discord.Color.blue(),
            )

        await interaction.followup.send(embed=embed)


    @app_commands.command(name="homophones", description="Get homophones for vocab prep")
    async def give_homophones(self, interaction: discord.Interaction, number: int=1):
        await interaction.response.defer()

        if number>20:
            embed = discord.Embed(
                title=f"❌ Max limit is 20 pairs!",
                color=discord.Color.red(),
            )

        elif number<=0:
            embed = discord.Embed(
                title=f"❌ Ask for at least 1 homphone pair!",
                color=discord.Color.red(),
            )


        else:
            returnlist = sample(self.homophones, number)

            embed = discord.Embed(
                title=f"Here are {number} homophones",
                description="\n".join(returnlist),
                color=discord.Color.blue(),
            )

        await interaction.followup.send(embed=embed)


    @app_commands.command(name="synoanto", description="Get words with 3 synonyms and antonyms for vocab prep")
    async def give_synoanto(self, interaction: discord.Interaction, number: int=1):
        await interaction.response.defer()

        if number>20:
            embed = discord.Embed(
                title=f"❌ Max limit is 20 words!",
                color=discord.Color.red(),
            )

        elif number<=0:
            embed = discord.Embed(
                title=f"❌ Ask for at least 1 word!",
                color=discord.Color.red(),
            )


        else:
            returnlist = sample(self.synoanto, number)

            embed = discord.Embed(
                title=f"Here are {number} Words with 3 synonyms and antonyms each",
                description="\n".join(returnlist),
                color=discord.Color.blue(),
            )

        await interaction.followup.send(embed=embed)

    
    @app_commands.command(name="vocabfiles", description="Get list of files which bot uses for vocab prep commands")
    async def vocabfiles(self, interaction: discord.Interaction):
        await interaction.response.defer()
        returnlist = ["[Vocab](https://raw.githubusercontent.com/Rizen54/NDA-Bot/refs/heads/main/english/vocab.txt)",
                      "[Idioms](https://raw.githubusercontent.com/Rizen54/NDA-Bot/refs/heads/main/english/idioms.txt)",
                      "[Synonyms/Antonyms](https://raw.githubusercontent.com/Rizen54/NDA-Bot/refs/heads/main/english/synoanto.txt)",
                      "[Homophones](https://raw.githubusercontent.com/Rizen54/NDA-Bot/refs/heads/main/english/homophones.txt)"]

        embed = discord.Embed(
            title=f"Here is the list to files that are used by me for vocab prep commands",
            description="\n".join(returnlist),
            color=discord.Color.blue(),
        )

        await interaction.followup.send(embed=embed)


    @app_commands.command(name="nda", description="Get an in-depth NDA guide")
    async def nda_guide(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📚 NDA Guide",
            description="[Here is an in-depth nda guide](https://tranquilizer014.blogspot.com/2025/02/nda-national-defence-academy-entry.html)",
            color=discord.Color.blue(),
        )

        embed.add_field(name="By", value="Tranquilizer", inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="cds", description="Get an in-depth CDS guide")
    async def cds_guide(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📚 CDS Guide",
            description="[Here is an in-depth CDS guide](https://tranquilizer014.blogspot.com/2025/02/combined-defence-services-cds.html)",
            color=discord.Color.blue(),
        )
        
        embed.set_footer(text="By Tranquilizer")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="wiki", description="Get the r/NDATards official wiki link"
    )
    async def wiki(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📖 Wiki",
            description="[Link](https://www.reddit.com/r/NDATards/comments/1kgn848/rndatards_official_wiki)",
            color=discord.Color.blue(),
        )
        embed.set_footer(text="By the great contributors of NDATards")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="mock", description="Get links to online NDA mock tests")
    async def mock(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📝 NDA Mock Test Links",
            description="Here are some great platforms to practice NDA mock tests:",
            color=discord.Color.blue(),
        )

        embed.add_field(
            name="🔗 Resources:",
            value=(
                "[Mockers](https://www.mockers.in/exam/nda-mock-test)\n"
                "[EduRev](https://edurev.in/courses/8741_NDA--National-Defence-Academy--Mock-Test-Series)"
            ),
            inline=False,
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="pyqs", description="Get link to online mock NDA tests")
    async def pyqs(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📚 NDA PYQs",
            description="Here are some curated mock test & previous year question paper links:",
            color=discord.Color.blue(),
        )

        embed.add_field(
            name="🔗 Resources:",
            value=(
                "[Official UPSC PDFs](https://upsc.gov.in/examinations/previous-question-papers/archives?field_exam_name_value=National%20Defence%20Academy)\n"
                "[SelfStudys (Online Mock Tests - 54 Papers)](https://www.mockers.in/exam/nda-mock-test)\n"
                "[StudyIQ (PDFs - 20 Papers)](https://www.studyiq.com/articles/nda-previous-year-question-papers/)"
            ),
            inline=False,
        )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="material", description="List of amazon links to good prep books (none sponsored)")
    async def material(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📚 Material",
            color=discord.Color.blue(),

        )

        embed.add_field(
            name="🔗 Resources:",
            value=(
                "[Disha NDA PYQ Books](https://amzn.in/d/1nYZgw6)\n"
                "[Pathfinder](https://amzn.in/d/7zeyvIH)\n"
                "[Mission NDA](https://amzn.in/d/iUifB1B)\n"
                "[Arihant topicwise solved pyqs](https://amzn.in/d/6DSJ046)\n"
                "[RS Aggarwal Maths for NDA/NA](https://amzn.in/d/1x9YegG)\n"
            ),
            inline=False,
        )
        embed.set_footer(text="Suggest more books in #suggestions")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="daysleftto",
        description="Gives number of days remaining to nda or cds exam",
    )
    async def dlte(self, interaction: discord.Interaction, exam: str):
        embed = discord.Embed(colour=discord.Colour.red())

        if exam.lower() == "nda":
            exam_date = datetime(2025, 9, 14)  # NDA 2 2025
            today = datetime.now()
            days_remaining = (exam_date - today).days
        elif exam.lower() == "cds":
            exam_date = datetime(2025, 9, 14)  # CDS 2 2025
            today = datetime.now()
            days_remaining = (exam_date - today).days

        try:
            if days_remaining > 0:
                embed.title = f"🗓️ ``{days_remaining} days`` left until the {exam} exam on `{exam_date.date()}`."
            elif days_remaining == 0:
                embed.title = f"🎯 The {exam} exam is **today**! Give it your best!"
            else:
                embed.title = f"✅ The last {exam} exam date has **passed**. Date for the next will be set soon."

            await interaction.response.send_message(embed=embed)
        except:
            embed.title = f"Please enter either nda or cds."
            await interaction.response.send_message(embed=embed)
            

    @app_commands.command(
        name="attemptnda",
        description="Calculate your NDA eligibility based on your date of birth.",
    )
    async def attemptnda(self, interaction: discord.Interaction, birthdate: str):
        """
        Calculates NDA eligibility based on DOB.
        Usage: /attemptnda DD-MM-YYYY
        Example: /attemptnda 23-09-2008
        """
        await interaction.response.defer()
        try:
            birthdate = str(birthdate).replace("/", "-")
            parts = birthdate.replace("/", "-").split("-")
            if len(parts) == 3:
                day = parts[0].zfill(2)
                month = parts[1].zfill(2)
                year = parts[2]
                birthdate = f"{day}-{month}-{year}"

            # Accept DOB in DD-MM-YYYY format
            dob = datetime.strptime(birthdate, "%d-%m-%Y").date()
            current_year = datetime.now().year

            eligible_attempts = []

            # Check NDA eligibility for the next 6 years
            for year in range(current_year, current_year + 6):
                # NDA 1: DOB must be between 2nd July (year - 19) and 1st July (year - 16)
                nda1_start = date(year - 19, 7, 2)
                nda1_end = date(year - 16, 7, 1)
                if nda1_start <= dob <= nda1_end:
                    eligible_attempts.append(f"NDA 1 {year}")

                # NDA 2: DOB must be between 2nd January (year - 19) and 1st January (year - 16)
                nda2_start = date(year - 18, 1, 2) 
                nda2_end = date(year - 16, 1, 1)
                if nda2_start <= dob <= nda2_end:
                    eligible_attempts.append(f"NDA 2 {year}")

            if not eligible_attempts:
                await interaction.followup.send(
                    "❌ You are not eligible for any upcoming NDA exams based on your date of birth."
                )
                return

            embed = discord.Embed(
                title="🪖 NDA Eligibility Checker",
                description=f"Based on your birthdate: `{birthdate}`",
                color=discord.Color.green(),
            )
            embed.add_field(
                name="✅ Eligible NDA Attempts:",
                value="\n".join(eligible_attempts),
                inline=False,
            )
            embed.add_field(
                name="⚠️ NOTE:",
                value="If you're in school currently, the first nda attempt you're eligible for will be NDA 2 of your class 12th year. For eg: if you're in class 12th in 2026, you can apply for nda 2 2026 and the upcoming nda attempts. This is because joining of NDA 1 happens in January and you won't have passed 12th by then so youre not eligible for nda 1 during 12th or any previous attempts.",
            )
            embed.set_footer(text=f"Total Eligible Attempts: {len(eligible_attempts)}")
            await interaction.followup.send(embed=embed)

        except ValueError:
            await interaction.followup.send(
                "⚠️ Invalid date format. Please use `DD-MM-YYYY` (e.g., 01-07-2011)."
            )

    @app_commands.command(
        name="attemptcds",
        description="Calculate your CDS eligibility based on your date of birth.",
    )
    async def attemptcds(self, interaction: discord.Interaction, birthdate: str):
        """
        Calculates CDS eligibility based on DOB.
        Usage: /attemptcds DD-MM-YYYY
        Example: /attemptcds 23-09-2008
        """
        await interaction.response.defer()
        birthdate = str(birthdate).replace("/", "-")
        parts = birthdate.replace("/", "-").split("-")
        if len(parts) == 3:
            day = parts[0].zfill(2)
            month = parts[1].zfill(2)
            year = parts[2]
            birthdate = f"{day}-{month}-{year}"
        try:
            dob = datetime.strptime(birthdate, "%d-%m-%Y").date()
            today = date.today()
            current_year = today.year

            cds_attempts = {}

            for year in range(current_year, current_year + 6):
                # CDS 1 - February exam
                attempt1 = f"CDS 1 {year}"
                academies1 = []

                if date(year - 24, 1, 2) <= dob <= date(year - 20, 1, 1):
                    academies1.extend(["IMA", "INA", "AFA"])
                if date(year - 23, 1, 2) <= dob <= date(year - 19, 1, 1):
                    academies1.append("OTA")

                if academies1:
                    cds_attempts[attempt1] = academies1

                # CDS 2 - September exam
                attempt2 = f"CDS 2 {year}"
                academies2 = []

                if date(year - 24, 7, 2) <= dob <= date(year - 20, 7, 1):
                    academies2.extend(["IMA", "INA", "AFA"])
                if date(year - 23, 7, 2) <= dob <= date(year - 19, 7, 1):
                    academies2.append("OTA")

                if academies2:
                    cds_attempts[attempt2] = academies2

            if not cds_attempts:
                await interaction.followup.send(
                    "❌ You are not eligible for any upcoming CDS attempts based on your date of birth."
                )
                return

            embed = discord.Embed(
                title="CDS Eligibility Checker",
                description=f"Based on your birthdate: `{birthdate}`",
                color=discord.Color.green(),
            )

            total_attempts = len(cds_attempts)
            for attempt, academies in cds_attempts.items():
                embed.add_field(name=attempt, value=", ".join(academies), inline=False)

            embed.set_footer(text=f"Total Eligible CDS Attempts: {total_attempts}")
            await interaction.followup.send(embed=embed)

        except ValueError:
            await interaction.followup.send(
                "⚠️ Invalid date format. Please use `DD-MM-YYYY` (e.g., 01-07-2011)."
            )

    @commands.hybrid_command(name="timer", description="Start a timer with buttons.")
    async def timer(self, ctx: commands.Context, minutes: int = 25):
        view = timerView(user_id=ctx.author.id, duration=minutes, bot=ctx.bot)
        await view.start(
            ctx
        )  # This feels odd so I won't make this an interaction only command
        # Feels like it would fuck up since interaction responses tend to only want one reply
        # and they typically want it within a minute or so


# Timer backend code
class timerView(ui.View):
    def __init__(self, user_id: int, duration: int = 25, bot=None):
        super().__init__(timeout=None)
        self.bot = bot
        self.user_id = user_id
        self.duration = duration * 60
        self.remaining = self.duration
        self.paused = False
        self.stopped = False
        self._pause_event = asyncio.Event()
        self._pause_event.set()
        self._stop_event = asyncio.Event()
        self.message = None
        self.task = None
        self.start_time = None

    def _format_time(self, seconds: int) -> str:
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02}:{secs:02}"

    async def _get_user_display_name(self, guild: discord.Guild = None) -> str:
        member = None
        if guild:
            member = guild.get_member(self.user_id)
            if member is None:
                try:
                    member = await guild.fetch_member(self.user_id)
                except Exception:
                    pass
        if member:
            return member.display_name  # This respects nickname
        else:
            # fallback to user object
            user = self.bot.get_user(self.user_id) if self.bot else None
            if user is None:
                try:
                    user = await self.bot.fetch_user(self.user_id)
                except Exception:
                    return f"User {self.user_id}"
            return user.name  # Username only

    async def _get_embed(self, guild=None) -> discord.Embed:
        username = await self._get_user_display_name(guild)

        if self.stopped:
            embed = discord.Embed(
                title=f"Timer - {username}",
                description="🛑 Stopped",
                color=discord.Color.red(),
            )
        else:
            color = discord.Color.red() if self.paused else discord.Color.green()
            embed = discord.Embed(
                title=f"{self.duration // 60} mins timer - {username}",
                description=f"⏳ Time Remaining: `{self._format_time(self.remaining)}`",
                color=color,
            )
            if self.paused:
                embed.set_footer(text="⏸️ Paused")

        return embed

    async def start(self, ctx: commands.Context):
        self.start_time = datetime.now()
        embed = await self._get_embed(guild=ctx.guild)

        if ctx.interaction:
            await ctx.interaction.response.send_message(
                embed=embed, view=self
            )
            self.message = await ctx.interaction.original_response()
        else:
            self.message = await ctx.send(embed=embed, view=self)

        self.task = asyncio.create_task(self.run())

    async def run(self):
        try:
            while self.remaining > 0:
                await self._pause_event.wait()
                await asyncio.sleep(1)
                self.remaining -= 1

                if self._stop_event.is_set():
                    return

                embed = await self._get_embed(
                    guild=self.message.guild if self.message else None
                )
                await self.message.edit(embed=embed, view=self)

            # Timer finished - edit embed title and remove view/buttons
            embed = await self._get_embed(
                guild=self.message.guild if self.message else None
            )
            embed.title = "⏰ timer session complete!"
            await self.message.edit(embed=embed, view=None)

        except asyncio.CancelledError:
            return

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "This isn't your timer!", ephemeral=True
            )
            return False
        return True

    @ui.button(label="Pause", style=discord.ButtonStyle.primary)
    async def pause_button(self, interaction: Interaction, button: ui.Button):
        if not self.paused:
            # Pause timer
            self._pause_event.clear()
            self.paused = True
            button.label = "Resume"
        else:
            # Resume timer
            self._pause_event.set()
            self.paused = False
            button.label = "Pause"

        embed = await self._get_embed(guild=interaction.guild)
        await interaction.response.edit_message(embed=embed, view=self)

    @ui.button(label="Stop", style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: Interaction, button: ui.Button):
        self._stop_event.set()
        self.stopped = True
        if self.task:
            self.task.cancel()

        # Disable all buttons after stopping
        for child in self.children:
            child.disabled = True

        embed = await self._get_embed(guild=interaction.guild)
        await interaction.response.edit_message(embed=embed, view=self)


async def setup(bot):
    await bot.add_cog(Prep(bot))
