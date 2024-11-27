# pragyan
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", "25121213"))
API_HASH = getenv("API_HASH", "b734dcc45da130a8156e2be836594706")
BOT_TOKEN = getenv("BOT_TOKEN", "8163585103:AAGLD2IdPHN4X6bALJFQobNmJX0UQA4VF9c")
OWNER_ID = list(map(int, getenv("OWNER_ID", "8025794193").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://AvyukthX:AvyukthX@bot.ctdiudr.mongodb.net/?retryWrites=true&w=majority")
LOG_GROUP = getenv("LOG_GROUP", "-1002380299642")
#CHANNEL_ID = int(getenv("CHANNEL_ID", "-1001573605549"))
CHANNEL_USERNAME="@VRindavanNeeko16008"
FREEMIUM_LIMIT = int(getenv("FREEMIUM_LIMIT", "1000000000000000000000000000000000000000000000000"))
PREMIUM_LIMIT = int(getenv("PREMIUM_LIMIT", "5001000000000000000000000000000000000000000000000000"))
SESSION_CHANNEL=-1002437500909
