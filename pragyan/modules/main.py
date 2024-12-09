import time
import random
import string
import asyncio
from pyrogram import filters, Client
from pragyan import app
from config import API_ID, API_HASH, FREEMIUM_LIMIT, PREMIUM_LIMIT, OWNER_ID
from pragyan.core.get_func import get_msg
from pragyan.core.func import *
from pragyan.core.mongo import db
from pyrogram.errors import FloodWait


async def generate_random_name(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


users_loop = {}


from telethon import events

# Handler for the /setchat <id> command
@gf.on(events.NewMessage(pattern='/setchat (\d+)'))
async def set_chat_command(event):
    user_id = event.sender_id
    chat_id = int(event.pattern_match.group(1))  # Extract the chat ID from the command
    # Set session type to 'setchat' for this user
    sessions[user_id] = 'setchat'
    user_chat_ids[user_id] = chat_id  # Save the chat ID for the user
    await event.respond(f"Session set to 'setchat'. Chat ID is {chat_id}.")

# Your existing handler for processing user input in 'setchat' session
@gf.on(events.NewMessage)
async def handle_user_input(event):
    user_id = event.sender_id
    if user_id in sessions:
        session_type = sessions[user_id]

        if session_type == 'setchat':
            try:
                chat_id = int(event.text)
                user_chat_ids[user_id] = chat_id
                await event.respond("Chat ID set successfully!")
            except ValueError:
                await event.respond("Invalid chat ID!")
        
        elif session_type == 'setrename':
            custom_rename_tag = event.text
            await set_rename_command(user_id, custom_rename_tag)
            await event.respond(f"Custom rename tag set to: {custom_rename_tag}")
        
        elif session_type == 'setcaption':
            custom_caption = event.text
            await set_caption_command(user_id, custom_caption)
            await event.respond(f"Custom caption set to: {custom_caption}")

        elif session_type == 'setreplacement':
            match = re.match(r"'(.+)' '(.+)'", event.text)
            if not match:
                await event.respond("Usage: 'WORD(s)' 'REPLACEWORD'")
            else:
                word, replace_word = match.groups()
                delete_words = load_delete_words(user_id)
                if word in delete_words:
                    await event.respond(f"The word '{word}' is in the delete set and cannot be replaced.")
                else:
                    replacements = load_replacement_words(user_id)
                    replacements[word] = replace_word
                    save_replacement_words(user_id, replacements)
                    await event.respond(f"Replacement saved: '{word}' will be replaced with '{replace_word}'")

        elif session_type == 'addsession':
            # Store session string in MongoDB
            session_data = {
                "user_id": user_id,
                "session_string": event.text
            }
            mcollection.update_one(
                {"user_id": user_id},
                {"$set": session_data},
                upsert=True
            )
            await event.respond("Session string added successfully.")
                
        elif session_type == 'deleteword':
            words_to_delete = event.message.text.split()
            delete_words = load_delete_words(user_id)
            delete_words.update(words_to_delete)
            save_delete_words(user_id, delete_words)
            await event.respond(f"Words added to delete list: {', '.join(words_to_delete)}")

        
@app.on_message(filters.regex(r'https?://[^\s]+'))
async def single_link(_, message):
    user_id = message.chat.id
    
    # Check if the user is already in the loop
    if users_loop.get(user_id, False):
        await message.reply(
            "You already have an ongoing process. Please wait for it to finish or cancel it with /cancel."
        )
        return    
        
    freecheck = await chk_user(message, user_id)
    if freecheck == 1 and FREEMIUM_LIMIT == 0 and user_id not in OWNER_ID:
        await message.reply("Freemium service is currently not available. Upgrade to premium for access.")
        return

    # Add the user to the loop
    users_loop[user_id] = True
    link = get_link(message.text) 
    userbot = None
    try:
        join = await subscribe(_, message)
        if join == 1:
            users_loop[user_id] = False
            return
     
        
        msg = await message.reply("Processing...")
        
        if 't.me/' in link and 't.me/+' not in link and 't.me/c/' not in link and 't.me/b/' not in link:
            await get_msg(None, user_id, msg.id, link, 0, message)
            # await msg.edit_text("Processed successfully without userbot!")
            return
            
        data = await db.get_data(user_id)
        
        if data and data.get("session"):
            session = data.get("session")
            try:
                device = 'Vivo Y20'
                session_name = await generate_random_name()
                userbot = Client(session_name, api_id=API_ID, api_hash=API_HASH, device_model=device, session_string=session)
                await userbot.start()                
            except:
                users_loop[user_id] = False
                return await msg.edit_text("Login expired /login again...")
        else:
            users_loop[user_id] = False
            await msg.edit_text("Login in bot first ...")
            return

        try:
            if 't.me/+' in link:
                q = await userbot_join(userbot, link)
                await msg.edit_text(q)
            elif 't.me/c/' in link:
                await get_msg(userbot, user_id, msg.id, link, 0, message)
            else:
                await msg.edit_text("Invalid link format.")
        except Exception as e:
            await msg.edit_text(f"Link: `{link}`\n\n**Error:** {str(e)}")
            
    except FloodWait as fw:
        await msg.edit_text(f'Try again after {fw.x} seconds due to floodwait from telegram.')
        
    except Exception as e:
        await msg.edit_text(f"Link: `{link}`\n\n**Error:** {str(e)}")
    finally:
        if userbot and userbot.is_connected:  # Ensure userbot was initialized and started
            await userbot.stop()
        users_loop[user_id] = False  # Remove user from the loop after processing


@app.on_message(filters.command("cancel"))
async def stop_batch(_, message):
    user_id = message.chat.id

    # Check if there is an active batch process for the user
    if user_id in users_loop and users_loop[user_id]:
        users_loop[user_id] = False  # Set the loop status to False
        await app.send_message(
            message.chat.id, 
            "Batch processing has been stopped successfully. You can start a new batch now if you want."
        )
    elif user_id in users_loop and not users_loop[user_id]:
        await app.send_message(
            message.chat.id, 
            "The batch process was already stopped. No active batch to cancel."
        )
    else:
        await app.send_message(
            message.chat.id, 
            "No active batch processing is running to cancel."
        )
        
# --------- PUBLIC CHANNEL 
@app.on_message(filters.command("batch"))
async def batch_link(_, message):
    user_id = message.chat.id

    if users_loop.get(user_id, False):  # Check if a batch process is already running
        await app.send_message(
            message.chat.id,
            "You already have a batch process running. Please wait for it to complete before starting a new one."
        )
        return

    # Determine user's limits based on their subscription
    lol = await chk_user(message, user_id)
    if lol == 1:
        max_batch_size = FREEMIUM_LIMIT  # Limit for free users
    else:
        max_batch_size = PREMIUM_LIMIT

    # Ask for start and end links
    start = await app.ask(message.chat.id, text="Please send the start link.")
    start_id = start.text
    s = start_id.split("/")[-1]
    cs = int(s)

    last = await app.ask(message.chat.id, text="Please send the end link.")
    last_id = last.text
    l = last_id.split("/")[-1]
    cl = int(l)

    # Check batch size
    if user_id not in OWNER_ID and (cl - cs) > max_batch_size:
        await app.send_message(
            message.chat.id,
            f"Batch size exceeds the limit of {max_batch_size}. Upgrade to premium for larger batch sizes."
        )
        return

    # Start processing links
    users_loop[user_id] = True
    try:
        # FIRST ITERATION: Process t.me/ links without userbot
        for i in range(cs, cl):
            if user_id in users_loop and users_loop[user_id]:
                try:
                    # Construct the link
                    x = start_id.split('/')
                    y = x[:-1]
                    result = '/'.join(y)
                    url = f"{result}/{i}"
                    link = get_link(url)

                    # Directly process links like t.me/ (no userbot needed)
                    if 't.me/' in link and 't.me/b/' not in link and 't.me/c' not in link:
                        msg = await app.send_message(message.chat.id, f"Processing link {url}...")
                        await get_msg(None, user_id, msg.id, link, 0, message)
                        sleep_msg = await app.send_message(
                                message.chat.id,
                                "Sleeping for 5 seconds to avoid flood..."
                        )
                        # Add delay to avoid floodwait
                        await asyncio.sleep(8)
                        await sleep_msg.delete()
                except Exception as e:
                    print(f"Error processing link {url}: {e}")
                    continue
                    
        if not any(prefix in start_id for prefix in ['t.me/c/', 't.me/b/']):
            # await app.send_message(message.chat.id, "Skipping second iteration as the link is not valid.")
            await app.send_message(message.chat.id, "Batch completed successfully! 🎉")
            return
        # edit kr lena kuchhu dikkat ho to
        data = await db.get_data(user_id)
        if data and data.get("session"):
            session = data.get("session")
            device = 'Vivo Y20'
            session_name = await generate_random_name()
            userbot = Client(
                session_name,
                api_id=API_ID,
                api_hash=API_HASH,
                device_model=device,
                session_string=session
            )
            await userbot.start()
        else:
            await app.send_message(message.chat.id, "Login in bot first ...")
            return

        try:
            for i in range(cs, cl):
                if user_id in users_loop and users_loop[user_id]:
                    try:
                        # Construct the link
                        x = start_id.split('/')
                        y = x[:-1]
                        result = '/'.join(y)
                        url = f"{result}/{i}"
                        link = get_link(url)

                        # Process links requiring userbot
                        if 't.me/b/' in link or 't.me/c/' in link:
                            msg = await app.send_message(message.chat.id, f"Processing link {url}...")
                            await get_msg(userbot, user_id, msg.id, link, 0, message)

                            # Add delay to avoid floodwait
                            sleep_msg = await app.send_message(
                                message.chat.id,
                                "Sleeping for 20 seconds to avoid flood..."
                            )
                            await asyncio.sleep(18)
                            await sleep_msg.delete()
                            await asyncio.sleep(2)
                    except Exception as e:
                        print(f"Error processing link {url}: {e}")
                        continue
        finally:
            if userbot.is_connected:
                await userbot.stop()

        await app.send_message(message.chat.id, "Batch completed successfully! 🎉")
    except FloodWait as fw:
        await app.send_message(
            message.chat.id,
            f"Try again after {fw.x} seconds due to floodwait from Telegram."
        )
    except Exception as e:
        await app.send_message(message.chat.id, f"Error: {str(e)}")
    finally:
        users_loop.pop(user_id, None)

    
