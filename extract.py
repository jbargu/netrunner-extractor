from pypdf import PdfReader, PdfWriter
from PIL import Image
import os, cv2

# PDF obtained from https://access.nullsignal.games/Gateway/English/English/SystemGatewayEnglish-A4%20Printable%20Sheets%203x.pdf
reader = PdfReader("./MSBooster-A4-Printable-Sheets-1x-1.pdf")

# page = reader.pages[0]
count = 1

WIDTH = 765 - 72
HEIGHT = 1033 - 72

folder_in = "imgs/"
folder_out = "bleed/"


def image_is_transparent(image: Image, opaque: int = 255) -> bool:
    if "A" in image.mode:
        # see if minimum alpha channel is below opaque threshold
        return image.getextrema()[image.mode.index("A")][0] < opaque
    if image.mode != "P" or "transparency" not in image.info:
        # format doesn't support transparency
        return False
    transparency = image.info["transparency"]
    colors = image.getcolors()
    # check each color in the image
    if isinstance(transparency, bytes):
        # transparency is one byte per palette entry
        for _, index in colors:
            if transparency[index] < opaque:
                return True
    else:
        # transparency is palette index of fully transparent
        for _, index in colors:
            if transparency == index:
                return True
    return False


count = 1
# Cuts the PDF into separate images, saving the images into "/imgs" folder
for page in reader.pages:
    for image_file_object in page.images:
        img_name = "tmp.png"
        with open(img_name, "wb") as fp:
            fp.write(image_file_object.data)

        count += 1

        img = Image.open("tmp.png")
        print(img.size)

        img_area = (1, 1, 505, 706)
        img_left = img.crop(img_area)
        img_left.save(folder_in + str(count) + image_file_object.name)


# Reads the images from the "/imgs" folder and adds the bleed on both sides
# Code from: https://old.reddit.com/r/Netrunner/comments/vn738u/printing_some_proxies_to_turn_nisei_netrunner/ie6xjsb/?context=3
dpi = 300
bleed_inches = 0.0625
bleed_pixels = int(bleed_inches * dpi)
size_card_inches = [2.5, 3.5]
size_card_pixels = [int(d * dpi) for d in size_card_inches]


for file in os.listdir(folder_in):
    im = cv2.imread(folder_in + file)
    im = cv2.resize(im, size_card_pixels)
    im = cv2.copyMakeBorder(
        im, bleed_pixels, bleed_pixels, bleed_pixels, bleed_pixels, cv2.BORDER_REPLICATE
    )
    cv2.imwrite(folder_out + file, im)
