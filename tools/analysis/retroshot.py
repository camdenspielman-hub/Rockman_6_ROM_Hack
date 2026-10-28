# Headless boot via stable-retro (FCEUmm core). usage: retroshot.py LIB ROM frames_csv presses OUT
import sys, os, shutil, tempfile; sys.path.insert(0, sys.argv[1])
import numpy as np, importlib.util, glob
lib = sys.argv[1] + '/stable_retro'
spec = importlib.util.spec_from_file_location('_retro', glob.glob(lib + '/_retro*.so')[0])
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
R.core_path(lib + '/cores'); R.RetroEmulator.load_core_info(open(lib + '/cores/fceumm.json').read())
from PIL import Image
tmp = tempfile.mkdtemp(); rom = os.path.join(tmp, 'game.nes'); shutil.copy(sys.argv[2], rom)
emu = R.RetroEmulator(rom)
marks = [int(x) for x in sys.argv[3].split(',')]
press = {int(f):int(b) for f,b in (x.split(':') for x in sys.argv[4].split(','))} if sys.argv[4] else {}
# NES button order in retro: B, nil, SELECT, START, UP, DOWN, LEFT, RIGHT, A
btn = 0; shots = []
for f in range(max(marks)+1):
    if f in press: btn = press[f]
    mask = np.zeros(16, dtype=np.uint8)
    if btn & 8: mask[3] = 1      # START
    if btn & 1: mask[8] = 1      # A
    emu.set_button_mask(mask, 0); emu.step()
    if f in marks: shots.append(Image.fromarray(emu.get_screen()))
w, h = shots[0].size; m = Image.new('RGB', (w*len(shots), h))
for i, s in enumerate(shots): m.paste(s, (w*i, 0))
m.save(sys.argv[5]); print('ok', w, h)
