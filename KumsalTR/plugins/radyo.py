from pyrogram import filters, types
from KumsalTR import anon, app, config, db, lang, queue
from KumsalTR.helpers import Media, buttons, utils
from KumsalTR.helpers._play import checkUB

RADIOS = {
    "kral": ("Kral FM", "http://46.20.7.126:80/"),
    "slow": ("Slow Türk", "http://radyo.slowturk.com.tr/stream.mp3"),
    "joy": ("Joy FM", "https://joyfm.listenpowerapp.com/joyfm/mpeg.128k"),
    "power": ("Power FM", "https://powerfm.listenpowerapp.com/powerfm/mpeg.128k"),
    "metro": ("Metro FM", "https://metrofm.listenpowerapp.com/metrofm/mpeg.128k"),
    "fenomen": ("Radyo Fenomen", "https://fenomen.listenpowerapp.com/fenomen/mpeg.128k"),
}

@app.on_message(filters.command(["radyo"]) & filters.group & ~app.blacklist_filter)
@lang.language()
@checkUB
async def radyo_hndlr(_, m: types.Message):
    if len(m.command) < 2:
        text = "<b>📻 Rᴀᴅʏᴏ İstᴀsʏᴏɴʟᴀʀı</b>\n\n"
        for key, (name, _) in RADIOS.items():
            text += f"• <code>/radyo {key}</code> - {name}\n"
        return await m.reply_text(text)

    query = m.command[1].lower()
    if query not in RADIOS:
        return await m.reply_text("<b>❌ Hᴀᴛᴀ:</b> Gᴇᴄ̧ᴇʀsɪᴢ ɪsᴛᴀsʏᴏɴ. Lɪsᴛᴇ ɪᴄ̧ɪɴ <code>/radyo</code> ʏᴀᴢıɴ.")

    name, url = RADIOS[query]
    sent = await m.reply_text(f"<b>📻 {name} Bᴀşʟᴀᴛıʟıʏᴏʀ...</b>")
    
    media = Media(
        id=query,
        duration="Live",
        duration_sec=0,
        file_path=url,
        message_id=sent.id,
        title=f"Radyo: {name}",
        url=url,
        user=m.from_user.mention,
        user_id=m.from_user.id,
    )

    if await db.is_logger():
        await utils.play_log(m, media.title, media.duration)

    # Radyo için sırayı temizleyip hemen çalmak daha mantıklı olabilir 
    # Ama standart play gibi sıraya ekleyelim.
    position = queue.add(m.chat.id, media)

    if position != 0 or await db.get_call(m.chat.id):
        await sent.edit_text(
            m.lang["play_queued"].format(
                position,
                media.url,
                media.title,
                media.duration,
                m.from_user.mention,
            )
        )
        return

    await anon.play_media(chat_id=m.chat.id, message=sent, media=media)
