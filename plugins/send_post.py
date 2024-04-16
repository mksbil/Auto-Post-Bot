import asyncio
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from helper.database import db
from config import Config
from helper.utils import extract_title_and_url
from pyromod.exceptions import ListenerTimeout


@Client.on_message(filters.private & filters.command('send_post'))
async def handle_send_post(bot: Client, message: Message):
    user_id = message.from_user.id
    posts = await db.get_posts(user_id)
    channels = await db.get_channels(user_id)
    if not posts:
        return await message.reply_text("**ʏᴏᴜ ᴅɪᴅɴ'ᴛ ʜᴀᴠᴇ ᴀᴅᴅᴇᴅ ᴀɴʏ ᴘᴏsᴛ ʏᴇᴛ ᴜsᴇ /my_posts ᴛᴏ ᴀᴅᴅ ʏᴏᴜʀ ᴘᴏsᴛ !**", reply_to_message_id=message.id)

    if not channels:
        return await message.reply_text("**ʏᴏᴜ ᴅɪᴅɴ'ᴛ ʜᴀᴠᴇ ᴀᴅᴅᴇᴅ ᴀɴʏ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ ᴜsᴇ /my_channels ᴛᴏ ᴀᴅᴅ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ !**", reply_to_message_id=message.id)

    buttons = []

    for idx, post in enumerate(posts):
        buttons.append([InlineKeyboardButton(
            f'ᴘᴏsᴛ {idx+1}', callback_data=f'send_{post}')])

    text = f"🛻 **sᴇʟᴇᴄᴛ ʏᴏᴜʀ ᴘᴏsᴛ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴇɴᴅ ?**"

    buttons.append([InlineKeyboardButton(
        f'sᴇʟᴇᴄᴛ ᴀʟʟ ᴘᴏsᴛs', callback_data=f'send_all')])
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


@Client.on_callback_query(filters.regex(r'^send_'))
async def handle_query_send(bot: Client, query: CallbackQuery):
    await query.message.edit("**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...**")
    user_id = query.from_user.id
    channels = await db.get_channels(user_id)
    post_id = query.data.split('_')[1]
    save_channels = []

    for channelid in channels:
        try:
            info = await bot.get_chat(channelid)
            save_channels.append([InlineKeyboardButton(
                f'{info.title}', callback_data=f'posting_{channelid}_{post_id}')])
        except:
            save_channels.append([InlineKeyboardButton(
                f'Not Admin', callback_data=f'posting_{None}#{channelid}')])

    text = f"🪴 **sᴇʟᴇᴄᴛ ᴄʜᴀɴɴᴇʟ ᴡʜᴇʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴇɴᴅ ?**"

    save_channels.append([InlineKeyboardButton(
        f'sᴇɴᴅ ᴛᴏ ᴀʟʟ ᴄʜᴀɴɴᴇʟs', callback_data=f'allposting_{post_id}')])
    await query.message.edit(text, reply_markup=InlineKeyboardMarkup(save_channels))


@Client.on_callback_query(filters.regex(r'^posting_'))
async def handle_single_posting(bot: Client, query: CallbackQuery):

    time, typ = await interval(bot, query)

    await query.message.edit("**ᴘʀᴏᴄᴇssɪɴɢ ♻️...**")

    if time != 0:
        await query.message.delete()
        ms = await query.message.reply_text(f"**ᴇᴀᴄʜ ᴘᴏsᴛ ᴡɪʟʟ ʙᴇ sᴇɴᴅ ᴀғᴛᴇʀ ᴇᴠᴇʀʏ {time}{typ}** ♻️")

    _, channelid, postid = query.data.split("_")
    userID = query.from_user.id
    buttons = await db.get_buttons(userID)
    save_button = []

    if channelid.startswith("None"):
        return query.message.edit("**⚠️ ғᴀɪʟᴅ ᴛᴏ sᴇɴᴅ ᴘᴏsᴛ**\n\nʀᴇᴀsᴏɴ :- ᴍᴀʏ ʙᴇ ɪ ᴀᴍ ɴᴏᴛ ᴀᴅᴍɪɴɢ ɪɴ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟ")

    if buttons:
        for button in buttons:
            title, url = extract_title_and_url(button)
            save_button.append(
                [InlineKeyboardButton(f'{title}', url=f'{url}')])

        if postid == "all":
            all_posts = await db.get_posts(userID)
            for post in all_posts:
                if time != 0:
                    await detect_time(time, typ)
                    await bot.copy_message(int(channelid), Config.LOG_CHANNEL, int(post), reply_markup=InlineKeyboardMarkup(save_button))
                    continue
                else:
                    await bot.copy_message(int(channelid), Config.LOG_CHANNEL, int(post), reply_markup=InlineKeyboardMarkup(save_button))

        else:
            if time != 0:
                await detect_time(time, typ)
                await bot.copy_message(int(channelid), Config.LOG_CHANNEL, int(postid), reply_markup=InlineKeyboardMarkup(save_button))
            else:
                await bot.copy_message(int(channelid), Config.LOG_CHANNEL, int(postid), reply_markup=InlineKeyboardMarkup(save_button))

    else:
        if postid == "all":
            all_posts = await db.get_posts(userID)

            for post in all_posts:
                if time != 0:
                    await detect_time(time, typ)
                    await bot.copy_message(int(channelid), Config.LOG_CHANNEL, int(post))

                else:
                    await bot.copy_message(int(channelid), Config.LOG_CHANNEL, int(post))

        else:
            if time != 0:
                await detect_time(time, typ)
                await bot.copy_message(int(channelid), Config.LOG_CHANNEL, int(postid))
            else:
                await bot.copy_message(int(channelid), Config.LOG_CHANNEL, int(postid))
    try:
        if ms:
            await ms.edit("**ᴘᴏsᴛ sᴇɴᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅**")
            return
    except:
        pass

    await query.message.edit("**ᴘᴏsᴛ sᴇɴᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅**")


