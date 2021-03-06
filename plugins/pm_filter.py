# Kanged From @TroJanZheX
import asyncio
import re
import ast
import pytz, datetime

from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from script import Script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import ADMINS, AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, P_TTI_SHOW_OFF, IMDB, \
    SINGLE_BUTTON, SPELL_CHECK_REPLY, IMDB_TEMPLATE
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.handlers import CallbackQueryHandler
from pyrogram import Client, filters
from plugins.buttons import KGF_BUTTON, KGF2_BUTTON, KGF_D_BUTTON
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results
from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}
FILTER_MODE = {}

@Client.on_message(filters.command('autofilter'))
async def fil_mod(client, message): 
      mode_on = ["yes", "on", "true"]
      mode_of = ["no", "off", "false"]

      try: 
         args = message.text.split(None, 1)[1].lower() 
      except: 
         return await message.reply("**πΈπ½π²πΎπΌπΏπ»π΄ππ΄ π²πΎπΌπΌπ°π½π³...**")
      
      m = await message.reply("**ππ΄πππΈπ½πΆ.../**")

      if args in mode_on:
          FILTER_MODE[str(message.chat.id)] = "True" 
          await m.edit("**π°πππΎπ΅πΈπ»ππ΄π π΄π½π°π±π»π΄π³**")
      
      elif args in mode_of:
          FILTER_MODE[str(message.chat.id)] = "False"
          await m.edit("**π°πππΎπ΅πΈπ»ππ΄π π³πΈππ°π±π»π΄π³**")
      else:
          await m.edit("πππ΄ :- /autofilter on πΎπ /autofilter off")

@Client.on_message(filters.group & filters.text & filters.incoming)
async def give_filter(client,message):
    group_id = message.chat.id
    name = message.text

    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await message.reply_text(reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await message.reply_text(
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button)
                            )
                    elif btn == "[]":
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or ""
                        )
                    else:
                        button = eval(btn) 
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button)
                        )
                except Exception as e:
                    print(e)
                break 

    else:
        if FILTER_MODE.get(str(message.chat.id)) == "False":
            return
        else:
            await auto_filter(client, message)

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    ad_user = query.from_user.id
    if int(ad_user) in ADMINS:
        pass
    elif int(req) not in [query.from_user.id, 0]:
        return await query.answer(
            "All right, but this is not yours.;\nNice Try! But, This Was Not Your Request, Request Yourself;",
            show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer("You are using one of my old messages, please send the request again.", show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    settings = await get_settings(query.message.chat.id)
    if settings['button']:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"π [{get_size(file.file_size)}] β§ {file.file_name}", callback_data=f'files#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}", callback_data=f'files#{file.file_id}'
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'files_#{file.file_id}',
                ),
            ]
            for file in files
        ]

    btn.insert(0,
        [
            InlineKeyboardButton(f"π? {search}", "dupe"),
            InlineKeyboardButton(f"ποΈ Files: {len(files)}", "dupe")
        ]
    )

    if 0 < offset <= 10:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 10
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("βͺ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
             InlineKeyboardButton(text=f"Check PM!", url=f"https://t.me/{temp.U_NAME}"),
             InlineKeyboardButton(f"π {round(int(offset) / 10) + 1} / {round(total / 10)}",
                                  callback_data="pages")]
        )
    elif off_set is None:
        btn.append(
            [InlineKeyboardButton(f"π {round(int(offset) / 10) + 1} / {round(total / 10)}", callback_data="pages"),
             InlineKeyboardButton(text=f"Check PM!", url=f"https://t.me/{temp.U_NAME}"),
             InlineKeyboardButton("NEXT β©", callback_data=f"next_{req}_{key}_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton("βͺ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"π {round(int(offset) / 10) + 1} / {round(total / 10)}", callback_data="pages"),
                InlineKeyboardButton("NEXT β©", callback_data=f"next_{req}_{key}_{n_offset}")]
        )
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()

