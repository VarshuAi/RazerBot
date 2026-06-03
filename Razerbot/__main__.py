import importlib
import re
import time
from platform import python_version as y
from sys import argv

from pyrogram import __version__ as pyrover
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram import __version__ as telever
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown
from telethon import __version__ as tlhver

import Razerbot.modules.sql.users_sql as sql
from Razerbot import (
    ALLOW_EXCL,
    CERT_PATH,
    LOGGER,
    OWNER_ID,
    PORT,
    UPDATE_CHANNEL,
    BOT_USERNAME,
    BOT_NAME,
    START_IMG,
    TOKEN,
    URL,
    OWNER_USERNAME,
    WEBHOOK,
    SUPPORT_CHAT,
    dispatcher,
    StartTime,
    telethn,
    pbot,
    updater,
)
from Razerbot.modules import ALL_MODULES
from Razerbot.modules.helper_funcs.chat_status import is_user_admin
from Razerbot.modules.helper_funcs.misc import paginate_modules


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


PM_START_TEXT = """
Hᴇʟʟᴏ {}![ ]({})
───────────────────────
× I'ᴍ A Mɪɴɪᴍᴀʟʟʏ Tʜᴇᴍᴇᴅ Gʀᴏᴜᴘ Mᴀɴᴀɢᴇᴍᴇɴᴛ Bᴏᴛ
× I'ᴍ Vᴇʀʏ Fᴀꜱᴛ Aɴᴅ Eꜰꜰɪᴄɪᴇɴᴛ ᴀɴᴅ I ᴄᴏᴍᴇ ᴡɪᴛʜ Aᴡᴇꜱᴏᴍᴇ Fᴇᴀᴛᴜʀᴇꜱ!
───────────────────────
× Uᴘᴛɪᴍᴇ: `{}`
× `{}` Uꜱᴇʀ, Aᴄʀᴏꜱꜱ `{}` Cʜᴀᴛꜱ.
───────────────────────"""

buttons = [
    [
        InlineKeyboardButton(text="ᴄᴏᴍᴍᴀɴᴅ ʜᴇʟᴘ", callback_data="razer_"),
    ],
    [
        InlineKeyboardButton(text="ɪɴꜰᴏ", callback_data="about_"),
        InlineKeyboardButton(text="ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}"),
    ],
   [
        InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇs", url=f"tg://resolve?domain={UPDATE_CHANNEL}"),
        InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", url=f"tg://resolve?domain={SUPPORT_CHAT}"),
    ],
    [  
        InlineKeyboardButton(text="➕️ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕️", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"),
    ],   
]

RAZER_IMG = f"{START_IMG}"

HELP_STRINGS = f"""➲ /start : ꜱᴛᴀʀᴛꜱ ᴍᴇ | ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍᴇ ʏᴏᴜ'ᴠᴇ ᴀʟʀᴇᴀᴅʏ ᴅᴏɴᴇ ɪᴛ.
➲ /help  : ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ꜱᴇᴄᴛɪᴏɴ.
  ‣ ɪɴ ᴘᴍ : ᴡɪʟʟ ꜱᴇɴᴅ ʏᴏᴜ ʜᴇʟᴘ ꜰᴏʀ ᴀʟʟ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ᴍᴏᴅᴜʟᴇꜱ.
  ‣ ɪɴ ɢʀᴏᴜᴘ : ᴡɪʟʟ ʀᴇᴅɪʀᴇᴄᴛ ʏᴏᴜ ᴛᴏ ᴘᴍ, ᴡɪᴛʜ ᴀʟʟ ᴛʜᴀᴛ ʜᴇʟᴘ ᴍᴏᴅᴜʟᴇꜱ.
  
*ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ʜᴇʟᴘ ᴀʙᴏᴜᴛ sᴘᴇᴄɪꜰɪᴄ ᴍᴏᴅᴜʟᴇs*"""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("Razerbot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard,
    )


@run_async
def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split("_", 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id,
                    HELPABLE[mod].__help__,
                    InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="help_back")]]
                    ),
                )

            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match.group(1))

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match.group(1), update.effective_user.id, False)
                else:
                    send_settings(match.group(1), update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rᴜʟᴇs" in IMPORTED:
                IMPORTED["rᴜʟᴇs"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            update.effective_message.reply_text(
                PM_START_TEXT.format(
                    escape_markdown(first_name),
                    START_IMG,
                    escape_markdown(uptime),
                    sql.num_users(),
                    sql.num_chats()),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
            )
    else:
        first_name = update.effective_user.first_name
        update.effective_message.reply_photo(
                RAZER_IMG, caption="""Hᴇʟʟᴏ {} !
───────────────────
× I'ᴍ A Mɪɴɪᴍᴀʟʟʏ Tʜᴇᴍᴇᴅ Gʀᴏᴜᴘ Mᴀɴᴀɢᴇᴍᴇɴᴛ Bᴏᴛ
× I'ᴍ Vᴇʀʏ Fᴀꜱᴛ Aɴᴅ Mᴏʀᴇ Eꜰꜰɪᴄɪᴇɴᴛ I Pʀᴏᴠɪᴅᴇ Aᴡᴇꜱᴏᴍᴇ Fᴇᴀᴛᴜʀᴇꜱ!
───────────────────
× Uᴘᴛɪᴍᴇ: `{}`
× `{}` Uꜱᴇʀ, Aᴄʀᴏꜱꜱ `{}` Cʜᴀᴛꜱ.
───────────────────""".format(
                    escape_markdown(first_name),
                    escape_markdown(uptime),
                    sql.num_users(),
                    sql.num_chats()),
                reply_markup=InlineKeyboardMarkup(
                 [
                  [InlineKeyboardButton(text="ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}"), 
                   InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", url=f"tg://resolve?domain={SUPPORT_CHAT}")]
                 ]
              ),
                parse_mode=ParseMode.MARKDOWN,              
            )


def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    LOGGER.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    message = (
        "An exception was raised while handling an update\n"
        "<pre>update = {}</pre>\n\n"
        "<pre>{}</pre>"
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(tb),
    )

    if len(message) >= 4096:
        message = message[:4096]
    # Finally, send the message
    context.bot.send_message(chat_id=OWNER_ID, text=message, parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


@run_async
def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "*ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅs ꜰᴏʀ* *{}* :\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="• ʙᴀᴄᴋ •", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")
                ),
            )

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )

        context.bot.answer_callback_query(query.id)

    except BadRequest:
        pass


