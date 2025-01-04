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

class ScenaCurva(ZoomedScene):
    def construct(self):
        num = 3
        ini = num * LEFT + UP
        fin = num * RIGHT + UP

        # Questa linea è dove effettivamente partirà il frattale
        l = Line(ini, fin)

        # Serve come linea iniziale per la trasformazione
        """ l_visiva = Line(ini, fin).scale(3/4).shift(4 * RIGHT + DOWN)

        similitudine = MathTex(
            r"& \mathbb{S} = (S_1,S_2,S_3,S_4) \ \text{applicato a} \ E = [0,1] \\",
            r"& S_1(x)=\textstyle\frac{1}{3}x \\",
            r"& S_2(x)=\textstyle\frac{1}{3}R_{\frac{\pi}{3}}(x) + \left(\textstyle\frac{1}{3},0\right) \\",
            r"& S_3(x)=\textstyle\frac{1}{3}R_{-\frac{\pi}{3}}(x) + \left(\textstyle\frac{1}{2},\textstyle\frac{\sqrt{3}}{6}\right) \\",
            r"& S_4(x)=\textstyle\frac{1}{3}x + \left(\textstyle\frac{2}{3},0\right)"
        )


        simbolo_e = MathTex(r"E").next_to(l_visiva, UP)
        s_x = MathTex(r"S_1(E)",
                     r"S_2(E)",
                     r"S_3(E)",
                     r"S_4(E)").scale(0.7)

        
        self.play(Write(similitudine.shift(7/4 * LEFT + 3/4 * UP)))

        self.play(Create(l_visiva)) """

        livelli = 6
        # Una lista di liste, dove ogni sottolista rappresenta un'iterazione del 
        # frattale che contiene tutti i tratti del frattale in quell'iterazione,
        # da sinstra verso destra
        lista = [[l,]]

        for i in range(livelli):
            linee = lista[i]
            m = []
            for linea in linee:
                k = Curva(linea.get_start(),linea.get_end())
                m.append(k.l_1)
                m.append(k.l_2)
                m.append(k.l_3)
                m.append(k.l_4)
            lista.append(m)

        """ lung = len(lista[1])
         
        self.play(Write(simbolo_e))

        for i in range(lung):
            self.play(Transform(l_visiva.copy(), lista[1][i]))

        self.play(Write(s_x[0].next_to(lista[1][0], DOWN)))
        self.play(Write(s_x[1].next_to(lista[1][1], 0.05 * LEFT)))
        self.play(Write(s_x[2].next_to(lista[1][2], 0.05 * RIGHT)))
        self.play(Write(s_x[3].next_to(lista[1][3], DOWN)))

        self.clear()
        self.wait(0.5) """

        autosimil = Tex("Autosimilarità").scale(2.5)
        strutt = Tex("Struttura fine").scale(2.5)
        irreg = Tex("Irregolarità").scale(2.5)
        dimensione = MathTex(r"\operatorname{dim}(C) \not \in \mathbb{N}").scale(2.5).set_color_by_tex("\not", RED)

        self.play(Write(autosimil))
        self.play(FadeOut(autosimil))

        curva_finale = Group(*[linea for linea in lista[livelli]])
        
        self.play(FadeIn(curva_finale))

        # TODO: capire come zoommare sulla funzione e sulla curva
        
        # self.play(self.get_zoom_in_animation())
        # self.activate_zooming()
        # self.play(self.zoomed_camera.frame.animate.move_to(ini))
        # self.play(self.zoomed_camera.frame.animate.move_to((fin - ini) / 2))
        # self.zoom_activated = False 

        axes = Axes(x_range = (-12, 12), y_range = (-1.5, 1.5), y_length = 2 ,tips = False).shift(2 * DOWN)
        axes.add_coordinates(font_size = 24)
        
        self.play(Write(axes))

        cos = axes.plot(lambda x: np.cos(x), color = RED)

        self.play(Write(cos))
        self.wait(2)

        self.clear()

        self.play(Write(strutt))
        self.play(FadeOut(strutt))

        self.play(Write(irreg))
        self.play(FadeOut(irreg))

        self.play(Write(dimensione))
        self.play(FadeOut(dimensione))




