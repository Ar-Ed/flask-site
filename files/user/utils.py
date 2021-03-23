import secrets
import os
from PIL import Image

def save_image(form_image):
    random = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_file_name = random + f_ext
    path = os.path.join(app.root_path,'static/img', image_file_name)

    output_size = (200,200)
    image = Image.open(form_image)
    image.thumbnail(output_size)
    image.save(path)

    return image_file_name