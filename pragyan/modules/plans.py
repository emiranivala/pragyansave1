#devgaganin

from datetime import timedelta
import pytz
import datetime, time
from devgagan import app
from config import OWNER_ID
from devgagan.core.func import get_seconds
from devgagan.core.mongo import plans_db  
from pyrogram import filters 



@app.on_message(filters.command("rem") & filters.user(OWNER_ID))
async def remove_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])  
        user = await client.get_users(user_id)
        data = await plans_db.check_premium(user_id)  
        
        if data and data.get("_id"):
            await plans_db.remove_premium(user_id)
            await message.reply_text("ᴜꜱᴇʀ ʀᴇᴍᴏᴠᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ !")
            await client.send_message(
                chat_id=user_id,
                text=f"<b>ʜᴇʏ {user.mention},\n\nʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ.\nᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴜsɪɴɢ ᴏᴜʀ sᴇʀᴠɪᴄᴇ 😊.</b>"
            )
        else:
            await message.reply_text("ᴜɴᴀʙʟᴇ ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴜꜱᴇᴅ !\nᴀʀᴇ ʏᴏᴜ ꜱᴜʀᴇ, ɪᴛ ᴡᴀꜱ ᴀ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ɪᴅ ?")
    else:
        await message.reply_text("ᴜꜱᴀɢᴇ : /rem user_id") 

@app.on_message(filters.command("check") & filters.user(OWNER_ID))
async def get_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        data = await plans_db.check_premium(user_id)  
        if data and data.get("expire_date"):
            expiry = data.get("expire_date") 
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")            
            
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            time_left = expiry_ist - current_time
            
            
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            
            time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
            await message.reply_text(f"⚜️ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ᴅᴀᴛᴀ :\n\n👤 ᴜꜱᴇʀ : {user.mention}\n⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n⏰ ᴛɪᴍᴇ ʟᴇꜰᴛ : {time_left_str}\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}")
        else:
            await message.reply_text("ɴᴏ ᴀɴʏ ᴘʀᴇᴍɪᴜᴍ ᴅᴀᴛᴀ ᴏꜰ ᴛʜᴇ ᴡᴀꜱ ꜰᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀꜱᴇ !")
    else:
        await message.reply_text("ᴜꜱᴀɢᴇ : /check user_id")


@app.on_message(filters.command("myplan"))
async def myplan(client, message):
    user_id = message.from_user.id
    user = message.from_user.mention
    data = await plans_db.check_premium(user_id)  
    if data and data.get("expire_date"):
        expiry = data.get("expire_date")
        expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")            
        
        current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
        time_left = expiry_ist - current_time
            
        
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
            
        
        time_left_str = f"{days} ᴅᴀʏꜱ, {hours} ʜᴏᴜʀꜱ, {minutes} ᴍɪɴᴜᴛᴇꜱ"
        await message.reply_text(f"⚜️ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ᴅᴀᴛᴀ :\n\n👤 ᴜꜱᴇʀ : {user}\n⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n⏰ ᴛɪᴍᴇ ʟᴇꜰᴛ : {time_left_str}\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}")   
    else:
        await message.reply_text(f"ʜᴇʏ {user},\n\nʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴʏ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs")
        


@app.on_message(filters.command("add") & filters.user(OWNER_ID))
async def give_premium_cmd_handler(client, message):
    time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
    current_time = time_zone.strftime("%d-%m-%Y\n⏱️ ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ : %I:%M:%S %p") 

    # Check if the command is a reply
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user = message.reply_to_message.from_user.mention
    elif len(message.command) == 3:
        # Check if a username is provided
        username = message.command[1]
        try:
            user = await client.get_users(username)
            user_id = user.id
        except Exception:
            await message.reply_text("Invalid username. Please provide a valid username.")
            return
    elif len(message.command) == 4:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
    else:
        await message.reply_text("Usage: /add <username> <time> or reply to a user with the command.")
        return

    time_input = message.command[-1]
    seconds = await get_seconds(time_input)

    # Ensure seconds is an integer
    if isinstance(seconds, str):
        try:
            seconds = int(seconds)
        except ValueError:
            await message.reply_text("Invalid time format. Please use a valid time format.")
            return

    if seconds > 0:
        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)  
        await plans_db.add_premium(user_id, expiry_time)  
        data = await plans_db.check_premium(user_id)
        expiry = data.get("expire_date")   
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")         
        
        await message.reply_text(f"ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ✅\n\n👤 ᴜꜱᴇʀ : {user}\n⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time_input}</code>\n\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist} \n\n__**Powered by Pragyan__**", disable_web_page_preview=True)

        await client.send_message(
            chat_id=user_id,
            text=f"👋 ʜᴇʏ {user},\nᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴘᴜʀᴄʜᴀꜱɪɴɢ ᴘʀᴇᴍɪᴜᴍ.\nᴇɴᴊᴏʏ !! ✨🎉\n\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time_input}</code>\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}", disable_web_page_preview=True
        )    
    else:
        await message.reply_text("Invalid time format. Please use '1 day for days', '1 hour for hours', '1 min for minutes', '1 month for months', or '1 year for years'.")

async def give_premium_cmd_handler(client, message):
    time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
    current_time = time_zone.strftime("%d-%m-%Y\n⏱️ ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ : %I:%M:%S %p") 

    # Check if the command is a reply
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user = message.reply_to_message.from_user.mention
    elif len(message.command) == 3:
        # Check if a username is provided
        username = message.command[1]
        try:
            user = await client.get_users(username)
            user_id = user.id
        except Exception:
            await message.reply_text("Invalid username. Please provide a valid username.")
            return
    elif len(message.command) == 4:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
    else:
        await message.reply_text("Usage: /add <username> <time> or reply to a user with the command.")
        return

    time_input = message.command[-1]
    seconds = await get_seconds(time_input)

    # Ensure seconds is an integer
    if isinstance(seconds, str):
        try:
            seconds = int(seconds)
        except ValueError:
            await message.reply_text("Invalid time format. Please use a valid time format.")
            return

    if seconds > 0:
        expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)  
        await plans_db.add_premium(user_id, expiry_time)  
        data = await plans_db.check_premium(user_id)
        expiry = data.get("expire_date")   
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")         
        
        await message.reply_text(f"ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ✅\n\n👤 ᴜꜱᴇʀ : {user}\n⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time_input}</code>\n\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist} \n\n__**Powered by Pragyan__**", disable_web_page_preview=True)

        await client.send_message(
            chat_id=user_id,
            text=f"👋 ʜᴇʏ {user},\nᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴘᴜʀᴄʜᴀꜱɪɴɢ ᴘʀᴇᴍɪᴜᴍ.\nᴇɴᴊᴏʏ !! ✨🎉\n\n⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : <code>{time_input}</code>\n⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {current_time}\n\n⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}", disable_web_page_preview=True
        )    
    else:
        await message.reply_text("Invalid time format. Please use '1 day for days', '1 hour for hours', '1 min for minutes', '1 month for months', or '1 year for years'.")

        await message.reply_text("Invalid time format. Please use '1 day for days', '1 hour for hours', or '1 min for minutes', or '1 month for months' or '1 year for year'")
