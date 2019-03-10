from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging

cookie_emoji = u'\U0001F36A'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GET_COOKIE, ASK = range(2)

def start(bot, update):
    update.message.reply_text(
        'Type /start to start')

    return ASK

def ask(bot, update):
    reply_keyboard = [['Yes', 'No']]

    update.message.reply_text(
        'Hi! Do you want cookies?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return GET_COOKIE

def give_cookie(bot, update):
    user = update.message.from_user
    logger.info("User %s wants cookie", user.first_name)
    update.message.reply_text('Take cookie ' + cookie_emoji)

    return ConversationHandler.END

def give_cookie_too(bot, update):
    user = update.message.from_user
    logger.info("User %s don't wants cookie", user.first_name)
    update.message.reply_text('It doesn\'t matter. Take cookie ' + cookie_emoji)

    return ConversationHandler.END

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    token = open("/Users/bffn/Documents/telegram_bot/bot_token","r").read()
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, start),
                      CommandHandler('start', ask)],

        states={
            ASK: [CommandHandler('start', ask)],

            GET_COOKIE: [RegexHandler('^(Yes)$', give_cookie),
                         RegexHandler('^(No)$', give_cookie_too)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()