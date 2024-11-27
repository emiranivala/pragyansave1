#devggn

from pragyan import app
from pyrogram import filters
from config import OWNER_ID
from pragyan.core.mongo.users_db import get_users, add_user, get_user
from pragyan.core.mongo.plans_db import premium_users

from speedtest import Speedtest



@app.on_message(group=10)
async def chat_watcher_func(_, message):
    try:
        if message.from_user:
            us_in_db = await get_user(message.from_user.id)
            if not us_in_db:
                await add_user(message.from_user.id)
    except:
        pass


@app.on_message(filters.command("stats"))
async def stats(client, message):
    users = len(await get_users())
    premium = await premium_users()
    await message.reply_text(f"""
**Total Stats of** {(await client.get_me()).mention} :

**Total Users** : {users}
**Premium Users** : {len(premium)}

**__Powered by Pragyan__**
""")

from speedtest import Speedtest

# Define the speed_convert function
def speed_convert(speed, to_mbps=True):
    """
    Converts speed from bits to human-readable format (e.g., Mbps, Gbps).
    
    :param speed: The speed in bits per second.
    :param to_mbps: If True, convert to Mbps. If False, return as raw bits.
    :return: A string with the formatted speed.
    """
    if to_mbps:
        # Convert bits to Megabits
        speed = speed / 1_000_000
        return f"{speed:.2f} Mbps"
    else:
        # Convert bits to Gigabits
        speed = speed / 1_000_000_000
        return f"{speed:.2f} Gbps"

# Define the get_readable_file_size function
def get_readable_file_size(size_in_bytes):
    """
    Converts a size in bytes to a human-readable format (KB, MB, GB, etc.).
    
    :param size_in_bytes: The size in bytes.
    :return: A string with the readable size.
    """
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    unit_index = 0
    size = size_in_bytes
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.2f} {units[unit_index]}"

def convert_to_mbps(speed_in_gbps):
    return speed_in_gbps * 1000  # 1 Gbps = 1000 Mbps

# Speedtest function
@app.on_message(filters.command("speedtest"))
async def speedtest(client, message):
    speed = await message.reply("Running Speed Test. Please wait a moment...")

    # Initialize Speedtest object
    test = Speedtest()
    test.get_best_server()  # Get the best server for the test

    # Perform download and upload speed tests
    download_speed = test.download() / 1_000_000  # Convert from bits to Mbps
    upload_speed = test.upload() / 1_000_000  # Convert from bits to Mbps

    # Wait for both tests to complete (using `test.results` to get results after both tests)
    test_results = test.results.dict()

    # Convert the speeds to Mbps
    download_speed_mbps = convert_to_mbps(download_speed)
    upload_speed_mbps = convert_to_mbps(upload_speed)

    # Format the output message
    string_speed = f'''
╭─《 🚀 SPEEDTEST INFO 》
├ <b>Upload:</b> <code>{upload_speed_mbps:.2f} Mbps</code>
├ <b>Download:</b>  <code>{download_speed_mbps:.2f} Mbps</code>
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
        if 'share' in test_results and test_results['share']:
            await message.reply_photo(test_results['share'], caption=string_speed)
        else:
            # If no screenshot is available, just send the message
            await message.reply_text(string_speed)  # No parse_mode used

        await speed.delete()  # Delete the initial speed test message
    except Exception as e:
        print(e)  # Log any errors that occur
        await speed.delete()
        await message.reply_text(string_speed)  # Send t
