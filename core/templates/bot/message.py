from config import TG_BOT_ADMIN

MESSAGE = {
    "start": "Hi there 👋\n\nExplain me what you need by message 👇",
    "need_access": f"You don't have access\\.\nRequest access from [admin](https://t\\.me/{TG_BOT_ADMIN})\\.",
    "confirm_request": "Double check your request 👇",
    "run_request": "Request confirmed\\.\nThinking and building ⌛",
    "reset_request": r"Okay\, let's start again 👇",
    "faq": r"*FAQ*\. Choose a question 👇",
    "faq_1": r"A bot that generates YAML and SQL scripts based on user request\.",
    "faq_2": (
        "You just need to request by message what you want to build\\. For example:\n\n"
        r'"I need to sum user trade volume for last 7 days"'
    ),
}
