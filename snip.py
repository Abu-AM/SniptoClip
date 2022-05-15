from tkinter import Tk, Canvas, BOTH
from PIL import ImageGrab

debug = False

global img


def draw_drag(event):
    canvas = event.widget
    cur_x = canvas.canvasx(event.x)
    cur_y = canvas.canvasy(event.y)

    x0, y0, x1, y1 = canvas.coords("current_rect")

    if debug == True:
        print("xy0 =", x0, y0, "xy1=", x1, y1)
        print("moving coord =", cur_x, cur_y)

    canvas.coords("current_rect", x0, y0, cur_x, cur_y)

    global snip_coord

    snip_coord = tuple(map(int, (x0, y0, x1, y1)))


def take_screenshot(coords):
    img = ImageGrab.grab(bbox=coords)

    img.save("snip_image.png")


def draw_stop(snip_coord, root):
    root.destroy()
    take_screenshot(snip_coord)


def draw_start(event):
    canvas = event.widget
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    canvas.create_rectangle(x, y, x, y, fill="red", outline="red", tags="current_rect")


def fill_screen(root):
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.1)
    root.configure(background="grey")


def snip():
    root = Tk()
    fill_screen(root)

    canvas = Canvas(root, cursor="cross")
    canvas.pack(fill=BOTH, expand=True)

    global snip_coord

    canvas.bind("<ButtonPress-1>", draw_start)
    canvas.bind("<B1-Motion>", draw_drag)
    canvas.bind("<ButtonRelease-1>", lambda event: draw_stop(snip_coord, root))

    root.mainloop()


if __name__ == "__main__":
    snip()
