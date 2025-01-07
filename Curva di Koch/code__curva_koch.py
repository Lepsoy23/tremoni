from __future__ import annotations
from typing import Callable, Iterable
from manim import *
from manim.typing import Point3D
from manim import config
import numpy as np

"""
ISTRUZIONI ALLA MODIFICA RAPIDA
per verificare il codice:                           riga 368
per cambiare i colori:                              riga 183
    (
        volendo si possono mettere dei gradienti:
        al posto di BLUE basta mettere
        qualcosa tipo [RED, WHITE, GREEN]
        !!! devono essere 4
    )
per cambiare i testi:                               riga 188
    (
        non cambiare l'ordine, né il numero di
        testi, a meno di cambiare anche il
        comportamento del resto del codice
        al riguardo
    )
per cambiare il numero di iterazioni esplicite:     riga 281
per cambiare il numero di iterazioni implicite:     riga 283
per cambiare i tempi:
- cercare i wait
- ad ogni animazione (anche quelle custom) si può imporre
  l'argomento "run_time" per decidere quanti secondi
  farla durare
"""

ROT90 = np.array([
    [0, -1, 0],
    [1, 0, 0],
    [0, 0, 1]
])

class Multiline(VMobject):
    def __init__(self, *points: Point3D, **kwargs):
        assert isinstance(points, Iterable)
        assert len(points) > 1

        if 'joint_type' not in kwargs.keys():
            kwargs['joint_type'] = LineJointType.MITER

        super().__init__(**kwargs)
        self.set_points_as_corners(points)

    
    def change_points(self, *points: Point3D) -> Multiline:
        assert isinstance(points, Iterable)
        assert len(points) > 1

        self.set_points_as_corners(points)

    def get_corners(self):
        anchors = self.get_anchors()
        points = anchors[0::2] + [anchors[-1]]
        return np.array(points)


class KochStep(Animation):
    mobject: Multiline

    def __init__(
            self,
            mobject: Multiline,
            dumb: bool = False,
            **kwargs
        ):
        assert isinstance(mobject, Multiline)

        super().__init__(mobject, **kwargs)

        self._dumb = dumb
        anchors = mobject.get_anchors()
        points = anchors[0::2] + [anchors[-1]]
        self._points = np.array(points)
        self.points_step()
        self.mobject.change_points(*self._shade)

    @staticmethod
    def linear_interpolation(a, b, t):
        return (1 - t) * a + t * b

    def points_step(self):
        meet = self._points[:-1]
        join = self._points[1:]
        last = self._points[-1]
        mid1 = KochStep.linear_interpolation(meet, join, 1/3)
        mid2 = KochStep.linear_interpolation(meet, join, 1/2)
        mid3 = KochStep.linear_interpolation(meet, join, 2/3)

        temp = np.array(list(zip(meet, mid1, mid2, mid3))).reshape(-1, 3)
        
        vectors = np.matmul(mid1 - meet, ROT90) * np.sqrt(3) / 2

        if self._dumb:
            vectors *= -1

        top = mid2 + vectors

        target = np.array(list(zip(meet, mid1, top, mid3))).reshape(-1, 3)

        self._shade = np.append(temp, [last], axis=0)
        self._target = np.append(target, [last], axis=0)

    def interpolate_mobject(self, alpha):
        beta = self.rate_func(alpha)

        newpoints = KochStep.linear_interpolation(self._shade, self._target, beta)
        self.mobject.change_points(*newpoints)

    def bake(self, by: int = 1):
        assert isinstance(by, int)
        if by <= 0:
            return None
        
        self.interpolate_mobject(1)

        anchors = self.mobject.get_anchors()
        points = anchors[0::2] + [anchors[-1]]
        self._points = np.array(points)
        self.points_step()
        self.mobject.change_points(*self._shade)
        
        self.bake(by - 1)


class KochDirect:
    def __init__(
            self,
            mobject: Multiline,
            dumb: bool = False,
        ):
        assert isinstance(mobject, Multiline)

        self._dumb = dumb
        self.mobject = mobject
        self.refresh()

    def refresh(self):
        self._points = self.mobject.get_corners()

    def step(self):
        meet = self._points[:-1]
        join = self._points[1:]
        last = self._points[-1]
        mid1 = KochStep.linear_interpolation(meet, join, 1/3)
        mid2 = KochStep.linear_interpolation(meet, join, 1/2)
        mid3 = KochStep.linear_interpolation(meet, join, 2/3)
        
        vectors = np.matmul(mid1 - meet, ROT90) * np.sqrt(3) / 2

        if self._dumb:
            vectors *= -1

        top = mid2 + vectors
        target = np.array(list(zip(meet, mid1, top, mid3))).reshape(-1, 3)

        self._points = np.append(target, [last], axis=0)

    def advance(self, by: int = 1):
        assert isinstance(by, int)
        assert by >= 0
        for _ in range(by):
            self.step()

    def baked(self) -> Multiline:
        new = self.mobject.copy()
        new.change_points(*self._points)
        return new
    
    def bake(self):
        self.mobject.change_points(*self._points)



