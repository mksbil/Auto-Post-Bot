import asyncio
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from helper.database import db
from config import Config, temp
from helper.utils import extract_title_and_url
from pyrogram.errors import FloodWait
from pyromod.exceptions import ListenerTimeout


def posts(userID, channelID, time, typ):

    postList = temp.POST_ID.get(userID)
    postBTN = []

    for idx, postID in enumerate(postList):
        if idx < 10:
            postBTN.append([InlineKeyboardButton(
                f'POST {idx+1}', callback_data=f'viewpost_{postID}'), InlineKeyboardButton(f'ᴅᴇʟᴇᴛᴇ', callback_data=f'delpost_{postID}_{channelID}_{time}_{typ}')])

    postBTN.append([InlineKeyboardButton('ʙᴀᴄᴋ', callback_data=f'back_{10}_{channelID}_{time}_{typ}'),
                   InlineKeyboardButton('ɴᴇxᴛ', callback_data=f'next_{10}_{channelID}_{time}_{typ}')])
    postBTN.append([InlineKeyboardButton(
        'sᴇɴᴅ', callback_data=f'finally_send_{channelID}_{time}_{typ}')])
    postBTN.append([InlineKeyboardButton(
        'ᴄᴀɴᴄᴇʟ', callback_data='finally_cancle')])
    return InlineKeyboardMarkup(postBTN)


@Client.on_message(filters.private & filters.command('send_post'))
async def handle_send_post(bot: Client, message: Message):
    user_id = message.from_user.id

    if user_id in temp.STORE_DATA:
        return await message.reply_text("** ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴜɴᴛɪʟ ᴘʀᴇᴠɪᴏᴜs ᴘʀᴏᴄᴇss ɪs ᴄᴏᴍᴘʟᴇᴛᴇᴅ **")

    channels = await db.get_channels(user_id)

    if not channels:
        return await message.reply_text("**ʏᴏᴜ ᴅɪᴅɴ'ᴛ ʜᴀᴠᴇ ᴀᴅᴅᴇᴅ ᴀɴʏ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ ᴜsᴇ /my_channels ᴛᴏ ᴀᴅᴅ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ !**", reply_to_message_id=message.id)

    buttons = []

    for channelid in channels:
        try:
            info = await bot.get_chat(int(channelid))
            buttons.append([InlineKeyboardButton(
                f'{info.title}', callback_data=f'posting_{channelid}')])
        except:
            buttons.append([InlineKeyboardButton(
                f'Not Admin', callback_data=f'posting_{None}#{channelid}')])

    text = f"🪴 **sᴇʟᴇᴄᴛ ᴄʜᴀɴɴᴇʟ ᴡʜᴇʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴇɴᴅ ?**"

    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))


async def detect_time(time, type):

    if str(type).lower() == "h":
        await asyncio.sleep(time * 3600)

    elif str(type).lower() == "m":
        await asyncio.sleep(time * 60)

    elif str(type).lower() == "s":
        await asyncio.sleep(time)


