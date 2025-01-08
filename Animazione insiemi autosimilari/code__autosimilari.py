from __future__ import annotations
from typing import Callable, Any
import numpy as np
from manim import (
    Animation,
    Polygram,
    LineJointType,
    Scene,
    ZoomedScene,
    Tex,
    Create,
    Uncreate,
    FadeOut,
    Group,
    FadeIn,
    always_redraw,
    Triangle,
)
from manim.animation.animation import DEFAULT_ANIMATION_RUN_TIME
from manim import UP, DOWN, GREEN, WHITE, BLUE, LEFT, PURPLE, PINK
from manim.utils.color import ParsableManimColor
from manim.typing import Point3D
from manim import rate_functions, config
from manim import *

NP_DOWN = np.array([0, -1, 0])
SMOOTH = rate_functions.smoothererstep
RATE_FUNC_FFI = SMOOTH
RATE_FUNC_SAS = RATE_FUNC_FFI
RATE_FUNC_FFO = RATE_FUNC_FFI


class SimilStep(Animation):
    def __init__(
        self,
        mobject: Polygram,
        functions: list[Callable[[np.array], np.array]] = [lambda a: a],
        shift: np.array = NP_DOWN,
        **kwargs,
    ):
        assert isinstance(mobject, Polygram)
        assert len(functions) > 0

        a = np.zeros((1, 5, 3))
        t = type(a)
        for func in functions:
            assert callable(func)
            assert isinstance(func(a), t)

        t = type(NP_DOWN)
        assert isinstance(shift, t)
        assert shift.shape == (3,)

        self.NUM = len(functions)
        self.LEN = len(mobject.get_vertex_groups())

        if "run_time" not in kwargs.keys() or kwargs["run_time"] is None:
            kwargs["run_time"] = self.NUM * DEFAULT_ANIMATION_RUN_TIME

        super().__init__(mobject, introducer=False, **kwargs)

        copy = mobject.copy()
        for _ in range(self.NUM):
            mobject.append_vectorized_mobject(copy.copy())

        self._starting_groups = copy.get_vertex_groups()
        self._ending_groups = [func(copy.get_vertex_groups()) for func in functions]
        self._shift_step = shift

        shape = list(self._starting_groups.shape)
        shape[0] = 0
        self._empty_shape = tuple(shape)

        self.color = copy.color
        self.joint = copy.joint_type

    @staticmethod
    def linear_interpolation(a, b, t):
        return (1 - t) * a + t * b

    def interpolate_mobject(self, alpha):
        step = int(alpha * self.NUM)
        zero = step / self.NUM
        real = (alpha - zero) * self.NUM if alpha != 1 else 1
        beta = self.rate_func(real)

        def lint(a, b):
            partial = SimilStep.linear_interpolation(a, b, beta)  # pow(beta, 1/5))
            shift = self._shift_step * beta
            final = partial + shift

            return final

        new_vertex_groups = np.zeros(self._empty_shape)
        for i in range(self.NUM):
            if i > step:
                new = self._starting_groups
            elif i == step:
                new = lint(self._starting_groups, self._ending_groups[i])
            else:
                new = self._ending_groups[i] + self._shift_step

            new_vertex_groups = np.append(new_vertex_groups, new, axis=0)

        new_mobject = Polygram(
            *new_vertex_groups, color=self.color, joint_type=self.joint
        )

        self.mobject.become(new_mobject)


class CantorActualStep(SimilStep):
    def __init__(self, mobject: Polygram, shift: np.array = NP_DOWN, **kwargs):

        lside = mobject.get_left()
        rside = mobject.get_right()

        center = lambda x: x - lside
        normal = lambda x: x + lside
        vector = 2 * (rside - lside) / 3
        s1 = lambda x: normal(center(x) / 3)
        s2 = lambda x: s1(x) + vector

        super().__init__(mobject, [s1, s2], shift, **kwargs)


def get_Polygram(
    *vertex_groups: Point3D, color: ParsableManimColor = WHITE, **kwargs: Any
) -> Polygram:
    kwargs.update(
        {
            "joint_type": LineJointType.BEVEL,
        }
    )

    poly = Polygram(*vertex_groups, color=color, stroke_color=color, **kwargs)
    poly.set_fill(color=color)
    return poly



class FakeFadeIn(FadeIn):
    def __init__(self, *mobjects, **kwargs):
        if "run_time" in kwargs.keys() and kwargs["run_time"] is None:
            kwargs["run_time"] = DEFAULT_ANIMATION_RUN_TIME

        if "rate_func" not in kwargs:
            kwargs["rate_func"] = RATE_FUNC_FFI

        super().__init__(*mobjects, **kwargs)

    def clean_up_from_scene(self, scene):
        super().clean_up_from_scene(scene)
        scene.remove(self.mobject)


