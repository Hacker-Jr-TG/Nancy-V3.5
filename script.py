class Script(object):
    START_TXT = """<b>{get} {},
My Name is <a href=https://t.me/{}>{}</a>. A Smart RoBot With Many Amazing Features. I Can Provide Movies & Help You To Manage Your Groups, Just Add Me To Your Group And Enjoy.🥰</b>"""

    HELP_TXT = """<b>Hey {}
Here Is The Help For My Commands.</b>"""

    HACKER_TXT = """<b>Here Is The Help For My Commands.</b>"""

    HELLP_TXT = """<b>Here Is The Help For My Commands.</b>"""

    BOTSTATUS_TXT = """Send /status for getting bot and heroku status"""

    ABOUT_TXT = """<b>✯ Mʏ Nᴀᴍᴇ : <a href='https://t.me/Oru_adaar_Robot'>Nᴀɴᴄʏ 🌸</a>
✯ Cʀᴇᴀᴛᴏʀ: <a href='https://t.me/Hacker_Jr'>HᴀᴄKᴇʀ Jʀ 🇮🇳 / 🇺🇸</a>
✯ Lɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʀᴏɢʀᴀᴍ</a>
✯ Lᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/'>Pʏᴛʜᴏɴ 3</a>
✯ Dᴀᴛᴀ Bᴀsᴇ: <a href='https://cloud.mongodb.com/'>Mᴏɴɢᴏ Dʙ</a>
✯ Bᴏᴛ Sᴇʀᴠᴇʀ: <a href='https://heroku.com/'>Hᴇʀᴏᴋᴜ</a>
✯ Bᴜʟʟᴅ Sᴛᴀᴛᴜs: <code>ᴠ3.0.2 [ Bᴇᴛᴀ ]</code></b>"""
   
    MANUALFILTER_TXT = """Help: <b>Filters</b>

- Filter is the feature were users can set automated replies for a particular keyword and Dingdi will respond whenever a keyword is found the message

<b>NOTE:</b>
1. Nancy should have admin privillage.
2. Only admins can add filters in a chat.
3. Alert buttons have a limit of 64 characters.

<b>Commands and Usage:</b>
• /filter - add a filter in chat.
• /filters - list all the filters of a chat.
• /del - delete a specific filter in chat.
• /delall - delete the whole filters in a chat (chat owner only)."""

    BUTTON_TXT = """Help: <b>Buttons</b>

- Nancy support both url and alert inline buttons.

<b>NOTE:</b>
1. Telegram will not allows you to send buttons without any content, so content is mandatory.
2. Nancy supports buttons with any telegram media type.
3. Buttons should be properly parsed as markdown format.

<b>URL buttons:</b>
<code>[Button Text](buttonurl:https://t.me/josprojects)</code>

<b>Alert buttons:</b>
<code>[Button Text](buttonalert:This is an alert message)</code>"""

    JSON_TXT ="""<b>JSON</b>

Bot Send Json For All Replied Messages Using A Simple Command.

<b>Command and Usage:</b>

◉ /json :- Reply To Any Message To Get Json
◉ You Can Use This Command In Pm And Groups."""

    IPADD_TXT = """Help: <b>IP ADDRESS</b>

- if you want to Find Details of a IP Address Use the Module.

<b><u>𝖢𝗈𝗆𝗆𝖺𝗇𝖽:</u></b>

➢ /ip [Ip Address] 
➢ /ip 192.180.0.1
<b>NOTE</b>:

• Nancy should have admin privillage.
• These commands works on both pm and group.
• These commands can be used by any group member."""

    COUNTRY_TXT = """Help: <b>COUNTRY</b>

Here is the help for County information module.

I am a country information finder.

/country [countryname] 
I can find information of any country of the world"""

    LOGO_TXT = """Help: <b>LOGO</b>

Create awesome cool logo with your name!

USAGE:
➢ /logo [text] - Create logo with given text.
➢ /logo [reply][colour] - Create logo with replied text.
➢ /logo [text]|[colour] - Create logo with text & colour.

<b>NOTE</b>:
• Nancy should have admin privillage.
• These commands works on both pm and group.
• These commands can be used by any group member."""

    CARBON_TXT = """HELP: <b>CARBON</b>

Beautify your code using carbon.now.sh!

USAGE:
➢ /carbon [text] - Create carbon from the given text.
➢ /carbon [reply] - Create carbon from the replied text.

<b>NOTE</b>:
• Nancy should have admin privillage.
• These commands works on both pm and group.
• These commands can be used by any group member."""

    IMG_TXT = """HELP: <b>TEXT-IMAGE</b>

If You Want To Make A Image Of Text Send.

USAGE:
➢ /text [text] to Get the Photo.

<b>NOTE</b>:
• Nancy should have admin privillage.
• These commands works on both pm and group.
• These commands can be used by any group member."""

    FONTS_TXT = """HELP: <b>FONTS</b>

Want Some Stylish Fonts Send.

USAGE:
➢ /font [text] Create Font with given text..

<b>NOTE</b>:
• Nancy should have admin privillage.
• These commands works on both pm and group.
• These commands can be used by any group member."""

    LOCK_TXT = """Here is the help for the <b>Locks</b> module:

<b>Admin only</b>:
× /lock <permission>: Lock Chat permission..
× /unlock <permission>: Unlock Chat permission.
× /locks: View Chat permission.
× /locktypes: Check available lock types!
Locks can be used to restrict a group's users.
Locking urls will auto-delete all messages with urls, locking stickers will delete all stickers, etc.
Locking bots will stop non-admins from adding bots to the chat.

Example:
/lock media: this locks all the media messages in the chat."""

    REPORT_TEXT = """𝖧𝖾𝗅𝗉: <b><u>𝖱𝖾𝗉𝗈𝗋𝗍</u></b>

Report something wrong to group admins for review!

<b><u>𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌:</u></b>
➢ /report [reply] - Report a message to admins for review.
➢ /report [reason] - Report a message to admins with reason.
➢ @admins - Same as report command, but not a command.

<b><u>NOTE:</u></b>
• Nancy should have admin privillage.
• These commands can be used only in group.
• These commands can be used by any group member."""

    SONG_TXT = """Help: <b>🎼Song Download🎼</b>

Song Download Module, For Those Who Love Music.

<b>𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌</b>
- /song [Song Name] - To Download Music 😁.

<b>Usage</b>
- Can Be Used By Everyone
- Works in bot pm."""

    VIDEO_TXT = """Help: <b>VIDEO</b>

Help You To Download Video From YouTube.

<b><u>𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌:</u></b>
• Type /video or /MP4 And [YouTube Link]
• Example:- <code>/video https://youtu.be/8FAUEv_E_xQ</code> 

<b>USAGE:</b>
• You Can Download Any Video From YouTube"""

    YTTHUMB_TXT = """Help: <b>YouTube Thumbnail</b>

Help To Download Any YouTube Video Thumbnail.

<b><u>𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌:</u></b>
• Type /ytthumb And [YouTube Link]
• Example:- <code>/ytthumb https://youtu.be/8FAUEv_E_xQ</code> 

<b>USAGE:</b>
• You Can Download From YouTube Thumbnail"""

    PASSWORD_GEN_TXT = """Help: <b>Password Generator</b>

There Is Nothing To Know More. Send Me The Limit Of Your Password.
- I Will Give The Password Of That Limit.

<b>Commands and Usage:</b>
• /genpassword or /genpw <code>20</code>

<b>NOTE:</b>
• Only Digits Are Allowed
• Maximum Allowed Digits Till 84 
(I Can't Generate Passwords Above The Length 84)
• Nancy should have admin privillage.
• These commands works on both pm and group.
• These commands can be used by any group member."""

    AFK_TXT = """Help: <b>AFK</b>

Away From Keyboard is to tell that you're not available!

<b>Commands and Usage:</b>
• /afk - Mark yourself as afk.
• /afk [reason] - Mark yourself as afk with reason.

NOTE:
• Nancy should have admin privillage.
• These commands can be used only in group.
• These commands can be used by any group member."""

    FILLINGS_TXT = """Help: <b>Fillings</b>

You can also customise the contents of your message with contextual data. For example, you could mention a user by name in the filter message, or mention them in a filter!

<b>Supported fillings:</b>
- <code>{first}</code>: The user's first name.
- <code>{last}</code>: The user's last name.
- <code{username}</code>: The user's username.
- <code>{mention}</code>: Mentions the user with their firstname.
- <code>{id}</code>: The user's ID.
- <code>{dcid}</code>: The user's DC ID.
- <code>{chatname}</code>: The chat's name.
- <code>{query}</code>: Any Replied Message.

<b>Example:</b>
<b>- Save a filter using the mention.</b>
-> <code>/filter test Hello {mention} This Is your Username : {username} And This Is your ID : {id}.</code>
"""

    AUTOFILTER_TXT = """Help: <b>Auto Filter</b>

<b>NOTE:</b>
1. Make me the admin of your channel if it's private.
2. Make sure that your channel does not contains camrips, porn and fake files.
3. Forward the last message to me with quotes.
 I'll add all the files in that channel to my db."""

    CONNECTION_TXT = """Help: <b>Connections</b>

- Used to connect bot to PM for managing filters 
- It helps to avoid spamming in groups.

<b>NOTE:</b>
1. Only admins can add a connection.
2. Send <code>/connect</code> for connecting me to ur PM

<b>Commands and Usage:</b>
• /connect  - connect a particular chat to your PM.
• /disconnect  - disconnect from a chat.
• /connections - list all your connections."""

    AUTO_MANUAL_TXT = """Help: <b>Filters</b>

<b>Select a filters type Below:</b>"""

    PASTE_TXT = """Help: <b>Paste</b>

Paste some texts or documents on a website!

<b>Commands and Usage:</b>
• /paste [text] - paste the given text on Pasty
• /paste [reply] - paste the replied text on Pasty

<b>NOTE:</b>
• Nancy should have admin privillage.
• These commands works on both pm and group.
• These commands can be used by any group member."""

    TGRAPH_TXT = """Help: <b>TGraph & Paste</b>

Do as you wish with telegra.ph module!

<b>Commands and Usage:</b>
• /tgmedia or /tgraph - upload supported media (within 5MB) to telegraph.

<b>NOTE:</b>
• Nancy should have admin privillage.
• These commands works on both pm and group.
• These commands can be used by any group member."""

    INFO_TXT = """Help: <b>Information</b>

Get information about something!

<b>Commands and Usage:</b>
• /id - get id of a specified user.
• /info  - get information about a user.
• /json - get the json details of a message.

<b>NOTE:</b>
• Nancy should have admin privillage.
• These commands works on both pm and group.
• These commands can be used by any group member."""

    TORRENT_TXT = """Help: <b>Torrent Search</b>

<b>Commands and Usage:</b>
• /torrent or /tor <movie name>: Get Your Torrent Link From Various Resource.

<b>NOTE:</b>
• Nancy should have admin privillage.
• These commands works on both pm and group.
• These commands can be used by any group member."""

    GTRANS_TXT = """Help: <b>Google Translator</b>

Translate texts to a specific language!

<b>Commands and Usage:</b>
• /tr [language code][reply] - translate replied message to specific language.

<b>NOTE:</b>
• Nancy should have admin privillage.
• These commands works on both pm and group.
• IMDb can translate texts to 200+ languages."""

    SEARCH_TXT = """Help: <b>IMDb</b>

Search many things without leaving telegram!

<b>Commands and Usage:</b>
• /imdb  - get the film information from IMDb source.
• /search  - get the film information from various sources.

<b>NOTE:</b>
• Nancy should have admin privillage.
• More search tools can be found on inline.
• Those commands works on both pm and group."""

    PURGE_TXT = """Help: <b>Purge</b>

Need to delete lots of messages? That's what purges are for!

<b>Commands and Usage:</b>
• /purge - delete all messages from the replied to message, to the current message.

<b>NOTE:</b>
• Nancy should have admin privillage.
• These commands works on group.
• These commands can be used by Only admin."""

    RESTRIC_TXT = """Help: <b>Restrictions</b>

Some people need to be publicly banned; spammers, annoyances, or just trolls.

This module allows you to do that easily, by exposing some common actions, so everyone will see!

<b>Commands and Usage:</b>
• /ban - ban a user.
• /tban - temporarily ban a user. Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.
• /mute - mute a user.
• /tmute - temporarily mute a user. Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.
• /unban or /unmute - unmute a user & unban a user.

<b>Examples:</b>
- Mute a user for two hours.
-> <code>/tmute @username 2h</code>

<b>NOTE:</b>
• Nancy should have admin privillage.
• These commands works on group.
• These commands can be used by Only admin."""

    PIN_MESSAGE_TXT = """Help: <b>Pin Message</b>

All the pin related commands can be found here; keep your chat up to date on the latest news with a simple pinned message!

<b>Commands and Usage:</b>
• /pin: Pin the message you replied to. Add 'loud' or 'notify' to send a notification to group members.
• /unpin: Unpin the current pinned message. If used as a reply, unpins the replied to message.

<b>NOTE:</b>
• Nancy should have admin privillage.
• These commands works only group.
• These commands can be used by Only admin."""

    ADMIN_TXT = """Help: <b>Admin Mods</b>

<b>NOTE:</b>
This module only works for my admins

<b>Commands and Usage:</b>
• /logs - to get the rescent errors.
• /stats - to get status of files in db.
• /delete - to delete a specific file from db.
• /users - to get list of my users and ids.
• /chats - to get list of the my chats and ids.
• /leave - to leave from a chat.
• /disable - do disable a chat.
• /ban_users - to ban a user.
• /unban_users - to unban a user.
• /channel - to get list of total connected channels.
• /broadcast - to broadcast a message to all users."""

    STATUS_TXT = """<b>Total Files:</b> <code>{}</code>
<b>Total Users:</b> <code>{}</code>
<b>Total Chats:</b> <code>{}</code>
<b>Used Storage:</b> <code>{}</code> MiB
<b>Free Storage:</b> <code>{}</code> MiB"""

    FORCESUB_TXT = """**♦️ READ THIS INSTRUCTION ♦️**

__🗣 In Order To Get The Movie Requested By You in Our Groups, You Will Have To Join Our Official Channel First. After That, Try Accessing That Movie Again From Our Group. I'll Send You That Movie Privately 🙈__

**👇 JOIN THIS CHANNEL & TRY AGAIN 👇**"""

    MEMES_TXT = """Help: <b>Memes</b>

Some dank memes for fun or whatever!

<b>Commands and Usage:</b>
• /throw or /dart - t𝗈 m𝖺𝗄𝖾 drat 
• /roll or /dice - roll the dice 
• /goal or /shoot - to make a goal or shoot
• /luck or /cownd - Spin the Lucky
• /runs strings

<b>NOTE:</b>
• Nancy should have admin privillage.
• These commands works on both pm and group.
• These commands can be used by any group member."""

    URL_SHORTNER_TXT = """Help: <b>URL Shortner</b>

Some URLs is Shortner

<b>Commands and Usage:</b>
• /short <code>(link)</code> - I will send the shorted links.

<b>Example:</b>
<code>/short https://t.me/josprojects</code>

<b>NOTE:</b>
• Nancy should have admin privillage.
• These commands works on both pm and group.
• These commands can be used by any group member."""

    TTS_TXT = """Help: <b>Text to Speech</b>

A module to convert text to voice with language support.

<b>Commands and Usage:</b>
• /tts - Reply to any text message with language code to convert as audio.

<b>NOTE:</b>
• Nancy should have admin privillage.
• These commands works on both pm and group.
• These commands can be used by any group member."""

    ABOOK_TXT = """➤ 𝐇𝐞𝐥𝐩: 𝖠𝗎𝖽𝗂𝗈𝖻𝗈𝗈𝗄
𝚈𝚘𝚞 𝚌𝚊𝚗 𝚌𝚘𝚗𝚟𝚎𝚛𝚝 𝚊 𝙿𝙳𝙵 𝚏𝚒𝚕𝚎 𝚝𝚘 𝚊 𝚊𝚞𝚍𝚒𝚘 𝚏𝚒𝚕𝚎 𝚠𝚒𝚝𝚑 𝚝𝚑𝚒𝚜 𝚌𝚘𝚖𝚖𝚊𝚗𝚍 ✯
➤ 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬 𝐚𝐧𝐝 𝐔𝐬𝐚𝐠𝐞:
➪ /audiobook: 𝖱𝖾𝗉𝗅𝗒 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗍𝗈 𝖺𝗇𝗒 𝖯𝖣𝖥 𝗍𝗈 𝗀𝖾𝗇𝖾𝗋𝖺𝗍𝖾 𝗍𝗁𝖾 𝖺𝗎𝖽𝗂𝗈"""

    FILE_TXT = """➤ 𝐇𝐞𝐥𝐩: 𝖥𝗂𝗅𝖾 𝖲𝗍𝗈𝗋𝖾
𝚆𝚒𝚝𝚑 𝚝𝚑𝚒𝚜 𝚌𝚘𝚖𝚖𝚊𝚍𝚜 𝚒 𝚌𝚊𝚗 𝚜𝚝𝚘𝚛𝚎 𝚏𝚒𝚕𝚎𝚜 𝚊𝚗𝚍 𝚐𝚒𝚟𝚎 𝚢𝚘𝚞 𝚊 𝚜𝚑𝚊𝚛𝚎𝚊𝚋𝚕𝚎 𝚕𝚒𝚗𝚔 𝚠𝚒𝚝𝚑 𝚝𝚑𝚒𝚜 𝚕𝚒𝚗𝚔 𝚒 𝚌𝚊𝚗 𝚜𝚑𝚊𝚛𝚎 𝚝𝚑𝚊𝚝 𝚏𝚒𝚕𝚎𝚜 𝚢𝚘𝚞 𝚐𝚒𝚟𝚎 𝚖𝚎 𝚏𝚛𝚘𝚖 𝚊𝚗𝚢 𝚌𝚑𝚊𝚗𝚗𝚎𝚕 𝚠𝚒𝚝𝚑𝚘𝚞𝚝 𝚊𝚍𝚍𝚒𝚗𝚐 𝚖𝚎
➤ 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬 𝐚𝐧𝐝 𝐔𝐬𝐚𝐠𝐞:
➪ /plink - 𝖱𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺𝗇𝗒 𝗆𝖾𝖽𝗂𝖺 𝗍𝗈 𝗀𝖾𝗍 𝗅𝗂𝗇𝗄
➪ /pbatch - 𝖴𝗌𝖾 𝗒𝗈𝗎𝗋 𝗆𝖺𝖽𝗂𝖺 𝗅𝗂𝗇𝗄 𝗐𝗂𝗍𝗁 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽
➪ /batch - To create link for multiple post
➛𝖤𝗑𝖺𝗆𝗉𝗅𝖾:
/pbatch <code>https://t.me/c/1508000334/555 https://t.me/c/1508000334/557</code>"""

    MUSIC_TXT = """Help: <b>Music</b>

Music download modules, for those who love music.

<b>Commands and Usage:</b>
• /song or /mp3 (songname) - download song from yt servers.
• /video or /mp4 (songname) - download video from yt servers.

<b>YouTube Thumbnail Download</b>
• /ytthumb (youtube link)
<b>Example:</b> <code>/ytthumb https://youtu.be/h6PtzFYaMxQ</code>

<b>NOTE:</b>
• Nancy should have admin privillage.
• These commands works on both pm and group.
• These commands can be used by any group member."""

    STICKER_TXT = """<b>𝗛𝗲𝗹𝗽 𝗙𝗼𝗿 𝗦𝘁𝗶𝗰𝗸𝗲𝗿 𝗶𝗱

• 𝗨𝘀𝗮𝗴𝗲
To Get Sticker ID

• 𝗛𝗼𝘄 𝗧𝗼 𝗨𝘀𝗲
◉ Reply To Any Sticker [<code>/stickerid</code>]</b>"""

    CORONA_TXT ="""Help: <b>Corona</b>

<b>Here is the help for the coron information module</b>

➢ /covid <code>(countryname)</code> <b>you can find a corona information of every country</b>

➢ <b>Example</b> : - /covid India"""

    PASSWORD_GEN_TXT = """Help: <b>Password Generator</b>

There Is Nothing To Know More. Send Me The Limit Of Your Password.
- I Will Give The Password Of That Limit.

<b>Commands and Usage:</b>
• /genpassword or /genpw <code>20</code>

<b>NOTE:</b>
• Only Digits Are Allowed
• Maximum Allowed Digits Till 84 
(I Can't Generate Passwords Above The Length 84)
• IMDb should have admin privillage.
• These commands works on both pm and group.
• These commands can be used by any group member."""

    SHARE_TXT = """Help: <b>Sharing Text Maker</b>

a bot to create a link to share text in the telegram.

<b>Commands and Usage:</b>
• /share (text or reply to message)

<b>NOTE:</b>
• Nancy should have admin privillage.
• These commands works on both pm and group.
• These commands can be used by any group member."""

    LOG_TEXT_G = """#NewGroup
Group = {}(<code>{}</code>)
Total Members = <code>{}</code>
Added By - {}
"""

    LOG_TEXT_P = """#NewUser
ID - <code>{}</code>
Name - {}"""

    ZOMBIES_TXT = """Help: <b>Zombies</b>

<b>Kick incative members from group. Add me as admin with ban users permission in group.</b>

<b>Commands and Usage:</b>
• /inkick - command with required arguments and i will kick members from group.
• /instatus - to check current status of chat member from group.
• /inkick within_month long_time_ago - to kick users who are offline for more than 6-7 days.
• /inkick long_time_ago - to kick members who are offline for more than a month and Deleted Accounts.
• /dkick - to kick deleted accounts."""

    CREATOR_REQUIRED = """❗You have to be the group creator to do that."""
      
    INPUT_REQUIRED = "❗ **Arguments Required**"
      
    KICKED = """✔️ Successfully Kicked {} members according to the arguments provided."""
      
    START_KICK = """🚮 Removing inactive members this may take a while..."""
      
    ADMIN_REQUIRED = """❗I am not an admin here\n__Leaving this chat, add me again as admin with ban user permission."""
      
    DKICK = """✔️ Kicked {} Deleted Accounts Successfully."""
      
    FETCHING_INFO = """Collecting users information..."""
      
    STATUS = """{}\nChat Member Status**\n\n```recently``` - {}\n```within_week``` - {}\n```within_month``` - {}\n```long_time_ago``` - {}\nDeleted Account - {}\nBot - {}\nUnCached - {}
"""

