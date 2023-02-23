import discord, csv
from helper_classes.pt import PT
from discord.ext import commands
from datetime import datetime

class OfficeHours(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.file_name = "cogs/pt_hours.csv"
        self.pts = {}

    def load_information(self):
        """ Create the PT objects based on the CSV file """
        with open(self.file_name,  "r") as file:
            reader = csv.reader(file, delimiter=",")

            # Go through row by row and only generate on complete entries
            for row in reader:
                name = row[4]

                # No name
                if name == "": 
                    continue

                # Create the PT if necessary
                if name not in self.pts:
                    self.pts[name] = PT()

                # Update the PT's information
                pt = self.pts[name]
                pt.add_class(row[0], row[1], row[2])
                pt.update_email(row[3])
                pt.update_name(row[4])
                pt.update_link(row[5])

    def convert_time(self, time: str):
        """ Takes the input times and splits into two 24 hour format times """
        formatted_time = "".join(time.split(" ")).upper()

        times = formatted_time.split("-")
        start, end = self.convert_ampm_to_military(times[0]), self.convert_ampm_to_military(times[1])

        print(start, end)

    def convert_ampm_to_military(self, time: str):
        """ Converts times from AM/PM format to 24 hour format """
        am_pm_time = datetime.strptime(time, "%I:%M%p")
        military_time = datetime.strftime(am_pm_time, "%H:%M")

        return military_time
        


OfficeHours(None).convert_time("11:00am - 12:45PM")
    

    
async def setup(bot):
    await bot.add_cog(OfficeHours(bot))