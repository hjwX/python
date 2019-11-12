import numpy as np
from PIL import ImageTk, Image
import tkinter as tk

def test_seed():
    np.random.seed(1)
    for i in range(5):
        print(np.random.random())
    print("---------------------------------------------------------------------")
    np.random.seed(1)
    for i in range(5):
        print(np.random.random())
    print("---------------------------------------------------------------------")
    np.random.seed(2)
    for i in range(5):
        print(np.random.random())

def test_image():
    image = Image.open('77686537.png')
    # image.show()
    print(image.mode, image.size, image.format)

class test_tk(tk.Tk):
    def __init__(self):
        super(test_tk, self).__init__()
        self.HEIGHT = 5
        self.UNIT = 100
        self.WIDTH = 5
        self.title('Q Learning')
        self.geometry('{0}x{1}'.format(self.HEIGHT * self.UNIT, self.WIDTH * self.UNIT))
        self.shapes = self.load_images()
        self.canvas = self._build_canvas()
        self.mainloop()

    def _build_canvas(self):
        canvas = tk.Canvas(self, bg='white',
                           height=self.HEIGHT * self.UNIT,
                           width=self.WIDTH * self.UNIT)
        # create grids
        for c in range(0, self.WIDTH *self.UNIT, self.UNIT):  # 0~500 by 100
            x0, y0, x1, y1 = c, 0, c, self.HEIGHT * self.UNIT
            canvas.create_line(x0, y0, x1, y1)
        for r in range(0, self.HEIGHT * self.UNIT, self.UNIT):  # 0~500 by 100
            x0, y0, x1, y1 = 0, r, self.HEIGHT * self.UNIT, r
            canvas.create_line(x0, y0, x1, y1)

        # add img to canvas
        self.rectangle = canvas.create_image(50, 50, image=self.shapes[0])
        self.triangle1 = canvas.create_image(250, 150, image=self.shapes[1])
        self.triangle2 = canvas.create_image(150, 250, image=self.shapes[1])
        self.circle = canvas.create_image(250, 250, image=self.shapes[2])

        # pack all
        canvas.pack()

        return canvas

    def load_images(self):
        rectangle = ImageTk.PhotoImage(
            Image.open("../img/rectangle.png").resize((80, 80)))
        triangle = ImageTk.PhotoImage(
            Image.open("../img/triangle.png").resize((80, 80)))
        circle = ImageTk.PhotoImage(
            Image.open("../img/circle.png").resize((80, 80)))

        return rectangle, triangle, circle

if __name__ == '__main__':
    # test_seed()
    # test_image()
    show = test_tk()