@Client.on_callback_query(filters.regex(r'^allposting_'))
async def handle_all_posting(bot: Client, query: CallbackQuery):
    try:
        await query.message.edit("**ᴘʀᴏᴄᴇssɪɴɢ ♻️...**")
        postid = query.data.split("_")[1]
        userID = query.from_user.id
        channels = await db.get_channels(userID)
        buttons = await db.get_buttons(userID)
        total_posts = await db.get_posts(userID)
        save_button = []
        time, typ = await interval(bot, query)
        success = 0
        faild = 0
        total_channels = len(channels)

        if time != 0:
            await query.message.delete()
            ms = await query.message.reply_text(f"**ᴇᴀᴄʜ ᴘᴏsᴛ ᴡɪʟʟ ʙᴇ sᴇɴᴅ ᴀғᴛᴇʀ ᴇᴠᴇʀʏ {time}{typ}** ♻️")

        if buttons:
            for button in buttons:
                title, url = extract_title_and_url(button)
                save_button.append(
                    [InlineKeyboardButton(f'{title}', url=f'{url}')])

        if postid == "all":
            for post in total_posts:
                if time != 0:
                    await detect_time(time, typ)
                    for channelID in channels:
                        try:
                            if buttons:
                                await bot.copy_message(int(channelID), Config.LOG_CHANNEL, int(post), reply_markup=InlineKeyboardMarkup(save_button))

                            else:
                                await bot.copy_message(int(channelID), Config.LOG_CHANNEL, int(post))

                            success += 1
                        except:
                            pass
                            faild += 1
                    continue
                else:

                    for channelID in channels:
                        try:
                            if buttons:
                                await bot.copy_message(int(channelID), Config.LOG_CHANNEL, int(post), reply_markup=InlineKeyboardMarkup(save_button))

                            else:
                                await bot.copy_message(int(channelID), Config.LOG_CHANNEL, int(post))

                            success += 1
                        except:
                            pass
                            faild += 1

        else:
            if time != 0:
                await detect_time(time, typ)
                for channelID in channels:
                    try:
                        if buttons:
                            await bot.copy_message(int(channelID), Config.LOG_CHANNEL, int(postid), reply_markup=InlineKeyboardMarkup(save_button))
                        else:
                            await bot.copy_message(int(channelID), Config.LOG_CHANNEL, int(postid))

                        success += 1
                    except:
                        faild += 1

            else:
                for channelID in channels:
                    try:
                        if buttons:
                            await bot.copy_message(int(channelID), Config.LOG_CHANNEL, int(postid), reply_markup=InlineKeyboardMarkup(save_button))
                        else:
                            await bot.copy_message(int(channelID), Config.LOG_CHANNEL, int(postid))

                        success += 1
                    except:
                        faild += 1
        try:
            if ms:
                await query.message.edit(f"**ᴘᴏsᴛ sᴇɴᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ✅**\n\nsᴜᴄᴄᴇss :- {success}\nғᴀɪʟᴇᴅ :- {faild}\nᴛᴏᴛᴀʟ ᴄʜᴀɴɴᴇʟs :- {total_channels}")
                return
        except:
            pass
        await query.message.edit(f"**ᴘᴏsᴛ sᴇɴᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ✅**\n\nsᴜᴄᴄᴇss :- {success}\nғᴀɪʟᴇᴅ :- {faild}\nᴛᴏᴛᴀʟ ᴄʜᴀɴɴᴇʟs :- {total_channels}")

    except Exception as e:
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
