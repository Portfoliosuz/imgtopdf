import os
import img2pdf

# create
def create_folder(directory):
    os.mkdir(directory)


# delete

def delete_file(file_name):
    os.remove(file_name)
def delete_folder(directory):
    for f  in os.listdir(str(directory)):
        delete_file(str(directory)+"/" + f)
    os.rmdir(str(directory))




# get images


def get_images(directory):
    images = []
    if directory in os.listdir():
        print("Finded")
    else:
        return []
    for file in os.listdir(f"{directory}/"):
        if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
            images.append(directory + "/" + str(file))
        else:
            continue
    return images
def uploading_images(id, message, bot):
    id = str(id)
    if id in os.listdir():
        print("Finded")
    else:
        create_folder(id)

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


def creating_pdf(directory, name=None):
    images_list = get_images(str(directory))
    if images_list:
        with open(f"{name}.pdf", "wb") as f:
            f.write(img2pdf.convert(images_list))