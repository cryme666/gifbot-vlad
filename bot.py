import telebot,os,requests
from telebot import types
from gif_search import search_gif
from image_search import search_image

BOT_API_KEY = os.getenv('BOT_API_KEY')

bot = telebot.TeleBot(BOT_API_KEY)

@bot.message_handler(commands=['start','help'])
def start(message):
    bot.reply_to(message,'''✨ Привіт! Я твій бот, який вміє робити спілкування яскравішим! 
Просто напиши запит, і я відправлю тобі відповідну гіфку або зображення 🎭🎨. 
Хочеш мем, кумедну реакцію чи гарну картинку? Я тут, щоб допомогти! 🚀😎''')

@bot.message_handler(func=lambda message: True)
def choose_search_type(message):
    querry = message.text
    
    markup = types.InlineKeyboardMarkup()
    gif_btn = types.InlineKeyboardButton("GIF",callback_data=f"gif:{querry}")
    image_btn = types.InlineKeyboardButton("Зображення",callback_data=f"img:{querry}")

    markup.add(gif_btn,image_btn)

    bot.send_message(message.chat.id,"Вибери, що шукати:",reply_markup=markup)


@bot.callback_query_handler(func=lambda cell:True)
def handle_query(call):
    action,query = call.data.split(":",1)
    
    if action == 'gif':
        gif_url = search_gif(query)
        if gif_url:
            bot.send_animation(call.message.chat.id,gif_url)
        else:
            bot.send_message(call.message.chat.id,'Вибач я нічого не знайшов.')          
    else:
        img_url = search_image(query)
        if img_url:
            img_data = requests.get(img_url).content
            with open('temp.jpg','wb') as img_file:
                img_file.write(img_data)

            with open("temp.jpg","rb") as img_file:
                bot.send_photo(call.message.chat.id,img_file)
            
            os.remove('temp.jpg')
        else:
            bot.send_message(call.message.chat.id,'Вибач я нічого не знайшов.')
    
if __name__ == '__main__':
    bot.polling(non_stop=True)
