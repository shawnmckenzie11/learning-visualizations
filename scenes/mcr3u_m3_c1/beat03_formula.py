"""Beat 3: mark m and d, display the root formula."""

from manim import *

from common import END_HOLD, STEP_HOLD, QuadraticSymmetryLayout


class Beat03Formula(Scene):
    """Build symmetry markers and the large root formula for b = -10, c = 21."""

    def construct(self) -> None:
        layout = QuadraticSymmetryLayout(self)
        layout.build(show_formula=True)

        b, c = -10, 21
        layout.set_state(
            b,
            c,
            ghost_previous=False,
            show_d_markers=False,
        )
        self.wait(STEP_HOLD)

        layout.animate_to(
            b,
            c,
            show_d_markers=True,
            ghost_previous=False,
            run_time=1.0,
        )
        self.wait(STEP_HOLD)

        layout.show_question("When are the roots whole numbers?")
        self.wait(END_HOLD)
