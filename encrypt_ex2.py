import os
import hashlib
import random
import secrets

from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
def extract_ppm_headers(file_path):
    headers = []
    with open(file_path, 'r') as f:

        P =  f.readline().strip()
        width, height = map(int, f.readline().split())
        max_color =  int(f.readline())


        header_string = f"{P} {width} {height} {max_color}"
        return header_string



def save_file_without_header(file_path, output_directory):
    with open(file_path, 'rb') as f:

        f.readline()
        f.readline()
        f.readline()


        content = f.read()

    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(content, AES.block_size))

    header = extract_ppm_headers(file_path)

    output_path = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(file_path))[0]}_encr2.ppm")

    with open(output_path, 'wb') as output_file:
        
        output_file.write(header.encode() + b'\n' + encrypted)


file_paths = ['A.ppm', 'N.ppm', 'D.ppm', 'R.ppm', 'E.ppm', 'I.ppm']
header_list = []
output_directory = "."
hashes = []
key = secrets.token_bytes(32)

for file_path in file_paths:
    header = extract_ppm_headers(file_path)
    header_list.append(header)

    hashed_header = hashlib.sha256(header.encode()).hexdigest()
    hashes.append(hashed_header)

    save_file_without_header(file_path, output_directory)



print(header_list)
random.shuffle(hashes)
print(hashes)

final_list = []

def bruteforce():
    for x in range(1, 1001):
        for y in range(1, 1001):
            header = f"P6 {x} {y} 255"
            hashed_header = hashlib.sha256(header.encode()).hexdigest()

            if hashed_header in hashes:
                final_list.append((hashed_header, x, y))



bruteforce()
final_list = sorted(final_list, key=lambda item: item[1] * item[2])

image_files = sorted([f for f in os.listdir('.') if f.endswith('_encr2.ppm')],
                     key = lambda f: os.path.getsize(f"{os.getcwd()}/{f}"))


for i, (_, x, y) in enumerate(final_list):
    image_file = image_files[i]

    with open(image_file, 'rb') as f:
        image_data = f.read()

    header = f"P6 {x} {y} 255"
    new_image_data = header.encode() + b'\n' + image_data

    new_image_file = f"new_{image_file}"
    with open(new_image_file, 'wb') as f:
        f.write(new_image_data)

    img = Image.open(new_image_file)
    img.save(f"image2_{i+1}.png")


order = [1, 4, 3, 5, 2, 6]

for i in order:
    img = Image.open(f"image2_{i}.png")
    img.show()