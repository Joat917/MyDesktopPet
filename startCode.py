import os
l=os.environ['PATH'].split(';')
s=next(filter(lambda s:('Code' in s), l))
os.system("start \"\" \"{}\\code.cmd\" %cd%".format(s))
os.system("timeout /t 3")
