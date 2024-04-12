import re
import shutil
import psutil
from pyrogram import Client, filters
import logging
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from config import Config, Txt
from helper.database import db
from helper.utils import humanbytes
import time

logger = logging.getLogger(__name__)


@Client.on_message(filters.private & filters.command("start"))
async def start(client: Client, message: Message):

    user = message.from_user
    button = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            '⛅ ᴜᴘᴅᴀᴛᴇs', url='https://t.me/Kdramaland'),
        InlineKeyboardButton(
            '🌨️ sᴜᴘᴘᴏʀᴛ', url='https://t.me/SnowDevs')
    ], [
        InlineKeyboardButton('• ᴀʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('• ʜᴇʟᴘ', callback_data='help')
    ],
    ])

    if Config.START_PIC:
        await message.reply_photo(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button)
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)


@Client.on_message(filters.private & filters.command('donate'))
async def func_donate(client, message):
    user = message.from_user
    buttons = [[InlineKeyboardButton('❄️ ѕησωвαℓℓ', url='https://t.me/Snowball_Official'),
                InlineKeyboardButton('✘ ᴄʟᴏsᴇ', callback_data='close')]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(chat_id=user.id, text=Txt.DONATE, reply_markup=reply_markup)


# ⚠️ Handling CallBack Query⚠️
@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    '⛅ Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/Kdramaland'),
                InlineKeyboardButton(
                    '🌨️ Sᴜᴩᴩᴏʀᴛ', url='https://t.me/SnowDevs')
            ], [
                InlineKeyboardButton('• ᴀʙᴏᴜᴛ', callback_data='about'),
                InlineKeyboardButton('• ʜᴇʟᴘ', callback_data='help')
            ]

            ]))

    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton('• sᴇʀᴠᴇʀ sᴛᴀᴛs', callback_data='stats')
            ], [
                InlineKeyboardButton("• ʙᴀᴄᴋ", callback_data="start"),
                InlineKeyboardButton("✘ ᴄʟᴏsᴇ", callback_data="close")
            ]])
        )

    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT.format(client.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("• ʙᴀᴄᴋ", callback_data="start"),
                InlineKeyboardButton("✘ ᴄʟᴏsᴇ", callback_data="close")
            ]])
        )

    elif data == "stats":
        buttons = [[InlineKeyboardButton(
            '• ʙᴀᴄᴋ', callback_data='help'), InlineKeyboardButton('⟲ ʀᴇʟᴏᴀᴅ', callback_data='stats')]]
        reply_markup = InlineKeyboardMarkup(buttons)
        currentTime = time.strftime("%Hh%Mm%Ss", time.gmtime(
            time.time() - Config.BOT_UPTIME))
        total, used, free = shutil.disk_usage(".")
        total = humanbytes(total)
        used = humanbytes(used)
        free = humanbytes(free)
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        await query.message.edit_text(
            text=Txt.STATS_TXT.format(
                currentTime, total, used, disk_usage, free, cpu_usage, ram_usage),
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()
