import os
import lzma
import hashlib
import base64


def digestFile(fp: str):
    with open(fp, 'rb') as file:
        data = file.read()
    d2 = lzma.compress(data, lzma.FORMAT_XZ)
    h1 = hashlib.sha256(data).digest()
    h2 = hashlib.sha256(d2).digest()
    d3 = h1+h2+d2
    h3 = hashlib.md5(d3).digest()
    d4 = len(fp.encode('utf-8')).to_bytes(4, 'little')+fp.encode('utf-8')+h3+d3
    d5 = bytes(map(lambda i: 214 ^ i, d4))
    fn = base64.b64encode(hashlib.md5(fp.encode('utf-8')).digest(), b'!@').decode()
    with open('./filedigest/{}.filedigest'.format(fn), 'wb') as file:
        file.write(d5)
    os.remove(fp)


def recoverFile(fn: str):
    with open(fn, 'rb') as file:
        d5 = file.read()
    d4 = bytes(map(lambda i: 214 ^ i, d5))
    fplen = int.from_bytes(d4[:4], 'little')
    fp = (d4[4:4+fplen]).decode('utf-8')
    h3, d3 = d4[4+fplen:20+fplen], d4[20+fplen:]
    assert hashlib.md5(d3).digest() == h3
    h1, h2, d2 = d3[:32], d3[32:64], d3[64:]
    assert hashlib.sha256(d2).digest() == h2
    d1 = lzma.decompress(d2, lzma.FORMAT_XZ)
    assert hashlib.sha256(d1).digest() == h1
    with open(f"./filedigest/{os.path.basename(fp)}.rawfile", 'wb') as file:
        file.write(d1)


def digestFileProc(fp: str):
    if fp.endswith(".filedigest"):
        recoverFile(fp)
    else:
        digestFile(fp)
