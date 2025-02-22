from config import TG_BOT_ADMIN

MESSAGE = {
    "start": "Hi there 👋\nExplain me what you need by message 👇",
    "need_access": f"You don't have access\\.\nRequest access from [admin](https://t\\.me/{TG_BOT_ADMIN})\\.",
    "confirm_request": "Please, double check your request\\.\nIf everything is correct, click *Confirm* 👇",
    "run_request": "Request confirmed\\.\nThinking and building ⌛",
    "reset_request": "Okay, let's start again 👇",
    "unknown_message": "I don't understand you 🤔\nYou sent me something that is not text or voice or audio\\.",
    "run_agent_error": "Something went wrong while running the agent 😵‍💫\nPlease, try again later or contact the [admin](https://t\\.me/{TG_BOT_ADMIN})\\.",
    "faq": r"*FAQ*\. Choose a question 👇",
    "faq_1": r"A bot that generates YAML and SQL scripts based on user request\.",
    "faq_2": (
        "You just need to request by message what you want to build\\. For example:\n\n"
        r'"I need to sum user trade volume for last 7 days"'
    ),
}
