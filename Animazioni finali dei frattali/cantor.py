import manim, numpy
import manim.typing
from operator import add, sub

class CantorSet(manim.Mobject):
    def __init__(
            self,
            meet:tuple[float]=(-1,0,0),
            join:tuple[float]=(1,0,0),
            offset:float=0.1,
            factor:float=1,
            *args,
            **kwargs
        ):
        super().__init__(*args, **kwargs)
        
        self.meet = meet
        self.join = join
        vector = tuple(map(lambda x, y: pow(y - x, 2), meet, join))
        self.unit = numpy.sqrt(sum(vector))
        self.factor = factor
        self.offset = offset * self.unit
        self.shift_step = tuple(map(lambda x: x * offset, (
            vector[1],
            -vector[0],
            vector[2]
        )))
        
        self.layers: list[manim.Group] = [manim.Group()]
        self.layers[0].add(manim.Line(meet, join))

        self.add(*self.layers)
        self.animated = False
        self.tmp = None

    def single_step(self, line:manim.Line) -> tuple[manim.Line]:
        meet = tuple(map(add, self.shift_step, line.start))
        join = tuple(map(add, self.shift_step, line.end))

        one = tuple(map(lambda x, y: (y - x) / 3, meet, join))
        new_join = tuple(map(add, meet, one))
        new_meet = tuple(map(sub, join, one))

        return (
            manim.Line(meet, new_join),
            manim.Line(new_meet, join)
        )

    def __inner_step(self) -> manim.Group:
        new_layer = manim.Group()
        for line in self.layers[-1]:
            new_layer.add(*self.single_step(line))

        self.layers.append(new_layer)
        return new_layer

    def step(self):
        new_layer = self.__inner_step()
        self.shift_step = tuple(map(lambda x: x * self.factor, self.shift_step))
        self.add(new_layer)

    def advance(self, time=1):
        if self.animated:
            return None
        
        self.animated = True

        if self.tmp is not None:
            self.tmp.remove_updater(self.tmp.updaters[0])
            self.tmp = None

        new_layer = self.__inner_step()
        clone = new_layer.copy()
        clone.shift(tuple(map(lambda x: -x, self.shift_step)))
        self.add(clone)

        self.elapsed = 0
        def updater(group:manim.Group, dt: float):
            if self.elapsed >= time:
                return None
            
            self.elapsed += dt
            fraction = dt / time
            group.shift(tuple(map(lambda x: fraction * x, self.shift_step)))

            if self.elapsed >= time:
                self.animated = False
                self.shift_step = tuple(map(lambda x: x * self.factor, self.shift_step))
    
                self.remove(group)
                self.add(self.layers[-1])
        
        clone.add_updater(updater)
        self.tmp = clone



c = CantorSet()

class IdioticScene(manim.Scene):
    def construct(self):
        c = CantorSet((-6,3.5,0), (6,3.5,0), factor=0.8, offset=0.01)
        self.add(c)
        for _ in range(6):
            self.wait(0.41)
            c.advance(0.4)
        self.wait(2)

