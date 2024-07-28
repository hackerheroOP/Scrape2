import os


DATABASE_CHANNEL = int(os.environ.get("DATABASE","-1002180333729"))
BOTUSERNAME = os.environ.get("BOT","desi_pauwa_bot")
TOPOSTCHANNEL = int(os.environ.get("POST","-1002182195778"))
API_ID = int(os.environ.get("API_ID","2066976"))
API_HASH = os.environ.get("API_HASH","6668d5406ac9675f9de3e8fd1ccc357d")
st = os.environ.get("STRING","AQApxggATQ1FaM5_FfwGRpr5-2EvF1a4fDB2umcKYHIV17gFvn2NaqU436WDzcPivgZ7uQYDLYnu2hsmXX-OdQbLBZUsjpcVNXtjAuab1X_MMNu0voCAuFzf2czeBZP2wZyPXpuzSl8aHrGWMo4iLmxZYUtW4pCRIAUDNZUMspD9QGIa8oxu7jXYgMExEY3luYQp8EBqbQhUMPjDRiqi-7YT5CNKRnJ7tQrVOcdlqjmVYsThQWIPKcCE81aOpf5YuO2qJjGs4skEB-UFF4uGJwuwzI0wR-QoL62vFnbAFF7b0OZj4iTjeixEc1J8r_doPBN9bdWqcq8KmfTMHR9AdXi9jBfDZAAAAAGpRFkfAA")


from pyrogram import Client
from pyrogram import Client, filters
import re
import asyncio
import subprocess
import uuid
from pyromod import listen
import base64
import os
from pyrogram import enums
from pyrogram import Client
import asyncio
import random,string

from PIL import Image, ImageDraw, ImageFont, ImageOps
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import time
from pyrogram import filters


async def take_screen_shot(video_file):
    print(f"Attempting to take screenshot of video file: {video_file}")
    
    if not os.path.exists(video_file):
        print(f"Error: Video file {video_file} does not exist.")
        return None
    metadata = extractMetadata(createParser(video_file))

    duration = 0
    if metadata.has("duration"):
        duration = metadata.get('duration').seconds
        ttl = random.randint(0, duration - 1)
    
    out_put_file_name =   str(time.time()) + ".jpg"
    
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
    
    # width = "90"
    if metadata.has("width"):
         width = metadata.get("width")
    if metadata.has("height"):
         height = metadata.get("height")
    
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    if stderr:
        print(f"Error in ffmpeg: {stderr.decode()}")
    if not os.path.exists(out_put_file_name):
        print(f"Failed to create output file: {out_put_file_name}")
        return None
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    x = Image.open(out_put_file_name).convert(
                   "RGB"
                 )
    x.save(out_put_file_name)
    x.close()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name,width,height,duration
    else:
        return None




async def encode(string):
    string_bytes = string.encode("ascii")
    print(f"Encoding string: {string}")
    base64_bytes = base64.urlsafe_b64encode(string_bytes)
    base64_string = (base64_bytes.decode("ascii")).strip("=")
    return base64_string


async def decode(encoded_string):
    padding = '=' * (-len(encoded_string) % 4)
    encoded_string_padded = encoded_string + padding
    base64_bytes = base64.urlsafe_b64decode(encoded_string_padded)
    decoded_string = base64_bytes.decode("ascii")
    return len(decoded_string.split("-"))


