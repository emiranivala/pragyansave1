import speedtest
from pragyan import app
from pyrogram import filters
from config import OWNER_ID
from pragyan.core.mongo.users_db import get_users, add_user, get_user
from pragyan.core.mongo.plans_db import premium_users

# Function to convert bytes to a human-readable file size
def get_readable_file_size(size_in_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0

# Function to convert speed (in bits per second) to a readable format
def speed_convert(speed, is_upload=True):
    if is_upload:
        return get_readable_file_size(speed / 8)  # Convert bits to bytes
    else:
        return get_readable_file_size(speed / 8)  # Convert bits to bytes

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

@app.on_message(filters.command("speedtest"))
async def speedtest_func(client, message):
    # Initialize Speedtest object
    st = speedtest.Speedtest()

    # Get best server for testing
    st.get_best_server()

    # Perform the speed test
    result = st.results.dict()

    # Prepare the message with the speedtest results
    speedtest_message = f"""
🚀 <b>SPEEDTEST INFO</b>
├ <b>Upload:</b> <code>{speed_convert(result['upload'], False)}</code>
├ <b>Download:</b>  <code>{speed_convert(result['download'], False)}</code>
├ <b>Ping:</b> <code>{result['ping']} ms</code>
├ <b>Time:</b> <code>{result['timestamp']}</code>
├ <b>Data Sent:</b> <code>{get_readable_file_size(int(result['bytes_sent']))}</code>
╰ <b>Data Received:</b> <code>{get_readable_file_size(int(result['bytes_received']))}</code>

🌐 <b>SPEEDTEST SERVER</b>
├ <b>Name:</b> <code>{result['server']['name']}</code>
├ <b>Country:</b> <code>{result['server']['country']}, {result['server']['cc']}</code>
├ <b>Sponsor:</b> <code>{result['server']['sponsor']}</code>
├ <b>Latency:</b> <code>{result['server']['latency']}</code>
├ <b>Latitude:</b> <code>{result['server']['lat']}</code>
╰ <b>Longitude:</b> <code>{result['server']['lon']}</code>

👤 <b>CLIENT DETAILS</b>
├ <b>IP Address:</b> <code>{result['client']['ip']}</code>
├ <b>Latitude:</b> <code>{result['client']['lat']}</code>
├ <b>Longitude:</b> <code>{result['client']['lon']}</code>
├ <b>Country:</b> <code>{result['client']['country']}</code>
├ <b>ISP:</b> <code>{result['client']['isp']}</code>
╰ <b>ISP Rating:</b> <code>{result['client']['isprating']}</code>
    """

    # Send the speedtest result as a reply
    await message.reply_text(speedtest_message)
