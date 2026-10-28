"""(cx-systems) python3 -I tools/analysis/cx/systems_dmgtable.py [rom]: print Rockman CX's boss weakness chart
straight from the ROM (bank $17, boss-hit dispatcher $A5F4).

Tables (14 bytes each, indexed by the boss number $B3; 0 = deflected):
  $A92B buster (also Dead Ringer rings and buster shots with the Ubercharge equipped)
  $A93B Mega Buster (x1/x2/x3 by charge)   $A94B Ringo Shield   $A95B Fire Ball (burn frames, 1 damage per tick)
  $A96B Print Cutter   $A97B Rider Kick   $A98B Power Bomb
  Cheat Saber: boss 0 -> the PLAYER's HP is set to 0; bosses 1-7 -> killed; 8-13 -> $A923+n-8 (overlaps the
  dispatcher's hi-byte table).  Quick Man ($9B bit 7) doubles the buster/Ringo/Mega Buster path ($A635).
Boss numbers: 0 Cheat Man, 1 Air Man, 2 Whispy Woods, 3 Fire Mario, 4 Yoshino Man, 5 Mega Man, 6 Kamen Rider,
7 Bomberman, 9 Quick Man (Light 2), 10 Guts Tank (Light 3), 13 Light 6; 8/11/12 other fortress bosses.
"""
import sys
rom = open(sys.argv[1] if len(sys.argv) > 1 else 'roms/cx_en.nes', 'rb').read()[16:]
def rd(addr, n): o = 0x17 * 0x2000 + addr - 0xA000; return list(rom[o:o + n])
BOSS = ['Cheat', 'Air', 'Whispy', 'FMario', 'Yoshino', 'MegaMan', 'Kamen', 'Bomber', '#8', 'QuickM', 'GutsTk', '#11', '#12', '#13']
rows = [('Buster/DeadRinger', rd(0xA92B, 14)), ('Cheat Saber', ['DIE'] + ['KILL'] * 7 + rd(0xA923, 6)),
        ('Ringo Shield', rd(0xA94B, 14)), ('Fire Ball (burn)', rd(0xA95B, 14)), ('Print Cutter', rd(0xA96B, 14)),
        ('Mega Buster x1', rd(0xA93B, 14)), ('Rider Kick', rd(0xA97B, 14)), ('Power Bomb', rd(0xA98B, 14))]
print('%-18s' % '' + ''.join('%8s' % b for b in BOSS))
for name, v in rows:
    print('%-18s' % name + ''.join('%8s' % ('-' if x == 0 else x) for x in v))
