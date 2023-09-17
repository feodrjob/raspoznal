import telebot
from deepface import DeepFace
import configparser
import random
import math
import uuid
import os

#  api key parseng
config = configparser.ConfigParser() 
config.read("settings.ini")  

api_key = config["TopSecret"]["API_KEY"]

bot = telebot.TeleBot(api_key) 

# handler for photos 
@bot.message_handler(content_types=['photo'])    
def face_analyze(message):
    try:
        # get new photo 
        file_name = uuid.uuid4()
        fileID = message.photo[-1].file_id   
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f'media/{file_name}.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # main method
        result_dict = DeepFace.analyze(
            img_path=f'media/{file_name}.jpg', 
            actions=['age', 'gender', 'race', 'emotion']
        )  
        
        # data sharing 
        age_level = result_dict[0]['age']
        dom_gn = result_dict[0]['dominant_gender']
        dom_gn_level = result_dict[0]['gender'][dom_gn]
        dom_rc = result_dict[0]['dominant_race'] 
        dom_rc_level = result_dict[0]['race'][dom_rc]
        dom_em = result_dict[0]['dominant_emotion']
        dom_em_level = result_dict[0]['emotion'][dom_em]

        # some fixes
        real_age = int(age_level) - random.randint(14, 25)  
        GETREAL_age = int(math.fabs(real_age))  

        # messages
        bot.send_message(message.chat.id, f"👶 Estimated age: {GETREAL_age}-{age_level}")
        bot.send_message(message.chat.id, f"👥 Estimated sex: {dom_gn}")
        bot.send_message(message.chat.id, f"👩🏻👦🏾 Estimated reace: {dom_rc}")
        bot.send_message(message.chat.id, f"🤯 Estimated emotion: {dom_em}")
        if (dom_em == 'neutral'):
            bot.send_message(message.chat.id, "🤓 Cooool Booooy")
        else:
            bot.send_message(message.chat.id, "🤓 Just Nerd")

        os.remove(f'media/{file_name}.jpg')

    except ValueError:
        bot.send_message(message.chat.id, "😖 Face Not Found")
    except:
        bot.send_message(message.chat.id, "☠️ Error")

         
# handlers for other text messages
@bot.message_handler(content_types = ['text'])               
def bot_message(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, "Sent photo with face")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

    

bot.infinity_polling()