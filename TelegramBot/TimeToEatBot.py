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

from collections import namedtuple
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import requests
import logging

logging.basicConfig(format='[%(asctime)s] %(name)s %(levelname)s: %(message)s', level=logging.INFO)
LOGGER = logging.getLogger('TimeToEatBot')

TGBOT_TOKEN = '967774018:AAEy8obt8JfEJVcHNcJhqnin9P5S3YAjkSM'
GOEAT_SERVER = 'http://127.0.0.1:8000'
ADD_TRACKING_TASK_ENDPOINT = GOEAT_SERVER + '/api/submit/'
KUKURUZA_CAM = 'https://lideo.tv/hamsternsk/streams/12620'

HELP_TEXT = "Введите команду /start и время, в которое вы обычно идёте обедать, например:\n/start 13:30 14:10"


def parse_time(time_str):
    """Parses time from input string expected to be in format 'HH:MM' or 'HH-MM'.
       Returns struct_time object or raises ValueError exception in case of bad input string."""

    split_symbol = ':'
    if time_str.find('-') != -1:
        split_symbol = '-'

    return datetime.strptime(time_str, f'%H{split_symbol}%M')


def on_start_command(update, context):
    LOGGER.info('got \'/start\' command from chatId %d, username \'%s\': "%s"',
                update.effective_chat.id, update.message.from_user.username, update.message.text)

    if len(context.args) != 2:
        context.bot.send_message(chat_id=update.effective_chat.id, text=HELP_TEXT)
        return

    try:
        start_time = parse_time(context.args[0])
        end_time = parse_time(context.args[1])
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Ошибка: не удалось определить диапазон времени: "' + ' '.join(context.args) +
                                      '".\n' + HELP_TEXT)
        return

    if end_time <= start_time:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Ошибка: время окончания диапазона должно быть больше времени его начала.\n" +
                                      HELP_TEXT)
        return

    data_to_send = {
        'tg_chat_id': update.effective_chat.id,
        'camera_url': KUKURUZA_CAM,
        'time_range_start': start_time.strftime("%H:%M"),
        'time_range_finish': end_time.strftime("%H:%M")
    }

    response = requests.post(ADD_TRACKING_TASK_ENDPOINT, data_to_send, timeout=5)

    # 200-299 range corresponds to HTTP success statuses
    is_success = 200 <= response.status_code <= 299

    if is_success:
        message = f'Успешно создано задание следить за камерой в период: ' \
                  f'{start_time.strftime("%H:%M")} - {end_time.strftime("%H:%M")}'
    else:
        message = 'Ошибка сервера: ' + response.status_code + ' ' + response.reason

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def on_help_command(update, context):
    LOGGER.info('got \'/help\' command from chatId %d, username \'%s\': "%s"',
                update.effective_chat.id, update.message.from_user.username, update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=HELP_TEXT)


def on_unknown_command(update, context):
    LOGGER.info('got unknown command from chatId %d, username \'%s\': "%s"',
                update.effective_chat.id, update.message.from_user.username, update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def on_any_text_message(update, context):
    LOGGER.info('got input message from chatId %d, username \'%s\': "%s"',
                update.effective_chat.id, update.message.from_user.username, update.message.text)


def run_bot():
    LOGGER.info('Starting @TimeToEatBot...')
    updater = Updater(token=TGBOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_command_handler = CommandHandler('start', on_start_command)
    help_command_handler = CommandHandler('help', on_help_command)
    unknown_command_handler = MessageHandler(Filters.command, on_unknown_command)
    any_text_message_handler = MessageHandler(Filters.text, on_any_text_message)

    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(help_command_handler)
    dispatcher.add_handler(unknown_command_handler)
    dispatcher.add_handler(any_text_message_handler)

    LOGGER.info('long polling started')
    updater.start_polling()

    # stop bot if Ctrl+C pressed
    updater.idle()


if __name__ == '__main__':
    run_bot()
