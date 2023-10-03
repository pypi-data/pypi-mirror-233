import os

import logging

logging.basicConfig(level=logging.DEBUG)

import revTongYi.qianwen as qwen

chatbot = qwen.Chatbot(
    cookies_str="your_cookies_str",
)

print(chatbot.list_session())
print(chatbot.ask("你好，你是谁？"))