async def interval(bot, query):
    try:
        time_interval = await bot.ask(chat_id=query.from_user.id, text="Eɴᴛᴇʀ ᴛʜᴇ ɪɴᴛᴇʀᴠᴀʟ ᴏғ ᴛɪᴍᴇ. Cʜᴏᴏsᴇ ᴀɴʏ ɪɴᴛᴇɢᴇʀ ᴜɴᴅᴇʀ 24, ᴀɴᴅ ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ sᴇɴᴅ ᴀ ᴍᴇssᴀɢᴇ ᴀᴛ ᴛʜᴀᴛ ʜᴏᴜʀ ᴏʀ ᴍɪɴᴜᴛᴇs. Fᴏʀ ᴇxᴀᴍᴘʟᴇ, ɪғ ʏᴏᴜ ᴇɴᴛᴇʀ `4ᴍ` ᴏʀ `4ʜ` ᴏʀ `4s`, ᴛʜᴇ ʙᴏᴛ ᴡɪʟʟ sᴇɴᴅ ᴀ ᴍᴇssᴀɢᴇ ᴇᴠᴇʀʏ `4 ʜᴏᴜʀs ᴏʀ` `4 ᴍɪɴᴜᴛᴇs` ᴏʀ `4 sᴇᴄᴏɴᴅs` ʀᴇsᴘᴇᴄᴛɪᴠᴇʟʏ ғᴏʀ ᴇᴀᴄʜ ᴘᴏsᴛ.\n\n/cancel - cancel this process")
    except ListenerTimeout:
        await query.message.reply_text("**Rᴇǫᴜᴇsᴛ Tɪᴍᴇᴏᴜᴛ !**\n\nYᴏᴜʀ ᴀʀᴇ ᴛᴀᴋɪɴɢ ᴛᴏᴏ ʟᴏɴɢ ᴛᴏ sᴇɴᴅ")
        return 0

    if time_interval.text == "/cancel":
        await query.message.reply_text("<b>process canceled</b>",)
        return 0

    elif not str(time_interval.text[:-1]).isnumeric():
        await query.message.reply_text("**Iɴᴠᴀʟɪᴅ Fᴏʀᴍᴀᴛ !**")
        return 0

    elif int(time_interval.text[:-1]) > 24:
        await query.message.reply_text("☘️ **sᴇɴᴅ ɴᴜᴍʙᴇʀ ᴜɴᴅᴇʀ 24**")
        return 0

    elif str(time_interval.text).lower().endswith('h') or str(time_interval.text).lower().endswith('m') or str(time_interval.text).lower().endswith('s'):
        return int(time_interval.text[:-1]), time_interval.text[-1]

    else:
        await query.message.reply_text("**Iɴᴠᴀʟɪᴅ Fᴏʀᴍᴀᴛ !**")
        return 0


@Client.on_callback_query(filters.regex(r'^posting_'))
async def handle_single_posting(bot: Client, query: CallbackQuery):

    await query.message.delete()
    channelID = query.data.split('_')[1]
    time, typ = await interval(bot, query)
    chat_id = query.message.chat.id
    userID = query.from_user.id

    if userID not in temp.STORE_DATA:
        if channelID == None:
            temp.STORE_DATA.update(
                {userID: [channelID, time, typ, query.data.split('#')[1]]})
        else:
            temp.STORE_DATA.update({userID: [channelID, time, typ]})

    if userID not in temp.BOOL_ADDPOST:
        temp.BOOL_ADDPOST.update({userID: True})

    await query.message.reply_text("**(FORWARD ME POST)**\n\nғᴏʀᴡᴀʀᴅ ᴍᴇ ᴛʜᴇ ᴘᴏsᴛs ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴀᴛ ᴛᴏ sᴀᴠᴇ")


@Client.on_callback_query(filters.regex(r'^viewpost_'))
async def handle_view_post(bot: Client, query: CallbackQuery):
    post_id = int(query.data.split('_')[1])
    user_id = query.from_user.id
    save_buttons = await db.get_buttons(user_id)
    btn = []
    if save_buttons:

        for button in save_buttons:
            title, url = extract_title_and_url(button)
            btn.append(
                [InlineKeyboardButton(f'{title}', url=f'{url}')])
    try:
        if btn:
            await bot.copy_message(user_id, Config.LOG_CHANNEL, post_id, reply_markup=InlineKeyboardMarkup(btn))
        else:
            await bot.copy_message(user_id, Config.LOG_CHANNEL, post_id)

    except:
        await query.answer(f'ʜᴇʏ {query.from_user.mention},\n\n**ᴛʜᴇ ᴘᴏsᴛ ʏᴏᴜ ᴀʀᴇ ᴛʀʏɪɴɢ ᴛᴏ ᴠɪᴇᴡ ɪs ᴅᴇʟᴇᴛᴇᴅ ʙʏ ᴀᴅᴍɪɴ**', show_alert=True)