app = Client("hiiibot",api_hash=API_HASH,api_id=API_ID,session_string=st)
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
                #bot_name, start_value = re.findall(r't.me/([^/?]+).*start=([^"&]+)', msg.caption)[0] if re.search(r't.me/([^/?]+).*start=([^"&]+)', msg.caption) else (None, None)
                bot_name, start_value = (
                re.search(r'https://t.me/([^/?]+)\?start=([^"&\s]+)', msg.caption).groups() 
               if msg.caption and re.search(r'https://t.me/([^/?]+)\?start=([^"&\s]+)', msg.caption) 
               else (None, None)
)
                start_value = start_value.strip().replace("TUTORIAL", "").replace("🔗How to open the link🔗","").replace("🔗 How to open the link🔗","").replace("🔗How to open the link 🔗","").replace("🔗 How to open the link 🔗","").replace("Tutorial", "").replace("How to open link in hindi","").replace("How to open link","").replace("🔗How to open the link🔗","").replace("How to open link in hindi","")
                if start_value:
                    v = await client.send_message(chat_id=bot_name, text=f"/start {start_value}")
                    await v.delete()
                    await asyncio.sleep(15)

                    first = False
                    w = await decode(start_value)
                    async for messag in app.get_chat_history(bot_name):
                        if w == 3:
                            if not messag.photo and not messag.video and not messag.document:
                                pass
                            if messag.photo:
                                file = await client.download_media(message=messag,file_name=".app/DOWNLOADS/seddd.jpeg")
                                msgid = await client.send_photo(photo=".app/DOWNLOADS/seddd.jpeg", chat_id=DATABASE_CHANNEL)
                                await messag.delete()

                                if first == False:
                                    first = msgid.id
                                else:
                                    last = msgid.id

                            elif messag.video:
                                print("Downloading")
                                random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
                                file = await client.download_media(message=messag, file_name=f".app/DOWNLOADS/{random_string}.mp4")
                                await messag.delete()
                                sed = await take_screen_shot(f'.app/DOWNLOADS/{random_string}.mp4')
                                print('uplo')
                                i = await client.send_video(video=f'.app/DOWNLOADS/{random_string}.mp4', chat_id=DATABASE_CHANNEL, thumb=sed[0], duration=sed[3], height=sed[2], width=sed[1])
                                if first == False:
                                    first = i.id
                                else:
                                    last = i.id
                            elif messag.document:
                                file = await messag.download(in_memory=True)
                                msgid = await client.send_document(document=file, chat_id=DATABASE_CHANNEL)
                                await messag.delete()
                                if first == False:
                                    first = msgid.id
                                else:
                                    last = msgid.id
                                await messag.delete()
                                
                         

                        else:
                          try:
                            if messag.video:
                                print('Downloading')
                                random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
                                await client.download_media(message=messag.video.file_id, file_name=f'.app/DOWNLOADS/{random_string}.mp4')
                                await messag.delete()
                                y = f'.app/DOWNLOADS/{random_string}.mp4'
                                sed = await take_screen_shot(y)
                                print('uplo')
                                i = await client.send_video(video=f'.app/DOWNLOADS/{random_string}.mp4', chat_id=DATABASE_CHANNEL, thumb=sed[0], duration=sed[3], height=sed[2], width=sed[1])
                                first = i.id
                            elif messag.document:
                                file = await messag.download(in_memory=True)
                                msgid = await client.send_document(document=file, chat_id=DATABASE_CHANNEL)
                                first = msgid.id
                                await messag.delete()
                            elif messag.photo:
                                file = await client.download_media(message=messag, in_memory=True)
                                msgid = await client.send_photo(photo=file, chat_id=DATABASE_CHANNEL)
                                first = msgid.id
                                await messag.delete()
                          except:
                              pass

                    if w == 3:
                        stringg = f"get-{first * abs(DATABASE_CHANNEL)}-{last * abs(DATABASE_CHANNEL)}"
                    else:
                        stringg = f"get-{first * abs(DATABASE_CHANNEL)}"

                    base64_string = await encode(stringg)
                    link = f"https://t.me/{BOTUSERNAME}?start={base64_string}"

                    try:
                        if msg.media_group_id:
                            await client.copy_media_group(chat_id=TOPOSTCHANNEL, captions=f"**\nHere is Your Link**\n\n{link}", message_id=msg.id, from_chat_id=chnid)


                        else:
                            await client.copy_message(parse_mode=enums.ParseMode.MARKDOWN, caption=f"**\n Here is Your Link**\n\n{link}", chat_id=TOPOSTCHANNEL, message_id=msg.id, from_chat_id=chnid)

                    except:
                        asyncio.sleep(60)

     except Exception as e:
         print(e)

app.run()
