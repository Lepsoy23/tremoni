from manim import *

class Curva(Mobject):
    def __init__(self, inizio = ORIGIN, fine = RIGHT, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Inizio del segmento
        self.inizio = inizio

        # Fine del segmento
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
        num = 3
        ini = num * LEFT + 2 * UP
        fin = num * RIGHT + 2 * UP
        l = Line(ini + 3 * DOWN, fin + 3 * DOWN)

        l_visiva = Line(ini, fin)

        self.add(l_visiva)

        iteraz = 3
        lista = [[l,]]

        for i in range(iteraz):
            linee = lista[i]
            m = []
            for linea in linee:
                k = Curva(linea.get_start(),linea.get_end())
                m.append(k.l_1)
                m.append(k.l_2)
                m.append(k.l_3)
                m.append(k.l_4)
            lista.append(m)

        lung = len(lista)
         
        for i in range(len(lista[1]) - 1):
            self.play(Transform(l_visiva.copy(), lista[1][i]))

        self.play(Transform(l_visiva, lista[1][i + 1]))

        frase = MathTex(
            r"& {{S = (S_1,S_2,S_3,S_4) \ \text{applicato a} \ E = [0,1]}} \\ & S_1(x)=\frac{1}{3}x \\ &S_1(x)=\frac{1}{3}R_{\frac{\pi}{3}}(x) + \left(\frac{1}{3},0\right) \\ &S_1(x)=\frac{1}{3}R_{-\frac{\pi}{3}}(x) + \left(\frac{1}{2},\frac{\sqrt{3}}{6}\right)",
            font_size = 12
        )

        self.add(frase.shift(3*UP))

        # offset = 4
        # for _ in range(iteraz):
        #     lung = len(lista)
        #     for j in range(0, lung):
        #         self.add(lista[offset * j])
        #         k = Curva(lista[offset * j].get_start(), lista[offset * j].get_end())
        #         ll = Line(k.inizio,k.terz1).add(k.l_1, k.l_2, k.l_3, k.l_4)
        #         self.play(Transform(lista[offset * j], ll))        
        #         lista.insert(offset * j, k.l_4)
        #         lista.insert(offset * j, k.l_3)
        #         lista.insert(offset * j, k.l_2)
        #         lista.insert(offset * j, k.l_1)
        #         lista.pop(offset * j)
        #     self.wait(0.5)

