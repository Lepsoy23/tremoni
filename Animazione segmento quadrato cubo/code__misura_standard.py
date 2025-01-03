from __future__ import annotations
from typing import Any
import numpy as np
from manim import (
    Polygram,
    LineJointType,
    ThreeDScene,
    Tex,
    Line,
    Square,
    Cube,
    Triangle,
    AnimationGroup,
    FadeIn,
    Create,
    Group,
)
from manim import DEGREES, OUT, RIGHT, WHITE
from manim.utils.color import ParsableManimColor
from manim.typing import Point3D


def get_Polygram(
    *vertex_groups: Point3D, color: ParsableManimColor = WHITE, **kwargs: Any
) -> Polygram:
    kwargs.update(
        {
            "joint_type": LineJointType.BEVEL,
        }
    )

    return Polygram(*vertex_groups, color=color, **kwargs)


class SierpinskiDirect:
    def __init__(self, mobject: Polygram):
        assert isinstance(mobject, Polygram)

        self._color = mobject.color
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


class LineSquareCubeScene(ThreeDScene):
    def construct(self):
        texts = [
            r"$\operatorname{dim}_H(A)=1$",  # 0
            r"$\operatorname{dim}_H(B)=2$",  # 1
            r"$\operatorname{dim}_H(C)=3$",  # 2
            r"$A$",  # 3
            r"$B$",  # 4
            r"$C$",  # 5
            r"Triangolo di Sierpinski",  # 6
            r"$T_S$",  # 7
            r"$\operatorname{dim}_H(T_S)=\dfrac{\log(2)}{\log(3)}\approx 1.585$",  # 8
        ]

        texs: list[Tex] = [Tex(text).scale(0.7) for text in texts]
        texs[0].move_to((-5, -2, 0))
        texs[1].move_to((0, -2, 0))
        texs[2].move_to((5, -2, 0))
        texs[3].move_to((-5, 0.5, 0))
        texs[4].move_to((0, -0.3, 0))
        texs[5].move_to((5, -0.5, 0))

        v = (3 * 14) / (5 * 2)
        texs[6].move_to((v, 3, 0))
        texs[7].move_to((v, -1, 0))
        texs[8].move_to((v, -2, 0))

        line = Line().move_to((-5, 1, 0))
        square = Square().move_to((0, 1, 0))
        cube = (
            Cube(fill_opacity=0.8)
            .rotate(-70 * DEGREES, axis=OUT)
            .rotate(-80 * DEGREES, axis=RIGHT)
            .move_to((5, 1, 0))
        )
        triangle = Triangle().scale(2).move_to((v, 1, 0))

        shapes = [line, square, cube, triangle]

        self.play(
            AnimationGroup(
                *[
                    AnimationGroup(
                        *[FadeIn(shapes[i]), Create(texs[3 + i]), Create(texs[i])],
                        lag_ratio=0.2,
                    )
                    for i in range(3)
                ],
                lag_ratio=0.7,
            )
        )

        groups = [Group(shapes[i], texs[3 + i], texs[i]) for i in range(3)]
        self.play(
            [
                groups[i].animate.shift(
                    RIGHT * (((i - 2) * (14 / 5)) - ((i - 1) * (15 / 3)))
                )
                for i in range(3)
            ]
        )

        SD = SierpinskiDirect(triangle)
        SD.advance(5)
        sierpinski = SD.baked()

        groups.append(Group(texs[6], texs[7], texs[8], sierpinski))
        self.play([Create(texs[i]) for i in range(6, 9)] + [FadeIn(SD.baked())])

        self.wait(2)
