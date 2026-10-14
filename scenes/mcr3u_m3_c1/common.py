"""Shared layout, styling, and math helpers for quadratic symmetry clips."""

from __future__ import annotations

import math
from typing import List, Optional, Tuple

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
BOX_STROKE = "#f5c518"

MIN_FONT = 32
FONT_SIZE = 36
PANEL_FONT = 34
STATS_FONT = 32
FORMULA_FONT_SIZE = 38
LABEL_FONT_SIZE = 36
GRAPH_LABEL_FONT = 32
TITLE_FONT = 34
STROKE_WIDTH = 4
PARABOLA_WIDTH = 5
GHOST_OPACITY = 0.35

STEP_HOLD = 1.35
END_HOLD = 2.8

X_RANGE = (0, 14)
Y_RANGE = (-10, 10)
TICK_STEP = 2

PANEL_ANCHOR = RIGHT * 4.2 + UP * 0.55
GRAPH_SHIFT = LEFT * 2.1 + DOWN * 0.15


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


def vertex_y(b: float, c: float) -> float:
    """Return the y-coordinate of the parabola vertex."""
    m = m_from_b(b)
    return m * m + b * m + c


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
    text = f"{x:.4g}"
    return text


def _sign_term(coeff: float, var: str = "x", first: bool = False) -> str:
    """Build a LaTeX term for a polynomial part."""
    if abs(coeff) < 1e-9:
        return ""
    sign = "+" if coeff > 0 and not first else "-"
    mag = abs(coeff)
    if var == "":
        body = format_num(mag)
    elif mag == 1:
        body = var
    else:
        body = f"{format_num(mag)}{var}"
    if first:
        return body if coeff > 0 else f"-{body}"
    return f" {sign} {body}"


def standard_form_latex(b: float, c: float) -> str:
    """LaTeX for x^2 + bx + c with readable signs."""
    parts = [r"x^2"]
    parts.append(_sign_term(b, "x"))
    parts.append(_sign_term(c, "", first=False))
    return "".join(parts).replace("+ -", "- ")


def factored_form_latex(b: float, c: float) -> Optional[str]:
    """LaTeX for factored form, or None when roots are complex."""
    if discriminant(b, c) < 0:
        return None
    r1, r2 = root_pair(b, c)
    if roots_are_integers(b, c):
        def factor(r: float) -> str:
            if r > 0:
                return f"(x - {format_num(r)})"
            if r < 0:
                return f"(x + {format_num(-r)})"
            return "(x)"
        return factor(r1) + factor(r2)
    # Exact real roots, non-integer: show decimal factors when concise.
    def factor(r: float) -> str:
        if abs(r) < 1e-9:
            return "(x)"
        if r > 0:
            return f"(x - {format_num(r)})"
        return f"(x + {format_num(-r)})"
    return factor(r1) + factor(r2)


def vertex_form_latex(b: float, c: float) -> str:
    """LaTeX for vertex form (x - m)^2 + k."""
    m = m_from_b(b)
    k = vertex_y(b, c)
    if m > 0:
        h_part = f"(x - {format_num(m)})^2"
    elif m < 0:
        h_part = f"(x + {format_num(-m)})^2"
    else:
        h_part = "x^2"
    if k > 0:
        return f"{h_part} + {format_num(k)}"
    if k < 0:
        return f"{h_part} - {format_num(-k)}"
    return h_part


def curve_equation_latex(b: float, c: float) -> str:
    """LaTeX for y = standard form."""
    return r"y = " + standard_form_latex(b, c)


