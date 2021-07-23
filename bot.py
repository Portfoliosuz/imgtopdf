from telebot import TeleBot, types
import config
import functions


bot = TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):
    id = message.chat.id
    bot.send_message(
        id, f"Hi, <b>{message.from_user.first_name}!</b>\nWelcome to pdf converter.\nSend image to me?👇\n\n/convert - Convert Images to Pdf file",
         parse_mode="html")
@bot.message_handler(content_types=["photo"])
def photo(message):
    id = message.chat.id
    try:
        functions.uploading_images(id,message,bot)
    except:
        print("Not upload")
    bot.delete_message(id, message.message_id)
@bot.message_handler(commands=["convert"])
def convert(message):
    global pdf
    id = message.chat.id
    bot.delete_message(id, message.message_id)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Pdf", callback_data="pdf"),types.InlineKeyboardButton(text="🗑", callback_data="del"))
    pdf = bot.send_message(id, "Images: " + str(functions.get_images_count(id)), reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def call_(call):
    if call.data == "pdf":
        id = call.message.chat.id
        bot.delete_message(id, pdf.message_id)
        try:
            functions.creating_pdf(directory=id, name=f"@{bot.get_me().username} {id}")
        except:
            print("Not Create Pdf")
        document = open(f"@{bot.get_me().username} {id}.pdf", "rb")
        bot.send_document(id, document)
        try:
            functions.delete_folder(id)
            functions.delete_file(f"@{bot.get_me().username} {id}.pdf")
        except:
            print(f"Not delete folder {id}")
    if call.data == "del":
        id = call.message.chat.id
        bot.delete_message(id, pdf.message_id)
        try:
            functions.delete_folder(id)
        except:
            print(f"Not delete folder {id}")
bot.polling()
