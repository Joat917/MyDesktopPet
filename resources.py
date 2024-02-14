import json
import itertools
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps
if 'tk' not in globals():
    import tkinter as tk
if 'traceback' not in globals():
    import traceback

FILES = {}
with open('files.json') as file:
    FILES = json.load(file)

FONT = ImageFont.truetype('times.ttf', 32)
_TEXT_RESERVE = 10


class Resources:
    "Manage media resources"

    def __init__(self) -> None:
        self.images = {}  # storage the origin images as PIL.Image here
        for t, k in FILES.items():
            try:
                self.images[t] = Image.open(k).convert('RGB')
            except:
                traceback.print_exc()
        self.photoImages = {}
        return

    def getImage(self, name, size):
        "return:Image NOT EXACTLY THE SIZE OF param(size)!"
        # try to get the image, otherwise return pure black
        try:
            # get the original image
            im = self.images[name]
        except KeyError:
            # not exist, return pure black
            return Image.new('RGB', size)
        # resize the image sothat it won't bigger than param(size)
        newSize = (round(size[1]/im.height*im.width),
                   round(size[0]/im.width*im.height))
        return im.resize((min(size[0], newSize[0]), min(size[1], newSize[1])))

    def getPhotoImage(self, im, caller, root):
        "return PhotoImage"
        # im.convert('RGB').save("_tmpfile.gif")
        # ph = tk.PhotoImage(file="_tmpfile.gif", master=root)
        ph = ImageTk.PhotoImage(im, master=root)
        # IMPORTANT!!!
        # must reserve a copy of the output image!!!!!
        # or it would be trashed and vanish and cannot be used again!!
        self.photoImages[caller] = ph
        return ph

    def getBubble(self, caller, text: str, root):
        "return PhotoImage"
        # cut off long lines
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            if len(lines[i]) > 30:
                lines.insert(i+1, lines[i][30:])
                lines[i] = lines[i][:30]
            i+=1
        text = '\n'.join(lines)

        # an empty canvas for text
        textim = Image.new('RGBA', (450, 35*len(lines)))
        ImageDraw.Draw(textim).text((0, 0), text, (255,)*4, FONT)

        # clip off surrounding spaces
        ima = textim.getchannel('A')
        mw = 0
        for c in range(ima.width-1, -1, -1):
            for r in range(ima.height):
                if ima.getpixel((c, r)):
                    mw = c+1
                    break
            if mw:
                break
        mh = 0
        for r in range(ima.height-1, -1, -1):
            for c in range(mw):
                if ima.getpixel((c, r)):
                    mh = r+1
                    break
            if mh:
                break
        textim = textim.crop((0, 0, mw+1, mh+5))

        # calculate bubble size
        bubbleSize = (textim.width+_TEXT_RESERVE*2,
                      textim.height+_TEXT_RESERVE*2)

        # create the bubble
        im = Image.new('RGB', bubbleSize)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle(
            (0, 0, im.width-1, im.height-1), 10, outline='white', width=4)

        # paste the text
        im.paste(textim, (_TEXT_RESERVE, _TEXT_RESERVE),
                 textim.getchannel('A'))

        # make photoimage
        ph = ImageTk.PhotoImage(im, master=root)
        self.photoImages[('bubble', caller)] = (im, ph)
        return ph


RESOURSES = Resources()
