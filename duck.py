from jmd_imagescraper.core import * # dont't worry, it's designed to work with import *
from pathlib import Path
from PIL import Image
import glob
import psutil

search = input("What image do you want to search for?")
root = Path().cwd()/"images"

duckduckgo_search(root, search, search, max_results=3)

image_folder = Path().cwd()/"images"/search
images_jpg = "images/" + search + "/*.jpg"
images=glob.glob(images_jpg)
inp = ""
iterator = len(images) -1
while inp != "q":
    if iterator == -1:
        print("no more images to display, starting again")
        iterator = len(images) -1
    im = Image.open(images[iterator])
    im.show()
    inp = input("Press any key to scroll to next image, s to save or q to quit ")
    if inp == "s":
        save_name = search +".jpg"
        im.save(save_name)
        inp = "q"
    for proc in psutil.process_iter():
        if proc.name() == "display":
            proc.kill()
    iterator = iterator -1