class ChangeOpacity(Animation):
    def __init__(self, mobject: Polygram, target: float = 0, *args, **kwargs):
        assert isinstance(mobject, Polygram)

        if "run_time" in kwargs.keys() and kwargs["run_time"] is None:
            kwargs["run_time"] = DEFAULT_ANIMATION_RUN_TIME

        if "rate_func" not in kwargs:
            kwargs["rate_func"] = RATE_FUNC_FFO

        super().__init__(mobject, *args, **kwargs)
        self.starting: float = self.mobject.fill_opacity
        self.finishing: float = target

    def interpolate_mobject(self, alpha):
        beta = self.rate_func(alpha)
        opacity = (1 - beta) * self.starting + beta * self.finishing
        self.mobject.set_fill(opacity=opacity)


class SierpinskiActualStep(Animation):
    def __init__(
        self,
        mobject: Polygram,
        run_time: float | None = None,
        opacity: float = 1,
        color: ParsableManimColor | None = None,
        **kwargs,
    ):
        assert isinstance(mobject, Polygram)

        if run_time is None:
            run_time = DEFAULT_ANIMATION_RUN_TIME

        if "rate_func" not in kwargs:
            kwargs["rate_func"] = RATE_FUNC_SAS

        super().__init__(
            None,
            introducer=False,
            run_time=run_time,
            **kwargs,
        )

        if color is None:
            self._color = mobject.color
        else:
            self._color = color

        self._original = mobject
        self._vertex_groups = mobject.get_vertex_groups()
        self._rolled_groups = np.roll(self._vertex_groups.copy(), 1, axis=1)
        self._current_groups = self._vertex_groups.copy()

        self.opacity = opacity

        self.in_use = always_redraw(lambda: self.drawer())

    def drawer(self) -> Polygram:
        poly = get_Polygram(*self._current_groups, color=self._color)
        poly.set_fill(opacity=self.opacity)

        return poly

    def vector_groups_interpolate(self, t: float):
        self._current_groups = (1 - t) * self._vertex_groups + t * self._rolled_groups

    def _setup_scene(self, scene):
        scene.add(self.in_use)

    def clean_up_from_scene(self, scene):
        self.in_use.clear_updaters()
        scene.remove(self.in_use)

        final = self.drawer()
        self.final = final

        next_groups = np.zeros((0, 3, 3))
        for i, group in enumerate(self._vertex_groups):
            p1s = self._current_groups[i]
            p2s = np.roll(p1s, -1, axis=0)

            new = np.array([[g, p2, p1] for g, p1, p2 in zip(group, p1s, p2s)])
            next_groups = np.append(next_groups, new, axis=0)

        self.next = get_Polygram(*next_groups, color=self._color)

        scene.add(final)

    def interpolate_mobject(self, alpha):
        beta = self.rate_func(alpha)
        self.vector_groups_interpolate(beta / 2)


class SierpinskiDirect:
    def __init__(self, mobject: Polygram, color: ParsableManimColor | None = None,):
        assert isinstance(mobject, Polygram)

        if color is None:
            self._color = mobject.color
        else:
            self._color = color
        
        self._original = mobject
        self._vertex_groups = mobject.get_vertex_groups()
        self._rolled_groups = np.roll(self._vertex_groups.copy(), 1, axis=1)
        self.all_groups = [self._vertex_groups]

    @staticmethod
    def linear_interpolation(a, b, t):
        return (1 - t) * a + t * b

    def step(self):
        final = SierpinskiDirect.linear_interpolation(
            self._vertex_groups, self._rolled_groups, 1 / 2
        )

        next_groups = np.zeros((0, 3, 3))
        for i, group in enumerate(self._vertex_groups):
            p1s = final[i]
            p2s = np.roll(p1s, -1, axis=0)

            new = np.array([[g, p2, p1] for g, p1, p2 in zip(group, p1s, p2s)])
            next_groups = np.append(next_groups, new, axis=0)

        self.all_groups.append(final)
        self._vertex_groups = next_groups
        self._rolled_groups = np.roll(self._vertex_groups.copy(), 1, axis=1)

    def advance(self, n: int):
        for _ in range(n):
            self.step()

    def baked(self) -> Polygram:
        all_vertex_groups = np.zeros((0, 3, 3))
        for group in self.all_groups:
            all_vertex_groups = np.append(all_vertex_groups, group, axis=0)

        return get_Polygram(*all_vertex_groups, color=self._color)

    def bake(self):
        new = self.baked()
        self._original.become(new)


