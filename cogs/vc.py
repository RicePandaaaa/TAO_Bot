import discord
from discord.ext import commands
from discord.ext.commands import Context


class VoiceChannel(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channel_number = 0
        self.voice_channels = []
        self.queue = []
        
    @commands.hybrid_command(aliases=["ohvc"])
    @commands.has_role("Panda Overlord")
    async def create_office_hours_vc(self, ctx: Context, room_size: int=2):
        """ Creates a voice channel for office hours """

        # Check user is in voice channel
        if ctx.author.voice is None:
            return await ctx.send("You need to be in a voice channel first.")

        # Validate the room size
        if room_size < 2:
            return await ctx.send("Your room size must be at least 2.")

        # Create the voice channel
        vc_name = f"Office Hours {self.channel_number}"
        vc_reason = f"{ctx.author.display_name} has requested to make a voice channel."
        vc_cat = discord.utils.get(ctx.guild.categories, id=1070134666260140032)
        voice_channel = await discord.Guild.create_voice_channel(ctx.guild, name=vc_name, reason=vc_reason, category=vc_cat, user_limit=room_size)
        
        # Add the voice channel to the list and add the user to the vc
        self.voice_channels.append(voice_channel)
        await ctx.author.move_to(voice_channel)
        self.channel_number += 1

    @commands.hybrid_command(aliases=["cq"])
    async def check_queue(self, ctx: Context):
        """ Outputs the first ten people in queue and the user's current position, if in queue """
        
        # Empty queue
        if len(self.queue) == 0:
            return await ctx.send("The queue is currently empty.")

        else:
            output = ""
            place = -1
            for index, member in enumerate(self.queue, start=1):
                output += f"{index}. {member.name}\n"

                # Save place if user is found in queue
                if member.id == ctx.author.id:
                    place = index
                
                # Stop once ten people are processed
                if index == 10:
                    break

            # Output
            placement = "" if (place == -1) else f"\n\nYour current position in queue is: {place}."
            await ctx.send(output + placement)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        """ Deletes inactive office hours voice channels and updates the queue """

        # Check for empty office hours voice channels
        for index in range(len(self.voice_channels) - 1, -1, -1):
            channel = self.voice_channels[index]

            # Empty voice channel
            if len(channel.voice_states) == 0:
                self.voice_channels.pop(index)

                # Update max channel number
                if index == self.channel_number - 1:
                    self.channel_number -= 1

                await channel.delete()

        # Remove user from the queue
        if before is not None and before.channel.id == 1070153319034667058:
            for index in range(len(self.queue) - 1, -1, -1):
                if self.queue[index].id == member.id:
                    self.queue.pop(index)

        # Add user to the queue
        if after is not None and after.channel.id == 1070153319034667058:
            self.queue.append(member)

        

async def setup(bot):
    await bot.add_cog(VoiceChannel(bot))
    