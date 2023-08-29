import os
from pprint import pprint

import pytz as pytz
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, Defaults, Application
from handlers import handlers_list, error_handler

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


async def init_data(app: Application):
    await app.bot.set_my_commands(
        [
            ("start", "开始"),
            ("help", "帮助"),
        ]
    )


def run():
    defaults = Defaults(tzinfo=pytz.timezone("Asia/Shanghai"))
    proxy_url = os.getenv('PROXY_URL')
    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .defaults(defaults)
        .post_init(init_data)
        .proxy_url(proxy_url)
        .get_updates_proxy_url(proxy_url)
        .build()
    )
    app.add_handlers(handlers_list)
    # app.add_error_handler(error_handler)
    app.run_polling()


if __name__ == '__main__':
    load_dotenv()
    run()
