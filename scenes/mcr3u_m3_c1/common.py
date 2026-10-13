"""Shared layout, styling, and math helpers for quadratic symmetry clips."""

from __future__ import annotations

import math
from typing import Iterable, List, Optional, Tuple

from manim import *

# Real-slice palette (LLOVES School m1c1-c1-real-slice.html)
BG_COLOR = "#070b14"
INK = "#e8eef8"
MUTED = "#5a6d85"
GOLD = "#f5c518"
PARABOLA_BLUE = "#3d8bfd"
PARABOLA_GHOST = "#1a4a8a"
GRID_COLOR = "#1e3a5f"
BAND_COLOR = "#03060c"

FONT_SIZE = 40
FORMULA_FONT_SIZE = 38
LABEL_FONT_SIZE = 36
STROKE_WIDTH = 4
PARABOLA_WIDTH = 5
GHOST_OPACITY = 0.35

STEP_HOLD = 1.5
END_HOLD = 3.0

X_RANGE = (0, 14)
Y_RANGE = (-10, 10)
TICK_STEP = 2


def m_from_b(b: float) -> float:
    """Return the axis-of-symmetry coordinate m = -b/2."""
    return -b / 2


def d_from_b_c(b: float, c: float) -> float:
    """Return d = sqrt(m^2 - c); assumes real roots."""
    m = m_from_b(b)
    return math.sqrt(max(0.0, m * m - c))


def discriminant(b: float, c: float) -> float:
    """Return b^2 - 4c."""
    return b * b - 4 * c


def is_perfect_square(n: float, tol: float = 1e-9) -> bool:
    """Return True if n is a non-negative perfect square (within tolerance)."""
    if n < -tol:
        return False
    r = math.isqrt(int(round(n)))
    return abs(r * r - n) < tol


def roots_are_integers(b: float, c: float) -> bool:
    """True when both roots of x^2+bx+c=0 are integers."""
    d = discriminant(b, c)
    if d < 0:
        return False
    return is_perfect_square(d)


def root_pair(b: float, c: float) -> Tuple[float, float]:
    """Return the two roots m-d and m+d."""
    m = m_from_b(b)
    d = d_from_b_c(b, c)
    return m - d, m + d


def d_is_whole_number(b: float, c: float) -> bool:
    """True when d is a whole number (not merely when roots are integers)."""
    d = d_from_b_c(b, c)
    return abs(d - round(d)) < 1e-9


def format_num(x: float) -> str:
    """Format a number for on-screen labels."""
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return f"{x:g}"


