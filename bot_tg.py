import telebot
import threading
import time
import os
from telebot import types
from video_search import get_latest_video_info

moornyx_bot = telebot.TeleBot('6200790926:AAEagh1ygT3Jmx5wgxguTt-gno1M1w2oAc8')

def create_file_if_not_exists(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            pass

def get_last_video_file_path():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'last_video.txt')
    return file_path

def get_video_id_from_link(video_link):
    return video_link.split('/')[-1]

def get_video_url_from_id(video_id):
    return f"https://youtu.be/{video_id}"

@moornyx_bot.message_handler(commands=['start'])
def startBot(message):
    first_mess = f"Рад тебя видеть, <b>{message.from_user.first_name}</b>! :)\nЧем могу помочь?"
    markup = types.InlineKeyboardMarkup()
    button_last_video = types.InlineKeyboardButton(text='Последнее видео', callback_data='last')
    markup.add(button_last_video)
    moornyx_bot.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)

@moornyx_bot.callback_query_handler(func=lambda call: True)
def response(function_call):
    markup = types.InlineKeyboardMarkup()
    button_last_video = types.InlineKeyboardButton(text='Последнее видео', callback_data='last')
    markup.add(button_last_video)
    
    if function_call.message:
        if function_call.data == "last":
            file_path = get_last_video_file_path()
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    cached_data = file.read().strip()
                if cached_data:
                    video_title, video_link = cached_data.split('\n')
                    try:
                        moornyx_bot.delete_message(function_call.message.chat.id, function_call.message.message_id)
                    except telebot.apihelper.ApiException:
                        pass
                    video_message = f"{video_title}\nhttps://youtu.be/{video_link}"
                    moornyx_bot.send_message(function_call.message.chat.id, video_message, parse_mode='html', reply_markup=markup)
                else:
                    moornyx_bot.send_message(function_call.message.chat.id, "Данные о последнем видео отсутствуют.", parse_mode='html', reply_markup=markup)
            else:
                moornyx_bot.send_message(function_call.message.chat.id, "Данные о последнем видео отсутствуют.", parse_mode='html', reply_markup=markup)
            moornyx_bot.answer_callback_query(function_call.id)

def check_for_updates():
    while True:
        print('Проверка нового видео...')
        latest_video_title, latest_video_link = get_latest_video_info('https://www.youtube.com/@moornyx/videos')
        file_path = get_last_video_file_path()
        print('Новые данные записаны в файл:', file_path)
        create_file_if_not_exists(file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            cached_data = file.read().strip()
        
        if cached_data:
            cached_video_link = cached_data.split('\n')[-1]
            latest_video_id = get_video_id_from_link(latest_video_link)
            cached_video_id = get_video_id_from_link(cached_video_link)
        
            if cached_video_id != latest_video_id:
                video_info = f"{latest_video_title}\n{latest_video_link}"
                moornyx_bot.send_message(chat_id='@moornyxxx', text='Новое видео')
                print('Записываю новые данные в файл...')
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(video_info)
            else:
                print('Данные не изменились, ничего не записываю.')
        else:
            print('Список видео пуст.')
            
        # Как часто проверять новое видео
        time.sleep(5)

def main():
    print('Запуск бота...')

    threading.Thread(target=check_for_updates).start()
    moornyx_bot.infinity_polling()

if __name__ == '__main__':
    main()
