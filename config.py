import re
import os
import time

id_pattern = re.compile(r'^.\d+$')


class Config(object):
    # pyro client config
    API_ID = os.environ.get("API_ID", "")  # ⚠️ Required
    API_HASH = os.environ.get("API_HASH", "")  # ⚠️ Required
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")  # ⚠️ Required
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "")  # ⚠️ Required

    # database config
    DB_URL = os.environ.get("DB_URL", "")  # ⚠️ Required

    # other configs
    BOT_UPTIME = time.time()
    START_PIC = os.environ.get("START_PIC", "https://graph.org/file/e30efcd2b42b81749996c.jpg")
    ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '').split()]  # ⚠️ Required
    FORCE_SUB = os.environ.get('FORCE_SUB', '') # ⚠️ Required without [@]
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", ""))  # ⚠️ Required

    # wes response configuration
    WEBHOOK = bool(os.environ.get("WEBHOOK", True))
    PORT = int(os.environ.get("PORT", "8080"))


class Txt(object):
    # part of text configuration
    START_TXT = """<b>Hello {} 👋,
━━━━━━━━━━━━━━━━━━━━━
Tʜɪs Bᴏᴛ Cᴀɴ Aᴜᴛᴏ Pᴏsᴛ Tᴏ Aʟʟ Yᴏᴜʀ Cʜᴀɴɴᴇʟ Aᴛ Oɴᴄᴇ
━━━━━━━━━━━━━━━━━━━━━
Sᴜᴘᴘᴏʀᴛs Cᴜsᴛᴏᴍ Bᴜᴛᴛᴏɴ & Mᴜʟᴛɪᴘʟᴇs Pᴏsᴛs & Mᴜʟᴛɪᴘʟᴇs Cʜᴀɴᴇʟs
"""

    ABOUT_TXT = """<b>
➥ ᴍy ɴᴀᴍᴇ : {}
➥ Pʀᴏɢʀᴀᴍᴇʀ : <a href=https://t.me/Snowball_Official>ѕησωвαℓℓ ❄️</a> 
➥ ꜰᴏᴜɴᴅᴇʀ ᴏꜰ : <a href=https://t.me/Kdramaland>K-Lᴀɴᴅ</a>
➥ Lɪʙʀᴀʀy : <a href=https://github.com/pyrogram>Pyʀᴏɢʀᴀᴍ</a>
➥ Lᴀɴɢᴜᴀɢᴇ: <a href=https://www.python.org>Pyᴛʜᴏɴ 3</a>
➥ Dᴀᴛᴀ Bᴀꜱᴇ: <a href=https://cloud.mongodb.com>Mᴏɴɢᴏ DB</a>
➥ ᴍʏ ꜱᴇʀᴠᴇʀ : <a href=https://dashboard.heroku.com>Heroku</a>
➥ ᴠᴇʀsɪᴏɴ : v1.0.0
"""

    HELP_TXT = """
Tʜɪs Bᴏᴛ Wɪʟʟ Hᴇʟᴘ Yᴏᴜ Tᴏ Sᴇɴᴅ Pᴏsᴛs Tᴏ Yᴏᴜʀ Mᴜʟᴛɪᴘʟᴇ Cʜᴀɴɴᴇʟs

❗ Dᴇᴠᴇʟᴏᴘᴇʀ :- <a href=https://t.me/Snowball_official>ѕησωвαℓℓ ❄️</a>
"""

    STATS_TXT = """
╔════❰ sᴇʀᴠᴇʀ sᴛᴀᴛs  ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼ ᴜᴩᴛɪᴍᴇ: `{0}`
║┣⪼ ᴛᴏᴛᴀʟ ᴅɪsᴋ sᴘᴀᴄᴇ: `{1}`
║┣⪼ ᴜsᴇᴅ: `{2} ({3}%)`
║┣⪼ ꜰʀᴇᴇ: `{4}`
║┣⪼ ᴄᴘᴜ: `{5}%`
║┣⪼ ʀᴀᴍ: `{6}%`
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍⊱❁۪۪        
"""


class temp(object):

    POST_ID = {}