@run_async
def Razer_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "razer_":
        query.message.edit_text(
            text="""𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐡𝐞𝐥𝐩 𝐦𝐞𝐧𝐮. 
────────────────────────
Sᴇʟᴇᴄᴛ Aʟʟ Cᴏᴍᴍᴀɴᴅs Fᴏʀ Fᴜʟʟ Hᴇʟᴘ Oʀ Sᴇʟᴇᴄᴛ Cᴀᴛᴇɢᴏʀʏ Fᴏʀ Mᴏʀᴇ Hᴇʟᴘ Dᴏᴄᴜᴍᴇɴᴛᴀᴛɪᴏɴ Oɴ Sᴇʟᴇᴄᴛᴇᴅ Fɪᴇʟᴅs""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                     InlineKeyboardButton(text="➕ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ➕", callback_data="help_back"),
                    ],                           
                    [InlineKeyboardButton(text="ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ?", callback_data="razer_help")],
                    [InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="razer_back")],
                ]
            ),
        )
    elif query.data == "razer_back":
        first_name = update.effective_user.first_name
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
                PM_START_TEXT.format(
                    escape_markdown(first_name),
                    START_IMG,
                    escape_markdown(uptime),
                    sql.num_users(),
                    sql.num_chats()),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=False,
        )
    elif query.data == "razer_help":
        query.message.edit_text(
            text=f"""Nᴇᴡ Tᴏ {BOT_NAME}? Hᴇʀᴇ Is Tʜᴇ Qᴜɪᴄᴋ Sᴛᴀʀᴛ Gᴜɪᴅᴇ Wʜɪᴄʜ Wɪʟʟ Hᴇʟᴘ Yᴏᴜ Tᴏ Uɴᴅᴇʀsᴛᴀɴᴅ Wʜᴀᴛ Is {BOT_NAME} Aɴᴅ Hᴏᴡ Tᴏ Usᴇ Iᴛ.

Cʟɪᴄᴋ Bᴇʟᴏᴡ Bᴜᴛᴛᴏɴ Tᴏ Aᴅᴅ Bᴏᴛ Iɴ Yᴏᴜʀ Gʀᴏᴜᴘ. Bᴀsɪᴄ Tᴏᴜʀ Sᴛᴀʀᴛᴇᴅ Tᴏ Kɴᴏᴡ Aʙᴏᴜᴛ Hᴏᴡ Tᴏ Usᴇ Mᴇ""",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
              [[InlineKeyboardButton(text="➕️ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕️", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],       
                [InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="razer_"),
                 InlineKeyboardButton(text="⇛", callback_data="razer_helpa")]
              ]
            ),
        )
    elif query.data == "razer_helpa":
        query.message.edit_text(
            text=f"""Hᴇʏ, Wᴇʟᴄᴏᴍᴇ Tᴏ Cᴏɴғɪɢᴜʀᴀᴛɪᴏɴ Tᴜᴛᴏʀɪᴀʟ

Bᴇғᴏʀᴇ Wᴇ Gᴏ Fᴜʀᴛʜᴇʀ, I Nᴇᴇᴅ Aᴅᴍɪɴ Pᴇʀᴍɪssɪᴏɴs Iɴ Tʜɪs Cʜᴀᴛ Tᴏ Wᴏʀᴋ Pʀᴏᴘᴇʀʟʏ.
1. Cʟɪᴄᴋ Mᴀɴᴀɢᴇ Gʀᴏᴜᴘ.
2. Gᴏ Tᴏ Aᴅᴍɪɴɪsᴛʀᴀᴛᴏʀs Aɴᴅ Aᴅᴅ @{BOT_USERNAME} As Aᴅᴍɪɴ.
3. Gɪᴠᴇ Fᴜʟʟ Pᴇʀᴍɪssɪᴏɴs Mᴀᴋᴇ @{BOT_USERNAME} Fᴜʟʟʏ Usᴇғᴜʟ""",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
              [[InlineKeyboardButton(text="⇚", callback_data="razer_help"),
                InlineKeyboardButton(text="⇛", callback_data="razer_helpb")],               
              ]
            ),
        )
    elif query.data == "razer_helpb":
        query.message.edit_text(
            text=f"""Cᴏɴɢʀᴀᴛᴜʟᴀᴛɪᴏɴs, {BOT_NAME} Is Nᴏᴡ Rᴇᴀᴅʏ Tᴏ Mᴀɴᴀɢᴇ Yᴏᴜʀ Gʀᴏᴜᴘ

Hᴇʀᴇ Aʀᴇ Sᴏᴍᴇ Essᴇɴᴛɪᴀʟs Tᴏ Tʀʏ Oɴ {BOT_NAME}.

× Aᴅᴍɪɴ Tᴏᴏʟs
ʙᴀsɪᴄ ᴀᴅᴍɪɴ ᴛᴏᴏʟs ʜᴇʟᴘ ʏᴏᴜ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ ᴀɴᴅ ᴘᴏᴡᴇʀᴜᴘ ʏᴏᴜʀ ɢʀᴏᴜᴘ
ʏᴏᴜ ᴄᴀɴ ʙᴀɴ ᴍᴇᴍʙᴇʀs, ᴋɪᴄᴋ ᴍᴇᴍʙᴇʀs, ᴘʀᴏᴍᴏᴛᴇ sᴏᴍᴇᴏɴᴇ ᴀs ᴀᴅᴍɪɴ ᴛʜʀᴏᴜɢʜ ᴄᴏᴍᴍᴀɴᴅs ᴏғ ʙᴏᴛ

× Wᴇʟᴄᴏᴍᴇs
ʟᴇᴛs sᴇᴛ ᴀ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ ᴛᴏ ᴡᴇʟᴄᴏᴍᴇ ɴᴇᴡ ᴜsᴇʀs ᴄᴏᴍɪɴɢ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ
sᴇɴᴅ /setwelcome [ᴍᴇssᴀɢᴇ] ᴛᴏ sᴇᴛ ᴀ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ
ᴀʟsᴏ ʏᴏᴜ ᴄᴀɴ sᴛᴏᴘ ᴇɴᴛᴇʀɪɴɢ ʀᴏʙᴏᴛs ᴏʀ sᴘᴀᴍᴍᴇʀs ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ ʙʏ sᴇᴛᴛɪɴɢ ᴡᴇʟᴄᴏᴍᴇ ᴄᴀᴘᴛᴄʜᴀ

Rᴇғᴇʀ Hᴇʟᴘ Mᴇɴᴜ Tᴏ Sᴇᴇ Eᴠᴇʀʏᴛʜɪɴɢ Iɴ Dᴇᴛᴀɪʟ""",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
              [
                [InlineKeyboardButton(text="⇚", callback_data="razer_helpa"),
                 InlineKeyboardButton(text="⇛", callback_data="razer_helpc")]
                ]
            ),
        )
    elif query.data == "razer_helpc":
        query.message.edit_text(
            text=f"""× Fɪʟᴛᴇʀs
ғɪʟᴛᴇʀs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴀs ᴀᴜᴛᴏᴍᴀᴛᴇᴅ ʀᴇᴘʟɪᴇs/ʙᴀɴ/ᴅᴇʟᴇᴛᴇ ᴡʜᴇɴ sᴏᴍᴇᴏɴᴇ ᴜsᴇ ᴀ ᴡᴏʀᴅ ᴏʀ sᴇɴᴛᴇɴᴄᴇ
ғᴏʀ  ᴇxᴀᴍᴘʟᴇ  ɪғ  ɪ  ғɪʟᴛᴇʀ  ᴡᴏʀᴅ  'ʜᴇʟʟᴏ'  ᴀɴᴅ  sᴇᴛ  ʀᴇᴘʟʏ  ᴀs  'ʜɪ'
ʙᴏᴛ  ᴡɪʟʟ  ʀᴇᴘʟʏ  ᴀs  'ʜɪ'  ᴡʜᴇɴ  sᴏᴍᴇᴏɴᴇ  sᴀʏ  'ʜᴇʟʟᴏ'
ʏᴏᴜ  ᴄᴀɴ  ᴀᴅᴅ  ғɪʟᴛᴇʀs  ʙʏ  sᴇɴᴅɪɴɢ  /filter  ғɪʟᴛᴇʀ  ɴᴀᴍᴇ

× Aɪ CʜᴀᴛBᴏᴛ
ᴡᴀɴᴛ sᴏᴍᴇᴏɴᴇ ᴛᴏ ᴄʜᴀᴛ ɪɴ ɢʀᴏᴜᴘ?
{BOT_NAME} ʜᴀs ᴀɴ ɪɴᴛᴇʟʟɪɢᴇɴᴛ ᴄʜᴀᴛʙᴏᴛ ᴡɪᴛʜ ᴍᴜʟᴛɪʟᴀɴɢ sᴜᴘᴘᴏʀᴛ
ʟᴇᴛ's ᴛʀʏ ɪᴛ,
Sᴇɴᴅ /chatbot enable Aɴᴅ Rᴇᴘʟʏ Tᴏ Aɴʏ Oғ Mʏ Mᴇssᴀɢᴇs Tᴏ Sᴇᴇ Tʜᴇ Mᴀɢɪᴄ""",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
              [
                [InlineKeyboardButton(text="⇚", callback_data="razer_helpb"),
                 InlineKeyboardButton(text="⇛", callback_data="razer_helpd")]
                ]
            ),
        )
    elif query.data == "razer_helpd":
        query.message.edit_text(
            text="""× Sᴇᴛᴛɪɴɢ Uᴘ Nᴏᴛᴇs
ʏᴏᴜ ᴄᴀɴ sᴀᴠᴇ ᴍᴇssᴀɢᴇ/ᴍᴇᴅɪᴀ/ᴀᴜᴅɪᴏ ᴏʀ ᴀɴʏᴛʜɪɴɢ ᴀs ɴᴏᴛᴇs ᴜsɪɴɢ /notes
ᴛᴏ ɢᴇᴛ ᴀ ɴᴏᴛᴇ sɪᴍᴘʟʏ ᴜsᴇ # ᴀᴛ ᴛʜᴇ ʙᴇɢɪɴɴɪɴɢ ᴏғ ᴀ ᴡᴏʀᴅ
sᴇᴇ ᴛʜᴇ ɪᴍᴀɢᴇ.

× Sᴇᴛᴛɪɴɢ Uᴘ Nɪɢʜᴛᴍᴏᴅᴇ
ʏᴏᴜ ᴄᴀɴ sᴇᴛ ᴜᴘ ɴɪɢʜᴛᴍᴏᴅᴇ ᴜsɪɴɢ /nightmode ᴏɴ/ᴏғғ ᴄᴏᴍᴍᴀɴᴅ.

Nᴏᴛᴇ- ɴɪɢʜᴛ ᴍᴏᴅᴇ ᴄʜᴀᴛs ɢᴇᴛ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴄʟᴏsᴇᴅ ᴀᴛ 12ᴘᴍ(ɪsᴛ)
ᴀɴᴅ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴏᴘᴇɴɴᴇᴅ ᴀᴛ 6ᴀᴍ(ɪsᴛ) ᴛᴏ ᴘʀᴇᴠᴇɴᴛ ɴɪɢʜᴛ sᴘᴀᴍs.""",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
              [
                [InlineKeyboardButton(text="⇚", callback_data="razer_helpc"),
                 InlineKeyboardButton(text="⇛", callback_data="razer_helpe")]
                ]
            ),
        )
    elif query.data == "razer_term":
        query.message.edit_text(
            text=f"""✗ Tᴇʀᴍs Aɴᴅ Cᴏɴᴅɪᴛɪᴏɴs:

- ᴏɴʟʏ ʏᴏᴜʀ ꜰɪʀsᴛ ɴᴀᴍᴇ, ʟᴀsᴛ ɴᴀᴍᴇ (ɪꜰ ᴀɴʏ) ᴀɴᴅ ᴜsᴇʀɴᴀᴍᴇ (ɪꜰ ᴀɴʏ) ɪs sᴛᴏʀᴇᴅ ꜰᴏʀ ᴀ ᴄᴏɴᴠᴇɴɪᴇɴᴛ ᴄᴏᴍᴍᴜɴɪᴄᴀᴛɪᴏɴ!
- ɴᴏ ɢʀᴏᴜᴘ ɪᴅ ᴏʀ ɪᴛ's ᴍᴇssᴀɢᴇs ᴀʀᴇ sᴛᴏʀᴇᴅ, ᴡᴇ ʀᴇsᴘᴇᴄᴛ ᴇᴠᴇʀʏᴏɴᴇ's ᴘʀɪᴠᴀᴄʏ.
- ᴍᴇssᴀɢᴇs ʙᴇᴛᴡᴇᴇɴ ʙᴏᴛ ᴀɴᴅ ʏᴏᴜ ɪs ᴏɴʟʏ ɪɴꜰʀᴏɴᴛ ᴏꜰ ʏᴏᴜʀ ᴇʏᴇs ᴀɴᴅ ᴛʜᴇʀᴇ ɪs ɴᴏ ʙᴀᴄᴋᴜsᴇ ᴏꜰ ɪᴛ.
- ᴡᴀᴛᴄʜ ʏᴏᴜʀ ɢʀᴏᴜᴘ, ɪꜰ sᴏᴍᴇᴏɴᴇ ɪs sᴘᴀᴍᴍɪɴɢ ʏᴏᴜʀ ɢʀᴏᴜᴘ, ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜᴇ ʀᴇᴘᴏʀᴛ ꜰᴇᴀᴛᴜʀᴇ ᴏꜰ ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ᴄʟɪᴇɴᴛ.
- ᴅᴏ ɴᴏᴛ sᴘᴀᴍ ᴄᴏᴍᴍᴀɴᴅs, ʙᴜᴛᴛᴏɴs, ᴏʀ ᴀɴʏᴛʜɪɴɢ ɪɴ ʙᴏᴛ ᴘᴍ.

ɴᴏᴛᴇ: ᴛᴇʀᴍs ᴀɴᴅ ᴄᴏɴᴅɪᴛɪᴏɴs ᴍɪɢʜᴛ ᴄʜᴀɴɢᴇ ᴀɴʏᴛɪᴍᴇ""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
              [InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇs", url=f"tg://resolve?domain{UPDATE_CHANNEL}"),       
              InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", url=f"tg://resolve?domain{SUPPORT_CHAT}")],       
              [InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="about_")]]
            ),
        )
    elif query.data == "razer_helpe":
        query.message.edit_text(
            text="""× Sᴏ Nᴏᴡ Yᴏᴜ Aʀᴇ Aᴛ Tʜᴇ Eɴᴅ Oғ Bᴀsɪᴄ Tᴏᴜʀ. Bᴜᴛ Tʜɪs Is Nᴏᴛ Aʟʟ I Cᴀɴ Dᴏ.

Sᴇɴᴅ /help Iɴ Bᴏᴛ Pᴍ Tᴏ Aᴄᴄᴇss Hᴇʟᴘ Mᴇɴᴜ

Tʜᴇʀᴇ Aʀᴇ Mᴀɴʏ Hᴀɴᴅʏ Tᴏᴏʟs Tᴏ Tʀʏ Oᴜᴛ.  
Aɴᴅ Aʟsᴏ Iғ Yᴏᴜ Hᴀᴠᴇ Aɴʏ Sᴜɢɢᴇssɪᴏɴs Aʙᴏᴜᴛ Mᴇ, Dᴏɴ'ᴛ Fᴏʀɢᴇᴛ Tᴏ Tᴇʟʟ Tʜᴇᴍ Tᴏ Dᴇᴠs

Aɢᴀɪɴ Tʜᴀɴᴋs Fᴏʀ Usɪɴɢ Mᴇ

× Bʏ Usɪɴɢ Tʜɪꜱ Bᴏᴛ Yᴏᴜ Aʀᴇ Aɢʀᴇᴇᴅ Tᴏ Oᴜʀ Tᴇʀᴍs & Cᴏɴᴅɪᴛɪᴏɴs""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="➕ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ➕", callback_data="help_back")],
                [InlineKeyboardButton(text="⇚", callback_data="razer_helpd"),
                InlineKeyboardButton(text="ᴍᴀɪɴ ᴍᴇɴᴜ", callback_data="razer_")]]
            ),
        )
    elif query.data == "razer_about":
        query.message.edit_text(
            text=f"""ꝛᴧᴢᴇʀ ɪs ᴏɴʟɪɴᴇ sɪɴᴄᴇ ᴀᴜɢᴜsᴛ 2022 ᴀɴᴅ ɪᴛ's ʙᴇɪɴɢ ᴄᴏɴsᴛᴀɴᴛʟʏ ᴜᴘᴅᴀᴛᴇᴅ!
            

⌁ @WH0907, ʙᴏᴛ ᴄʀᴇᴀᴛᴏʀ ᴀɴᴅ ᴍᴀɪɴ ᴅᴇᴠᴇʟᴏᴘᴇʀ.

            
× sᴜᴘᴘᴏʀᴛ
            
• [ᴄʟɪᴄᴋ ʜᴇʀᴇ](https://t.me/{SUPPORT_CHAT}) ᴛᴏ ɢᴏ ᴛᴏ ᴛʜᴇ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ.
            
• ɪ ᴛʜᴀɴᴋ ᴀʟʟ ᴛʜᴇ ɢʀᴏᴜᴘs ᴡʜᴏ ʀᴇʟʏ ᴏɴ ᴍʏ ʙᴏᴛ ꜰᴏʀ sᴇʀᴠɪᴄᴇ, ɪ ʜᴏᴘᴇ ʏᴏᴜ ᴡɪʟʟ ᴀʟᴡᴀʏs ʟɪᴋᴇ ɪᴛ. ɪ ᴀᴍ ᴄᴏɴsᴛᴀɴᴛʟʏ ᴡᴏʀᴋɪɴɢ ᴛᴏ ɪᴍᴘʀᴏᴠᴇ ɪᴛ!""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="about_")]]
            ),
        )
    elif query.data == "razer_support":
        query.message.edit_text(
            text="ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ʜᴇʟᴩ ᴀɴᴅ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍᴇ."
            f"\n\nɪғ ʏᴏᴜ ғᴏᴜɴᴅ ᴀɴʏ ʙᴜɢ ɪɴ {BOT_NAME} ᴏʀ ɪғ ʏᴏᴜ ᴡᴀɴɴᴀ ɢɪᴠᴇ ғᴇᴇᴅʙᴀᴄᴋ ᴀʙᴏᴜᴛ ᴛʜᴇ {BOT_NAME}, ᴩʟᴇᴀsᴇ ʀᴇᴩᴏʀᴛ ɪᴛ ᴀᴛ sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ.",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="sᴜᴩᴩᴏʀᴛ", url=f"tg://resolve?domain={SUPPORT_CHAT}"
                        ),
                        InlineKeyboardButton(
                            text="ᴜᴩᴅᴀᴛᴇs", url=f"tg://resolve?domain={SUPPORT_CHAT}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="ᴅᴇᴠᴇʟᴏᴩᴇʀ", url=f"tg://user?id=1413518510"
                        ),
                        InlineKeyboardButton(
                            text="ɢɪᴛʜᴜʙ",
                            url="https://github.com/LinuxGuy312",
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="• ʙᴀᴄᴋ •", callback_data="about_"),
                    ],
                ]
            ),
        )

