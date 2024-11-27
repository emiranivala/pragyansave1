from time import time
from speedtest import Speedtest
from pyrogram import Client, filters
from config import OWNER_ID

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
    download_speed = test.download()
    upload_speed = test.upload()

    # Wait for both tests to complete (using `test.results` to get results after both tests)
    test_results = test.results.dict()

    # Format the output message
    string_speed = f'''
╭─《 🚀 SPEEDTEST INFO 》
├ <b>Upload:</b> <code>{speed_convert(download_speed, False)}</code>
├ <b>Download:</b>  <code>{speed_convert(upload_speed, False)}</code>
├ <b>Ping:</b> <code>{test_results['ping']} ms</code>
├ <b>Time:</b> <code>{test_results['timestamp']}</code>
├ <b>Data Sent:</b> <code>{get_readable_file_size(int(test_results['bytes_sent']))}</code>
╰ <b>Data Received:</b> <code>{get_readable_file_size(int(test_results['bytes_received']))}</code>
╭─《 🌐 SPEEDTEST SERVER 》
├ <b>Name:</b> <code>{test_results['server']['name']}</code>
├ <b>Country:</b> <code>{test_results['server']['country']}, {test_results['server']['cc']}</code>
├ <b>Sponsor:</b> <code>{test_results['server']['sponsor']}</code>
├ <b>Latency:</b> <code>{test_results['server']['latency']}</code>
├ <b>Latitude:</b> <code>{test_results['server']['lat']}</code>
╰ <b>Longitude:</b> <code>{test_results['server']['lon']}</code>
╭─《 👤 CLIENT DETAILS 》
├ <b>IP Address:</b> <code>{test_results['client']['ip']}</code>
├ <b>Latitude:</b> <code>{test_results['client']['lat']}</code>
├ <b>Longitude:</b> <code>{test_results['client']['lon']}</code>
├ <b>Country:</b> <code>{test_results['client']['country']}</code>
├ <b>ISP:</b> <code>{test_results['client']['isp']}</code>
╰ <b>ISP Rating:</b> <code>{test_results['client']['isprating']}</code>
'''

    try:
        # Send the speed test results with the screenshot (if available)
        await message.reply(string_speed, file=test_results['share'], parse_mode='html')
        await speed.delete()  # Delete the initial speed test message
    except Exception as e:
        print(e)  # Log any errors that occur
        await speed.delete()
        await message.reply(string_speed, parse_mode='html')  # Send the result even if screenshot fails

# Event handler for /stats command
@app.on_message(filters.command("stats"))
async def stats(client, message):
    # Assume get_users() retrieves the user list
    users = len(await get_users())  # Replace with your logic to get the user list
    # Assume premium_users() retrieves premium users
    premium = await premium_users()  # Replace with your logic to get premium users
    await message.reply_text(f"""
**Total Stats of** {(await client.get_me()).mention} :

**Total Users** : {users}
**Premium Users** : {len(premium)}

**__Powered by Pragyan__**
""")

