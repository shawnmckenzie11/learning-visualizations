"""Beat 1: lower c with b fixed at -10; roots march outward."""

from manim import *

from common import END_HOLD, STEP_HOLD, QuadraticSymmetryLayout


class Beat01RootsNext(Scene):
    """Animate c stepping down while b = -10; end with the beat question."""

    def construct(self) -> None:
        layout = QuadraticSymmetryLayout(self)
        layout.build()

        b = -10
        c_values = [25, 24, 21, 16, 9]

        layout.set_state(b, c_values[0], ghost_previous=False)
        self.wait(STEP_HOLD)

        for c in c_values[1:]:
            layout.animate_to(b, c, run_time=0.85)
            self.wait(STEP_HOLD)

        layout.show_question("Where are the roots next?")
        self.wait(END_HOLD)
