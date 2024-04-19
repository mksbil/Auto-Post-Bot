from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from helper.database import db
from helper.utils import extract_title_and_url
from pyromod.exceptions import ListenerTimeout
from config import Config, temp


async def handle_post(user_id):
    if user_id in temp.CHNLID:
        for id in temp.CHNLID.get(user_id):
            await db.set_posts(user_id, id)
        temp.CHNLID.pop(user_id)

    posts = await db.get_posts(user_id)
    btn = []
    text = ""
    if not posts:
        btn.append([InlineKeyboardButton(
            '➕ ᴀᴅᴅ ᴘᴏsᴛ', callback_data='addpost')])
        btn.append([InlineKeyboardButton('✘ ᴄʟᴏsᴇ', callback_data='close')])
        text = "☘️ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘᴏsᴛs ʏᴇᴛ ᴄʟɪᴄᴋ ᴏɴ 'ᴀᴅᴅ ᴘᴏsᴛ' ʙᴜᴛᴛᴏɴ ᴛᴏ ᴀᴅᴅ ᴘᴏsᴛs"

    else:

        for idx, post in enumerate(posts):
            btn.append([InlineKeyboardButton(f'ᴘᴏsᴛ {idx+1}', callback_data=f'viewpost_{post}'),
                       InlineKeyboardButton(f'ᴅᴇʟᴇᴛᴇ', callback_data=f'delpost_{post}')])

        btn.append([InlineKeyboardButton(
            '➕ ᴀᴅᴅ ᴘᴏsᴛ', callback_data='addpost')])
        btn.append([InlineKeyboardButton('✘ ᴄʟᴏsᴇ', callback_data='close')])
        text = "☘️ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʙᴜᴛᴛᴏɴs sʜᴏᴡs ᴛʜᴇ ɴᴜᴍʙᴇʀ ᴏғ ᴘᴏsᴛs ʏᴏᴜ ʜᴀᴠᴇ ᴀᴅᴅᴇᴅ ʏᴏᴜ ᴄᴀɴ ᴄʟɪᴄᴋ ᴏɴ ᴀɴʏ ᴘᴏsᴛ ᴛᴏ ɢᴇᴛ ʀᴇᴘʟɪᴇᴅ ᴏғ ᴛʜᴀᴛ ᴘᴏsᴛ"

    return text, btn


@Client.on_message(filters.private & filters.command('my_posts'))
async def handle_my_posts(bot: Client, message: Message):
    ms = await message.reply_text("**Please Wait...**")
    user_id = message.from_user.id
    text, btn = await handle_post(user_id)
    await ms.delete()
    await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(btn))


@Client.on_callback_query(filters.regex(r'^addpost'))
async def handle_add_post(bot: Client, query: CallbackQuery):

    await query.message.delete()
    chat_id = query.message.chat.id

    while True:
        try:
            post = await bot.ask(chat_id=chat_id, text="**(FORWARD ME POST)**\n\nғᴏʀᴡᴀʀᴅ ᴍᴇ ᴛʜᴇ ᴘᴏsᴛ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴀᴛ ᴛᴏ sᴀᴠᴇ", timeout=60)
        except ListenerTimeout:
            await query.message.reply_text("ʀᴇǫᴜᴇsᴛ ᴛɪᴍᴇ ᴏᴜᴛ !\n\n**⚠️ ʏᴏᴜ ᴀʀᴇ ᴛᴀᴋɪɴɢ ᴛᴏᴏ ʟᴏɴɢ ᴛᴏ ғᴏʀᴡᴀʀᴅ ᴘᴏsᴛ**")
        print(post)
        if post.text == '/cancel':
            await bot.send_message(chat_id, text="**Process canceled successfully**")
            await bot.send_message(chat_id, "👁️ ᴠɪᴇᴡ ᴀʟʟ ʏᴏᴜʀ ᴘᴏsᴛs", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('ᴠɪᴇᴡ ᴘᴏsᴛs', callback_data='showposts')]]))
            break

        post_id = await bot.copy_message(Config.LOG_CHANNEL, chat_id, post.id)
        await db.set_posts(chat_id, post_id.id)

        await query.message.reply_text("**ᴛʜɪs ᴘᴏsᴛ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅**\n\nᴜsᴇ /cancel to stop the process", reply_to_message_id=post.id)
        continue


@Client.on_callback_query(filters.regex(r'^delpost_'))
async def handle_delete_post(bot: Client, query: CallbackQuery):

    user_id = query.from_user.id
    post_id = query.data.split('_')[1]
    await db.del_post(user_id, int(post_id))
    try:
        await bot.delete_messages(int(Config.LOG_CHANNEL), int(post_id))
    except Exception as e:
        print(e)

    text, btn = await handle_post(user_id)
    await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup(btn))


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


@Client.on_callback_query(filters.regex(r'^showposts'))
async def handle_showposts(bot: Client, query: CallbackQuery):

    user_id = query.from_user.id
    text, btn = await handle_post(user_id)
    await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup(btn))


@Client.on_message(filters.private & filters.forwarded)
async def handle_forward(bot: Client, message: Message):

    if message.from_user.id not in temp.CHNLID:
        temp.CHNLID.update({message.from_user.id: []})

    try:

        chat_id = message.from_user.id
        post_id = await bot.copy_message(Config.LOG_CHANNEL, chat_id, message.id)
        temp.CHNLID.get(message.from_user.id).append(post_id.id)
        await message.reply_text("**ᴛʜɪs ᴘᴏsᴛ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅**", reply_to_message_id=message.id)
    except Exception as e:
        print(e)