class CurvaDiKoch(Scene):
    def prepare(self):
        self._colors = [RED, BLUE, GREEN, YELLOW]
        assert len(self._colors) == 4
        self.make_texts()


    def make_texts(self):
        config.tex_template.add_to_preamble(r"""
        \newcommand{\XX}{\mathbf{x}}
        \newcommand{\XY}{\begin{bmatrix}x\\y\end{bmatrix}}
        \newcommand{\bXY}{\left(\XY\right)}    
        """)

        self._texts = [
            r"\huge Curva di Koch",
            r"$\mathbb{S}=(S_1,S_2,S_3,S_4)$\hspace{10pt}dove\hspace{10pt}$S_j\bXY=\dfrac{1}{3}O_j\bXY+b_j$",
            r"$b_1=\begin{bmatrix}0\\[10pt]0\end{bmatrix}$, " +
                r"$b_2=\begin{bmatrix}\dfrac{1}{3}\\[10pt]0\end{bmatrix}$, " +
                r"$b_3=\begin{bmatrix}\dfrac{1}{2}\\[10pt]\dfrac{\sqrt{3}}{6}\end{bmatrix}$, " +
                r"$b_4=\begin{bmatrix}\dfrac{2}{3}\\[10pt]0\end{bmatrix}$",
            r"$O_1 = Id_{\mathbb{R}^2}$, $O_2 = R_{\pi/3}$, $O_3 = R_{-\pi/3}$, $O_4 = Id_{\mathbb{R}^2}$",
            r"$R_\theta\bXY=\begin{bmatrix}\cos(\theta)&-\sin(\theta)\\\sin(\theta)&\cos(\theta)\end{bmatrix}\XY$",
            r"$S_1$",
            r"$S_2$",
            r"$S_3$",
            r"$S_4$",
        ]
        assert len(self._texts) == 9
        assert self._texts[5:9] == [
            r"$S_1$",
            r"$S_2$",
            r"$S_3$",
            r"$S_4$",
        ]

        self._texs: list[Tex] = [Tex(text).scale(0.7) for text in self._texts]

        p1 = np.array((-2, -3, 0))
        p2 = np.array((2, -3, 0))

        locations = [
            3 * UP,
            1.5 * UP,
            0.5 * DOWN,
            2 * DOWN,
            3 * DOWN,
            p1,
            KochStep.linear_interpolation(p1, p2, 1/3),
            KochStep.linear_interpolation(p1, p2, 2/3),
            p2
        ]

        for tex, loc in zip(self._texs, locations):
            tex.move_to(loc)

        for i in range(4):
            self._texs[5 + i].set_color(self._colors[i])

    def construct(self):
        self.prepare()
        for i in range(5):
            self.play(Create(self._texs[i]))
        self.wait(2)
        self.play([
            Uncreate(tex)
            for tex in self._texs[:5]
        ])
        self.wait(2)

        def label(degree: int = 0, above: bool = True) -> Tex:
            if degree == 0:
                text = "$E$"
            elif degree == 1:
                text = r"$\mathbb{S}(E)$"
            else:
                text = r"$\mathbb{S}^{" + str(degree) + r"}(E)$"

            if above:
                position = (-4, 1, 0)
            else:
                position = (-4, -2, 0)

            tex = Tex(text).scale(0.7).move_to(position)
            return tex


        above = Multiline((-3, 1, 0), (3, 1, 0))
        kd_a = KochDirect(above, dumb=True)
        kd_a.step()
        below_points = kd_a.baked().shift((0, -3, 0)).get_corners()
        belows = [
            Multiline(below_points[i], below_points[i+1], stroke_color=self._colors[i])
            for i in range(4)
        ]
        kd_b = [KochDirect(below, dumb=True) for below in belows]

        kd_a.refresh()
        tag = label(0)
        line = above.copy()
        N = 3   # numero di iterazioni svolte esplicitamente
        assert N > 0
        M = 3   # numero di iterazioni svolte implicitamente

        for n in range(N - 1):
            self.rolling(kd_a, kd_b, label, tag, line, n)
        self.rolling(kd_a, kd_b, label, tag, line, N - 1, True)

        for i in range(M):
            self.play([
                KochStep(line, dumb=True),
                Transform(tag, label(N+1+i).move_to((0, -2, 0)))
            ])

        self.wait(2)

    def rolling(
        self,
        kd_a: KochDirect,
        kd_b: list[KochDirect],
        label: Callable[[int, bool], Tex],
        label0: Tex,
        above: Multiline,
        n: int = 0,
        final: bool = False
    ):
        kd_a.step()
        up = np.array((0, 3.0, 0))

        copies = [above.copy() for _ in range(4)]
        label1 = label(n + 1, False)
        if n == 0:
            transitions = [
                    AnimationGroup(Transform(copies[i], kd_b[i].mobject), Create(self._texs[5+i]))
                    for i in range(4)
                ]
            self.play([Create(label0), Create(above)])
        else:
            transitions = [Transform(copies[i], kd_b[i].mobject) for i in range(4)]

        self.play([
            Create(label1),
            AnimationGroup(
                *transitions,
                lag_ratio = 1
            )
        ])

        if final:
            up *= 0.5
            group = VGroup(*copies)
            rolling = [
                group.animate.shift(up).set_color(WHITE).scale(2).set_stroke(width=1)
            ] + [
                Uncreate(self._texs[5+i])
                for i in range(4)
            ]

            shift_label = label1.animate.move_to((0, -2, 0))

            kd_a.bake()
            kd_a.mobject.shift(-up).scale(2).set_stroke(width=1)
            kd_a.refresh()
        else:
            shift_label = label1.animate.shift(up)
            rolling = [
                copy.animate.shift(up).set_color(WHITE)
                for copy in copies
            ]

        self.play([
            Uncreate(label0),
            Uncreate(above),
            shift_label,
            *rolling,
        ])

        label0.become(label1.copy())
        above.become(kd_a.baked())

        self.remove(label1, *copies)
        self.add(label0, above)

        for kd in kd_b:
            kd.step()
            kd.bake()

    rick = rolling
