# Rockman CX: graphics survey

Agent: cx-graphics. Build: `roms/cx_en.nes` (EN v1.1), compared against `roms/rm2j.nes` (vanilla Rockman 2 J).
Scripts: `build/research/cx/cx-graphics/` (see "Method" at the end). Status: **in progress**, extended as work goes.

## 1. Where the art lives (ROM map)

CX, like RM2, has **CHR-RAM**: every tile is stored uncompressed in PRG and copied to the PPU. The PPU runs with
`$2000 = $90`: BG from pattern table `$1000`, sprites from `$0000`, 8x8 sprites [seen: every state].

**Live CHR layout during play** (from 89 savestates, each tile traced back to its ROM offset) [seen]:

| CHR tiles | Contents | Source |
|---|---|---|
| `$000-$08F` | player: fake Rockman, or Quick Man | `0x01000` (bank `$00`), Quick Man `0x4E900` (bank `$27`) |
| `$090-$09C` | weapon shots and common sprites | `0x23F00` (bank `$11`) |
| `$0A0-$0FF` | six 16-tile enemy pages, swapped per room | any stage bank, plus new banks `$2A`, `$2B`, `$39` |
| `$100-$15F` | common BG (HUD, ladders, items) | `0x24100` (bank `$12`) |
| `$160-$1FF` | stage tileset | the stage's own bank, offset `+$2000` |

(rest of the doc follows below as sections are filled in)
