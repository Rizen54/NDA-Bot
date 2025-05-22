from datetime import datetime, date, timedelta
import discord
from discord import app_commands, Interaction, ui
from discord.ext import commands
import asyncio


class Prep(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="nda", description="Get an in-depth NDA guide")
    async def nda_guide(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📚 NDA Guide",
            description="Here is an in-depth nda guide:",
            color=discord.Color.blue(),
        )
        embed.add_field(
            name="Link:",
            value="https://tranquilizer014.blogspot.com/2025/02/nda-national-defence-academy-entry.html",
            inline=True,
        )
        embed.add_field(name="By", value="Tranquilizer", inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="cds", description="Get an in-depth CDS guide")
    async def cds_guide(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📚 CDS Guide",
            description="Here is an in-depth CDS guide:",
            color=discord.Color.blue(),
        )
        embed.add_field(
            name="Link:",
            value="https://tranquilizer014.blogspot.com/2025/02/combined-defence-services-cds.html",
            inline=True,
        )
        embed.set_footer(text="By Tranquilizer")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="wiki", description="Get the r/NDATards official wiki link"
    )
    async def wiki(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📖 Wiki",
            description="Here is the official r/NDATards wiki:",
            color=discord.Color.blue(),
        )
        embed.add_field(
            name="Link:",
            value="https://www.reddit.com/r/NDATards/comments/1kgn848/rndatards_official_wiki/",
            inline=True,
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

    @app_commands.command(
        name="daysleftto",
        description="Gives number of days remaining to nda or cds exam",
    )
    async def dlte(self, interaction: discord.Interaction, exam: str):
        if exam == "nda":
            exam_date = datetime(2025, 9, 14)  # NDA 2 2025
            today = datetime.now()
            days_remaining = (exam_date - today).days
        elif exam == "cds":
            exam_date = datetime(2025, 9, 14)  # CDS 2 2025
            today = datetime.now()
            days_remaining = (exam_date - today).days

        embed = discord.Embed(colour=discord.Colour.red())

        if days_remaining > 0:
            embed.title = f"🗓️ ``{days_remaining} days`` left until the {exam} exam on `{exam_date.date()}`."
        elif days_remaining == 0:
            embed.title = f"🎯 The {exam} exam is **today**! Give it your best!"
        else:
            embed.title = f"✅ The last {exam} exam date has **passed**. Date for the next will be set soon."

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
            birthdate = str(birthdate)
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
                nda2_start = date(year - 19, 1, 2)
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
                title=f"timer - {username}",
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
                embed=embed, view=self, ephemeral=True
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
