from stegano import lsb
from stegano.lsb import generators
import time

def hide_message(image_path, message):
    secret_image = lsb.hide(image_path, message, generators.eratosthenes())
    secret_image.save('secret_' + image_path)
    return secret_image

def reveal_message(secret_image_path):
    revealed_message = lsb.reveal(secret_image_path, generators.eratosthenes())
    return revealed_message

images = ['image1.png', 'image2.png', 'image3.png',]
message = 'This is a secret message.'

for image in images:
    start_time = time.time()
    hide_message(image, message)
    end_time = time.time()
    print(f'Hiding message in {image} took {end_time - start_time} seconds.')
    
    s_image = 'secret_' + image
    start_time = time.time()
    reveal_message(s_image)
    end_time = time.time()
    print(f'Revealing message in {s_image} took {end_time - start_time} seconds.')


