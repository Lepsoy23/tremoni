from manim import *

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

        # Serve per calcolare gli altri punti. E' la lunghezza della linea
        self.diff = self.fine - self.inizio 

        # Punto che sta a un terzo del segmento, partendo da inizio verso fine
        self.terz1 = 1/3 * self.diff + self.inizio 

        # Punto che sta a due terzo del segmento, partendo da inizio verso fine
        self.terz2 = 2/3 * self.diff + self.inizio 

        # Linea iniziale
        self.linea = Line(self.inizio, self.fine)

        # Linee dell'iterazione fatta su self.linea
        self.l_1 = Line(self.inizio, self.terz1)
        self.l_2 = Line(self.terz1, self.terz2).rotate(PI / 3, about_point= self.terz1)
        self.l_3 = Line(self.terz1, self.terz2).rotate( - PI / 3, about_point= self.terz2)
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
        offset = 4

        for _ in range(iteraz):
            lung = len(lista)
            for j in range(0, lung):
                self.add(lista[offset * j])
                k = Curva(lista[offset * j].get_start(), lista[offset * j].get_end())
                ll = Line(k.inizio,k.terz1).add(k.l_1, k.l_2, k.l_3, k.l_4)
                self.play(Transform(lista[offset * j], ll))

                lista.insert(offset * j, k.l_4)
                lista.insert(offset * j, k.l_3)
                lista.insert(offset * j, k.l_2)
                lista.insert(offset * j, k.l_1)
                lista.pop(offset * j)
            self.wait(0.5)

