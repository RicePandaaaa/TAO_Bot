import discord, typing
from discord.ext import commands
from discord.ext.commands import Context, Greedy


class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def sync(self, ctx: Context, guilds: Greedy[discord.Object], spec: typing.Optional[typing.Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException as error:
                print(error)
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @commands.hybrid_command()
    async def howdy(self, ctx: Context):
        """ Basic command for obtaining info about the bot """
        await ctx.send("Howdy, I was created to assist PTs and professors in managing voice channels for one-on-one " \
                        "sessions for students and content reviews. I can also provide students with information " \
                        "related to office hours! Please type `!help` for a complete command list!")

    @commands.hybrid_command(aliases=["oh"])
    async def officehours(self, ctx: Context):
        """ Basic command redirecting users to the office hours channel (for now) """
        await ctx.send("This bot is still under developement! Please consult the <#1070134719754289194> channel" \
                       " to see office hours posted by your PTs!")


async def setup(bot):
    await bot.add_cog(General(bot))
