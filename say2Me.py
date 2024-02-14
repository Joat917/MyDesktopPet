"""
say to the PET to get answer: copy or calculate or analyze a number. 
"""
dpow = pow

from cmath import *
from math import *



_PRIME_NUM = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 43, 47, 53, 59]
_PRIME_MAX = 60


def isPrime(x):
    assert isinstance(x, int)
    if x <= _PRIME_MAX:
        return x in _PRIME_NUM
    if x < 1e9:
        for p in range(2, int(sqrt(x))+1):
            if x % p == 0:
                return False
        return True

    t = x-1
    h = 0
    while t & 1 == 0:
        h += 1
        t >>= 1

    for a in _PRIME_NUM:
        a %= x
        if a <= 1:  # a==0 or a==1: to check 0^ or 1^ is meaningless, do not need the test
            continue
        v = dpow(a, t, x)
        if v in [1, x-1]:
            continue  # pass the test

        for i in range(1, h+1):
            v = v*v % x
            if v == x-1 and i != h:
                v = 1  # pass the test
                break
            if v == 1:
                # a^m!=+-1(mod n) but a^(2m)==1(mod n), which means n is not a prime!!!
                return False
        if v != 1:
            return False
    return True


def getFactText(x):
    if x <= 100:
        return "It is Too Small!!!"

    def fact(x, _p=2):
        if x<=1:
            return []
        for p in range(_p, min(int(sqrt(x))+1, 10000)):
            if x % p == 0:
                return [p]+fact(x//p, _p=p)
        return [x]
    f = fact(x)
    if len(f) == 1:
        return "I cannot fact it at all!"
    return f"{x} = {'*'.join(map(str, f))}"


def getPrmString(x):
    o = ""
    if isPrime(x):
        o += f"{x} is indeed a prime! \n"
        if x < 100:
            o += "It's simply too small. "
        else:
            o += ':) '
    else:
        o += f"{x} is not a prime. \nIn fact, "
        o += getFactText(x)
    return o


class Say2Me:
    def __init__(self, pet) -> None:
        self.pet = pet
        self.bubble = pet.speechBubble
        self.string = ""
        self.pet.say2meKeyFunc = self.onkey
        self.bubble.reText("Speaking...", 0)

    def onkey(self, event):
        if event.char == '\x08':
            self.string = self.string[:-1]
            if self.string:
                self.bubble.reText(self.string, 0)
            else:
                self.bubble.reText("Are you Speaking?", 0)
        elif ' ' <= event.char <= '~':
            self.string += event.char
            self.bubble.reText(self.string, 0)
        elif event.keycode in [10, 13]:
            self.process()
        else:
            pass
        return

    def process(self):
        "Process the inputed string"
        self.pet.say2meKeyFunc = lambda ev: None
        if not self.string:
            self.bubble.reText(
                "Tell me something. \nI know about numbers. ", 5)
            return
        try:
            i = eval(self.string)
            assert isinstance(i, int)
            i = abs(i)
        except:
            self.bubble.reText(
                "Is this a number? \nI don't understand English. ", 5)
            return
        else:
            self.pet.root.after(
                0, lambda: self.bubble.reText(getPrmString(i), 10))
            return