class QuadraticSymmetryLayout:
    """Fixed graph (left) + live panel (right) shared across all beats."""

    def __init__(self, scene: Scene) -> None:
        self.scene = scene
        self.axes: Optional[Axes] = None
        self.panel_lines: dict[str, Text] = {}
        self.formula: Optional[MathTex] = None
        self.symmetry_line: Optional[DashedLine] = None
        self.m_label: Optional[Text] = None
        self.root_dots: VGroup = VGroup()
        self.d_markers: VGroup = VGroup()
        self.ghost_parabolas: VGroup = VGroup()
        self.active_parabola: Optional[ParametricFunction] = None
        self.question_band: Optional[VGroup] = None

    def build(self, show_formula: bool = False, show_panel: bool = True) -> None:
        """Create axes, panel shell, and optional formula slot."""
        scene = self.scene
        scene.camera.background_color = BG_COLOR

        axes = Axes(
            x_range=[X_RANGE[0], X_RANGE[1], TICK_STEP],
            y_range=[Y_RANGE[0], Y_RANGE[1], TICK_STEP],
            x_length=7.6,
            y_length=5.6,
            axis_config={
                "color": MUTED,
                "stroke_width": 2,
                "include_tip": False,
                "font_size": 28,
            },
            tips=False,
        )
        axes.set_color(MUTED)

        grid = NumberPlane(
            x_range=[X_RANGE[0], X_RANGE[1], TICK_STEP],
            y_range=[Y_RANGE[0], Y_RANGE[1], TICK_STEP],
            x_length=axes.x_length,
            y_length=axes.y_length,
            background_line_style={
                "stroke_color": GRID_COLOR,
                "stroke_width": 1,
                "stroke_opacity": 0.55,
            },
            axis_config={"stroke_opacity": 0},
        )
        graph_group = VGroup(grid, axes)
        graph_group.move_to(LEFT * 2.15 + UP * 0.35)
        self.axes = axes

        panel_lines: dict[str, Text] = {}
        formula = None
        if show_panel:
            panel_x = RIGHT * 4.35 + UP * 1.2
            labels = ("b", "c", "m", "d")
            for i, key in enumerate(labels):
                line = Text(
                    f"{key} = —",
                    font_size=FONT_SIZE,
                    color=INK,
                    weight=BOLD,
                )
                line.move_to(panel_x + DOWN * i * 0.85)
                panel_lines[key] = line
            self.panel_lines = panel_lines

            if show_formula:
                formula = MathTex(
                    r"x = m \pm \sqrt{m^2 - c}",
                    font_size=FORMULA_FONT_SIZE,
                    color=INK,
                )
                formula.move_to(panel_x + DOWN * 3.6)
                self.formula = formula

            scene.add(*panel_lines.values())
            if formula:
                scene.add(formula)

        scene.add(graph_group)

    def parabola_graph(
        self,
        b: float,
        c: float,
        color=PARABOLA_BLUE,
        width=PARABOLA_WIDTH,
        opacity: float = 1.0,
    ):
        """Return a parabola y = x^2 + bx + c clipped to the visible x-range."""
        assert self.axes is not None
        graph = self.axes.plot(
            lambda x: x * x + b * x + c,
            x_range=[X_RANGE[0], X_RANGE[1]],
            color=color,
            stroke_width=width,
        )
        graph.set_stroke(opacity=opacity)
        return graph

    def _update_symmetry(self, b: float) -> VGroup:
        """Build dashed symmetry line and m label at x = m."""
        assert self.axes is not None
        m = m_from_b(b)
        y0 = Y_RANGE[0]
        y1 = Y_RANGE[1]
        line = DashedLine(
            self.axes.c2p(m, y0),
            self.axes.c2p(m, y1),
            color=INK,
            stroke_width=3,
            dash_length=0.12,
        )
        m_label = Text("m", font_size=LABEL_FONT_SIZE, color=INK, weight=BOLD)
        m_label.move_to(self.axes.c2p(m, y1) + UP * 0.35)
        return VGroup(line, m_label)

    def _root_dots(self, b: float, c: float) -> VGroup:
        """Gold dots on the x-axis when roots are integers; else muted dots."""
        assert self.axes is not None
        r1, r2 = root_pair(b, c)
        gold = roots_are_integers(b, c)
        color = GOLD if gold else MUTED
        dots = VGroup()
        for r in (r1, r2):
            if X_RANGE[0] <= r <= X_RANGE[1]:
                dot = Dot(self.axes.c2p(r, 0), color=color, radius=0.09)
                dot.set_stroke(INK if not gold else GOLD, width=2)
                dots.add(dot)
        return dots

    def _d_brackets(self, b: float, c: float) -> VGroup:
        """Horizontal double-arrows from m to each root, labeled d (gold if d is whole)."""
        assert self.axes is not None
        m = m_from_b(b)
        d = d_from_b_c(b, c)
        gold = d_is_whole_number(b, c)
        color = GOLD if gold else INK
        group = VGroup()
        for sign in (-1, 1):
            r = m + sign * d
            if not (X_RANGE[0] <= r <= X_RANGE[1]):
                continue
            start = self.axes.c2p(m, 0.35)
            end = self.axes.c2p(r, 0.35)
            arrow = DoubleArrow(
                start,
                end,
                color=color,
                stroke_width=3,
                buff=0,
                max_tip_length_to_length_ratio=0.15,
            )
            lbl = Text("d", font_size=LABEL_FONT_SIZE, color=color, weight=BOLD)
            lbl.move_to((start + end) / 2 + UP * 0.25)
            group.add(arrow, lbl)
        return group

    def _panel_text(self, b: float, c: float) -> dict[str, Text]:
        """Build updated panel lines with correct d coloring."""
        m = m_from_b(b)
        d = d_from_b_c(b, c)
        d_gold = d_is_whole_number(b, c)
        lines = {}
        for key, val in (
            ("b", b),
            ("c", c),
            ("m", m),
            ("d", d),
        ):
            color = GOLD if key == "d" and d_gold else INK
            lines[key] = Text(
                f"{key} = {format_num(val)}",
                font_size=FONT_SIZE,
                color=color,
                weight=BOLD,
            )
        return lines

    def set_state(
        self,
        b: float,
        c: float,
        *,
        show_symmetry: bool = True,
        show_roots: bool = True,
        show_d_markers: bool = False,
        ghost_previous: bool = True,
    ) -> None:
        """Jump to a (b, c) state without animation."""
        scene = self.scene
        assert self.axes is not None

        if ghost_previous and self.active_parabola is not None:
            ghost = self.active_parabola.copy()
            ghost.set_stroke(color=PARABOLA_GHOST, opacity=GHOST_OPACITY, width=3)
            self.ghost_parabolas.add(ghost)
            scene.add(ghost)

        if self.active_parabola is not None:
            scene.remove(self.active_parabola)
        if self.symmetry_line is not None:
            scene.remove(self.symmetry_line)
        if self.root_dots:
            scene.remove(self.root_dots)
        if self.d_markers:
            scene.remove(self.d_markers)

        self.active_parabola = self.parabola_graph(b, c)
        scene.add(self.active_parabola)

        if show_symmetry:
            self.symmetry_line = self._update_symmetry(b)
            scene.add(self.symmetry_line)

        if show_roots:
            self.root_dots = self._root_dots(b, c)
            scene.add(self.root_dots)

        if show_d_markers:
            self.d_markers = self._d_brackets(b, c)
            scene.add(self.d_markers)

        if self.panel_lines:
            panel_x = RIGHT * 4.35 + UP * 1.2
            new_lines = self._panel_text(b, c)
            for key, mobj in new_lines.items():
                mobj.move_to(panel_x + DOWN * list(self.panel_lines.keys()).index(key) * 0.85)
                if key in self.panel_lines:
                    scene.remove(self.panel_lines[key])
                self.panel_lines[key] = mobj
                scene.add(mobj)

    def animate_to(
        self,
        b: float,
        c: float,
        *,
        show_symmetry: bool = True,
        show_roots: bool = True,
        show_d_markers: bool = False,
        ghost_previous: bool = True,
        run_time: float = 0.8,
    ) -> None:
        """Animate from the current parabola/panel to a new (b, c)."""
        scene = self.scene
        assert self.axes is not None

        new_curve = self.parabola_graph(b, c)
        new_sym = self._update_symmetry(b) if show_symmetry else VGroup()
        new_roots = self._root_dots(b, c) if show_roots else VGroup()
        new_d = self._d_brackets(b, c) if show_d_markers else VGroup()
        new_panel = self._panel_text(b, c)
        if self.panel_lines:
            panel_x = RIGHT * 4.35 + UP * 1.2
            for i, key in enumerate(self.panel_lines):
                new_panel[key].move_to(panel_x + DOWN * i * 0.85)

        anims: List = []
        if self.active_parabola is not None:
            if ghost_previous:
                ghost = self.active_parabola.copy()
                ghost.set_stroke(color=PARABOLA_GHOST, opacity=GHOST_OPACITY, width=3)
                self.ghost_parabolas.add(ghost)
                scene.add(ghost)
            anims.append(Transform(self.active_parabola, new_curve))
        else:
            self.active_parabola = new_curve
            scene.add(new_curve)

        if show_symmetry:
            if self.symmetry_line is None:
                self.symmetry_line = new_sym
                scene.add(new_sym)
            else:
                anims.append(Transform(self.symmetry_line, new_sym))

        if show_roots:
            if len(self.root_dots) == 0:
                self.root_dots = new_roots
                scene.add(new_roots)
            else:
                anims.append(Transform(self.root_dots, new_roots))

        if show_d_markers:
            if len(self.d_markers) == 0:
                self.d_markers = new_d
                scene.add(new_d)
            else:
                anims.append(Transform(self.d_markers, new_d))

        for key in self.panel_lines:
            anims.append(Transform(self.panel_lines[key], new_panel[key]))

        if anims:
            scene.play(*anims, run_time=run_time)

    def show_question(self, text: str) -> VGroup:
        """Reveal the bottom question band (final frame only)."""
        if self.question_band is not None:
            self.scene.remove(self.question_band)
        band_h = 0.95
        band = Rectangle(
            width=config.frame_width,
            height=band_h,
            fill_color=BAND_COLOR,
            fill_opacity=1,
            stroke_width=0,
        )
        band.to_edge(DOWN, buff=0)
        q = Text(text, font_size=FONT_SIZE, color=INK, weight=BOLD)
        q.move_to(band.get_center())
        group = VGroup(band, q)
        self.question_band = group
        self.scene.add(group)
        return group
