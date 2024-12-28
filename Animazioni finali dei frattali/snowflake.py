from manim import *
import numpy as np

# class KochCurve(manim.Mobject):
#     def __init__(
#             self, 
#             color = manim.color.WHITE,
#             meet: tuple[float]=(-2,0,0),
#             join: tuple[float]=(2,0,0),
#             *args,
#             **kwargs
#         ):
#         super().__init__(*args, **kwargs)

#         self.meet = meet
#         self.join = join

        

# k = KochCurve()

class Curva(Scene):
    def __init__(
            self,
            lung = 3, # Lunghezza del segmento
            inizio = ORIGIN, # Inizio del segmento
            direz = RIGHT # Direzione del segmento
            ):
        super().__init__()

        self.lung = lung
        self.inizio = inizio
        self.direz = direz
        self.fine = lung * direz

    def construct(self):
        k = Curva()
        linea = Line(k.inizio, k.fine)
        l_1 = Line(k.inizio, k.fine).scale(1/3).next_to(linea, -k.fine * 1/3).set_color(RED)
        l_2 = Line(k.inizio, k.fine).scale(1/3).next_to(k.fine, 1/3 * RIGHT).set_color(ORANGE)

        self.add(linea,l_1,l_2)


        # b_1 = Dot(inizio).set_color(RED)
        # b_2 = Dot(fine * (1/3)).set_color(BLUE)
        # b_3 = Dot(inizio + (1/2) * lung* RIGHT + (1/6 * np.sqrt(3)) * lung * UP).set_color(GREEN)
        # b_4 = Dot(fine * (2/3)).set_color(ORANGE)

        # self.add(linea, b_1, b_2, b_3, b_4)


        # b_1: tuple[float] = [0,0,0]
        # b_2: tuple[float] = [1/3,0,0]
        # b_3: tuple[float] = [1/2,1/6 * np.sqrt(3),0]
        # b_4: tuple[float] = [2/3,0,0]
        # b_5: tuple[float] = [1,0,0]
        # uno = Line(b_1,b_2).scale(lung)
        # due = Line(b_2,b_3).scale(lung)
        # tre = Line(b_3,b_4).scale(lung)
        # quattro = Line(b_4,b_5).scale(lung)
        
        # self.add(uno, due, tre, quattro)