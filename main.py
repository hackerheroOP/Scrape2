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