@Client.on_callback_query(filters.regex(r'^delpost_'))
async def handle_delete_post(bot: Client, query: CallbackQuery):

    user_id = query.from_user.id
    post_id = query.data.split('_')[1]
    channel_id = query.data.split('_')[2]
    time = query.data.split('_')[3]
    typ = query.data.split('_')[4]

    try:
        await bot.delete_messages(int(Config.LOG_CHANNEL), int(post_id))
        temp.POST_ID[user_id].remove(int(post_id))
    except Exception as e:
        print(e)

    postList = temp.POST_ID.get(user_id)

    info = await bot.get_chat(chat_id=int(channel_id))
    text = f"Dᴏᴜʙʟᴇ Cʜᴇᴄᴋ !\n\n** ᴛᴀʀɢᴇᴛ ᴄʜᴀɴɴᴇʟ : ** {info.title}\n** ᴅᴇʟᴀʏ : ** {time}{typ}\n** ᴛᴏᴛᴀʟ ᴘᴏsᴛs : ** {len(postList)}\n\n👁️ ᴘᴏsᴛs ᴀʀᴇ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ᴄᴀɴ ᴠɪᴇᴡ ᴏʀ ᴅᴇʟᴇᴛᴇ ᴛʜᴇ ᴘᴏsᴛs"
    markup = posts(user_id, channel_id, time, typ)
    await query.message.edit(text=text, reply_markup=markup)


@Client.on_callback_query((filters.regex(r'^finally_')))
async def handle_finally_post(bot: Client, query: CallbackQuery):

    option = query.data.split('_')[1]
    chat_id = query.message.chat.id
    userID = query.from_user.id

    if option == 'cancle':
        await query.message.delete()
        if userID in temp.POST_ID:
            temp.POST_ID.pop(userID)
        if userID in temp.BOOL_ADDPOST:
            temp.BOOL_ADDPOST.pop(userID)
        if userID in temp.STORE_DATA:
            temp.STORE_DATA.pop(userID)

        return await bot.send_message(chat_id, text="**Process canceled successfully**")

    else:
        await query.message.edit("** ᴠᴇʀɪғʏɪɴɢ ᴅᴀᴛᴀ ... **")
        channelID = query.data.split('_')[2]
        time = int(query.data.split('_')[3])
        typ = query.data.split('_')[4]
        info = await bot.get_chat(int(channelID))
        buttons = await db.get_buttons(userID)
        saveBTN = []
        await query.message.edit(f"** ᴘᴏsᴛs ᴡɪʟʟ ʙᴇ sᴇɴᴅ ᴛᴏ {info.title} ᴀғᴛᴇʀ {time}{typ} ᴅᴇʟᴀʏ ** ♻️")
        if buttons:
            for btn in buttons:
                text, url = extract_title_and_url(btn)
                saveBTN.append([InlineKeyboardButton(text, url=url)])

            for postID in temp.POST_ID[userID]:
                if time != 0:
                    await detect_time(time, typ)
                    await bot.copy_message(int(channelID), Config.LOG_CHANNEL, int(postID), reply_markup=InlineKeyboardMarkup(saveBTN))
                else:
                    await bot.copy_message(int(channelID), Config.LOG_CHANNEL, int(postID), reply_markup=InlineKeyboardMarkup(saveBTN))
        else:
            for postID in temp.POST_ID[userID]:
                if time != 0:
                    await detect_time(time, typ)
                    await bot.copy_message(int(channelID), Config.LOG_CHANNEL, int(postID))
                else:
                    await bot.copy_message(int(channelID), Config.LOG_CHANNEL, int(postID))

        await query.message.delete()
        # clearing stored user datas
        if userID in temp.POST_ID:
            temp.POST_ID.pop(userID)
        if userID in temp.BOOL_ADDPOST:
            temp.BOOL_ADDPOST.pop(userID)
        if userID in temp.STORE_DATA:
            temp.STORE_DATA.pop(userID)
        await query.message.reply_text(f" ** ᴘᴏsᴛs ʜᴀs ʙᴇᴇɴ sᴇɴᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴛᴏ {info.title} ** ✅")


