"""Beat 2: fixed c = 24, vary b to hunt integer roots."""

from manim import *

from common import END_HOLD, STEP_HOLD, QuadraticSymmetryLayout


class Beat02WholeRoots(Scene):
    """Step b through values that mix integer and non-integer root pairs."""

    def construct(self) -> None:
        layout = QuadraticSymmetryLayout(self)
        layout.build()

        c = 24
        # -25 dropped: m = 12.5 and a root at 24 lies outside x in [0, 14].
        b_values = [-10, -11, -14]

        layout.set_state(b_values[0], c, ghost_previous=False)
        self.wait(STEP_HOLD)

        for b in b_values[1:]:
            layout.animate_to(b, c, run_time=0.85)
            self.wait(STEP_HOLD)

        layout.show_question("Which b gives whole-number roots?")
        self.wait(END_HOLD)
