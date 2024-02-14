# About

Stick an image on your desktop, specifically an anime girl. 

She loves prime numbers, and is feed on files. 

# Credits

Idea came from [this project](https://github.com/tommyli3318/desktop-pet.git),  but codes are original. 

# Run

```
pythonw main.pyw
```

1. Drag her anywhere on the screen.

2. Right click to zoom her and to summon more different images. All possibilities are shown in `files.json`. You can edit this json file to add more images. 

3. Right click and choose `Quit` to kill her; choose `QuitAll` to kill all at one time.

4. Drop a file on the image to be "eaten". Press `y` key to confirm and `n` key to cancel. After 5 seconds she'll stop attempting to eat anything. 

5. Eaten files can be recovered by eating corresponding `.filedigest` file in `filedigest` folder. The origin file will appear in this folder with a `.rawfile` suffix. 

---

## Special Note:

1. `white2black.py` in folder `img` turns an image with white background into transparent background and is not intended to run. 

2. `startCode.py` starts VSCode on MY COMPUTER and nobody knows how it'll behave elsewhere. 

3. `readme.pdf` is very likely to fall out of date. READ ME!!!
