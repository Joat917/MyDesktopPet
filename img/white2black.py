from PIL import Image
import itertools


def getBox(im):
    BOX = [0, 0, im.width, im.height]
    ima = im.getchannel('A')
    transp = True
    for c in range(im.width):
        for r in range(im.height):
            if ima.getpixel((c, r)) > 1:
                transp = False
                break
        if not transp:
            BOX[0] = c
            break
    transp = True
    for c in range(im.width-1, -1, -1):
        for r in range(im.height):
            if ima.getpixel((c, r)) > 1:
                transp = False
                break
        if not transp:
            BOX[2] = c+1
            break
    transp = True
    for r in range(im.height):
        for c in range(BOX[0], BOX[2]):
            if ima.getpixel((c, r)) > 1:
                transp = False
                break
        if not transp:
            BOX[1] = r
            break
    transp = True
    for r in range(im.height-1, -1, -1):
        for c in range(BOX[0], BOX[2]):
            if ima.getpixel((c, r)) > 1:
                transp = False
                break
        if not transp:
            BOX[3] = r+1
            break
    return tuple(BOX)


def main():
    file = input("file?")
    if file[0] == file[-1] == "\"":
        file = file[1:-1]
    im = Image.open(file).convert('RGBA')
    print("SIZE:", im.size)
    thre = eval('('+input("threhold?")+')')
    if isinstance(thre, int):
        thre = (thre,)*3
    elif not isinstance(thre, tuple):
        raise TypeError("thre!!!tuple.")
    if all([(0 < thre[i] < 256) for i in range(3)]):
        for p in itertools.product(
                range(im.width), range(im.height)):
            pix = im.getpixel(p)
            if pix[0] >= thre[0] and pix[1] >= thre[1] and pix[2] >= thre[2]:
                im.putpixel(p, (0, 0, 0, 0))
    ima = im.getchannel('A')
    for p in itertools.product(
            range(im.width), range(im.height)):
        if ima.getpixel(p) <= 1:
            im.putpixel(p, (0, 0, 0, 0))

    im = im.crop(getBox(im))
    print("SIZE", im.size)
    im.show()
    if eval(input("Is it ok?"), {'y': True, 'n': False}):
        print("Saving...", end='')
        im.save(file[:-4]+'edit.png')
        print("\rSaved.      ")


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as exc:
            print(exc)
