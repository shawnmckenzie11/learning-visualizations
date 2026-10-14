#!/usr/bin/env bash
# Render MCK-209 quadratic symmetry clips at 720p medium quality.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export PATH="${HOME}/.local/bin:${PATH}"
cd "$ROOT"
mkdir -p renders/mcr3u_m3_c1

SCENES=(
  "scenes/mcr3u_m3_c1/beat01_roots_next.py:Beat01RootsNext"
  "scenes/mcr3u_m3_c1/beat02_whole_roots.py:Beat02WholeRoots"
  "scenes/mcr3u_m3_c1/beat03_formula.py:Beat03Formula"
  "scenes/mcr3u_m3_c1/beat04_gold_frame.py:Beat04GoldFrame"
)

for entry in "${SCENES[@]}"; do
  file="${entry%%:*}"
  cls="${entry##*:}"
  manim -qm "$file" "$cls"
  src="media/videos/$(basename "$file" .py)/720p30/${cls}.mp4"
  cp "$src" "renders/mcr3u_m3_c1/${cls}.mp4"
done

echo "Rendered clips copied to renders/mcr3u_m3_c1/"
