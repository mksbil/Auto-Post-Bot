from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from helper.database import db
from helper.utils import extract_title_and_url
from pyromod.exceptions import ListenerTimeout
from config import Config


async def handle_post(user_id):
    posts = await db.get_posts(user_id)
    btn = []
    text = ""
    if not posts:
        btn.append([InlineKeyboardButton('➕ ᴀᴅᴅ ᴘᴏsᴛ', callback_data='addpost')])
        btn.append([InlineKeyboardButton('✘ ᴄʟᴏsᴇ', callback_data='close')])
        text = "☘️ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘᴏsᴛs ʏᴇᴛ ᴄʟɪᴄᴋ ᴏɴ 'ᴀᴅᴅ ᴘᴏsᴛ' ʙᴜᴛᴛᴏɴ ᴛᴏ ᴀᴅᴅ ᴘᴏsᴛs"
    
    else:
    
        for idx, post in enumerate(posts):
            btn.append([InlineKeyboardButton(f'ᴘᴏsᴛ {idx+1}', callback_data=f'viewpost_{post}'), InlineKeyboardButton(f'ᴅᴇʟᴇᴛᴇ', callback_data=f'delpost_{post}')])
        
        btn.append([InlineKeyboardButton('➕ ᴀᴅᴅ ᴘᴏsᴛ', callback_data='addpost')])
        btn.append([InlineKeyboardButton('✘ ᴄʟᴏsᴇ', callback_data='close')])
        text = "☘️ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʙᴜᴛᴛᴏɴs sʜᴏᴡs ᴛʜᴇ ɴᴜᴍʙᴇʀ ᴏғ ᴘᴏsᴛs ʏᴏᴜ ʜᴀᴠᴇ ᴀᴅᴅᴇᴅ ʏᴏᴜ ᴄᴀɴ ᴄʟɪᴄᴋ ᴏɴ ᴀɴʏ ᴘᴏsᴛ ᴛᴏ ɢᴇᴛ ʀᴇᴘʟɪᴇᴅ ᴏғ ᴛʜᴀᴛ ᴘᴏsᴛ"
    
    return text, btn

@Client.on_message(filters.private & filters.command('my_posts'))
async def handle_my_posts(bot: Client, message: Message):

    user_id = message.from_user.id
    text, btn = await handle_post(user_id)
    await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(btn))
    

@Client.on_callback_query(filters.regex(r'^addpost'))
async def handle_add_post(bot: Client, query: CallbackQuery):
    
    await query.message.delete()
    chat_id = query.message.chat.id
    try:
        post = await bot.ask(chat_id=chat_id, text="**(FORWARD ME POST)**\n\nғᴏʀᴡᴀʀᴅ ᴍᴇ ᴛʜᴇ ᴘᴏsᴛ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴀᴛ ᴛᴏ sᴀᴠᴇ", filters=filters.forwarded, timeout=30)
    except ListenerTimeout:
        await query.message.reply_text("ʀᴇǫᴜᴇsᴛ ᴛɪᴍᴇ ᴏᴜᴛ !\n\n**⚠️ ʏᴏᴜ ᴀʀᴇ ᴛᴀᴋɪɴɢ ᴛᴏᴏ ʟᴏɴɢ ᴛᴏ ғᴏʀᴡᴀʀᴅ ᴘᴏsᴛ**")

    
    post_id = await bot.copy_message(Config.LOG_CHANNEL, chat_id, post.id)

    await db.set_posts(chat_id, post_id.id)
    
    await query.message.reply_text("**ᴛʜɪs ᴘᴏsᴛ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅**\n\nᴜsᴇ /my_posts ᴛᴏ ᴠɪᴇᴡ ᴀʟʟ ʏᴏᴜʀ ᴘᴏsᴛs", reply_to_message_id=post.id)

@Client.on_callback_query(filters.regex(r'^delpost_'))
async def handle_delete_post(bot: Client, query: CallbackQuery):
    
    user_id = query.from_user.id
    post_id = query.data.split('_')[1]
    await db.del_post(user_id, int(post_id))
    
    await bot.delete_messages(int(Config.LOG_CHANNEL), int(post_id))
    
    text, btn = await handle_post(user_id)
    await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup(btn))
    
@Client.on_callback_query(filters.regex(r'^viewpost_'))
async def handle_view_post(bot: Client, query: CallbackQuery):
    post_id = int(query.data.split('_')[1])
    user_id = query.from_user.id
    save_buttons = await db.get_buttons(user_id)
    btn = []
    if save_buttons:

        for button in button:
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


    
