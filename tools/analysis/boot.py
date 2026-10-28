import sys; sys.path.insert(0, sys.argv[1])
from cynes import NES, NES_INPUT_START
from PIL import Image
nes = NES(sys.argv[2]); seq = [(int(f), int(b)) for f,b in (x.split(':') for x in sys.argv[4].split(','))] if len(sys.argv)>4 else []
frame=0; fr=None
for upto, btn in seq + [(int(sys.argv[3]),0)]:
    while frame < upto:
        nes.controller = btn; fr = nes.step(); frame += 1
Image.fromarray(fr).save(sys.argv[5] if len(sys.argv)>5 else 'shot.png'); print('ok', fr.shape, 'frames', frame)
