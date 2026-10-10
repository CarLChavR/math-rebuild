"""
core/manim_helpers.py — Reusable Manim scene templates.

No LaTeX required. Uses Text instead of MathTex, and
number lines without auto-numbering (numbers drawn as Text).
"""


def number_line_scene(value: int, min_val: int = -10, max_val: int = 10) -> tuple[str, str]:
    """Number line with a moving dot pointing at `value` (no LaTeX)."""
    scene_class = "NumberLineDemo"
    code = f'''
from manim import *

class {scene_class}(Scene):
    def construct(self):
        nl = NumberLine(
            x_range=[{min_val}, {max_val}, 1],
            length=10,
            include_numbers=False,
            include_ticks=True,
        )
        self.add(nl)

        # Manually add tick labels with Text (no LaTeX)
        for i in range({min_val}, {max_val} + 1):
            if i % 5 == 0:
                label = Text(str(i), font_size=20)
                label.next_to(nl.number_to_point(i), DOWN, buff=0.2)
                self.add(label)

        dot = Dot(color=YELLOW).scale(1.3)
        self.add(dot)
        self.wait(0.3)

        target_point = nl.number_to_point({value})
        self.play(dot.animate.move_to(target_point), run_time=1.5)
        self.wait(0.5)

        label = Text(str({value}), font_size=36, color=YELLOW)
        label.next_to(dot, UP, buff=0.3)
        self.play(Write(label))
        self.wait(1)
'''
    return code, scene_class


def two_numbers_scene(a: int, b: int, result: int,
                      min_val: int = -15, max_val: int = 15) -> tuple[str, str]:
    """Two numbers on a number line, then the result."""
    scene_class = "TwoNumbersDemo"
    code = f'''
from manim import *

class {scene_class}(Scene):
    def construct(self):
        nl = NumberLine(
            x_range=[{min_val}, {max_val}, 1],
            length=12,
            include_numbers=False,
            include_ticks=True,
        )
        self.add(nl)

        for i in range({min_val}, {max_val} + 1):
            if i % 5 == 0:
                label = Text(str(i), font_size=18)
                label.next_to(nl.number_to_point(i), DOWN, buff=0.2)
                self.add(label)

        dot_a = Dot(color=BLUE).scale(1.2)
        dot_b = Dot(color=RED).scale(1.2)
        dot_r = Dot(color=GREEN).scale(1.5)

        dot_a.move_to(nl.number_to_point({a}))
        dot_b.move_to(nl.number_to_point({b}))
        dot_r.move_to(nl.number_to_point(0))

        self.play(FadeIn(dot_a), FadeIn(dot_b), run_time=0.8)
        self.wait(0.3)

        label_a = Text(str({a}), font_size=28, color=BLUE).next_to(dot_a, UP, buff=0.3)
        label_b = Text(str({b}), font_size=28, color=RED).next_to(dot_b, UP, buff=0.3)
        self.play(Write(label_a), Write(label_b))
        self.wait(0.5)

        if {a} != {result}:
            arrow = Arrow(
                start=nl.number_to_point({a}),
                end=nl.number_to_point({result}),
                buff=0.1,
                color=GREEN,
                stroke_width=4,
            )
            self.play(Create(arrow), run_time=1)

        self.play(
            dot_r.animate.move_to(nl.number_to_point({result})),
            run_time=1,
        )
        label_r = Text("= " + str({result}), font_size=32, color=GREEN)
        label_r.next_to(dot_r, DOWN, buff=0.3)
        self.play(Write(label_r))
        self.wait(1.5)
'''
    return code, scene_class


def fraction_bar_scene(numerator: int, denominator: int) -> tuple[str, str]:
    """Bar split into `denominator` parts, `numerator` filled."""
    scene_class = "FractionBarDemo"
    code = f'''
from manim import *

class {scene_class}(Scene):
    def construct(self):
        n = {numerator}
        d = {denominator}

        parts = VGroup()
        for i in range(d):
            rect = Rectangle(width=1.0, height=0.8, stroke_width=3, color=WHITE)
            parts.add(rect)
        parts.arrange(RIGHT, buff=0)

        fills = VGroup()
        for i in range(d):
            if i < n:
                fill = Rectangle(
                    width=1.0, height=0.8,
                    stroke_width=0, fill_color=YELLOW, fill_opacity=0.7,
                )
            else:
                fill = Rectangle(
                    width=1.0, height=0.8,
                    stroke_width=0, fill_color=BLACK, fill_opacity=0,
                )
            fills.add(fill)
        fills.arrange(RIGHT, buff=0)
        fills.align_to(parts, LEFT)
        fills.align_to(parts, UP)

        self.play(Create(parts))
        self.wait(0.3)
        self.play(FadeIn(fills))
        self.wait(0.5)

        frac = Text(str(n) + "/" + str(d), font_size=48).next_to(parts, DOWN, buff=0.8)
        self.play(Write(frac))
        self.wait(1.5)
'''
    return code, scene_class