@Client.on_message(filters.private & filters.forwarded)
async def handle_forward(bot: Client, message: Message):
    try:
        userID = message.from_user.id
        if temp.BOOL_ADDPOST.get(userID):
            try:
                post_id = await bot.copy_message(Config.LOG_CHANNEL, userID, message.id)
                if userID not in temp.POST_ID:
                    temp.POST_ID.update({userID: []})
                temp.POST_ID.get(userID).append(post_id.id)
                await message.reply_text("**ᴛʜɪs ᴘᴏsᴛ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅**\n\n ⚠️ ᴡʜᴇɴ ʏᴏᴜ'ʀᴇ ᴅᴏɴᴇ ᴜsᴇ /done", reply_to_message_id=message.id)
            except Exception as e:
                print(e)
    except FloodWait as e:
        await asyncio.sleep(e.value)


@Client.on_message(filters.private & filters.command('done'))
async def handle_cancle_addingPost(bot: Client, message: Message):

    userID = message.from_user.id
    chat_id = message.chat.id
    channelID = temp.STORE_DATA.get(userID)[0]
    time = temp.STORE_DATA.get(userID)[1]
    typ = temp.STORE_DATA.get(userID)[2]

    if temp.BOOL_ADDPOST.get(userID):
        temp.BOOL_ADDPOST.pop(userID)

    if channelID == None:
        return await bot.send_message(chat_id, f"** ⚠️ ᴍᴀᴋᴇ sᴜʀᴇ ʙᴏᴛ ɪs ᴀᴅᴍɪɴ ɪɴ ᴛᴀʀɢᴇᴛ ᴄʜᴀɴɴᴇʟ ** \n\nᴄʜᴀᴛ ɪᴅ: `{temp.STORE_DATA.get(userID)[3]}` ")
    else:
        info = await bot.get_chat(chat_id=int(channelID))
        postList = temp.POST_ID.get(userID)
        text = f"Dᴏᴜʙʟᴇ Cʜᴇᴄᴋ !\n\n** ᴛᴀʀɢᴇᴛ ᴄʜᴀɴɴᴇʟ : ** {info.title}\n** ᴅᴇʟᴀʏ : ** {time}{typ}\n** ᴛᴏᴛᴀʟ ᴘᴏsᴛs : ** {len(postList)}\n\n👁️ ᴘᴏsᴛs ᴀʀᴇ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ᴄᴀɴ ᴠɪᴇᴡ ᴏʀ ᴅᴇʟᴇᴛᴇ ᴛʜᴇ ᴘᴏsᴛs"
        markup = posts(userID, channelID, time, typ)
        await bot.send_message(chat_id, text, reply_markup=markup)


