
import os
import re
import asyncio
import random
import string
from pyrogram import Client, filters, enums
from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import time
import base64

# Environment variables
DATABASE_CHANNEL = int(os.environ.get("DATABASE_CHANNEL", "-1002180333729"))
API_ID = int(os.environ.get("API_ID", "2066976"))
API_HASH = os.environ.get("API_HASH", "6668d5406ac9675f9de3e8fd1ccc357d")
st = os.environ.get("STRING", "BQAfiiAANSd5YZwDSNv4GB35Ue4CMQU00vqldAq3_kbuswtkmb6ylbyRww07BZGe2_tYqJmLTH38WWTOvLdmLiWgAdT19_udM8jyu1O5ttNO7p1837c0jIGwdQ16uGYFfl8VreJbAGwRI0Bo3YyDkP_xxC9pxAm-rObOaKQBSjzENW4INhYuyMuKCUY2vEDCev5SSKWFQM5KmCY1KDPksp1V_n1_ztyQtRsEBeiEMWgrtmy7J3fM7FQnlpixV-SP2ErWdOy8v8hX-I6m4f0x5xBFajcstSdY1lHbCqKKSL1Gc9xLqNkWPZgxxO4zgunuSr4LCM3CT5_n_I8rmf-Zt_I0SZtwIgAAAAG6eRFnAA")

# Pyrogram client
app = Client("hiiibot", api_hash=API_HASH, api_id=API_ID, session_string=st)

async def take_screen_shot(video_file):
    print(f"Attempting to take screenshot of video file: {video_file}")
    if not os.path.exists(video_file):
        print(f"Error: Video file {video_file} does not exist.")
        return None
    metadata = extractMetadata(createParser(video_file))
    duration = metadata.get("duration").seconds if metadata.has("duration") else 0
    ttl = random.randint(0, duration - 1)
    out_put_file_name = str(time.time()) + ".jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        f"{video_file}",
        "-vframes",
        "1",
        out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if stderr:
        print(f"Error in ffmpeg: {stderr.decode()}")
    if not os.path.exists(out_put_file_name):
        print(f"Failed to create output file: {out_put_file_name}")
        return None
    x = Image.open(out_put_file_name).convert("RGB")
    x.save(out_put_file_name)
    x.close()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name, metadata.get("width"), metadata.get("height"), duration
    else:
        return None

async def encode(string):
    string_bytes = string.encode("ascii")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    return (base64_bytes.decode("ascii")).strip("=")

async def decode(encoded_string):
    padding = '=' * (-len(encoded_string) % 4)
    encoded_string_padded = encoded_string + padding
    base64_bytes = base64.urlsafe_b64decode(encoded_string_padded)
    decoded_string = base64_bytes.decode("ascii")
    return len(decoded_string.split("-"))

@app.on_message(filters.private & filters.command(["li"]))
async def hello(client, message):
    x = await message.reply_text("hiii")
    await x.delete()
    x = message.text.split("/li")[1].split('https://t.me/c/')[1]
    chnid = int(f'-100{x.split("/")[0]}')
    await message.delete()
    s = app.get_chat_history(chnid)

    async for msg in s:
        try:
            await asyncio.sleep(5)
            if msg.photo or msg.video:
                if "https://t.me/" in str(msg.caption) and "start" in str(msg.caption):
                    bot_name, start_value = (
                        re.search(r'https://t.me/([^/?]+)\?start=([^"&\s]+)', msg.caption).groups()
                        if msg.caption and re.search(r'https://t.me/([^/?]+)\?start=([^"&\s]+)', msg.caption)
                        else (None, None)
                    )
                    start_value = re.sub(r'https?://\S+|@\w+', '', start_value).strip()
                    if start_value:
                        v = await client.send_message(chat_id=bot_name, text=f"/start {start_value}")
                        await v.delete()
                        await asyncio.sleep(15)
                        first = False
                        w = await decode(start_value)
                        async for messag in app.get_chat_history(bot_name):
                            if messag.photo:
                                file = await client.download_media(message=messag, in_memory=True)
                                msgid = await client.send_photo(photo=file, chat_id=DATABASE_CHANNEL)
                                if not first:
                                    first = msgid.id
                            elif messag.video:
                                random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
                                file = await client.download_media(message=messag, file_name=f".app/DOWNLOADS/{random_string}.mp4")
                                sed = await take_screen_shot(file)
                                i = await client.send_video(video=file, chat_id=DATABASE_CHANNEL, thumb=sed[0], duration=sed[3], height=sed[2], width=sed[1])
                                if not first:
                                    first = i.id
                            elif messag.document:
                                file = await messag.download(in_memory=True)
                                msgid = await client.send_document(document=file, chat_id=DATABASE_CHANNEL)
                                if not first:
                                    first = msgid.id
                        stringg = f"get-{first * abs(DATABASE_CHANNEL)}"
                        base64_string = await encode(stringg)
                        link = f"https://t.me/{bot_name}?start={base64_string}"
                        # Remove links and usernames from captions
                        original_caption = msg.caption if msg.caption else ""
                        cleaned_caption = re.sub(r'https?://\S+|@\w+', '', original_caption).strip()
                        try:
                            if msg.media_group_id:
                                await client.copy_media_group(
                                    chat_id=TOPOSTCHANNEL,
                                    from_chat_id=chnid,
                                    message_id=msg.id,
                                    captions=f"{cleaned_caption}\n\n**Here is Your Link:** {link}"
                                )
                            else:
                                await client.copy_message(
                                    chat_id=TOPOSTCHANNEL,
                                    from_chat_id=chnid,
                                    message_id=msg.id,
                                    caption=f"{cleaned_caption}\n\n**Here is Your Link:** {link}",
                                    parse_mode=enums.ParseMode.MARKDOWN
                                )
                        except Exception as e:
                            print(f"Error while copying: {e}")
                            await asyncio.sleep(60)
        except Exception as e:
            print(e)

app.run()
