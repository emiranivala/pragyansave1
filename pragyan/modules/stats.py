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

