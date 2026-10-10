"""
core/manim_helpers.py — Reusable Manim scene templates.

Each helper returns a tuple (scene_code: str, scene_class: str)
that can be passed directly to manim_runner.render_manim_scene().

The templates are self-contained strings. They do NOT import from
this module — everything the scene needs is inlined so the subprocess
can run them in isolation.
"""


# ---------------------------------------------------------------------------
# Helper 1: Number line with a marker
# ---------------------------------------------------------------------------
def number_line_scene(value: int, min_val: int = -10, max_val: int = 10) -> tuple[str, str]:
    """Animate a number line with a dot moving to `value`."""
    scene_class = "NumberLineDemo"
    code = f'''
from manim import *

class {scene_class}(Scene):
    def construct(self):
        nl = NumberLine(
            x_range=[{min_val}, {max_val}, 1],
            length=10,
            include_numbers=True,
            label_direction=DOWN,
            font_size=24,
        )
        self.add(nl)

        dot = Dot(color=YELLOW).scale(1.3)
        self.play(Create(dot))
        self.wait(0.3)

        target_point = nl.number_to_point({value})
        self.play(dot.animate.move_to(target_point), run_time=1.5)
        self.wait(0.5)

        label = MathTex(r"{value}").next_to(dot, UP, buff=0.3).set_color(YELLOW)
        self.play(Write(label))
        self.wait(1)
'''
    return code, scene_class


# ---------------------------------------------------------------------------
# Helper 2: Two numbers on a number line (for sum/difference)
# ---------------------------------------------------------------------------
def two_numbers_scene(a: int, b: int, result: int,
                      min_val: int = -15, max_val: int = 15) -> tuple[str, str]:
    """Show a and b on a number line, then the result."""
    scene_class = "TwoNumbersDemo"
    code = f'''
from manim import *

class {scene_class}(Scene):
    def construct(self):
        nl = NumberLine(
            x_range=[{min_val}, {max_val}, 1],
            length=12,
            include_numbers=False,
            font_size=20,
        )
        self.add(nl)

        dot_a = Dot(color=BLUE).scale(1.2)
        dot_b = Dot(color=RED).scale(1.2)
        dot_r = Dot(color=GREEN).scale(1.5)

        self.play(
            dot_a.animate.move_to(nl.number_to_point({a})),
            run_time=1,
        )
        self.play(
            dot_b.animate.move_to(nl.number_to_point({b})),
            run_time=1,
        )
        self.wait(0.3)

        label_a = MathTex(r"{a}").next_to(dot_a, UP, buff=0.3).set_color(BLUE)
        label_b = MathTex(r"{b}").next_to(dot_b, UP, buff=0.3).set_color(RED)
        self.play(Write(label_a), Write(label_b))
        self.wait(0.5)

        # Arrow from a to result (skip if a == result)
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
        label_r = MathTex(r"= {result}").next_to(dot_r, DOWN, buff=0.3).set_color(GREEN)
        self.play(Write(label_r))
        self.wait(1.5)
'''
    return code, scene_class


# ---------------------------------------------------------------------------
# Helper 3: Fraction bar visualization
# ---------------------------------------------------------------------------
def fraction_bar_scene(numerator: int, denominator: int) -> tuple[str, str]:
    """Draw a bar split into `denominator` parts, with `numerator` filled."""
    scene_class = "FractionBarDemo"
    code = f'''
from manim import *

class {scene_class}(Scene):
    def construct(self):
        n = {numerator}
        d = {denominator}

        # Create a row of rectangles
        parts = VGroup()
        for i in range(d):
            rect = Rectangle(width=1.0, height=0.8, stroke_width=3, color=WHITE)
            parts.add(rect)
        parts.arrange(RIGHT, buff=0)

        # Fill the first n parts
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

        frac = MathTex(r"\\frac{{{n}}}{{{d}}}").scale(2).next_to(parts, DOWN, buff=0.8)
        self.play(Write(frac))
        self.wait(1.5)
'''
    return code, scene_class