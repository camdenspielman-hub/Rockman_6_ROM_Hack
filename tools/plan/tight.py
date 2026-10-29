#!/usr/bin/env python3
"""critic-scope: the proposed TIGHT Must (v1.0) with reduced-scope session estimates per item."""
tight = {
 'tech': [  # round 2: docs/design/tech.md "v1.0 scope" (43 items by milestone, RULINGS R1.1-R1.14); was 98, now 102:
            # +2.5 fight loader (moved here from meta, R1.7), +2 OAM-builder lag steps (R1.8), +1 $9B audit (R1.12),
            # -1.5 F-SIZES (Should, R3.6)
  ('M0: MMC5 go/no-go spike on Mesen', 1.5), ('M0: workbench, registry, bank/WORK ledgers, test runner, golden record', 4),
  ('M0: reassemblable fixed banks + sound driver', 3), ('M0: round trips + censuses ($51/$063D/$9B, damage steps) + stagetab', 4),
  ('M1: insertion, header, RESET, stubs, re-entrant CW, FAR', 2.5), ('M1: helpers (vanilla A), sound service, mirroring', 2),
  ('M1: IRQ literal port + calibration', 3.5), ('M1: shadow6 MMC5 + golden equivalence', 2.5),
  ('M1: PRG-RAM, ram_probe, save skeleton, mailbox, Mesen, lag baseline', 2.5),
  ('M2: stage record v0 + init hook + $CE44 on id change', 1), ('M2: WRAM layouts + slot loader + poke tiers + map-edit service', 3),
  ('M2: families + object lists v2 + slot plan', 3), ('M2: CHR set table v2', 2),
  ('M2: art pipeline chr/sprites/palettes/artcheck', 5), ('M2: level pipeline + free-id scan', 3),
  ('M2: raster list (24 bands) + presets + IRQ logic move', 4),
  ('M2: text v1a (glyph cache, compiler + dictionary, pop-ups, debrief/help)', 3.5),
  ('M2: sound driver ext + mml compile + D9 mute mask', 4), ('M2: DEV build / EXTRA CONFIG engine / DEV combos', 1.5),
  ('M2: CHR stream (ROM copier, staging) + lag steps 1, 5', 1.5),
  ('M3: LATCHSRC + frozen handlers + LFSR + death audit', 1.5), ('M3: T6 + X-BONK', 2.5), ('M3: player states + X-WRAP', 1),
  ('M3: HUD widget module', 2), ('M3: commentator bus', 2.5), ('M3: OAM-builder lag steps 3-4 + cap re-measure (R1.8)', 2),
  ('M5: attribute-table readers + ids $10-$21', 3), ('M5: T3', 2.5), ('M5: T7', 2), ('M5: T8', 2),
  ('M5: attach state (T5 vines, balloon, condor)', 2), ('M5: X-EXWP', 1.5), ('M5: boss panel ext', 1.5),
  ('M5: pattern-table split', 1),
  ('M6: text v1b (dialogue, ROM restore, choices, NPC menus)', 2.5), ('M6: T1-lite', 3), ('M6: vehicle state', 1.5),
  ('M6: palette-flash / lighting service', 1.5),
  ('M7: bgboss.py', 2), ('M7: fight loader + FIGHT_CTX + return-to snapshot (from meta, R1.7)', 2.5), ('M7: F-PIECES', 2.5),
  ('M7: $9B tables with a 4th row (R1.12)', 1), ('M8: 8-band floor (W3)', 1.5),
 ],
 'systems': [  # round 2: docs/design/systems.md "v1.0 scope" (RULINGS R2.1-R2.11); was 46.5, now 49.5
  ('SELECT + toggle + input rules', 2), ('quick form swap + slot-set map', 3), ('forms fire taps', 2), ('adaptors by wins', 1),
  ('Ice Block alt (slice)', 1.5), ('frozen tick (handlers + boss stall)', 2.5), ('GP_BOSSHIT', 2.5), ('mook rules', 1),
  ('WEAK! + flash safety', 2), ('attribution (LATCHSRC)', 2.5), ('scorecard', 3), ('economy/shop', 2), ('chip framework', 2),
  ('5 shop chips + Balancer', 2), ('8 venue chips', 3), ('pickups', 2), ('presets + CASUAL levers + INPUT LAG', 3),
  ('tap tweaks (costs, dark rooms)', 0.5), ('plates/Beat', 2), ('HARD framework', 1.5), ('SC1,5,6,8,9,11', 3.5),
  ('M.BEAM (max 2)', 2), ('Super fist (+hop)', 3),
 ],
 'meta': [  # round 2: docs/design/meta.md "v1.0 scope" (16 Must items, RULINGS R0.2-R0.4); total unchanged at 31:
            # the fight loader (2.5) moved to 'tech' (R1.7); +0.5 RULESET + bits.inc, +0.5 fight table data + interface,
            # -0.5 title (attract crawl and PASS WORD gag are Could), -0.5 fortress maps (bracket node renderer reused)
  ('M2: saves (A/B, trailer, migrations, BROKEN paths, autosaves, unplug, save tests)', 3.5),
  ('M2: title + boot (license line, health notice, menu)', 1.5), ('M2: file select + NEW/ERASE + difficulty pick', 2.5),
  ('M2/M5/M6: bracket (nodes, states, centre, rematch hook, Riot trigger, event queue)', 4),
  ('M2: results screen (judges desk)', 2.5), ('M2: debrief engine + predicates (tier B) + stage counters', 2),
  ('M2: medals/HoF + unlock bits', 1), ('M2: RULESET + bits.inc', 0.5), ('M2: CONFIG (INPUT LAG, CASUAL, FLASHES)', 1.5),
  ('M2/M7: EXTRA CONFIG UI + mailbox (+ FIGHT n at M7)', 3),
  ('M3: pit stop (shop, 14-chip grid + help, file CONFIG)', 2.5), ('M3: game over/RETIRE/unplug', 1.5),
  ('M6: RECORDS 1-3 + venue mini-records', 1.5), ('M7: fight table v1.0 rows + loader interface (loader is tech)', 0.5),
  ('M7: fortress maps + BACK TO BRACKET', 1.5), ('M8: rating (re-derived, 100 reachable, R2.7) + Break Man debrief', 1.5),
 ],
 'venues': [  # core homage + secret exit + hidden room + behaviour chip + boss rework; arena twists -> Should
  ('Wind (sortie w/o destroyer; AYACO simple)', 14), ('Knight (no Inn/Princess)', 14), ('Tomahawk (train 3 bands)', 14),
  ('Plant', 14), ('Blizzard (v0.1 slice: ladder stubs, no ski; + SNOW CHAINS, replay skip, Ice Block tests)', 13.5),
  ('Flame (+ mouse room, FIREPROOF; no chompers/skeleton/throne shadow)', 13),
  ('Centaur (tidal shaft, + CENTURION; no Reap-bot/Mage/spring)', 13.5),
  ('Yamato (trimmed: + Daruma/DARUMA, the draft; no sekisho/kites/nightingale/kabuki)', 13),
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
