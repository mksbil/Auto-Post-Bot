from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from helper.database import db
from pyromod.exceptions import ListenerTimeout
from config import Config
from helper.utils import extract_title_and_url


async def button_text(user_id):
    buttons = await db.get_buttons(user_id)
    btn = []
    text = ""
    if not buttons:
        btn.append([InlineKeyboardButton('🔘 ᴀᴅᴅ ʙᴜᴛᴛᴏɴ', callback_data='addbutton')])
        btn.append([InlineKeyboardButton('✘ ᴄʟᴏsᴇ', callback_data='close')])
        text = "☘️ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ʙᴜᴛᴛᴏɴ ʏᴇᴛ ᴄʟɪᴄᴋ ᴏɴ 'ᴀᴅᴅ ʙᴜᴛᴛᴏɴ' ʙᴜᴛᴛᴏɴ ᴛᴏ ᴀᴅᴅ ʙᴜᴛᴛᴏɴs"
    
    else:
        for button in buttons:
            title, url = extract_title_and_url(button)
            btn.append([InlineKeyboardButton(f'{title}', url=f'{url}'), InlineKeyboardButton(f'ᴅᴇʟᴇᴛᴇ', callback_data=f'delbutton_{buttons.index(button)}')])
            
        btn.append([InlineKeyboardButton('🔘 ᴀᴅᴅ ʙᴜᴛᴛᴏɴ', callback_data='addbutton')])
        btn.append([InlineKeyboardButton('✘ ᴄʟᴏsᴇ', callback_data='close')])
        text = "☘️ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʙᴜᴛᴛᴏɴs sʜᴏᴡs ᴛʜᴇ ɴᴜᴍʙᴇʀ ᴏғ ʙᴜᴛᴛᴏɴs ʏᴏᴜ ʜᴀᴠᴇ ᴀᴅᴅᴇᴅ ʏᴏᴜ ᴄᴀɴ ᴄʟɪᴄᴋ ᴏɴ ᴀɴʏ ʙᴜᴛᴛᴏɴ ᴛᴏ ᴠɪᴇᴡ ʏᴏᴜʀ ʙᴜᴛᴛᴏɴ"
    return text, btn

@Client.on_message(filters.private & filters.command('my_buttons'))
async def handle_buttons(bot: Client, message: Message):
    text, btn = await button_text(user_id=message.from_user.id)
    await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(btn))
    
    

@Client.on_callback_query(filters.regex(r'^addbutton'))
async def handle_add_button(bot: Client, query: CallbackQuery):
    
    await query.message.delete()
    chat_id = query.message.chat.id
    try:
        button = await bot.ask(chat_id=chat_id, text="**(SEND ME BUTTON)**\n\nsᴇɴᴅ ᴍᴇ ʙᴜᴛᴛᴏɴ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴀᴛ ᴛᴏ sᴀᴠᴇ\nғᴏʀ ᴇ.ɢ - `[K-Lᴀɴᴅ][buttonurl:https://t.me/Kdramaland]`", filters=filters.text, timeout=30)
    except ListenerTimeout:
        await query.message.reply_text("ʀᴇǫᴜᴇsᴛ ᴛɪᴍᴇ ᴏᴜᴛ !\n\n**⚠️ ʏᴏᴜ ᴀʀᴇ ᴛᴀᴋɪɴɢ ᴛᴏᴏ ʟᴏɴɢ ᴛᴏ ғᴏʀᴡᴀʀᴅ ᴘᴏsᴛ**")
        
    title, url = extract_title_and_url(button.text)

    if title and url:
        try:
            await db.set_buttons(chat_id, button.text)
        except Exception as e:
            print(e)
        await query.message.reply_text("**ᴛʜɪs ʙᴜᴛᴛᴏɴ ᴀᴅᴅᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅**\n\nᴜsᴇ /my_buttons ᴛᴏ ᴠɪᴇᴡ ᴀʟʟ ʏᴏᴜʀ ʙᴜᴛᴛᴏɴ", reply_to_message_id=button.id)
    else:
        await query.message.reply_text("**ɪɴᴠᴀʟɪᴅ ʙᴜᴛᴛᴏɴ ғᴏʀᴍᴀᴛ !**")

@Client.on_callback_query(filters.regex(r'^delbutton_'))
async def handle_del_button(bot: Client, query: CallbackQuery):
    
    btn_idx = query.data.split('_')[1]
    user_id = query.from_user.id

    await db.del_button(user_id, int(btn_idx))
    
    text, btn = await button_text(user_id=query.from_user.id)
    await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup(btn))