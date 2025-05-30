# utils/menu_utils.py

def create_menu_options(options):
    """
    Создает список опций для выпадающего меню.
    :param options: Список строк (названия опций).
    :return: Список кортежей (опция, callback_data).
    """
    return [(option, option.lower()) for option in options]