# sunnyspeed studio
# YouTube: https://www.youtube.com/sunnyspeedstudio
# Purpose: Add timestamp on an image. The time information is retrived from image's exif.

from PIL import Image, ExifTags, ImageDraw, ImageFont
from pathlib import Path
import os
import sys


# config, feel free play around
text_font = ImageFont.truetype("DigitalTime.ttf", 160)
text_color = (255,255,255)
text_position = 'bottom_right'    # top_right, bottom_left, bottom_right
text_offset_x = 1200
text_offset_y = 200
subfolder = 'timestamp'


def getDateTime(image_file):
    img = Image.open(image_file)
    exif = dict(img.getexif())
    for key, value in exif.items():
        if key in ExifTags.TAGS:
            # print all exif info for debug
            # print(ExifTags.TAGS[key], value)
            if ExifTags.TAGS[key] == 'DateTimeOriginal':
                return value    # you may want to do some formatting on the datetime
            elif ExifTags.TAGS[key] == 'DateTimeDigitized': # fallback
                return value
            elif ExifTags.TAGS[key] == 'DateTime': # fallback
                return value
    return None # no date time info is found in exif

def printDateTime(image_file, resized_image_file):
    text = getDateTime(image_file)
    img = Image.open(image_file)
    draw = ImageDraw.Draw(img)

    # get text postion
    # default: top_left
    x = text_offset_x
    y = text_offset_y
    if text_position == 'top_right' and img.width > text_offset_x:
        x = img.width - text_offset_x
    elif text_position == 'bottom_left' and img.height > text_offset_y:
        y = img.height - text_offset_y
    elif text_position == 'bottom_right' and img.width > text_offset_x and img.height > text_offset_y:
        x = img.width - text_offset_x
        y = img.height - text_offset_y
    
    draw.text((x, y), text, text_color, text_font)
    img.save(resized_image_file)


if len(sys.argv) < 2:
    print("Need one argument: the full path to the image folder")
else:
    folder_path = sys.argv[1] + "\\"
    subfolder_path = folder_path + subfolder + "\\"
    # create subfolder
    Path(subfolder_path).mkdir(parents=True, exist_ok=True)
    # loop through all images in the current folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg"):
            printDateTime(folder_path + filename, subfolder_path + filename)
            print(filename, "- timestamp added")