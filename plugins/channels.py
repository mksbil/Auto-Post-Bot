from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from helper.database import db
from pyromod.exceptions import ListenerTimeout


async def handle_channel(bot, user_id):
    channels = await db.get_channels(user_id)
    btn = []
    text = ""
    if not channels:
        btn.append([InlineKeyboardButton(
            '➕ ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ', callback_data='addchnl')])
        btn.append([InlineKeyboardButton('✘ ᴄʟᴏsᴇ', callback_data='close')])
        text = "☘️ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ ᴄʟɪᴄᴋ ᴏɴ 'ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ' ʙᴜᴛᴛᴏɴ ᴛᴏ ᴀᴅᴅ ᴄʜᴀɴɴᴇʟs"

    else:

        for channelid in channels:
            try:
                info = await bot.get_chat(channelid)
                btn.append([InlineKeyboardButton(f'{info.title}', callback_data=f'info_{channelid}'), InlineKeyboardButton(
                    f'ᴅᴇʟᴇᴛᴇ', callback_data=f'delchl_{channelid}')])
            except:
                btn.append([InlineKeyboardButton(f'Not Admin', callback_data=f'info_{None}#{channelid}'), InlineKeyboardButton(
                    f'ᴅᴇʟᴇᴛᴇ', callback_data=f'delchl_{channelid}')])

        btn.append([InlineKeyboardButton(
            '➕ ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ', callback_data='addchnl')])
        btn.append([InlineKeyboardButton('✘ ᴄʟᴏsᴇ', callback_data='close')])
        text = "☘️ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʙᴜᴛᴛᴏɴs sʜᴏᴡs ᴛʜᴇ ɴᴜᴍʙᴇʀ ᴏғ ᴄʜᴀɴɴᴇʟs ʏᴏᴜ ʜᴀᴠᴇ ᴀᴅᴅᴇᴅ ʏᴏᴜ ᴄᴀɴ ᴄʟɪᴄᴋ ᴏɴ ᴀɴʏ ᴄʜᴀɴɴᴇʟs ᴛᴏ ɢᴇᴛ ɪɴғᴏ ᴏғ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟs "

    return text, btn


@Client.on_message(filters.private & filters.command('my_channels'))
async def handle_my_channels(bot: Client, message: Message):

    user_id = message.from_user.id

    text, btn = await handle_channel(bot, user_id)
    await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(btn))


@Client.on_callback_query(filters.regex(r'^addchnl'))
async def handle_add_channel(bot: Client, query: CallbackQuery):

    await query.message.delete()
    chat_id = query.message.chat.id
    try:
        channel = await bot.ask(chat_id=chat_id, text="**(SEND ME CHANNEL CHAT ID)**\n\nsᴇɴᴅ ᴍᴇ ᴄʜᴀɴɴᴇʟ ᴄʜᴀᴛ ɪᴅ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴀᴛ ᴛᴏ sᴀᴠᴇ", filters=filters.text, timeout=30)
    except ListenerTimeout:
        await query.message.reply_text("ʀᴇǫᴜᴇsᴛ ᴛɪᴍᴇ ᴏᴜᴛ !\n\n**⚠️ ʏᴏᴜ ᴀʀᴇ ᴛᴀᴋɪɴɢ ᴛᴏᴏ ʟᴏɴɢ ᴛᴏ sᴇɴᴅ ᴄʜᴀɴɴᴇʟ ᴄʜᴀᴛ ɪᴅ**")

    if not channel.text.startswith("-100"):
        return await query.message.reply_text("**ᴄʜᴀɴɴᴇʟ ᴄʜᴀᴛ ɪᴅ ᴍᴜsᴛ sᴛᴀʀᴛs ᴡɪᴛʜ `-100` **", reply_to_message_id=channel.id)

    await db.set_channels(chat_id, int(channel.text))

    await query.message.reply_text("**ᴛʜɪs ᴄʜᴀɴɴᴇʟ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅**\n\nᴜsᴇ /my_channels ᴛᴏ ᴠɪᴇᴡ ᴀʟʟ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟs ", reply_to_message_id=channel.id, reply_markup=InlineKeyboardMarkup(
        [[InlineKeyboardButton("• ʙᴀᴄᴋ", callback_data="back_channels"),]]))


@Client.on_callback_query(filters.regex(r'^delchl_'))
async def handle_delete_channel(bot: Client, query: CallbackQuery):

    user_id = query.from_user.id
    chnl_id = query.data.split('_')[1]
    await db.del_channel(user_id, int(chnl_id))
    text, btn = await handle_channel(bot, user_id)
    await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup(btn))


@Client.on_callback_query(filters.regex(r'^info_'))
async def handle_info_channel(bot: Client, query: CallbackQuery):

    channelid = query.data.split('_')[1]

    if channelid.startswith('None'):
        try:
            idz = channelid.split("#")[1]
            text = f"⚠️ **ᴡᴀʀɴɪɴɢ ᴛʜɪs ʙᴏᴛ ɪs ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ᴄʜᴀɴɴᴇʟ/ɢʀᴏᴜᴘ**\nnᴍᴀᴋᴇ sᴜʀᴇ ɪ'ᴀᴍ ᴀᴅᴍɪɴ ᴛʜᴇʀᴇ ᴛᴏ ᴡᴏʀᴋ sᴇᴀᴍʟᴇssʟʏ\n\nᴄʜᴀᴛ-ɪᴅ : `{idz}`"
            await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("• ʙᴀᴄᴋ", callback_data="back_channels")]]))
        except Exception as e:
            print(e)
    else:

        info = await bot.get_chat(channelid)
        text = f"☘️ **CHANNEL INFO**\n\nᴛɪᴛʟᴇ : `{info.title}`\nᴜsᴇʀɴᴀᴍᴇ : `{info.username}`\nᴄʜᴀᴛ-ɪᴅ : `{info.id}`\nʟɪɴᴋ : `{info.invite_link}`\nᴅᴄ-ɪᴅ : `{info.dc_id}`\nᴛᴏᴛᴀʟ-ᴍᴇᴍʙᴇʀs : `{info.members_count}`"
        await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("• ʙᴀᴄᴋ", callback_data="back_channels"),]]))


@Client.on_callback_query(filters.regex(r'^back_channels'))
async def handle_back_list(bot: Client, query: CallbackQuery):
    user_id = query.from_user.id
    text, btn = await handle_channel(bot, user_id)
    await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup(btn))