@run_async
def razer_callback_query(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "about_":
        query.message.edit_text(
            text="ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ᴍᴇ.",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
               [
                 [
                     InlineKeyboardButton(text="ᴀʙᴏᴜᴛ", callback_data="razer_about"),
                     InlineKeyboardButton(text="sᴏᴜʀᴄᴇ", callback_data="source_"),
                 ],
                  [  
                     InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", callback_data="razer_support"),
                     InlineKeyboardButton(text="ᴏᴡɴᴇʀ", url=f"https://t.me/{OWNER_USERNAME}"),
                  ],
                 [
                     InlineKeyboardButton(text="ᴛᴇʀᴍs ᴀɴᴅ ᴄᴏɴᴅɪᴛɪᴏɴs", callback_data="razer_term"),
                 ],
                 [
                     InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="about_back"),
                 ]    
               ]
            ),
        )
    elif query.data == "about_back":
        first_name = update.effective_user.first_name
        uptime = get_readable_time((time.time() - StartTime))
        query.message.edit_text(
                PM_START_TEXT.format(
                    escape_markdown(first_name),
                    START_IMG,
                    escape_markdown(uptime),
                    sql.num_users(),
                    sql.num_chats()),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=False,
        )

@run_async
def Source_about_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "source_":
        query.message.edit_text(
            text=f"""
ʜᴇʏ,
ᴛʜɪs ɪs {BOT_NAME},
ᴀɴ ᴏᴩᴇɴ sᴏᴜʀᴄᴇ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴩ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ.

ᴡʀɪᴛᴛᴇɴ ɪɴ ᴩʏᴛʜᴏɴ ᴡɪᴛʜ ᴛʜᴇ ʜᴇʟᴩ ᴏғ : [ᴛᴇʟᴇᴛʜᴏɴ](https://github.com/LonamiWebs/Telethon)
[ᴩʏʀᴏɢʀᴀᴍ](https://github.com/pyrogram/pyrogram)
[ᴩʏᴛʜᴏɴ-ᴛᴇʟᴇɢʀᴀᴍ-ʙᴏᴛ](https://github.com/python-telegram-bot/python-telegram-bot)
ᴀɴᴅ ᴜsɪɴɢ [sǫʟᴀʟᴄʜᴇᴍʏ](https://www.sqlalchemy.org) ᴀɴᴅ [ᴍᴏɴɢᴏ](https://cloud.mongodb.com) ᴀs ᴅᴀᴛᴀʙᴀsᴇ.


*ʜᴇʀᴇ ɪs ᴍʏ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ :* [ɢɪᴛʜᴜʙ](https://github.com/LinuxGuy312/RazerBot)


{BOT_NAME} ɪs ʟɪᴄᴇɴsᴇᴅ ᴜɴᴅᴇʀ ᴛʜᴇ [ᴍɪᴛ ʟɪᴄᴇɴsᴇ](https://github.com/LinuxGuy312/RazerBot/blob/master/LICENSE).
© 2022 - 2023 @{SUPPORT_CHAT}, ᴀʟʟ ʀɪɢʜᴛs ʀᴇsᴇʀᴠᴇᴅ.
""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="• ʙᴀᴄᴋ •", callback_data="about_")]]
            ),
        )


@run_async
def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴍ ᴛᴏ ɢᴇᴛ ʜᴇʟᴘ ᴏꜰ {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="ʜᴇʟᴘ",
                                url="https://t.me/{}?start=ghelp_{}".format(
                                    context.bot.username, module
                                ),
                            )
                        ]
                    ]
                ),
            )
            return
        update.effective_message.reply_text(
            "» ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ғᴏʀ ɢᴇᴛᴛɪɴɢ ʜᴇʟᴩ.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ᴏᴩᴇɴ ɪɴ ᴩʀɪᴠᴀᴛᴇ",
                            url="https://t.me/{}?start=help".format(
                                context.bot.username
                            ),
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="ᴏᴩᴇɴ ʜᴇʀᴇ",
                            callback_data="help_back",
                        )
                    ],
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "ʜᴇʀᴇ ɪs ᴛʜᴇ ᴀᴠᴀɪʟᴀʙʟᴇ ʜᴇʟᴘ ꜰᴏʀ ᴛʜᴇ {} ᴍᴏᴅᴜʟᴇ:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="• ʙᴀᴄᴋ •", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join(
                "*{}*:\n{}".format(mod.__mod_name__, mod.__user_settings__(user_id))
                for mod in USER_SETTINGS.values()
            )
            dispatcher.bot.send_message(
                user_id,
                "ᴛʜᴇsᴇ ᴀʀᴇ ʏᴏᴜʀ ᴄᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢs:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN,
            )

        else:
            dispatcher.bot.send_message(
                user_id,
                "sᴇᴇᴍs ʟɪᴋᴇ ᴛʜᴇʀᴇ ᴀʀᴇɴ'ᴛ ᴀɴʏ ᴜsᴇʀ sᴘᴇᴄɪꜰɪᴄ sᴇᴛᴛɪɴɢs ᴀᴠᴀɪʟᴀʙʟᴇ :(",
                parse_mode=ParseMode.MARKDOWN,
            )

    else:
        if CHAT_SETTINGS:
            chat_name = dispatcher.bot.getChat(chat_id).title
            dispatcher.bot.send_message(
                user_id,
                text="ᴡʜɪᴄʜ ᴍᴏᴅᴜʟᴇ ᴡᴏᴜʟᴅ ʏᴏᴜ ʟɪᴋᴇ ᴛᴏ ᴄʜᴇᴄᴋ {}'s sᴇᴛᴛɪɴɢs ꜰᴏʀ?".format(
                    chat_name
                ),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )
        else:
            dispatcher.bot.send_message(
                user_id,
                "sᴇᴇᴍs ʟɪᴋᴇ ᴛʜᴇʀᴇ ᴀʀᴇɴ'ᴛ ᴀɴʏ ᴄʜᴀᴛ sᴇᴛᴛɪɴɢs ᴀᴠᴀɪʟᴀʙʟᴇ :(\n"
                "sᴇɴᴅ ᴛʜɪs ɪɴ ᴀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ ʏᴏᴜ'ʀᴇ ᴀᴅᴍɪɴ ɪɴ ᴛᴏ ꜰɪɴᴅ ɪᴛs ᴄᴜʀʀᴇɴᴛ sᴇᴛᴛɪɴɢs!",
                parse_mode=ParseMode.MARKDOWN,
            )


@run_async
def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match.group(1)
            module = mod_match.group(2)
            chat = bot.get_chat(chat_id)
            text = "{} ʜᴀs ᴛʜᴇ ꜰᴏʟʟᴏᴡɪɴɢ sᴇᴛᴛɪɴɢs ꜰᴏʀ ᴛʜᴇ {} ᴍᴏᴅᴜʟᴇ:\n\n".format(
                escape_markdown(chat.title), CHAT_SETTINGS[module].__mod_name__
            ) + CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="⇚",
                                callback_data="stngs_back({})".format(chat_id),
                            )
                        ]
                    ]
                ),
            )

        elif prev_match:
            chat_id = prev_match.group(1)
            curr_page = int(prev_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "ʜɪ ᴛʜᴇʀᴇ! ᴛʜᴇʀᴇ ᴀʀᴇ ǫᴜɪᴛᴇ ᴀ ꜰᴇᴡ sᴇᴛᴛɪɴɢs ꜰᴏʀ {} - ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘɪᴄᴋ ᴡʜᴀᴛ "
                "ʏᴏᴜ'ʀᴇ ɪɴᴛᴇʀᴇsᴛᴇᴅ ɪɴ.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif next_match:
            chat_id = next_match.group(1)
            next_page = int(next_match.group(2))
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                "ʜɪ ᴛʜᴇʀᴇ! ᴛʜᴇʀᴇ ᴀʀᴇ ǫᴜɪᴛᴇ ᴀ ꜰᴇᴡ sᴇᴛᴛɪɴɢs ꜰᴏʀ {} - ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘɪᴄᴋ ᴡʜᴀᴛ "
                "ʏᴏᴜ'ʀᴇ ɪɴᴛᴇʀᴇsᴛᴇᴅ ɪɴ.".format(chat.title),
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )

        elif back_match:
            chat_id = back_match.group(1)
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text="ʜɪ ᴛʜᴇʀᴇ! ᴛʜᴇʀᴇ ᴀʀᴇ ǫᴜɪᴛᴇ ᴀ ꜰᴇᴡ sᴇᴛᴛɪɴɢs ꜰᴏʀ {} - ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ᴘɪᴄᴋ ᴡʜᴀᴛ "
                "ʏᴏᴜ'ʀᴇ ɪɴᴛᴇʀᴇsᴛᴇᴅ ɪɴ.".format(escape_markdown(chat.title)),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s", str(query.data))


@run_async
def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type != chat.PRIVATE:
        if is_user_admin(chat, user.id):
            text = "ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ɢᴇᴛ ᴛʜɪs ᴄʜᴀᴛ's sᴇᴛᴛɪɴɢs, ᴀs ᴡᴇʟʟ ᴀs ʏᴏᴜʀs."
            msg.reply_text(
                text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="sᴇᴛᴛɪɴɢs",
                                url="t.me/{}?start=stngs_{}".format(
                                    context.bot.username, chat.id
                                ),
                            )
                        ]
                    ]
                ),
            )
        else:
            text = "ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴇᴛᴛɪɴɢs."

    else:
        send_settings(chat.id, user.id, True)


def migrate_chats(update: Update, context: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def main():

    if SUPPORT_CHAT is not None and isinstance(SUPPORT_CHAT, str):
        try:
            dispatcher.bot.sendMessage(f"@{SUPPORT_CHAT}", "ꝛᴧᴢᴇʀ ᴜᴘᴅᴧᴛᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ ✅")
        except Unauthorized:
            LOGGER.warning(
                "Bot isnt able to send message to support_chat, go and check!"
            )
        except BadRequest as e:
            LOGGER.warning(e.message)

    start_handler = CommandHandler("start", start)

    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_.*")

    settings_handler = CommandHandler("settings", get_settings)
    settings_callback_handler = CallbackQueryHandler(settings_button, pattern=r"stngs_")

    about_callback_handler = CallbackQueryHandler(
        Razer_about_callback, pattern=r"razer_"
    )
    source_callback_handler = CallbackQueryHandler(
        Source_about_callback, pattern=r"source_"
    )
    razer_callback_handler = CallbackQueryHandler(
        razer_callback_query, pattern=r"about_"
    )
    migrate_handler = MessageHandler(Filters.status_update.migrate, migrate_chats)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(razer_callback_handler)
    dispatcher.add_handler(source_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)

    dispatcher.add_error_handler(error_callback)

    LOGGER.info("Started Successfully")
    updater.start_polling(timeout=15, read_latency=4, clean=True)

    if len(argv) not in (1, 3, 4):
        telethn.disconnect()
    else:
        telethn.run_until_disconnected()

    updater.idle()


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    try:
        telethn.start(bot_token=TOKEN)
    except FloodWaitError as e:
        LOGGER.info(f"[FloodWaitError] Have to wait {e.seconds} seconds due to FloodWait.")
        time.sleep(e.seconds)
        telethn.start(bot_token=TOKEN)
    pbot.start()
    main()