def sierpinski_step(
    scene: Scene,
    poly: Polygram,
    run_time: float | None = None,
    color: ParsableManimColor | None = None,
    *args, **kwargs
) -> tuple[Polygram, Polygram]:
    if run_time is None:
        rtFFI = None
        rtSAS = None
        rtFFO = None
    else:
        rtFFI = run_time / 3
        rtSAS = run_time / 3
        rtFFO = run_time / 3

    copy = poly.copy()
    copy.set_fill(opacity=1)

    animFFI = FakeFadeIn(copy, run_time=rtFFI)
    animSAS = SierpinskiActualStep(poly, run_time=rtSAS, opacity=1, color=color)

    scene.play(animFFI)
    scene.play(animSAS)

    final = animSAS.final
    animFFO = ChangeOpacity(final, run_time=rtFFO)

    scene.play(animFFO)

    return final, animSAS.next


class SimilScene(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.6,
            zoomed_display_height=6,
            zoomed_display_width=6,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
            },
            **kwargs,
        )

    def construct(self):
        texts = [
            # 0
            r"\centering Una \textbf{similitudine} con \textbf{fattore di riscalamento} $r$ è una funzione",
            # 1
            r"""\begin{align*}
                S\colon\mathbb{R}^n&\rightarrow\mathbb{R}^n\\
                \mathbf{x}&\mapsto r O(\mathbf{x}) + b
            \end{align*}""",
            # 2
            r"dove $O$ è una trasformazione ortogonale e $b\in\mathbb{R}$",
            # 3
            r"\centering Data una famiglia finita di similitudini\\$\mathbb{S}=(S_1, \ldots, S_m)$, si ha una funzione",
            # 4
            r"""\begin{align*}
                \mathbb{S}\colon\mathcal{P}(\mathbb{R}^n)&\rightarrow\mathcal{P}(\mathbb{R}^n)\\
                E&\mapsto \mathbb{S}(E)=\bigcup_{i=1}^m S_i(E)
            \end{align*}
            """,
            # 5
            r"""\begin{minipage}{5cm} \centering
                Una simile funzione può essere usata
                per costruire un insieme \textbf{autosimilare}
                come l'insieme di Cantor $\mathcal{C}$
            \end{minipage}""",
            # 6
            r"""
            \begin{gather*}
                \mathbb{S} = (S_1,S_2)\colon\quad\mathcal{P}(\mathbb{R})\rightarrow\mathcal{P}(\mathbb{R})\\[10pt]
                \begin{aligned}
                    S_1(x) &= \dfrac{1}{3}x\\
                    S_2(x) &= \dfrac{1}{3}x + \dfrac{2}{3}\\
                \end{aligned}\\[10pt]
                \begin{aligned}
                    E &= [0, 1]\\
                    \mathcal{C} &= \bigcap_{n=1}^{+\infty}\mathbb{S}^n(E)
                \end{aligned}
            \end{gather*}
            """,
            # 7
            r"$E$",
            *[
                # 7 + i
                r"$\mathbb{S}^" + f"{i}" + r"(E)$"
                for i in range(1, 7)
            ],
        ]

        texs: list[Tex] = [Tex(text).scale(0.7) for text in texts]

        texs[0].shift(UP * 2)
        texs[2].shift(DOWN * 2)
        texs[3].shift(DOWN * 1)
        texs[4].shift(DOWN * 2.5)

        texs[5].move_to((4, 2.5, 0))
        texs[6].move_to((4, -1, 0))

        #for tex in texs[:3]:
        #   self.play(Create(tex))
                # Colori per il gradiente
        gradient_colors = [BLUE, PURPLE, PINK]
        
        # Titolo
        title = Text("Insiemi auto-similari", gradient=gradient_colors).scale(0.8).to_edge(UP)
        definizione = MathTex(
            r"\text{Si definisce una similitudine con fattore di riscalamento } r \in (0,1) ",
        ).scale(0.7).to_edge(UP).to_edge(LEFT, buff=0.5).next_to(title, DOWN, buff=0.5)
        # Equazioni e spiegazioni
        equations = MathTex(
            r"S_i : \mathbb{R}^n \to \mathbb{R}^n \\",
            r"x \mapsto r O_i(x) + b_i\hspace{1 cm} O_i \in \text{SO}(n), b_i \in \mathbb{R}^n \\ ",
        ).scale(0.7).next_to(definizione, DOWN, buff=0.5)
        
        # Spostare la seconda riga a destra
        equations[0].shift(LEFT*3.5)
        equations[1].shift(RIGHT*1.6)

        # Definizione della famiglia di similitudini
        famiglia = MathTex(
            r"\text{Sia ora }  \mathbb{S} = \{S_1, \dots, S_m\} \text{ una famiglia finita di similitudini con fattore di riscalamento } r.\\",
            r"\text{Dato } E \subseteq \mathbb{R}^n \;\text{si dice che E è un insieme auto-similare se soddisfa la seguente proprietà:} \\",
            r" E = \cup_{i=1}^m S_i(E) =  \mathbb{S}(E) = \mathbb{S}^k(E) \; \text{(invarianza per } \mathbb{S}\text{)} \text{ ed inoltre } m({S^k}_i(E) \cap {S^k}_j(E)) = 0 \\",
            r"\text{ se } i\not = j \\"
        ).scale(0.7).next_to(equations, DOWN, aligned_edge=LEFT, buff=0.5)
        famiglia[0].shift(LEFT*1.3)
        famiglia[1].shift(LEFT*1.5)
        famiglia[2].shift(LEFT*1.7)
        famiglia[3].shift(LEFT*3)
        famiglia.shift(LEFT*3.2)
        start_index = 29  # Posizione di "a" in "auto-similare"
        end_index = 42    # Posizione dell'ultimo carattere "e" in "auto-similare"
        num_chars = end_index - start_index
        # Colora i caratteri nell'intervallo specificato
        for i in range(start_index, end_index):
            progress = (i - start_index) / num_chars
            color = interpolate_color(gradient_colors[0], gradient_colors[1], progress)
            famiglia[1][i].set_color(color) 
     # Effetti di apparizione con runtime di 4 secondi
        # self.play(Write(title, shift=UP, run_time=2))
        # self.wait(0.5)
        # self.play(Write(definizione, shift=UP, run_time=6))
        # self.wait(0.5)
        # self.play(Write(equations, shift=LEFT * 1.3, run_time=4))
        # self.play(Write(famiglia[0], shift=LEFT * 3, run_time=8))
        # self.wait(10)
        # for i in range(1, 4):
        #     self.play(Write(famiglia[i], shift=LEFT * 3, run_time=8))
        # self.wait(3)
        # self.clear()
        # self.wait(2)
       # self.play(
        #    [
        #        texs[0].animate.move_to((0, 3, 0)),
        #        texs[1].animate.move_to((0, 1.9, 0)),
        #        texs[2].animate.move_to((0, 1, 0)),
        #    ]
      #  )

        #for tex in texs[3:5]:
            #self.play(Create(tex))

        #self.wait(1)
       # self.play([Uncreate(tex) for tex in texs[:5]])

        for tex in texs[5:7]:
            self.play(Create(tex))
        
        self.wait(19)

        poly = Polygram([(-5, 3, 0), (0, 3, 0)], color=GREEN)
        shapes = [poly.copy()]
        texs[7].move_to((-6, 3, 0))

        self.play([Create(shapes[0]), Create(texs[7])])

        self.wait(0.2)
        for i in range(1, 7):
            texs[7 + i].move_to((-6, 3 - i, 0))
            self.add(poly)
            self.play([CantorActualStep(poly), Create(texs[7 + i])])
            shapes.append(poly)
            poly = poly.copy()

        fattori = MathTex(
            r"&\text{Numero similitudini N } = 2 \text{,} \\& \text{fattore di riscalamento r} = \frac{1}{3}"
            #,substrings_to_isolate=["N", "r"]
        )#.set_color_by_tex("N", RED).set_color_by_tex("r", BLUE)
        formula_dim= MathTex(r"\operatorname{dim}_{H} = \log_{\frac{1}{r}}(N)=\log_{3}(2)=0,6309...")

        self.wait(11)

        self.play(FadeOut(Group(*self.mobjects)))

        self.play(Create(fattori))
        self.wait(5)
        self.play(Uncreate(fattori))

        self.play(Create(formula_dim))
        self.wait(5)


        # color = [BLUE, PURPLE, PINK]
        # poly = Triangle(stroke_color=color, joint_type=LineJointType.BEVEL)
        # poly.set_fill(color=color)
        # poly.scale(4)
        # copy = poly.copy()

        # triangle = copy.copy()
        # shapes = [copy]

        # run_time = 2
        # steps = 6
        # self.play(FadeIn(copy, rate_func=RATE_FUNC_FFI, run_time=run_time / 3))
        # for _ in range(steps - 1):
        #     final, poly = sierpinski_step(self, poly, run_time=run_time, color=color)
        #     shapes.append(final)

        # SD = SierpinskiDirect(triangle, color=color)
        # SD.advance(steps)

        # SD.bake()
        # original = Triangle(
        #     stroke_color=color,
        #     joint_type=LineJointType.MITER
        # ).scale(4)
        # self.play([FadeIn(triangle), FadeIn(original)])
        # self.remove(*shapes)

        # group = Group(triangle, original)

        # self.play(self.get_zoom_in_animation())
        # shift = 3 * LEFT
        # self.play(
        #     [self.get_zoomed_display_pop_out_animation(), group.animate.shift(shift)]
        # )
        # self.activate_zooming()

        # a = SD.all_groups[0][0][1]
        # b = SD.all_groups[1][0][2]
        # c = SD.all_groups[1][0][1]
        # center = (a + b + c) / 3 + (0, 0.5, 0) + shift
        # self.play(self.zoomed_camera.frame.animate.move_to(center))

        self.wait(20)
