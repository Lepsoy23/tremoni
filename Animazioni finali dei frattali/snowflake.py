from manim import *
import numpy as np

class Curva(Mobject):
    def __init__(
            self,
            inizio = ORIGIN, # Inizio del segmento
            fine = RIGHT, # Fine del segmento
            *args,
            **kwargs
        ):
        super().__init__(*args, **kwargs)

        self.inizio = inizio
        self.fine = fine
        self.diff = self.fine - self.inizio
        self.terz1 = 1/3 * self.diff + self.inizio
        self.terz2 = 2/3 * self.diff + self.inizio

        # self.linea = Line(self.inizio, self.fine)
        self.l_1 = Line(self.inizio, self.terz1)
        self.l_2 = Line(self.terz1, self.terz2).rotate(PI / 3, about_point= self.terz1)
        self.l_3 = Line(self.terz2, self.terz1).rotate( - PI / 3, about_point= self.terz2)
        self.l_4 = Line(self.terz2, self.fine)

class ScenaCurva(Scene):
    def construct(self):
        num = 7
        ini = num * LEFT + DOWN
        fin = num * RIGHT + DOWN
        k = Curva(ini, fin)
        l = Line(ini, fin)#.set_color(ORANGE)

        self.add(l)

        iteraz = 3
        lista = [l,]

        for i in range(iteraz):
            for j in range(0, len(lista), 3 * (i+1)):
                k = Curva(lista[j].get_start(),lista[j].get_end())
                ll = Line(k.inizio,k.terz1).add(k.l_1,k.l_2,k.l_3,k.l_4)
                self.play(Transform(lista[j], ll))
                lista.insert(j, k.l_4)
                lista.insert(j, k.l_3)
                lista.insert(j, k.l_2)
                lista.insert(j, k.l_1)
                lista.pop(j)
            self.wait(0.5)

        # self.add(k.l_1,k.l_2,k.l_3,k.l_4)

        # k2 = Curva(k.l_1.get_start(),k.l_1.get_end())
        # self.add(k2.l_1,k2.l_2,k2.l_3,k2.l_4)



        # linee1 = Line(ORIGIN,ORIGIN).add(k.l_1,k.l_2,k.l_3,k.l_4)

        # k2 = Curva(k.l_1.get_start(),k.l_1.get_end())

        # linee2 =  Line(ORIGIN,ORIGIN).add(k2.l_1,k2.l_2,k2.l_3,k2.l_4)

        # self.add(linee1, linee2)



