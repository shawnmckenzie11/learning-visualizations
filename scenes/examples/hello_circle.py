"""Minimal Manim Community smoke-test scene."""

from manim import *


class HelloCircle(Scene):
    """A calm intro: title + circle draw."""

    def construct(self):
        title = Text("Learning visualizations", font_size=40)
        title.to_edge(UP)
        circle = Circle(radius=1.5, color=BLUE)
        label = Text("Hello, Manim", font_size=28).next_to(circle, DOWN)

        self.play(Write(title))
        self.play(Create(circle))
        self.play(FadeIn(label))
        self.wait(1)
