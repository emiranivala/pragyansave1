from time import time
from speedtest import Speedtest
from telethon import events
from pyrogram import filters
from config import OWNER_ID

# Define constants for the size units
SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

# Function to convert seconds into a readable time format
def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result

# Function to convert file size into a human-readable format
def get_readable_file_size(size_in_bytes) -> str:
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)}{SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'

# Function to convert speed into a human-readable format
def speed_convert(size, byte=True):
    if not byte: size = size / 8  # Convert bits to bytes
    power = 2 ** 10
    zero = 0
    units = {0: "B/s", 1: "KB/s", 2: "MB/s", 3: "GB/s", 4: "TB/s"}
    while size >= power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"

# Event handler for /speedtest command
@app.on_message(filters.command("speedtest"))
async def speedtest(client, message):
    speed = await message.reply("Running Speed Test. Please wait a moment...")

    # Initialize Speedtest object
    test = Speedtest()
    test.get_best_server()  # Get the best server for the test

    # Perform download and upload speed tests
    test.download()
    test.upload()
    test.results.share()  # Share the results for screenshot link
    result = test.results.dict()  # Get result in dictionary format

    # Format the output message
    currentTime = get_readable_time(time() - botStartTime)
    string_speed = f'''
╭─《 🚀 SPEEDTEST INFO 》
├ <b>Upload:</b> <code>{speed_convert(result['upload'], False)}</code>
├ <b>Download:</b>  <code>{speed_convert(result['download'], False)}</code>
├ <b>Ping:</b> <code>{result['ping']} ms</code>
├ <b>Time:</b> <code>{result['timestamp']}</code>
├ <b>Data Sent:</b> <code>{get_readable_file_size(int(result['bytes_sent']))}</code>
╰ <b>Data Received:</b> <code>{get_readable_file_size(int(result['bytes_received']))}</code>
╭─《 🌐 SPEEDTEST SERVER 》
├ <b>Name:</b> <code>{result['server']['name']}</code>
├ <b>Country:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
├ <b>Sponsor:</b> <code>{result['server']['sponsor']}</code>
├ <b>Latency:</b> <code>{result['server']['latency']}</code>
├ <b>Latitude:</b> <code>{result['server']['lat']}</code>
╰ <b>Longitude:</b> <code>{result['server']['lon']}</code>
╭─《 👤 CLIENT DETAILS 》
├ <b>IP Address:</b> <code>{result['client']['ip']}</code>
├ <b>Latitude:</b> <code>{result['client']['lat']}</code>
├ <b>Longitude:</b> <code>{result['client']['lon']}</code>
├ <b>Country:</b> <code>{result['client']['country']}</code>
├ <b>ISP:</b> <code>{result['client']['isp']}</code>
╰ <b>ISP Rating:</b> <code>{result['client']['isprating']}</code>
'''

    try:
        # Send the speed test results with the screenshot (if available)
        await message.reply(string_speed, file=result['share'], parse_mode='html')
        await speed.delete()  # Delete the initial speed test message
    except Exception as e:
        print(e)  # Log any errors that occur
        await speed.delete()
        await message.reply(string_speed, parse_mode='html')  # Send the result even if screenshot fails

# Event handler for /stats command
@app.on_message(filters.command("stats"))
async def stats(client, message):
    users = len(await get_users())  # Assume get_users() retrieves the user list
    premium = await premium_users()  # Assume premium_users() retrieves premium users
    await message.reply_text(f"""
**Total Stats of** {(await client.get_me()).mention} :

**Total Users** : {users}
**Premium Users** : {len(premium)}

**__Powered by Pragyan__**
""")
