"""
Snipping & saving implementation taken from: https://stackoverflow.com/a/61603758
"""

import subprocess
from tkinter import Toplevel, Frame, Canvas, Tk, BOTH, YES
from PIL import Image
import pyautogui
import pytesseract


class Application:
    def __init__(self, master):
        self.master = master
        self.rect = None
        self.x = self.y = 0
        self.start_x = None
        self.start_y = None
        self.curX = None
        self.curY = None
        self.img = None

        root.withdraw()

        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "blue")

        self.picture_frame = Frame(self.master_screen, background="blue")
        self.picture_frame.pack(fill=BOTH, expand=YES)
        self.create_screen_canvas()

    def OCR(self):

        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

        txt = pytesseract.image_to_string(Image.open("sniptoclip.png")).rstrip()
        subprocess.run(["clip.exe"], input=txt.strip().encode("utf-16"), check=True)
        exit()

    def take_bounded_screenshot(self, x1, y1, x2, y2):
        im = pyautogui.screenshot(region=(x1, y1, x2, y2))
        im.save("sniptoclip.png")
        self.OCR()

    def create_screen_canvas(self):
        self.master_screen.deiconify()
        root.withdraw()

        self.screen_canvas = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.screen_canvas.pack(fill=BOTH, expand=YES)

        self.screen_canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.screen_canvas.bind("<B1-Motion>", self.on_move_press)
        self.screen_canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes("-fullscreen", True)
        self.master_screen.attributes("-alpha", 0.3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):
        self.rec_position()

        if self.start_x <= self.curX and self.start_y <= self.curY:
            print("right down")
            self.take_bounded_screenshot(
                self.start_x,
                self.start_y,
                self.curX - self.start_x,
                self.curY - self.start_y,
            )

        elif self.start_x >= self.curX and self.start_y <= self.curY:
            print("left down")
            self.take_bounded_screenshot(
                self.curX,
                self.start_y,
                self.start_x - self.curX,
                self.curY - self.start_y,
            )

        elif self.start_x <= self.curX and self.start_y >= self.curY:
            print("right up")
            self.take_bounded_screenshot(
                self.start_x,
                self.curY,
                self.curX - self.start_x,
                self.start_y - self.curY,
            )

        elif self.start_x >= self.curX and self.start_y >= self.curY:
            print("left up")
            self.take_bounded_screenshot(
                self.curX, self.curY, self.start_x - self.curX, self.start_y - self.curY
            )

        self.exit_screenshot_mode()
        return event

    def exit_screenshot_mode(self):
        print("Screenshot mode exited")
        self.screen_canvas.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    def exit_application(self):
        print("Application exit")
        root.quit()

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.screen_canvas.canvasx(event.x)
        self.start_y = self.screen_canvas.canvasy(event.y)

        self.rect = self.screen_canvas.create_rectangle(
            self.x, self.y, 1, 1, outline="red", width=3, fill="blue"
        )

    def on_move_press(self, event):
        self.curX, self.curY = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.screen_canvas.coords(
            self.rect, self.start_x, self.start_y, self.curX, self.curY
        )

    def rec_position(self):
        print(self.start_x)
        print(self.start_y)
        print(self.curX)
        print(self.curY)


if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()
