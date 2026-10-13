"""Beat 4: silent summary — stacked parabolas and gold root lattice."""

from manim import *

from common import (
    END_HOLD,
    GOLD,
    INK,
    PARABOLA_BLUE,
    PARABOLA_GHOST,
    STEP_HOLD,
    X_RANGE,
    QuadraticSymmetryLayout,
    m_from_b,
    root_pair,
)


class Beat04GoldFrame(Scene):
    """Final gold frame with no on-screen words."""

    def construct(self) -> None:
        layout = QuadraticSymmetryLayout(self)
        layout.build(show_panel=False)

        b = -10
        c_steps = [25, 24, 21, 16, 9]
        layout.set_state(b, c_steps[0], ghost_previous=False)
        self.wait(STEP_HOLD * 0.5)

        for c in c_steps[1:]:
            layout.animate_to(b, c, run_time=0.6)
            self.wait(STEP_HOLD * 0.35)

        # Layer additional parabolas for the summary look (frame 4 mockup).
        assert layout.axes is not None
        extra_pairs = [(-11, 24), (-14, 24)]
        for eb, ec in extra_pairs:
            ghost = layout.parabola_graph(
                eb, ec, color=PARABOLA_GHOST, width=3, opacity=0.45
            )
            layout.ghost_parabolas.add(ghost)
            self.add(ghost)

        # Integer root dots x = 1 … 9 on the axis; emphasize the c = 21 pair.
        dots = VGroup()
        for x in range(1, 10):
            dot = Dot(layout.axes.c2p(x, 0), color=GOLD, radius=0.07)
            dots.add(dot)

        highlight_roots = root_pair(b, 21)
        rings = VGroup()
        for r in highlight_roots:
            ring = Circle(radius=0.16, color=INK, stroke_width=3)
            ring.move_to(layout.axes.c2p(r, 0))
            rings.add(ring)

        self.play(FadeIn(dots, lag_ratio=0.08), FadeIn(rings), run_time=1.2)
        self.wait(END_HOLD)
