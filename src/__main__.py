import logging  # log handler
import os
import sys
import discord  # py-cord: discord bot framework
from yaml import safe_load as load_yaml

__version__ = "0.0.1"
__program__ = "example"

logger = logging.getLogger(__program__)  # get the logger for this script
handler = logging.StreamHandler(stream=sys.stdout)  # set logs to be sent to stdout
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)  # attach the handler to the logger
logger.setLevel(logging.DEBUG)  # set the logs to output at debug verbosity
logger.info("Logging started")

config_file = str(os.getenv(f"{__program__.upper()}_CONFIG_FILE"))
if not os.path.isfile(config_file): # check the config file actually exists
    msg = f"{__program__.upper()}_CONFIG_FILE environment variable is not a valid path, cannot start"
    logger.error(msg)
    sys.exit()

# read config file
with open(config_file, "r") as file:
    config = load_yaml(file)
config = config["config"]
logger.info("Config loaded")

with open(config["token_file"], "r") as file: # read the token file
    token = file.read()
logger.info('Token loaded')

# create the Bot object
intents = discord.Intents.default()
intents.members = True
bot = discord.Bot(intents = intents)  # create a bot instance
logger.debug("Bot object created")

@bot.event
async def on_ready() -> None:
    activity = discord.Game("Status...")
    status = discord.Status.online
    await bot.change_presence(activity=activity, status=status)
    logger.info("Bot started, ready for interaction")

@bot.event
async def on_application_command_error(ctx:discord.ApplicationContext, error:discord.DiscordException):
      logger.error(error, stack_info = True, exc_info = True)
      await ctx.channel.send(f'<@{config["error_ping"]}> An unspecified error occurred.')

bot.run(token)
