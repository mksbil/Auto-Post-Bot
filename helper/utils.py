from base64 import standard_b64decode, standard_b64encode
import math
import random
import re
import string
import logging
import time
import uuid
from datetime import datetime
from pytz import timezone
from config import Config, Txt

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



async def send_log(b, u):
    if Config.LOG_CHANNEL is not None:
        curr = datetime.now(timezone("Asia/Kolkata"))
        date = curr.strftime("%d %B, %Y")
        time_str = curr.strftime("%I:%M:%S %p")
        await b.send_message(
            Config.LOG_CHANNEL,
            f"**--Nᴇᴡ Uꜱᴇʀ Sᴛᴀʀᴛᴇᴅ Tʜᴇ Bᴏᴛ--**\n\n"
            f"Uꜱᴇʀ: {u.mention}\nIᴅ: `{u.id}`\nUɴ: @{u.username}\n\n"
            f"Dᴀᴛᴇ: {date}\nTɪᴍᴇ: {time_str}\n\nBy: {b.mention}",
        )


def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def extract_title_and_url(string):
    # Regular expression pattern to match the desired format
    pattern = r'\[(.*?)\]\[buttonurl:(.*?)\]'
    
    # Using re.match() to check if the string matches the pattern
    match = re.match(pattern, string)
    
    if match:
        # Extracting 'K-Land' and the URL from the match
        title = match.group(1)
        url = match.group(2)
        return title, url
    else:
        return None, None