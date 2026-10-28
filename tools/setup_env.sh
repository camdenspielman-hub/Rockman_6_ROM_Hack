#!/usr/bin/env bash
# Python-only toolchain. In the Claude cloud container, GitHub downloads are
# blocked by the proxy (HTTP 403) but PyPI works, so everything comes from pip.
set -euo pipefail
LIB="$(cd "$(dirname "$0")/.." && pwd)/.pylib"
pip3 install -q --target "$LIB" py65 ophis-asm cynes numpy pillow
# stable-retro bundles the FCEUmm libretro core (MMC5 + CHR-RAM + battery OK).
# --no-deps: we load its native module directly and skip gymnasium.
pip3 install -q --no-deps --target "$LIB" stable-retro
echo "toolchain installed in $LIB"
