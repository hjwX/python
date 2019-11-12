import tkinter as tk
from PIL import ImageTk, Image
import numpy as np

class Mode(tk.Tk):
    def __init__(self):
        super(Mode, self).__init__()
        self.image = ImageTk.PhotoImage(Image.open('miku.jpg').resize((50, 50)))
        self.title('mode_1')
        self.geometry('500x500')
        self.canvas =self.load_canvas()
        self.bind('<KeyPress-d>', self.move)
        self.bind('<KeyPress-a>', self.move)
        self.bind('<KeyPress-w>', self.move)
        self.bind('<KeyPress-s>', self.move)
        self.mainloop()

    def load_canvas(self):
        canvas = tk.Canvas(self, bg='white',
                           height=5 * 100,
                           width=5 * 100)
        # create grids
        for c in range(0, 5 * 100, 100):  # 0~500 by 100
            x0, y0, x1, y1 = c, 0, c, 5 * 100
            canvas.create_line(x0, y0, x1, y1)
        for r in range(0, 5 * 100, 100):  # 0~500 by 100
            x0, y0, x1, y1 = 0, r, 5 * 100, r
            canvas.create_line(x0, y0, x1, y1)

        self.rectangle = canvas.create_image(50, 50, image=self.image)
        # self.triangle1 = canvas.create_image(250, 150, image=self.image)
        # self.triangle2 = canvas.create_image(150, 250, image=self.image)
        # self.circle = canvas.create_image(250, 250, image=self.image)

        canvas.pack()
        return canvas

    def move(self, event):
        base_action = np.array([0, 0])
        state = self.canvas.coords(self.rectangle)
        print(state)
        if event.char == 'a':
            if state[0] >= 100:
                base_action[0] = -100
        if event.char == 'd':
            if state[0] <= 500 - 100:
                base_action[0] = 100
        if event.char == 'w':
            if state[1] >= 100:
                base_action[1] = -100
        if event.char == 's':
            if state[1] <= 500 - 100:
                base_action[1] = 100
        self.canvas.move(self.rectangle, base_action[0], base_action[1])


if __name__ == '__main__':
    test = Mode()