@Client.on_callback_query(filters.regex('^next_'))
async def handle_nextpage(bot: Client, query: CallbackQuery):
    currentPosition = int(query.data.split('_')[1])

    userID = query.from_user.id
    postList = temp.POST_ID.get(userID)

    channelID = query.data.split('_')[2]
    time = query.data.split('_')[3]
    typ = query.data.split('_')[4]

    nextBtn = []
    try:
        for idx, postID in enumerate(postList):
            if idx >= currentPosition and idx < currentPosition + 10:
                nextBtn.append([InlineKeyboardButton(
                    f'POST {idx+1}', callback_data=f'viewpost_{postID}'), InlineKeyboardButton(f'ᴅᴇʟᴇᴛᴇ', callback_data=f'delpost_{postID}_{channelID}_{time}_{typ}')])

        if currentPosition >= len(postList):
            return await query.answer('No More Pages', show_alert=True)

        nextBtn.append([InlineKeyboardButton('ʙᴀᴄᴋ', callback_data=f'back_{currentPosition+10}_{channelID}_{time}_{typ}'),
                        InlineKeyboardButton('ɴᴇxᴛ', callback_data=f'next_{currentPosition+10}_{channelID}_{time}_{typ}')])

        nextBtn.append([InlineKeyboardButton(
            'sᴇɴᴅ', callback_data=f'finally_send_{channelID}_{time}_{typ}')])
        nextBtn.append([InlineKeyboardButton(
            'ᴄᴀɴᴄᴇʟ', callback_data='finally_cancle')])
        info = await bot.get_chat(int(channelID))
        text = f"Dᴏᴜʙʟᴇ Cʜᴇᴄᴋ !\n\n** ᴛᴀʀɢᴇᴛ ᴄʜᴀɴɴᴇʟ : ** {info.title}\n** ᴅᴇʟᴀʏ : ** {time}{typ}\n** ᴛᴏᴛᴀʟ ᴘᴏsᴛs : ** {len(postList)}\n\n👁️ ᴘᴏsᴛs ᴀʀᴇ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ᴄᴀɴ ᴠɪᴇᴡ ᴏʀ ᴅᴇʟᴇᴛᴇ ᴛʜᴇ ᴘᴏsᴛs"
        await query.message.edit(text, reply_markup=InlineKeyboardMarkup(nextBtn))

    except Exception as e:
        print(e)


@Client.on_callback_query(filters.regex('^back_'))
async def handle_backpage(bot: Client, query: CallbackQuery):

    currentPosition = int(query.data.split('_')[1])

    if currentPosition - 10 == 0:
        return await query.answer('You are in first page can not go back further', show_alert=True)

    userID = query.from_user.id
    postList = temp.POST_ID.get(userID)

    channelID = query.data.split('_')[2]
    time = query.data.split('_')[3]
    typ = query.data.split('_')[4]

    nextBtn = []

    for idx, postID in enumerate(postList):
        if idx >= int(currentPosition-20) and idx < currentPosition - 10:
            nextBtn.append([InlineKeyboardButton(
                f'POST {idx+1}', callback_data=f'viewpost_{postID}'), InlineKeyboardButton(f'ᴅᴇʟᴇᴛᴇ', callback_data=f'delpost_{postID}_{channelID}_{time}_{typ}')])

    nextBtn.append([InlineKeyboardButton('ʙᴀᴄᴋ', callback_data=f'back_{currentPosition-10}_{channelID}_{time}_{typ}'),
                   InlineKeyboardButton('ɴᴇxᴛ', callback_data=f'next_{currentPosition-10}_{channelID}_{time}_{typ}')])

    nextBtn.append([InlineKeyboardButton(
        'sᴇɴᴅ', callback_data=f'finally_send_{channelID}_{time}_{typ}')])
    nextBtn.append([InlineKeyboardButton(
        'ᴄᴀɴᴄᴇʟ', callback_data='finally_cancle')])
    info = await bot.get_chat(int(channelID))
    text = f"Dᴏᴜʙʟᴇ Cʜᴇᴄᴋ !\n\n** ᴛᴀʀɢᴇᴛ ᴄʜᴀɴɴᴇʟ : ** {info.title}\n** ᴅᴇʟᴀʏ : ** {time}{typ}\n** ᴛᴏᴛᴀʟ ᴘᴏsᴛs : ** {len(postList)}\n\n👁️ ᴘᴏsᴛs ᴀʀᴇ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ᴄᴀɴ ᴠɪᴇᴡ ᴏʀ ᴅᴇʟᴇᴛᴇ ᴛʜᴇ ᴘᴏsᴛs"
    await query.message.edit(text, reply_markup=InlineKeyboardMarkup(nextBtn))