@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    ad_user = query.from_user.id
    if int(ad_user) in ADMINS:
        pass
    elif int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("βͺ ππΌππΎπ π λΈμ", show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message.message_id)
    if not movies:
        return await query.answer("You are clicking on an old button which is expired.", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('Checking for Movie in database...')
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
        if files:
            k = (movie, files, offset, total_results)
            await auto_filter(bot, query, k)
        else:
            k = await query.message.edit('This Movie Not Found In DataBase')
            await asyncio.sleep(10)
            await k.delete()


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == "private":
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                    return await query.answer('βͺ ππΌππΎπ π λΈμ')
            else:
                await query.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )
                return await query.answer('βͺ ππΌππΎπ π λΈμ')

        elif chat_type in ["group", "supergroup"]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return await query.answer('βͺ ππΌππΎπ π λΈμ')

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == "creator") or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == "private":
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in ["group", "supergroup"]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == "creator") or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("That's not for you!!", show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Group Name : **{title}**\nGroup ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode="md"
        )
        return await query.answer('βͺ ππΌππΎπ π λΈμ')
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Connected to **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text('Some error occurred!!', parse_mode="md")
        return await query.answer('βͺ ππΌππΎπ π λΈμ')
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode="md"
            )
        return await query.answer('βͺ ππΌππΎπ π λΈμ')
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode="md"
            )
        return await query.answer('βͺ ππΌππΎπ π λΈμ')
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return await query.answer('βͺ ππΌππΎπ π λΈμ')
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    if query.data.startswith("file"):
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        user = query.message.reply_to_message.from_user.id
        ad_user = query.from_user.id
        if int(ad_user) in ADMINS:
            pass
        elif int(user) != 0 and query.from_user.id != int(user):
            return await query.answer(
                "All right, but this is not yours.;\nNice Try! But, This Was Not Your Request, Request Yourself;",
                show_alert=True)

        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"
        buttons = [
            [
                InlineKeyboardButton('π° α΄Κα΄Ι΄Ι΄α΄Κ', url='https://t.me/+CeY_RGCtK1g0ZWQ9'),
                InlineKeyboardButton('π± α΄Κα΄Ι΄Ι΄α΄Κ', url='https://t.me/kerala_rockers')
            ]
            ]

        try:
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            elif settings['botpm']:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            else:
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    protect_content=True if ident == "filep" else False 
                )
                await query.answer('Check PM, I have sent files in pm', show_alert=True)
        except UserIsBlocked:
            await query.answer('Unblock the bot mahn !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
        except Exception as e:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
    elif query.data.startswith("checksub"):
        if AUTH_CHANNEL and not await is_subscribed(client, query):
            await query.answer("I Like Your Smartness, But Don't Be Oversmart π", show_alert=True)
            return
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        if f_caption is None:
            f_caption = f"{title}"
        buttons = [
            [
                InlineKeyboardButton('π° α΄Κα΄Ι΄Ι΄α΄Κ', url='https://t.me/+CeY_RGCtK1g0ZWQ9'),
                InlineKeyboardButton('π± α΄Κα΄Ι΄Ι΄α΄Κ', url='https://t.me/kerala_rockers')
            ]
            ]
        await query.answer()
        await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption,
            reply_markup=InlineKeyboardMarkup(buttons),
            protect_content=True if ident == 'checksubp' else False
        )
    elif query.data == "pages":
        await query.answer()
    elif query.data == "start":
        buttons =[[
            InlineKeyboardButton('β α΄α΄α΄ α΄α΄ α΄α΄ Κα΄α΄Κ Ι’Κα΄α΄α΄s β', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ],[
            InlineKeyboardButton('π sα΄α΄Κα΄Κ', switch_inline_query_current_chat=''),
            InlineKeyboardButton('βοΈ Κα΄Κα΄', callback_data='help')
            ],[
            InlineKeyboardButton('π α΄Κα΄α΄α΄', callback_data='about'),
            InlineKeyboardButton('π α΄Κα΄sα΄', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
        await query.answer('βͺ ππΌππΎπ π λΈμ')
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('α΄α΄α΄ΙͺΙ΄', callback_data='admin'),
            InlineKeyboardButton('α΄α΄Ι΄Ι΄α΄α΄α΄', callback_data='coct'),
            InlineKeyboardButton('κ°ΙͺΚα΄α΄Κs', callback_data='auto_manual')
            ],[
            InlineKeyboardButton('α΄κ°α΄', callback_data='afk'),
            InlineKeyboardButton('ΙͺΙ΄κ°α΄', callback_data='info'),
            InlineKeyboardButton('α΄α΄sα΄α΄', callback_data='paste')
            ],[
            InlineKeyboardButton('α΄α΄ΚΙ’α΄', callback_data='purge'),
            InlineKeyboardButton('Κα΄Ι΄s', callback_data='restric'),
            InlineKeyboardButton('Ιͺα΄α΄Κ', callback_data='search')
            ],[
            InlineKeyboardButton('α΄α΄α΄Ιͺα΄-Κα΄α΄α΄', callback_data='abook'),
            InlineKeyboardButton('α΄ΙͺΙ΄', callback_data='pin'),
            InlineKeyboardButton('Ι’α΄α΄α΄s', callback_data='memes')
            ],[
            InlineKeyboardButton('Β«Κα΄α΄α΄', callback_data='start'),
            InlineKeyboardButton('Ι΄α΄xα΄Β»', callback_data='hacker')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.HELP_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "hacker":
        buttons = [[
            InlineKeyboardButton('α΄Ι’Κα΄α΄Κ', callback_data='tgraph'),
            InlineKeyboardButton('sα΄Ιͺα΄α΄α΄Κ', callback_data='sticker'),
            InlineKeyboardButton('α΄α΄ΚΚα΄Ι΄α΄', callback_data='torrent')
            ],[
            InlineKeyboardButton('α΄α΄Κα΄Ι΄α΄', callback_data='corona'),
            InlineKeyboardButton('Κα΄α΄α΄Κα΄s', callback_data='report'),
            InlineKeyboardButton('κ°ΙͺΚα΄-sα΄α΄Κα΄', callback_data='addfle')
            ],[
            InlineKeyboardButton('α΄ΚΚ sΚα΄Κα΄', callback_data='shortner'),
            InlineKeyboardButton('α΄’α΄α΄ΚΙͺα΄s', callback_data='zombies'),
            InlineKeyboardButton('α΄α΄-sα΄α΄α΄α΄Κ', callback_data='tts')
            ],[
            InlineKeyboardButton('Ι’α΄Κα΄Ι΄s', callback_data='gtrans'),
            InlineKeyboardButton('α΄sα΄Ι΄', callback_data='json'),
            InlineKeyboardButton('sΚα΄Κα΄-α΄α΄xα΄', callback_data='sharetext')
            ],[
            InlineKeyboardButton('Β«Κα΄α΄α΄', callback_data='help'),
            InlineKeyboardButton('Ι΄α΄xα΄Β»', callback_data='hellp')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.HACKER_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "hellp":
        buttons = [[
            InlineKeyboardButton('Κα΄α΄α΄s', callback_data='lock'),
            InlineKeyboardButton('Κα΄α΄-sα΄α΄α΄α΄s', callback_data='restatus'),
            InlineKeyboardButton('α΄α΄ΚΚα΄Ι΄', callback_data='carbon')
            ],[
            InlineKeyboardButton('Κα΄Ι’α΄', callback_data='logo'),
            InlineKeyboardButton('α΄α΄α΄Ι΄α΄ΚΚ', callback_data='country'),
            InlineKeyboardButton('α΄α΄xα΄-Ιͺα΄Ι’', callback_data='img')
            ],[
            InlineKeyboardButton('κ°α΄Ι΄α΄s', callback_data='fonts'),
            InlineKeyboardButton('sα΄Ι΄Ι’', callback_data='songs'),
            InlineKeyboardButton('Κα΄-α΄Κα΄α΄Κ', callback_data='ytthumb')
            ],[
            InlineKeyboardButton('α΄ Ιͺα΄α΄α΄', callback_data='video'),
            InlineKeyboardButton('Ιͺα΄-α΄α΄α΄Κα΄ss', callback_data='ipad'),
            InlineKeyboardButton('Ι’-α΄α΄ssα΄‘α΄Κα΄', callback_data='genpassword')
            ],[          
            InlineKeyboardButton('Β«Κα΄α΄α΄', callback_data='hacker'),
            InlineKeyboardButton('α΄Κα΄sα΄', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.HELLP_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "about":
        buttons= [[
            InlineKeyboardButton('π§βπ» α΄α΄α΄ α΄Κα΄α΄α΄Κ', url='https://t.me/Hacker_Jr'),
            InlineKeyboardButton('β€οΈ sα΄α΄Κα΄α΄', callback_data='code')
            ],[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='start'),
            InlineKeyboardButton('β»οΈ sα΄α΄α΄α΄s', callback_data='stats'),
            InlineKeyboardButton('π α΄Κα΄sα΄', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.ABOUT_TXT.format(temp.B_NAME),
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "downlod":    
        await query.message.edit(
            text="""<b>π§Ώ Title : K.G.F: Chapter 1 & 2
π Release : 13 Apr 2022
π Languages : Kannada, Hindi, Tamil, Malayalam, Telugu
β­ Ratings : 9.6 / 10.0
π­ Genres : Action, Crime, Drama, Thriller

βοΈ Note: This message will be Auto-deleted after 10 hours to avoid copyright issues.</b>""",
            reply_markup=InlineKeyboardMarkup(KGF_BUTTON)
        )
    elif query.data == "kgfdownlod":    
        await query.message.edit(
            text="""<b>π§Ώ Title : K.G.F: Chapter 1 & 2
π Release : 13 Apr 2022
π Languages : Kannada, Hindi, Tamil, Malayalam, Telugu
β­ Ratings : 9.6 / 10.0
π­ Genres : Action, Crime, Drama, Thriller

βοΈ Note: This message will be Auto-deleted after 10 hours to avoid copyright issues.</b>""",
            reply_markup=InlineKeyboardMarkup(KGF_D_BUTTON)
        )
    elif query.data == "smovies":    
        await query.message.edit(
            text="""<b>π§Ώ Title : K.G.F: Chapter 1 & 2
π Release : 13 Apr 2022
π Languages : Kannada, Hindi, Tamil, Malayalam, Telugu
β­ Ratings : 9.6 / 10.0
π­ Genres : Action, Crime, Drama, Thriller

βοΈ Note: This message will be Auto-deleted after 10 hours to avoid copyright issues.</b>""",
            reply_markup=InlineKeyboardMarkup(KGF2_BUTTON)
        )
    elif query.data == "ssmovies":
        await query.answer("Coming Soon π", show_alert=True)
    elif query.data == "code":
        await query.answer("ΰ΄¨ΰ΅ ΰ΄ΰ΄€ΰ΄Ύ..... ΰ΄ΰ΄¨ΰ΅ΰ΄¨ΰ΅ ΰ΄ͺΰ΅ΰ΄ΰ΅ΰ΄―ΰ΅ ΰ΄ΰ΄΅ΰ΅» Source Code ΰ΄ΰ΅ΰ΄―ΰ΅ΰ΄ΰ΅ΰ΄ΰ΅ ΰ΄΅ΰ΄¨ΰ΅ΰ΄¨ΰ΄Ώΰ΄°ΰ΄Ώΰ΄ΰ΅ΰ΄ΰ΅ΰ΄¨ΰ΅ΰ΄¨ΰ΅. ΰ΄¨ΰ΅ΰ΄ΰ΅ΰ΄ΰ΄Ώ ΰ΄ΰ΄°ΰ΅ΰ΄¨ΰ΅ΰ΄¨ΰ΅, ΰ΄ΰ΄ͺΰ΅ΰ΄ͺΰ΅ ΰ΄ΰ΄Ώΰ΄ΰ΅ΰ΄ΰ΅ΰ΄. π ΰ΄?ΰ΄Ύΰ΄?ΰ΄¨ΰ΅ΰ΄ΰ΅ ΰ΄ΰ΄¨ΰ΅ΰ΄¨ΰ΅ΰ΄ ΰ΄€ΰ΅ΰ΄¨ΰ΅ΰ΄¨ΰ΄²ΰ΅ΰ΄²ΰ΅ ΰ΄?ΰ΄ΰ΅ΰ΄ΰ΄³ΰ΅. π",show_alert=True)
    elif query.data == "torrent":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hacker'),
            InlineKeyboardButton('π α΄Κα΄sα΄', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.TORRENT_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "manualfilter":
        buttons = [[
            InlineKeyboardButton('Κα΄α΄α΄α΄Ι΄s', callback_data='button'),
            InlineKeyboardButton('FILLINGS', callback_data='fillings')
            ],[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='auto_manual'),
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.MANUALFILTER_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "button":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='manualfilter')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.BUTTON_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "songs":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hellp')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.SONG_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "ipad":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hellp')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.IPADD_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "ytthumb":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hellp')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.YTTHUMB_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "video":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hellp')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.VIDEO_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "genpassword":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hellp')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.PASSWORD_GEN_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "img":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hellp')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.IMG_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "restatus":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hellp')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.BOTSTATUS_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "lock":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hellp')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.LOCK_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "logo":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hellp')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.LOGO_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "carbon":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hellp')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.CARBON_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "fonts":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hellp')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.FONTS_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "country":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hellp')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.COUNTRY_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "autofilter":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='auto_manual')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.AUTOFILTER_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "auto_manual":
        buttons = [[
            InlineKeyboardButton('α΄α΄α΄α΄', callback_data='autofilter'),
            InlineKeyboardButton('α΄α΄Ι΄α΄α΄Κ', callback_data='manualfilter')
            ],[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='help'),
            InlineKeyboardButton('π α΄Κα΄sα΄', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.AUTO_MANUAL_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "coct":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.CONNECTION_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "afk":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.AFK_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "corona":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hacker')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.CORONA_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "sticker":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hacker')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.STICKER_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "paste":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='help'),
            InlineKeyboardButton('π α΄Κα΄sα΄', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.PASTE_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "report":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hacker')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.REPORT_TEXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "json":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hacker')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.JSON_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "tgraph":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hacker')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.TGRAPH_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "info":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.INFO_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "search":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.SEARCH_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "gtrans":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hacker'),
            InlineKeyboardButton('π§Ύ Κα΄Ι΄Ι’ α΄α΄α΄α΄s', url='https://cloud.google.com/translate/docs/languages')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.GTRANS_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "abook":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.ABOOK_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "addfle":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hacker')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.FILE_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "admin":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.ADMIN_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "zombies":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hacker')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.ZOMBIES_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "purge":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.PURGE_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "restric":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.RESTRIC_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "memes":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.MEMES_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "shortner":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hacker')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.URL_SHORTNER_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "tts":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hacker')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.TTS_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "pin":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.PIN_MESSAGE_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "music":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.MUSIC_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "genpassword":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.PASSWORD_GEN_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "sharetext":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.SHARE_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "fillings":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='manualfilter')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Script.FILLINGS_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='about'),
            InlineKeyboardButton('β»οΈ Κα΄κ°Κα΄sΚ', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=Script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "rfrsh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('π§βπ¦― Κα΄α΄α΄', callback_data='hacker'),
            InlineKeyboardButton('β»οΈ Κα΄κ°Κα΄sΚ', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=Script.STATUS_TXT.format(total, users, chats, monsize, free),
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
      )
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if str(grp_id) != str(grpid):
            await query.message.edit("Your Active Connection Has Been Changed. Go To /settings.")
            return await query.answer('βͺ ππΌππΎπ π λΈμ')

        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Filter Button',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Single' if settings["button"] else 'Double',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Bot PM', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('β Yes' if settings["botpm"] else 'β No',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('File Secure',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('β Yes' if settings["file_secure"] else 'β No',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('IMDB', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('β Yes' if settings["imdb"] else 'β No',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Spell Check',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('β Yes' if settings["spell_check"] else 'β No',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Welcome', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('β Yes' if settings["welcome"] else 'β No',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)
    elif query.data == 'tips':
        await query.answer("=> {title} Ask {runtime} with correct  are not released in OTTheatre Quality Availableπ€§\n=> For better results:\n\t\t\t\t\t\t- MovieName year\n\t\t\t\t\t\t- Eg: Kuruthi 2021", True)
    try: await query.answer('βͺ ππΌππΎπ π λΈμ')
    except: pass

async def auto_filter(client, msg, spoll=False):
    if not spoll:
        message = msg
        settings = await get_settings(message.chat.id)
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if 2 < len(message.text) < 100:
            search = message.text
            files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)
            if not files:
                if settings["spell_check"]:
                    return await advantage_spell_chok(msg)
                else:
                    return
        else:
            return
    else:
        settings = await get_settings(msg.message.chat.id)
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
    pre = 'filep' if settings['file_secure'] else 'file'
    if settings["button"]:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"π [{get_size(file.file_size)}] β§ {file.file_name}", callback_data=f'{pre}#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}",
                    callback_data=f'{pre}#{file.file_id}',
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'{pre}_#{file.file_id}',
                ),
            ]
            for file in files
        ]

    if offset != "":
        key = f"{message.chat.id}-{message.message_id}"
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        btn.append(
            [InlineKeyboardButton(text=f"π 1/{round(int(total_results) / 10)}", callback_data="pages"),
             InlineKeyboardButton(text="CHECK PM!", url=f"https://t.me/{temp.U_NAME}"),
             InlineKeyboardButton(text="NEXT β©", callback_data=f"next_{req}_{key}_{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="π 1/1", callback_data="pages"),
             InlineKeyboardButton(text="CHECK PM!", url=f"https://t.me/{temp.U_NAME}")]
        )

    btn.insert(0, [
        InlineKeyboardButton(f"π? {search}", "dupe"),
        InlineKeyboardButton(f"ποΈ Files: {total_results}", "dupe")
    ])
    reply_id = message.reply_to_message.message_id if message.reply_to_message else message.message_id
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap = TEMPLATE.format(
            query=search,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title=imdb['localized_title'],
            kind=imdb['kind'],
            imdb_id=imdb["imdb_id"],
            cast=imdb["cast"],
            runtime=imdb["runtime"],
            countries=imdb["countries"],
            certificates=imdb["certificates"],
            languages=imdb["languages"],
            director=imdb["director"],
            writer=imdb["writer"],
            producer=imdb["producer"],
            composer=imdb["composer"],
            cinematographer=imdb["cinematographer"],
            music_team=imdb["music_team"],
            distributors=imdb["distributors"],
            release_date=imdb['release_date'],
            year=imdb['year'],
            genres=imdb['genres'],
            poster=imdb['poster'],
            plot=imdb['plot'],
            rating=imdb['rating'],
            url=imdb['url'],
            **locals()
        )
    else:
        cap = f"<b>π?ββΙ΄α΄α΄Ιͺα΄α΄ :- Ιͺπ΅ Κα΄α΄ α΄α΄ Ι΄α΄α΄ sα΄α΄ α΄Κα΄ π΅ΙͺΚα΄π α΄π΅ α΄ΚΙͺπ α΄α΄α΄ Ιͺα΄ Κα΄α΄ α΄πα΄α΄α΄ π΅α΄Κ. Κα΄α΄α΄ α΄α΄ Ι΄α΄πα΄ α΄α΄Ι’α΄\n Β©οΈ α΄α΄α΄‘α΄Κα΄α΄ ΚΚ :{message.chat.title}</b>"
    if imdb and imdb.get('poster'):
        try:
            hehe = await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_to_message_id=reply_id, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(1000)
            await hehe.delete()
            await message.delete()
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            hmm = await message.reply_photo(photo=poster, caption=cap[:1024], reply_to_message_id=reply_id, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(1000)
            await hmm.delete()
            await message.delete()
        except Exception as e:
            logger.exception(e)
            fek = await message.reply_photo(photo="https://telegra.ph/file/a35355b224548e197f989.jpg", caption=cap, reply_to_message_id=reply_id, reply_markup=InlineKeyboardMarkup(btn))
            await asyncio.sleep(1000)
            await fek.delete()
            await msg.delete()
    else:
        fuk = await message.reply_photo(photo="https://telegra.ph/file/a35355b224548e197f989.jpg", caption=cap, reply_to_message_id=reply_id, reply_markup=InlineKeyboardMarkup(btn))
        await asyncio.sleep(1000)
        await fuk.delete()
        await msg.delete()
    if spoll:
        await msg.message.delete()


async def advantage_spell_chok(msg):
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", msg.text, flags=re.IGNORECASE)  # plis contribute some common words
    search = msg.text
    query = query.strip() + " movie"
    g_s = await search_gagala(query)
    g_s += await search_gagala(msg.text)
    gs_parsed = []
    if not g_s:
        k = await msg.reply("I couldn't find any movie in that name.")
        await asyncio.sleep(8)
        await k.delete()
        return
    regex = re.compile(r".*(imdb|wikipedia).*", re.IGNORECASE)  # look for imdb / wiki results
    gs = list(filter(regex.match, g_s))
    gs_parsed = [re.sub(
        r'\b(\-([a-zA-Z-\s])\-\simdb|(\-\s)?imdb|(\-\s)?wikipedia|\(|\)|\-|reviews|full|all|episode(s)?|film|movie|series)',
        '', i, flags=re.IGNORECASE) for i in gs]
    if not gs_parsed:
        reg = re.compile(r"watch(\s[a-zA-Z0-9_\s\-\(\)]*)*\|.*",
                         re.IGNORECASE)  # match something like Watch Niram | Amazon Prime
        for mv in g_s:
            match = reg.match(mv)
            if match:
                gs_parsed.append(match.group(1))
    user = msg.from_user.id if msg.from_user else 0
    movielist = []
    gs_parsed = list(dict.fromkeys(gs_parsed))  # removing duplicates https://stackoverflow.com/a/7961425
    if len(gs_parsed) > 3:
        gs_parsed = gs_parsed[:3]
    if gs_parsed:
        for mov in gs_parsed:
            imdb_s = await get_poster(mov.strip(), bulk=True)  # searching each keyword in imdb
            if imdb_s:
                movielist += [movie.get('title') for movie in imdb_s]
    movielist += [(re.sub(r'(\-|\(|\)|_)', '', i, flags=re.IGNORECASE)).strip() for i in gs_parsed]
    movielist = list(dict.fromkeys(movielist))  # removing duplicates
    if not movielist:
        button = InlineKeyboardMarkup(
        [[
           InlineKeyboardButton("β Google β", url=f"https://www.google.com/search?q={search}")
        ],
        [
           InlineKeyboardButton("β­οΈ IMDb", url=f"https://www.imdb.com/find?q={search}"),
           InlineKeyboardButton("Wikipedia β­οΈ", url=f"https://en.m.wikipedia.org/w/index.php?search={search}")
        ]])
        k = await msg.reply(f"Hey, Your word <b>{search}</b> is No Movie/Series Related to the Given Word Was Found π₯Ί\n\n<s>Please Go to Google and Confirm the Correct Spelling π₯Ίπ</s>", reply_markup=button)
        await asyncio.sleep(60)
        await k.delete()
        return
    SPELL_CHECK[msg.message_id] = movielist
    btn = [[
        InlineKeyboardButton(
            text=movie.strip(),
            callback_data=f"spolling#{user}#{k}",
        )
    ] for k, movie in enumerate(movielist)]
    btn.append([InlineKeyboardButton(text="Close", callback_data=f'spolling#{user}#close_spellcheck')])
    m = await msg.reply("I couldn't find anything related to that\nDid you mean any one of these?",
                    reply_markup=InlineKeyboardMarkup(btn))
    await asyncio.sleep(20)
    await m.delete()


async def manual_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.message_id if message.reply_to_message else message.message_id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await message.reply_text(
                             reply_text.format(
                                 first = message.from_user.first_name,
                                 last = message.from_user.last_name,
                                 username = None if not message.from_user.username else '@' + message.from_user.username,
                                 mention = message.from_user.mention,
                                 id = message.from_user.id,
                                 dcid = message.from_user.dc_id,
                                 chatname = message.chat.title,
                                 query = name
                             ),
                             group_id,
                             disable_web_page_preview=True,
                             reply_to_message_id=reply_id
                            )
                        else:
                            button = eval(btn)
                            await message.reply_text(
                                reply_text.format(
                                    first = message.from_user.first_name,
                                    last = message.from_user.last_name,
                                    username = None if not message.from_user.username else '@' + message.from_user.username,
                                    mention = message.from_user.mention,
                                    id = message.from_user.id,
                                    dcid = message.from_user.dc_id,
                                    chatname = message.chat.title,
                                    query = name
                                ),
                                group_id,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id = reply_id
                            )
                    elif btn == "[]":
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text.format(
                                first = message.from_user.first_name,
                                last = message.from_user.last_name,
                                username = None if not message.from_user.username else '@' + message.from_user.username,
                                mention = message.from_user.mention,
                                id = message.from_user.id,
                                dcid = message.from_user.dc_id,
                                chatname = message.chat.title,
                                query = name
                            ) or "",
                            reply_to_message_id = reply_id
                        )
                    else:
                        button = eval(btn) 
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text.format(
                                first=message.from_user.first_name,
                                last=message.from_user.last_name,
                                username = None if not message.from_user.username else '@' + message.from_user.username,
                                mention = message.from_user.mention,
                                id=message.from_user.id,
                                dcid = message.from_user.dc_id,
                                chatname = message.chat.title,
                                query = name
                            ) or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id = reply_id
                        )
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False
