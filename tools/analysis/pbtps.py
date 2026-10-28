# Minimal PBTPS interpreter (copy DST LEN SRC semantics, verified against R4MI scripts)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ips import apply_ips
def run(script, rom, base):
    lines = open(os.path.join(base, script),'rb').read().split(b'\r\n')
    i = 0
    while i < len(lines):
        l = lines[i].strip(); i += 1
        if not l.startswith(b'\\') or l.startswith(b'\\\\'): continue
        t = l[1:].split(); cmd = t[0].decode()
        if cmd == 'include': rom = run(t[1].decode(), rom, base)
        elif cmd == 'copy':
            d, n, s = (int(x,16) for x in t[1:4]); rom[d:d+n] = rom[s:s+n]
        elif cmd == 'revbit':
            a, n = (int(x,16) for x in t[1:3])
            for k in range(a, a+n): rom[k] = int(f'{rom[k]:08b}'[::-1], 2)
        elif cmd == 'insert':
            a, n, v = (int(x,16) for x in t[1:4]); rom[a:a] = bytes([v])*n
        elif cmd == 'write_i':
            a, n = (int(x,16) for x in t[1:3]); hexs = b''
            while not lines[i].strip().startswith(b'\\eod'):
                if lines[i].strip().startswith(b'\\\\'): hexs += lines[i].strip()[2:].replace(b' ',b'')
                i += 1
            i += 1; data = bytes.fromhex(hexs.decode()); assert len(data)==n, (a,n,len(data)); rom[a:a+n] = data
        elif cmd == 'ips_o':
            rom, recs = apply_ips(bytes(rom), open(os.path.join(base, t[1].decode()),'rb').read()); rom = bytearray(rom)
            print('ips records', len(recs), 'bytes', sum(r[1] for r in recs))
    return rom
rom = bytearray(open(sys.argv[1],'rb').read())
out = run(os.path.basename(sys.argv[2]), rom, os.path.dirname(os.path.abspath(sys.argv[2])))
open(sys.argv[3],'wb').write(out); print(len(out))
