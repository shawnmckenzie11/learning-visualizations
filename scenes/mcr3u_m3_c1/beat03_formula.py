"""Beat 3: boxed shortcut steps with m and d on the graph."""

from manim import *

from common import END_HOLD, STEP_HOLD, QuadraticSymmetryLayout


class Beat03Formula(Scene):
    """Build worksheet boxed steps for b = -10, c = 21."""

    def construct(self) -> None:
        layout = QuadraticSymmetryLayout(self)
        layout.build(title="Discover a shortcut")

        b, c = -10, 21
        layout.set_state(b, c, ghost_previous=False)
        self.wait(STEP_HOLD * 0.85)

        steps = VGroup()
        layout.reveal_boxed_step(r"m = -\frac{b}{2} = 5", steps, 0)
        layout.reveal_boxed_step(r"(m - d)(m + d) = c", steps, 1)
        layout.reveal_boxed_step(r"d = \sqrt{m^2 - c} = 2", steps, 2)
        layout.reveal_boxed_step(
            r"x = m \pm \sqrt{m^2 - c}",
            steps,
            3,
        )

        layout.show_question("When are the roots whole numbers?")
        self.wait(END_HOLD)
