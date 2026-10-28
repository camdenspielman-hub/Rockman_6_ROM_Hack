import sys; sys.path.insert(0, sys.argv[1])
from cynes import NES
from PIL import Image
nes = NES(sys.argv[2]); marks=[int(x) for x in sys.argv[3].split(',')]
press = {int(f):int(b) for f,b in (x.split(':') for x in sys.argv[4].split(','))} if sys.argv[4] else {}
shots=[]; btn=0
for f in range(max(marks)+1):
    if f in press: btn=press[f]
    nes.controller=btn; fr=nes.step()
    if f in marks: shots.append(Image.fromarray(fr))
m=Image.new('RGB',(256*len(shots),240))
for i,s in enumerate(shots): m.paste(s,(256*i,0))
m.save(sys.argv[5]); print('ok')
