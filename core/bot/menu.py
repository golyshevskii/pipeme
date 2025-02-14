from core.templates.bot.button import BUTTON_MAP, INLINE_CONFIRM_REQUEST_MENU_BUTTON, INLINE_FAQ_MENU_BUTTON
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


async def set_menu(only_faq=False):
    """Set keyboard menu."""
    if only_faq:
        keyboard = [[KeyboardButton(BUTTON_MAP["faq"])]]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    keyboard = [[KeyboardButton(BUTTON_MAP["request"]), KeyboardButton(BUTTON_MAP["faq"])]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def set_faq_inline_menu():
    """Set FAQ inline menu."""
    inline_keyboard = [
        [InlineKeyboardButton(BUTTON_MAP[button], callback_data=f"{button}")]
        for button in INLINE_FAQ_MENU_BUTTON
    ]
    return InlineKeyboardMarkup(inline_keyboard)


async def set_confirm_request_inline_menu():
    """Set confirm request inline menu."""
    inline_keyboard = [
        [InlineKeyboardButton(BUTTON_MAP[button], callback_data=f"{button}")]
        for button in INLINE_CONFIRM_REQUEST_MENU_BUTTON
    ]
    return InlineKeyboardMarkup(inline_keyboard)
