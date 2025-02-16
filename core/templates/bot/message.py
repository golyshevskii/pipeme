from config import G8AGENT_BOT_ADMIN

MESSAGE = {
    "start": "Hi there 👋\n\nExplain me what you need by message 👇",
    "need_access": f"You don't have access\\.\nRequest access from [admin](https://t\\.me/{G8AGENT_BOT_ADMIN})\\.",
    "confirm_request": "Double check your request 👇",
    "run_request": r"Request confirmed\. Thinking ⌛",
    "reset_request": "Request reset\\.\nLet's start again 👇",
    "faq": r"*FAQ*\. Choose a question 👇",
    "faq_1": (
        "A bot that snipe token for divergences on the exchanges you choose\\.\n\n"
        "*Divergence* is when the price of a token moves in one direction but an indicator \\(like RSI or MACD\\) moves in the opposite direction\\.\n\n"
        r"It can signal a possible trend reversal or weakening\."
    ),
    "faq_2": r"You just need to setup the exchanges and coins you want the bot to snipe\.",
}
