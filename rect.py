class Rect:
    def __init__(self, root, width, height, left, top, reserve=0) -> None:
        "calculations about positions of window"
        self.width = int(width)
        self.height = int(height)
        self._left = int(left)
        self._top = int(top)
        self._reserve = int(reserve)
        self.screen_width = root.winfo_screenwidth()  # width of the entire screen
        self.screen_height = root.winfo_screenheight()  # height of the entire screen
        # in case left or top is negative
        while self._left < 0:
            self._left += self.screen_width
        while self._top < 0:
            self._top += self.screen_height
        # call @setter to format left and top
        self.left = self._left
        self.top = self._top

    @property
    def left(self):
        return self._left

    @property
    def top(self):
        return self._top

    @left.setter
    def left(self, _v):
        _v = int(_v)
        if _v < self._reserve:
            self._left = self._reserve
        elif _v > self.screen_width-self._reserve-self.width//2:
            self._left = self.screen_width-self._reserve-self.width//2
        else:
            self._left = _v

    @top.setter
    def top(self, _v):
        _v = int(_v)
        if _v < self._reserve:
            self._top = self._reserve
        elif _v > self.screen_height-self._reserve-self.height//2:
            self._top = self.screen_height-self._reserve-self.height//2
        else:
            self._top = _v

    @property
    def right(self):
        return self._left+self.width

    @property
    def bottom(self):
        return self._top+self.height

    @right.setter
    def right(self, _v):
        self.left = _v-self.width

    @bottom.setter
    def bottom(self, _v):
        self.top = _v-self.top

    def __iter__(self):
        yield self.width
        yield self.top
        yield self._left
        yield self._top

    def as_geometry(self):
        return "{}x{}+{}+{}".format(
            self.width, self.height, self._left, self._top)

    def copy(self):
        return Rect(*self, self._reserve)
