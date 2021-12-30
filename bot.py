from telebot import TeleBot, types
import config
import functions
from time import sleep

bot = TeleBot(config.token)

pdf = ''
@bot.message_handler(commands=['start'])
def start(message):
    id = message.chat.id
    bot.send_message(
        id, f"Hi, <b>{message.from_user.first_name}!</b>\nWelcome to pdf converter.\nSend image to me?👇\n\n/convert - Convert Images to Pdf file",
         parse_mode="html")
@bot.message_handler(content_types=["photo"])
def photo(message):
    global pdf
    id = message.chat.id
    functions.uploading_images(id,message,bot)
    bot.delete_message(id, message.message_id)



@bot.message_handler(commands=["convert"])
def convert(message):
    global pdf
    id = message.chat.id
    bot.delete_message(id, message.message_id)
    try:
        key = functions.get_key(id, bot)
        pdf = bot.send_message(id, "Images: " + str(functions.get_images_count(id)), reply_markup=key)
    except:
        pdf = bot.send_message(id, "Not Found!")
@bot.message_handler(content_types='text')
def convert(message):
    id = message.chat.id
    if '/convert' in message.text and message.text[8:]:
        try:
            quality = message.text[8:]
            bot.delete_message(id, message.message_id)
            msg = bot.send_message(id, functions.progress(100, 0))


            msg = bot.edit_message_text(chat_id=id, message_id=msg.message_id, text=functions.progress(100, 30))
            functions.creating_pdf(directory=id, name=f"@{bot.get_me().username} {id}",qua=quality)
            msg = bot.edit_message_text(chat_id=id, message_id=msg.message_id, text=functions.progress(100, 60))

            document = open(f"@{bot.get_me().username} {id}.pdf", "rb")
            msg = bot.edit_message_text(chat_id=id, message_id=msg.message_id, text=functions.progress(100, 90))
            bot.send_document(id, document)
            msg = bot.edit_message_text(chat_id=id, message_id=msg.message_id, text=functions.progress(100, 100))
            msg = bot.edit_message_text(chat_id=id, message_id=msg.message_id, text="✅")
            bot.delete_message(id, msg.message_id)

            functions.delete_folder(id)
            functions.delete_file(f"@{bot.get_me().username} {id}.pdf")
        except:
            return ''


    return ''

@bot.message_handler(content_types=['video', 'audio', 'voice', 'sticker'])
def start(message):
    id = message.chat.id
    bot.send_message(
        id, f"<b>Only picture, Please!</b>",
         parse_mode="html")

@bot.callback_query_handler(func=lambda call:True)
def call_(call):
    id = call.message.chat.id
    if call.data == "pdf":
        try:
            bot.delete_message(id, call.message.message_id)
            msg = bot.send_message(id, functions.progress(100, 0))
            print(f"@{bot.get_me().username} {id}.pdf")
            msg = bot.edit_message_text(chat_id=id,message_id=msg.message_id, text=functions.progress(100, 30))
            functions.creating_pdf(directory=id, name=f"@{bot.get_me().username} {id}")
            msg = bot.edit_message_text(chat_id=id,message_id=msg.message_id, text=functions.progress(100, 60))

            document = open(f"@{bot.get_me().username} {id}.pdf", "rb")
            msg = bot.edit_message_text(chat_id=id,message_id=msg.message_id, text=functions.progress(100, 90))
            bot.send_document(id, document)
            msg = bot.edit_message_text(chat_id=id,message_id=msg.message_id, text=functions.progress(100, 100))
            msg = bot.edit_message_text(chat_id=id,message_id=msg.message_id, text="✅")

            bot.delete_message(id, msg.message_id)
            functions.delete_folder(id)
            functions.delete_file(f"@{bot.get_me().username} {id}.pdf")

            functions.delete_file(f"@{bot.get_me().username} {id}1.3.pdf")
            functions.delete_file(f"@{bot.get_me().username} {id}1.5.pdf")
            functions.delete_file(f"@{bot.get_me().username} {id}1.pdf")
        except:
            pass

        

    if call.data == "del":
        id = call.message.chat.id
        try:
            bot.delete_message(id, pdf.message_id)
            functions.delete_folder(str(id))
        except:
            print(f"Not delete folder {id}")
    if call.data[:7] == 'convert':
        try:
            bot.delete_message(id, pdf.message_id)
            msg = bot.send_message(id, functions.progress(100, 0))
            print(f"@{bot.get_me().username} {id}.pdf")
            msg = bot.edit_message_text(chat_id=id, message_id=msg.message_id, text=functions.progress(100, 30))
            msg = bot.edit_message_text(chat_id=id, message_id=msg.message_id, text=functions.progress(100, 60))
    
            document = open(f'@{bot.get_me().username} {id}{call.data[7:]}.pdf', "rb")
            msg = bot.edit_message_text(chat_id=id, message_id=msg.message_id, text=functions.progress(100, 90))
            bot.send_document(id, document)
            msg = bot.edit_message_text(chat_id=id, message_id=msg.message_id, text=functions.progress(100, 100))
            msg = bot.edit_message_text(chat_id=id, message_id=msg.message_id, text="✅")

            bot.delete_message(id, msg.message_id)
            functions.delete_folder(id)
            functions.delete_file(f"@{bot.get_me().username} {id}1.3.pdf")
            functions.delete_file(f"@{bot.get_me().username} {id}1.5.pdf")
            functions.delete_file(f"@{bot.get_me().username} {id}1.pdf")
        except:
            print("err")
bot.polling()
