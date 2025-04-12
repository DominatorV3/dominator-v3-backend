import os
from src.wallet_utils import get_balance
import json
from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Bot,
)
from telegram.ext import (
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
)

from panic_utils import set_panic_mode, is_panic_mode
from src.wallet_utils import get_balance

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")

bot = Bot(token=TELEGRAM_TOKEN)

# ✅ START → Affiche le bouton Menu DOMINATOR
def handle_start(update: Update, context: CallbackContext):
    keyboard = [["🔥🔥🔥 MENU DOMINATOR V3 🔥🔥🔥"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text("✅ DOMINATOR prêt à te servir !", reply_markup=reply_markup)

# ✅ PANIC / RESUME / STATUS
def handle_panic(update: Update, context: CallbackContext):
    set_panic_mode(True)
    update.message.reply_text("🛑 PANIC MODE activé.")

def handle_resume(update: Update, context: CallbackContext):
    set_panic_mode(False)
    update.message.reply_text("✅ Mode normal réactivé.")

def handle_status(update: Update, context: CallbackContext):
    status = "🛑 PANIC MODE ACTIVÉ" if is_panic_mode() else "✅ Mode normal"
    update.message.reply_text(f"📊 Status du bot : {status}")

# ✅ NOTIF DÉMARRAGE + CLAVIER
def notify_startup():
    try:
        keyboard = [["🔥🔥🔥 MENU DOMINATOR V3 🔥🔥🔥"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="🚀 Bot DOMINATOR V3 Activé 🚀", reply_markup=reply_markup)
    except Exception as e:
        print("Erreur notify_startup :", e)

# ✅ TX OK
def notify_tx_result(token, tx_hash, amount):
    try:
        message = f"✅ Transaction effectuée\n\nToken : {token}\nMontant : {amount} SOL\nHash : {tx_hash}"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        print("Erreur notify_tx_result :", e)

# ✅ LEADERBOARD
def send_leaderboard(context: CallbackContext):
    try:
        with open("DOMINATOR_V3_REPLIT/leaderboard.json", "r") as f:
            data = json.load(f)
        if not data:
            context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="🏆 Leaderboard vide.")
            return

        message = "🏆 TOP TOKENS\n"
        for i, (token, montant) in enumerate(data.items(), 1):
            message += f"{i}. {token} — {montant:.4f} SOL\n"

        context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

    except Exception as e:
        context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"Erreur leaderboard : {e}")

# ✅ GRAPHIQUE
def send_graphique(context: CallbackContext):
    try:
        with open("DOMINATOR_V3_REPLIT/graphique_trades.png", "rb") as photo:
            context.bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo)
    except Exception as e:
        context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"Erreur graphique : {e}")

# ✅ SOLDE
def send_solde(context: CallbackContext):
    try:
        solde = get_balance(WALLET_ADDRESS)
        if solde is None:
            context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="❌ Impossible de récupérer le solde.")
        else:
            context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"💰 Solde actuel : {solde:.4f} SOL")
    except Exception as e:
        context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"Erreur solde : {e}")

# ✅ MENU 3 COLONNES INLINE
def handle_menu_command(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("💰 Solde", callback_data="solde"),
            InlineKeyboardButton("📉 Graphique", callback_data="graphique"),
            InlineKeyboardButton("📈 Leaderboard", callback_data="leaderboard"),
        ],
        [
            InlineKeyboardButton("🔐 Whitelist", callback_data="whitelist"),
            InlineKeyboardButton("⛔️ Blacklist", callback_data="blacklist"),
            InlineKeyboardButton("🔁 Reload", callback_data="reload"),
        ],
        [
            InlineKeyboardButton("📛 Panic", callback_data="panic"),
            InlineKeyboardButton("✅ Resume", callback_data="resume"),
            InlineKeyboardButton("📊 Status", callback_data="status"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if hasattr(update, "message") and update.message:
        context.bot.send_message(chat_id=update.message.chat_id, text="🔥🔥🔥 MENU DOMINATOR V3 🔥🔥🔥", reply_markup=reply_markup)
    elif hasattr(update, "callback_query") and update.callback_query:
        update.callback_query.answer()
        update.callback_query.edit_message_text("🔥🔥🔥 MENU DOMINATOR V3 🔥🔥🔥", reply_markup=reply_markup)

# ✅ CALLBACK BOUTONS
def handle_menu_button(update: Update, context: CallbackContext):
    query = update.callback_query
    if query is None:
        return

    data = query.data
    query.answer()

    if data == "panic":
        set_panic_mode(True)
        query.edit_message_text("🛑 PANIC MODE activé.")
    elif data == "resume":
        set_panic_mode(False)
        query.edit_message_text("✅ Mode normal réactivé.")
    elif data == "status":
        status = "🛑 PANIC MODE ACTIVÉ" if is_panic_mode() else "✅ Mode normal"
        query.edit_message_text(f"📊 Status du bot : {status}")
    elif data == "leaderboard":
        send_leaderboard(context)
    elif data == "graphique":
        send_graphique(context)
    elif data == "solde":
        send_solde(context)
    elif data == "whitelist":
        context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="/whitelist")
    elif data == "blacklist":
        context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="/blacklist")
    elif data == "reload":
        context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="/reload")

# ✅ ENREGISTREMENT COMMANDES + SILENCE BOUTON PERMANENT
def register_commands(dispatcher):
    dispatcher.add_handler(CommandHandler("start", handle_start))
    dispatcher.add_handler(CommandHandler("menu", handle_menu_command))
    dispatcher.add_handler(CommandHandler("panic", handle_panic))
    dispatcher.add_handler(CommandHandler("resume", handle_resume))
    dispatcher.add_handler(CommandHandler("status", handle_status))
    dispatcher.add_handler(CommandHandler("reload", handle_menu_command))

    # ✅ Silence total du bouton permanent + menu propre
    dispatcher.add_handler(MessageHandler(
        Filters.regex("^🔥🔥🔥 MENU DOMINATOR V3 🔥🔥🔥$"),
        lambda update, context: (
            context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id),
            handle_menu_command(update, context)
        )
    ))

    dispatcher.add_handler(CallbackQueryHandler(handle_menu_button))
