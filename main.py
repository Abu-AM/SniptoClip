import os
import subprocess
from tkinter import filedialog, Tk
import pytesseract
from PIL import Image
from snip import *


def OCR(filepath):
    pytesseract.pytesseract.tesseract_cmd = filepath
    txt = pytesseract.image_to_string(Image.open("snip_image.png")).rstrip()
    return txt


def to_clipboard(txt):
    subprocess.run(["clip.exe"], input=txt.strip().encode("utf-16"), check=True)


def get_OCR_path():
    root = Tk()
    root.geometry("1x1+0+0")
    root.withdraw()

    file = filedialog.askopenfile(mode="r", filetypes=[("tesseract.exe", "*.exe")])
    if file:
        filepath = os.path.abspath(file.name)
        root.deiconify()
        root.destroy()
        return filepath
    return


def config_check():
    return os.path.exists("config.ini")


def create_config(filepath):
    file = open("config.ini", "w")
    file.write('filepath="' + filepath + '"')
    file.close()
    return filepath


def read_config():
    file = open("config.ini", "r")
    filepath = file.readline().strip("filepath=").strip('"')
    file.close()
    return filepath


def delete_img():
    os.remove("snip_image.png")


def main():
    if config_check() == False:
        filepath = create_config(get_OCR_path())
    else:
        filepath = read_config()

    snip()
    to_clipboard(OCR(filepath))
    delete_img()


if __name__ == "__main__":
    main()
