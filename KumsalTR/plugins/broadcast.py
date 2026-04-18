import os
import asyncio

from pyrogram import errors, filters, types

from KumsalTR import app, db, lang


broadcasting = False

@app.on_message(filters.command(["duyuru", "broadcast", "gcast"]) & app.sudo_filter)
@lang.language()
async def _broadcast(_, message: types.Message):
    global broadcasting
    
    if not message.reply_to_message:
        return await message.reply_text(message.lang["gcast_usage"])

    if broadcasting:
        return await message.reply_text(message.lang["gcast_active"])

    msg = message.reply_to_message
    count, ucount = 0, 0
    chats, groups, users = [], [], []
    sent = await message.reply_text(message.lang["gcast_start"])

    # Flag parsing
    broadcast_groups = "-nochat" not in message.text
    broadcast_users = "-user" in message.text or "-all" in message.text
    
    # If -all is used, we do both. If no flag is used, default was groups only.
    # User might expect -all to cover everything.

    if broadcast_groups:
        groups.extend(await db.get_chats())
    if broadcast_users:
        users.extend(await db.get_users())

    chats.extend(groups + users)
    # Remove duplicates if any
    chats = list(set(chats))
    
    broadcasting = True

    try:
        await msg.forward(app.logger)
        log_msg = await app.send_message(
            chat_id=app.logger, 
            text=message.lang["gcast_log"].format(
                message.from_user.id,
                message.from_user.mention,
                message.text.replace("{", "(").replace("}", ")"),
            )
        )
        try:
            await log_msg.pin(disable_notification=False)
        except:
            pass
    except Exception as e:
        app.logger.warning(f"Broadcast log failed: {e}")

    await asyncio.sleep(2)

    failed = ""
    for chat in chats:
        if not broadcasting:
            break

        try:
            (
                await msg.copy(chat, reply_markup=msg.reply_markup)
                if "-copy" in message.text
                else await msg.forward(chat)
            )
            if chat in groups:
                count += 1
            else:
                ucount += 1
            await asyncio.sleep(0.05) # Slightly faster but safe
        except errors.FloodWait as fw:
            await asyncio.sleep(fw.value + 5)
        except Exception as ex:
            failed += f"{chat} - {ex}\n"
            continue

    text = message.lang["gcast_end"].format(count, ucount)
    if failed:
        with open("errors.txt", "w") as f:
            f.write(failed)
        try:
            await message.reply_document(
                document="errors.txt",
                caption=text,
            )
        except:
            await message.reply_text(text)
        os.remove("errors.txt")
    else:
        await sent.edit_text(text)
        
    broadcasting = False


@app.on_message(filters.command(["stop_gcast", "stop_broadcast", "duyurustop"]) & app.sudo_filter)
@lang.language()
async def _stop_gcast(_, message: types.Message):
    global broadcasting
    if not broadcasting:
        return await message.reply_text(message.lang["gcast_inactive"])

    broadcasting = False
    try:
        log_msg = await app.send_message(
            chat_id=app.logger,
            text=message.lang["gcast_stop_log"].format(
                message.from_user.id,
                message.from_user.mention
            )
        )
        try:
            await log_msg.pin(disable_notification=False)
        except:
            pass
    except:
        pass
        
    await message.reply_text(message.lang["gcast_stop"])
