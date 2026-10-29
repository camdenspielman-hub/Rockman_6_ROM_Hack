#!/usr/bin/env python3
"""critic-scope: the proposed TIGHT Must (v1.0) with reduced-scope session estimates per item."""
tight = {
 'tech': [
  ('M0 workbench incl. reassemblable source, round trips, golden record', 11),
  ('MMC5 go/no-go spike on Mesen', 1.5),
  ('M1 MMC5 port + golden equivalence + PRG-RAM', 13),
  ('stage-attribute table + readers', 4), ('WRAM layouts + map_set', 3), ('families + object lists', 3),
  ('raster list + presets + IRQ logic move', 4), ('text engine v1 (caps VWF EN + kana JP, no portraits in stages)', 6),
  ('sound driver ext + mml compile + D9/D11', 4), ('level pipeline + canvas table', 3), ('DEV build / EXTRA CONFIG engine', 1.5),
  ('CHR stream + latch/frozen tick/LFSR/death audit', 3), ('CHR set table v2 (hidden today)', 2),
  ('art pipeline chr/sprites/palettes/artcheck/bgboss (hidden today)', 7),
  ('T3', 2.5), ('T6 + X-BONK', 2.5), ('T1-lite', 3), ('player states + X-WRAP', 2.5), ('T5', 2), ('T7', 2), ('T8', 2),
  ('HUD widget module (meter/label/clock/counters)', 2), ('X-EXWP', 1.5), ('F-PIECES', 2.5), ('F-SIZES (1-2 sizes only)', 1.5),
  ('8-band floor (W3)', 1.5), ('commentator bus', 2.5), ('boss panel ext', 1.5), ('lighting service', 1.5), ('pattern-table split', 1),
 ],
 'systems': [
  ('SELECT + toggle', 1.5), ('quick form swap', 2.5), ('forms fire taps', 2), ('adaptors by wins', 1), ('Super fist (+hop)', 3),
  ('tap tweaks', 1.5), ('M.BEAM', 2.5), ('GP_BOSSHIT', 2.5), ('frozen tick', 2.5), ('mook rules', 1), ('WEAK!', 1.5),
  ('SC1,5,6,8,9 only', 3), ('attribution', 2.5), ('scorecard', 3), ('economy/shop', 2), ('chip framework', 2),
  ('~6 shop chips + Balancer', 2), ('8 venue chips', 3), ('plates/Beat', 2), ('pickups', 2), ('presets', 2), ('HARD framework', 1.5),
 ],
 'meta': [
  ('saves', 3.5), ('title', 2), ('file select', 2.5), ('bracket', 4), ('results', 2.5), ('debrief (tier B only)', 2),
  ('pit stop', 2.5), ('game over/RETIRE', 1.5), ('medals/HoF', 1), ('rating (no TURBO trap) + debrief', 1.5),
  ('fortress maps', 2), ('fight loader', 2.5), ('RECORDS 1-3', 1.5), ('EXTRA CONFIG UI + mailbox', 3), ('CONFIG', 1.5),
 ],
 'venues': [  # core homage + secret exit + hidden room + behaviour chip + boss rework; arena twists -> Should
  ('Wind (sortie w/o destroyer; AYACO simple)', 14), ('Knight (no Inn/Princess)', 14), ('Tomahawk (train 3 bands)', 14),
  ('Plant', 14), ('Blizzard (ladder stubs, no ski)', 12), ('Flame (no skeleton/throne shadow)', 12),
  ('Centaur (no Reap-bot/Mage/spring)', 12), ('Yamato (no nightingale/Daruma/kabuki)', 12),
 ],
 'fortress': [
  ('Opening-lite (lanes + one-size mascot)', 8), ('Semifinal (2 reject types, NPC Break Man beats, Bass duel 1)', 10),
  ('H1', 9), ('H3 (Doc Robot via fight loader or cut)', 10), ('H5 (low-grav fallback, unmasking)', 9),
  ('W2', 8), ('W3 (8 bands, one machine size, escape without eras)', 11), ('ending + vanilla-style staff roll', 4),
 ],
 'overhead': [('user gates', 8), ('balance', 4), ('release/matrix', 4)],
}
total = 0
for area, items in tight.items():
    s = sum(x for _, x in items); total += s
    print(f'{area:9} {s:6.1f}')
print(f'{"CODE":9} {total:6.1f}')
art_tiles, art_frames = 3900, 350   # tight Must art after the cuts in the report
prog = art_tiles * 0.35 * 0.6       # ~60% of the 35% BG share assumed reuse/programmatic under the tight plan
art = (art_tiles*0.65 - prog*0)/80*0.66 + art_frames/12
print(f'art ~{art:.0f}  music ~10  text ~12')
print(f'TIGHT MUST TOTAL ~{total+art+10+12:.0f} sessions')
