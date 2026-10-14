# Learning Visualizations

Manim **Community Edition** scenes for calm, precise learning visuals.

> This project uses [Manim Community](https://www.manim.community/) (`ManimCommunity/manim`), not ManimGL (`3b1b/manim`).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

System packages (Debian/Ubuntu example): `ffmpeg`, `libcairo2-dev`, `libpango1.0-dev`, `python3-dev`, and a LaTeX install for `MathTex`.

## Render an example

From the repo root:

```bash
# low-quality smoke render (fast)
manim -ql scenes/examples/hello_circle.py HelloCircle

# higher quality (720p configured in manim.cfg)
manim -qm scenes/examples/hello_circle.py HelloCircle
```

Outputs land under `media/` (gitignored). Committed preview renders for MCK-209 live under `renders/`.

## MCR3U M3 C1 — Quadratic symmetry (MCK-209)

Scenes in `scenes/mcr3u_m3_c1/`:

| Scene | File | Beat |
|-------|------|------|
| `Beat01RootsNext` | `beat01_roots_next.py` | Lower `c` with `b = -10` (includes `c = 20`) |
| `Beat02WholeRoots` | `beat02_whole_roots.py` | Vary `b` with `c = 24` |
| `Beat03Formula` | `beat03_formula.py` | Mark `m`, `d`, worksheet boxed shortcut steps |
| `Beat04GoldFrame` | `beat04_gold_frame.py` | Silent gold summary frame |

Render all four:

```bash
bash scripts/render_mcr3u_m3_c1.sh
```

## Layout

- `scenes/examples/` — small demo scenes
- `scenes/mcr3u_m3_c1/` — MCK-209 quadratic symmetry clips
- `renders/` — checked-in MP4 outputs (when present)

## Docs

- Community docs: https://docs.manim.community/
