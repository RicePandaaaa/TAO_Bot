import discord
from discord.ext import commands
from discord.ext.commands import Context


class VoiceChannel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channel_number = 0
        self.voice_channels = []
        
    @commands.hybrid_command(aliases=["ohvc"])
    async def create_office_hours_vc(self, ctx: Context):
        """ Creates a voice channel for office hours """

        # Check user is in voice channel
        if ctx.author.voice is None:
            return await ctx.send("You need to be in a voice channel first.")

        # Create the voice channel
        vc_name = f"Office Hours {self.channel_number}"
        vc_reason = f"{ctx.author.display_name} has requested to make a voice channel."
        vc_cat = discord.utils.get(ctx.guild.categories, id=1070134666260140032)
        VC_SIZE = 2
        voice_channel = await discord.Guild.create_voice_channel(ctx.guild, name=vc_name, reason=vc_reason, category=vc_cat, user_limit=VC_SIZE)
        
        # Add the voice channel to the list and add the user to the vc
        self.voice_channels.append(voice_channel)
        await ctx.author.move_to(voice_channel)
        self.channel_number += 1

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """ Deletes inactive office hours voice channels """

        for index in range(len(self.voice_channels) - 1, -1, -1):
            channel = self.voice_channels[index]
            print(channel.voice_states)

            # Empty voice channel
            if len(channel.voice_states) == 0:
                self.voice_channels.pop(index)

                # Update max channel number
                if index == self.channel_number - 1:
                    self.channel_number -= 1

                await channel.delete()

async def setup(bot):
    await bot.add_cog(VoiceChannel(bot))
    