class QuadraticSymmetryLayout:
    """Fixed graph (left) + live panel (right) shared across all beats."""

    def __init__(self, scene: Scene) -> None:
        self.scene = scene
        self.axes: Optional[Axes] = None
        self.x_numbers: Optional[VGroup] = None
        self.y_numbers: Optional[VGroup] = None
        self.panel_standard: Optional[MathTex] = None
        self.panel_factored: Optional[MathTex] = None
        self.panel_vertex: Optional[MathTex] = None
        self.panel_stats: Optional[Text] = None
        self.symmetry_line: Optional[VGroup] = None
        self.root_dots: VGroup = VGroup()
        self.d_markers: VGroup = VGroup()
        self.ghost_parabolas: VGroup = VGroup()
        self.active_parabola: Optional[VMobject] = None
        self.curve_label: Optional[MathTex] = None
        self.vertex_dot: Optional[Dot] = None
        self.vertex_label: Optional[MathTex] = None
        self.question_band: Optional[VGroup] = None
        self.title_band: Optional[VGroup] = None
        self._current_b: Optional[float] = None
        self._current_c: Optional[float] = None
        self.d_bracket_labels: bool = True

    def build(
        self,
        *,
        show_panel: bool = True,
        title: Optional[str] = None,
        d_bracket_labels: bool = True,
    ) -> None:
        """Create axes, optional title band, and optional right panel."""
        scene = self.scene
        scene.camera.background_color = BG_COLOR
        self.d_bracket_labels = d_bracket_labels

        if title:
            self._add_title_band(title)

        axes = Axes(
            x_range=[X_RANGE[0], X_RANGE[1], TICK_STEP],
            y_range=[Y_RANGE[0], Y_RANGE[1], TICK_STEP],
            x_length=7.35,
            y_length=5.15,
            axis_config={
                "color": MUTED,
                "stroke_width": 2,
                "include_tip": False,
                "include_numbers": False,
            },
            tips=False,
        )
        axes.set_color(MUTED)

        x_nums = axes.get_x_axis().add_numbers(
            range(X_RANGE[0], X_RANGE[1] + 1, TICK_STEP),
            font_size=STATS_FONT,
            color=MUTED,
        )
        y_nums = axes.get_y_axis().add_numbers(
            range(Y_RANGE[0], Y_RANGE[1] + 1, TICK_STEP),
            font_size=STATS_FONT,
            color=MUTED,
        )

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
        graph_group = VGroup(grid, axes, x_nums, y_nums)
        graph_group.move_to(GRAPH_SHIFT)
        self.axes = axes
        self.x_numbers = x_nums
        self.y_numbers = y_nums

        if show_panel:
            self.panel_standard = MathTex(r"x^2", font_size=PANEL_FONT, color=INK)
            self.panel_factored = MathTex(r"(x)", font_size=PANEL_FONT, color=INK)
            self.panel_vertex = MathTex(r"x^2", font_size=PANEL_FONT, color=INK)
            self.panel_stats = Text(
                "b = —   c = —   m = —   d = —",
                font_size=STATS_FONT,
                color=INK,
                weight=BOLD,
            )
            forms = VGroup(
                self.panel_standard,
                self.panel_factored,
                self.panel_vertex,
                self.panel_stats,
            )
            forms.arrange(DOWN, aligned_edge=LEFT, buff=0.38)
            forms.move_to(PANEL_ANCHOR)
            scene.add(forms)

        scene.add(graph_group)

    def _add_title_band(self, title: str) -> None:
        """Add a top title strip (beats 1–3)."""
        band_h = 0.72
        band = Rectangle(
            width=config.frame_width,
            height=band_h,
            fill_color=BAND_COLOR,
            fill_opacity=0.92,
            stroke_width=0,
        )
        band.to_edge(UP, buff=0)
        label = Text(title, font_size=TITLE_FONT, color=INK, weight=BOLD)
        label.move_to(band.get_center())
        self.title_band = VGroup(band, label)
        self.scene.add(self.title_band)

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
        y1 = Y_RANGE[1] - 0.5
        line = DashedLine(
            self.axes.c2p(m, y0),
            self.axes.c2p(m, y1),
            color=INK,
            stroke_width=3,
            dash_length=0.12,
        )
        m_label = Text("m", font_size=LABEL_FONT_SIZE, color=INK, weight=BOLD)
        m_label.move_to(self.axes.c2p(m, y1) + UP * 0.22)
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
                dot = Dot(self.axes.c2p(r, 0), color=color, radius=0.085)
                dot.set_stroke(INK if not gold else GOLD, width=2)
                dots.add(dot)
        return dots

    def _d_brackets(self, b: float, c: float, show_labels: bool = True) -> VGroup:
        """Horizontal brackets on the x-axis from m to each root (real roots only)."""
        assert self.axes is not None
        if discriminant(b, c) < 0:
            return VGroup()
        m = m_from_b(b)
        d = d_from_b_c(b, c)
        if d < 1e-9:
            return VGroup()
        gold = d_is_whole_number(b, c)
        color = GOLD if gold else INK
        group = VGroup()
        y_axis = 0.0
        for sign in (-1, 1):
            r = m + sign * d
            if not (X_RANGE[0] <= r <= X_RANGE[1]):
                continue
            start = self.axes.c2p(m, y_axis)
            end = self.axes.c2p(r, y_axis)
            arrow = DoubleArrow(
                start,
                end,
                color=color,
                stroke_width=3,
                buff=0,
                max_tip_length_to_length_ratio=0.15,
            )
            group.add(arrow)
            if show_labels:
                lbl = Text("d", font_size=LABEL_FONT_SIZE, color=color, weight=BOLD)
                lbl.move_to((start + end) / 2 + UP * 0.28)
                group.add(lbl)
        return group

    def _panel_mobjects(self, b: float, c: float) -> Tuple[MathTex, MathTex, MathTex, Text]:
        """Build the three forms and stats row for (b, c)."""
        std = MathTex(standard_form_latex(b, c), font_size=PANEL_FONT, color=INK)
        fac_tex = factored_form_latex(b, c)
        if fac_tex:
            fac = MathTex(fac_tex, font_size=PANEL_FONT, color=INK)
        else:
            fac = MathTex(r"\text{(not real)}", font_size=PANEL_FONT, color=MUTED)
        vtx = MathTex(vertex_form_latex(b, c), font_size=PANEL_FONT, color=INK)

        m = m_from_b(b)
        d = d_from_b_c(b, c)
        d_gold = d_is_whole_number(b, c)
        d_color = GOLD if d_gold else INK
        stats = Text(
            f"b = {format_num(b)}   c = {format_num(c)}   "
            f"m = {format_num(m)}   d = {format_num(d)}",
            font_size=STATS_FONT,
            color=INK,
            weight=BOLD,
        )
        # Color only the d segment by rebuilding with gold substring — use t2c on MathTex
        # for stats we keep one Text; highlight d via separate gold Text overlay is heavy.
        # Use MathTex for stats row for d coloring:
        stats = MathTex(
            f"b = {format_num(b)} \\quad c = {format_num(c)} \\quad "
            f"m = {format_num(m)} \\quad d = {format_num(d)}",
            font_size=STATS_FONT,
            color=INK,
        )
        stats.set_color_by_tex(f"d = {format_num(d)}", d_color)

        anchor = PANEL_ANCHOR
        std.move_to(anchor + UP * 1.35)
        fac.move_to(anchor + UP * 0.55)
        vtx.move_to(anchor + DOWN * 0.25)
        stats.move_to(anchor + DOWN * 1.05)
        return std, fac, vtx, stats

    def _graph_labels(self, b: float, c: float) -> Tuple[MathTex, VGroup]:
        """Curve label and vertex marker + coordinate label."""
        assert self.axes is not None
        m = m_from_b(b)
        vy = vertex_y(b, c)

        # Sample a point on the right arm for the y= label.
        x_arm = 11.5 if m < 7 else 10.0
        y_arm = x_arm * x_arm + b * x_arm + c
        curve = MathTex(
            curve_equation_latex(b, c),
            font_size=GRAPH_LABEL_FONT,
            color=INK,
        )
        curve_point = self.axes.c2p(x_arm, y_arm)
        curve.next_to(curve_point, UR, buff=0.08)

        # At c ≈ 20 the vertex sits higher and collides with the curve label — nudge.
        if -6 < vy < -3:
            curve.shift(DOWN * 0.35 + LEFT * 0.15)
        if vy > -4:
            curve.shift(DOWN * 0.25)

        dot = Dot(self.axes.c2p(m, vy), color=INK, radius=0.07)
        vlabel = MathTex(
            f"({format_num(m)},\\; {format_num(vy)})",
            font_size=GRAPH_LABEL_FONT,
            color=INK,
        )
        if vy >= -5:
            vlabel.next_to(dot, DOWN + LEFT, buff=0.12)
        else:
            vlabel.next_to(dot, UP + RIGHT, buff=0.12)

        return curve, VGroup(dot, vlabel)

    def _clear_graph_decor(self, scene: Scene) -> None:
        """Remove animated graph decorations."""
        for mob in (
            self.symmetry_line,
            self.curve_label,
            self.vertex_dot,
            self.vertex_label,
        ):
            if mob is not None:
                scene.remove(mob)
        if self.root_dots:
            scene.remove(self.root_dots)
        if self.d_markers:
            scene.remove(self.d_markers)

    def set_state(
        self,
        b: float,
        c: float,
        *,
        show_symmetry: bool = True,
        show_roots: bool = True,
        show_d_markers: bool = True,
        show_graph_labels: bool = True,
        ghost_previous: bool = True,
        d_bracket_labels: Optional[bool] = None,
    ) -> None:
        """Jump to a (b, c) state without animation."""
        scene = self.scene
        assert self.axes is not None
        self._current_b, self._current_c = b, c

        if ghost_previous and self.active_parabola is not None:
            ghost = self.active_parabola.copy()
            ghost.set_stroke(color=PARABOLA_GHOST, opacity=GHOST_OPACITY, width=3)
            self.ghost_parabolas.add(ghost)
            scene.add(ghost)

        if self.active_parabola is not None:
            scene.remove(self.active_parabola)
        self._clear_graph_decor(scene)

        self.active_parabola = self.parabola_graph(b, c)
        scene.add(self.active_parabola)

        if show_symmetry:
            self.symmetry_line = self._update_symmetry(b)
            scene.add(self.symmetry_line)

        if show_roots:
            self.root_dots = self._root_dots(b, c)
            scene.add(self.root_dots)

        if show_d_markers:
            label_d = (
                d_bracket_labels
                if d_bracket_labels is not None
                else self.d_bracket_labels
            )
            self.d_markers = self._d_brackets(b, c, show_labels=label_d)
            scene.add(self.d_markers)

        if show_graph_labels:
            self.curve_label, vtx_group = self._graph_labels(b, c)
            self.vertex_dot = vtx_group[0]
            self.vertex_label = vtx_group[1]
            scene.add(self.curve_label, vtx_group)

        if self.panel_standard is not None:
            std, fac, vtx, stats = self._panel_mobjects(b, c)
            for old, new in (
                (self.panel_standard, std),
                (self.panel_factored, fac),
                (self.panel_vertex, vtx),
                (self.panel_stats, stats),
            ):
                scene.remove(old)
            self.panel_standard, self.panel_factored = std, fac
            self.panel_vertex, self.panel_stats = vtx, stats
            scene.add(std, fac, vtx, stats)

    def animate_to(
        self,
        b: float,
        c: float,
        *,
        show_symmetry: bool = True,
        show_roots: bool = True,
        show_d_markers: bool = True,
        show_graph_labels: bool = True,
        ghost_previous: bool = True,
        d_bracket_labels: Optional[bool] = None,
        run_time: float = 0.75,
    ) -> None:
        """Animate from the current parabola/panel to a new (b, c)."""
        scene = self.scene
        assert self.axes is not None
        self._current_b, self._current_c = b, c

        new_curve = self.parabola_graph(b, c)
        new_sym = self._update_symmetry(b) if show_symmetry else VGroup()
        new_roots = self._root_dots(b, c) if show_roots else VGroup()
        label_d = (
            d_bracket_labels if d_bracket_labels is not None else self.d_bracket_labels
        )
        new_d = (
            self._d_brackets(b, c, show_labels=label_d) if show_d_markers else VGroup()
        )
        new_curve_lbl, new_vtx = (
            self._graph_labels(b, c) if show_graph_labels else (None, VGroup())
        )
        new_panel = self._panel_mobjects(b, c) if self.panel_standard else None

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

        if show_graph_labels and new_curve_lbl is not None:
            if self.curve_label is None:
                self.curve_label = new_curve_lbl
                self.vertex_dot = new_vtx[0]
                self.vertex_label = new_vtx[1]
                scene.add(new_curve_lbl, new_vtx)
            else:
                anims.append(Transform(self.curve_label, new_curve_lbl))
                anims.append(Transform(self.vertex_label, new_vtx[1]))
                anims.append(Transform(self.vertex_dot, new_vtx[0]))

        if new_panel and self.panel_standard:
            replacements = []
            for old, new in zip(
                (
                    self.panel_standard,
                    self.panel_factored,
                    self.panel_vertex,
                    self.panel_stats,
                ),
                new_panel,
            ):
                replacements.append(ReplacementTransform(old, new))
            self.panel_standard, self.panel_factored, self.panel_vertex, self.panel_stats = (
                new_panel
            )
            anims.extend(replacements)

        if anims:
            scene.play(*anims, run_time=run_time)

    def show_question(self, text: str) -> VGroup:
        """Reveal the bottom question band (final frame only)."""
        if self.question_band is not None:
            self.scene.remove(self.question_band)
        band_h = 0.88
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

    def reveal_boxed_step(self, latex: str, box_group: VGroup, index: int) -> VGroup:
        """Add one worksheet-style boxed formula step (beat 3)."""
        step = MathTex(latex, font_size=FORMULA_FONT_SIZE, color=INK)
        box = SurroundingRectangle(step, color=BOX_STROKE, buff=0.18, stroke_width=2)
        group = VGroup(step, box)
        anchor = LEFT * 3.85 + UP * (1.35 - index * 1.05)
        group.move_to(anchor, aligned_edge=LEFT)
        box_group.add(group)
        self.scene.play(FadeIn(group, shift=UP * 0.15), run_time=0.55)
        self.scene.wait(0.65)
        return group
