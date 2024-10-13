from datetime import datetime
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
import os

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="renamer",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=min(32, os.cpu_count() + 4),
            plugins={"root": "plugins"},
            sleep_threshold=15,
            max_concurrent_transmissions=Config.MAX_CONCURRENT_TRANSMISSIONS,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username  
        self.uptime = Config.BOT_UPTIME     

        if Config.WEB_SUPPORT:
            app = web.Application(client_max_size=30000000)
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, "0.0.0.0", 8000)
            await site.start()  # Ensure this line has await

        print(f"\033[1;96m @{me.username} Sᴛᴀʀᴛᴇᴅ......⚡️⚡️⚡️\033[0m")
        
        # Notify admins about bot startup
        try:
            [await self.send_message(id, f"**__{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**") for id in Config.ADMIN]                              
        except Exception as e:
            print(f"Error notifying admins: {e}")

        # Log channel startup message
        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(
                    Config.LOG_CHANNEL,
                    f"**__{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!**\n\n📅 Dᴀᴛᴇ : `{date}`\n⏰ Tɪᴍᴇ : `{time}`\n🌐 Tɪᴍᴇᴢᴏɴᴇ : `Asia/Kolkata`\n\n🉐 Vᴇʀsɪᴏɴ : `v{__version__} (Layer {layer})`</b>"
                )
            except Exception as e:
                print(f"Error sending log channel message: {e}")
                print("Pʟᴇᴀꜱᴇ Mᴀᴋᴇ Sᴜʀᴇ Tʜɪs Bᴏᴛ Is Aᴅᴍɪɴ In Yᴏᴜʀ Lᴏɢ Cʜᴀɴɴᴇʟ")

Bot().run()
