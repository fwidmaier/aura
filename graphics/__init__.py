import numpy as np
from concurrent.futures import ProcessPoolExecutor
import concurrent.futures
from PIL import Image
from graphics.ray import Ray
from helpers import *
import time

from viewer import *


class Renderer:
    def __init__(self):
        self.scene = None
        self.w = 500
        self.h = 500

    def part(self, x0,y0,x1,y1):
        box = np.zeros((self.w, self.h, 3))
        for x in range(x0, x1):
            for y in range(y0,y1):
                box[x][y] = self.scene.camera.getPixel(x, y)
        return box

    def box(self, x, y, id, s=20):
        return self.part((x-1)*s, y * s, x*s, (y+1)*s)
        # time.sleep(0.267)
        # return id

    def construct(self, col, pxls):
        for i in range(self.w):
            for j in range(self.h):
                if i % 2 != 0 or j %2 != 0:
                    continue
                b = col[i][j]
                pxls[i,j] = (int(b[0]), int(b[1]), int(b[2]))
        return pxls

    def render(self):
        img = Image.new("RGB", size=(self.w, self.h))
        self.scene.camera.set_height(self.h)
        self.scene.camera.set_width(self.w)
        pixels = img.load()
        st = time.time()
        self.box(6, 0, 0)
        print(time.time() - st)
        print("START!")
        start = time.time()
        col = np.zeros((self.w, self.h, 3))
        # RENDERING
        s = 20
        with ProcessPoolExecutor(max_workers=8) as executer:

            th = list()
            v = Viewer(th)
            for x in range(int(self.w / s)):
                for y in range(int(self.h / s)):
                    th.append(executer.submit(self.box, x+1, y, id=x + y * int(self.w/s)))
                    #col += self.box(x+1, y, id=x + y * int(self.w/s))
                    #v.update(Image.fromarray(col.astype(np.uint8)))
            print(len(th), "Jobs")

            #v = Viewer(th)
            #v.title("aura - render")

            for f in concurrent.futures.as_completed(th):
                col += f.result()
                #pixels = self.construct(col, pixels)
                #v.update(img)
                v.update(Image.fromarray(col.astype(np.uint8)))

        print(time.time() - start)

        for i in range(self.w):
            for j in range(self.h):
                b = col[i][j]
                pixels[i,j] = (int(b[0]), int(b[1]), int(b[2]))

        print(time.time() - start)
        v.update(img)
        v.mainloop()
        img.save("render.jpg")
        img.show()
