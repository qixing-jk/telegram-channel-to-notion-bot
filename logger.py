import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def log(func, level="info"):
    def wrapper(*args, **kwargs):
        try:
            message = (f"在[{args[0].effective_chat.title}]中({args[0].effective_user.name})" + "执行了操作"
                       + f"【{args[0].effective_message.text}】")
            if level == "warn":
                logging.warning(f'{func.__name__}:{message}')
            elif level == "info":
                logging.info(f'{func.__name__}:{message}')
        except Exception as e:
            logging.error(f'{func.__name__}:{e}')
        return func(*args, **kwargs)

    return wrapper
