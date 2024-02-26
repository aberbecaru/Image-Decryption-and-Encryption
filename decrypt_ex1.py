import os
from PIL  import Image
import hashlib


hashes = [
    "602a4a8fff652291fdc0e049e3900dae608af64e5e4d2c5d4332603c9938171d",
    "f40e838809ddaa770428a4b2adc1fff0c38a84abe496940d534af1232c2467d5",
    "aa105295e25e11c8c42e4393c008428d965d42c6cb1b906e30be99f94f473bb5",
    "70f87d0b880efcdbe159011126db397a1231966991ae9252b278623aeb9c0450",
    "77a39d581d3d469084686c90ba08a5fb6ce621a552155730019f6c02cb4c0cb6",
    "456ae6a020aa2d54c0c00a71d63033f6c7ca6cbc1424507668cf54b80325dc01",
    "bd0fd461d87fba0d5e61bed6a399acdfc92b12769f9b3178f9752e30f1aeb81d",
    "372df01b994c2b14969592fd2e78d27e7ee472a07c7ac3dfdf41d345b2f8e305"
]

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

image_files = sorted([f for f in os.listdir('.') if f.endswith('_encr.ppm')],
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
    img.save(f"image_{i+1}.png")


order = [8, 7, 3, 1, 6, 2, 5, 4]

for i in order:
    img = Image.open(f"image_{i}.png")
    img.show()