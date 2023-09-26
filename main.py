import openai
import telebot
import json
import os



def read_secrets() -> dict: 
    filename = os.path.join('secrets.json')
    try:
        with open(filename, mode='r') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}
secrets = read_secrets()

openai.api_key = secrets["OPENAI_TOKEN"]
bot = telebot.TeleBot(secrets["TG_TOKEN"])

model_engine = 'text-davinci-003'

@bot.message_handler(regexp='Хей, .*$')
def ai_answer(msg):
    completion = openai.Completion.create(
    engine=model_engine,
    prompt= msg.text,
    max_tokens=1024,
    temperature=0.5,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
    bot.send_message(msg.chat.id, completion.choices[0].text, reply_to_message_id=msg.id)

bot.infinity_polling(timeout=10, long_polling_timeout = 5)

