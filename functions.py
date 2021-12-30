import os
import img2pdf
from PIL import Image
from telebot import types

def progress(lenght, width):
          percent = width /lenght
          percent = round(percent, 3) *100
          done = "█" * int(percent/5) # 
          go = "░" * (20 -int(percent/5))
          return "|"+ done +go  +f"| [{(round(percent, 2))} %]"



# create
def create_folder(directory):
    os.mkdir(directory)


# delete

def delete_file(file_name):
    os.remove(str(file_name))
def delete_folder(directory):
    for f  in os.listdir(str(directory)):
        delete_file(str(directory)+"/" + f)
    os.rmdir(str(directory))




# get images

def resize(file_path, qua):
    print(file_path)
    qua = float(qua)
    file_path = str(file_path)
    img = Image.open(file_path)
    size = img.size
    img = img.resize((int(size[0] / qua), int(size[1] / qua)))
    file_path = file_path[:-4] + 'r' + '.jpg'
    img.save(file_path)
    return file_path
def get_images(directory, qua=None):
    images = []
    if directory in os.listdir():
        print("Finded directory: ", directory)
    else:
        return images
    if 'Thumbs.db' in os.listdir(directory + "/"):
        os.remove(directory + "/Thumbs.db")

    for i in  [*range(1,len(os.listdir(str(directory))) + 1)]:
        if qua:
            filepath = resize(f'{directory}/{i}.jpg', qua)
            images.append(filepath)
        else:
            images.append(f'{directory}/{i}.jpg')

    return images
def uploading_images(id, message, bot):
    id = str(id)
    if id in os.listdir():
        print("Finded")
    else:
        create_folder(id)
    if 'Thumbs.db' in os.listdir(id+"/"):
        os.remove(id+"/Thumbs.db")
    raw = message.photo[len(message.photo)-1].file_id
    path = raw + ".jpg"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    no = len(os.listdir(id+"/"))
    with open(str(id) + f"/{no+1}" + ".jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    print(f"Tugadi {no+1}")
def get_images_count(id):
    result = os.listdir(f"{id}/")
    result = len(result)
    return result
def creating_pdf(directory, name=None, qua=''):
    images_list = get_images(str(directory),qua=qua)
    print(images_list)
    if images_list:
        with open(f"{name}{qua}.pdf", "wb") as f:
            f.write(img2pdf.convert(images_list))
    for i in images_list:
        if str(i)[-5] == "r":
            os.remove(i)
def get_key(id, bot):
    markup = types.InlineKeyboardMarkup()
    for i in [1.5, 1.3, 1]:
        creating_pdf(id, name=f"@{bot.get_me().username} {id}",qua=i)
        file_size = os.path.getsize(f'@{bot.get_me().username} {id}{i}.pdf') / 1024
        size_in = 'kb'
        if file_size > 1024:
            file_size  /= 1024
            size_in = 'mb'
        markup.add(types.InlineKeyboardButton(text=f"📁  {int(file_size):,} {size_in}", callback_data=f'convert{i}'))
    markup.add(types.InlineKeyboardButton(text="Original", callback_data="pdf"),
               types.InlineKeyboardButton(text="🗑", callback_data="del"))
    return markup
