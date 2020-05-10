# Copyright © 2020 Roman Kuskov. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""@TimeToEatBot Telegram bot implementation."""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime

import logging
logging.basicConfig(format='[%(asctime)s] %(name)s %(levelname)s: %(message)s', level=logging.INFO)
LOGGER = logging.getLogger('TimeToEatBot')

TGBOT_TOKEN = '967774018:AAEy8obt8JfEJVcHNcJhqnin9P5S3YAjkSM'


def parse_time(time_str):
    """Parses time from input string expected to be in format 'HH:MM' or 'HH-MM'.
       Returns struct_time object or raises ValueError exception in case of bad input string."""

    split_symbol = ':'
    if time_str.find('-') != -1:
        split_symbol = '-'

    return datetime.strptime(time_str, f'%H{split_symbol}%M')


def on_start_command(update, context):
    welcome_text = "Введите команду /start и время, в которое вы обычно идёте обедать, например:\n  /start 13:30 14:10"

    if len(context.args) != 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_text)
        return

    try:
        start_time = parse_time(context.args[0])
        end_time = parse_time(context.args[1])
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Ошибка: не удалось определить диапазон времени: "' + ' '.join(context.args) +
                                      '".\n' + welcome_text)
        return

    if end_time <= start_time:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Ошибка: время окончания диапазона должно быть больше времени его начала.\n" +
                                      welcome_text)
        return

    context.bot.send_message(chat_id=update.effective_chat.id, text=f'start time: {start_time.strftime("%H:%M")}; end '
                                                                    f'time: {end_time.strftime("%H:%M")}')


def on_unknown_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def on_any_text_message(update, context):
    LOGGER.info('got input message from chatId %d, username \'%s\': "%s"',
                update.effective_chat.id, update.message.from_user.username, update.message.text)


def run_bot():
    LOGGER.info('Starting @TimeToEatBot...')
    updater = Updater(token=TGBOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_command_handler = CommandHandler('start', on_start_command)
    unknown_command_handler = MessageHandler(Filters.command, on_unknown_command)
    any_text_message_handler = MessageHandler(Filters.text, on_any_text_message)

    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(unknown_command_handler)
    dispatcher.add_handler(any_text_message_handler)

    LOGGER.info('long polling started')
    updater.start_polling()

    # stop bot if Ctrl+C pressed
    updater.idle()


if __name__ == '__main__':
    run_bot()
