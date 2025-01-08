from manim import *

class Curva(Mobject):
    def __init__(self, inizio = ORIGIN, fine = RIGHT, spessore = DEFAULT_STROKE_WIDTH, *args, **kwargs):
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
        self.l_1 = Line(self.inizio, self.terz1).set_stroke(width=spessore)
        self.l_2 = Line(self.terz1, self.terz2).rotate(PI / 3, about_point= self.terz1).set_stroke(width=spessore)
        self.l_3 = Line(self.terz1, self.terz2).rotate( - PI / 3, about_point= self.terz2).set_stroke(width=spessore)
        self.l_4 = Line(self.terz2, self.fine).set_stroke(width=spessore)


class ScenaCaratt(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.222,
            zoomed_display_height=2,
            zoomed_display_width=2,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
            },
            **kwargs
        )


    def construct(self):
        num = 3
        ini = num * LEFT + DOWN
        fin = num * RIGHT + DOWN
        spess = 2

        # Questa linea è dove effettivamente partirà il frattale
        l = Line(ini, fin).set_stroke(width=spess)

        livelli = 6
        # Una lista di liste, dove ogni sottolista rappresenta un'iterazione del
        # frattale che contiene tutti i tratti del frattale in quell'iterazione,
        # da sinstra verso destra
        lista = [[l,]]

        for i in range(livelli):
            linee = lista[i]
            m = []
            for linea in linee:
                k = Curva(linea.get_start(),linea.get_end(),spess)
                m.append(k.l_1)
                m.append(k.l_2)
                m.append(k.l_3)
                m.append(k.l_4)
            lista.append(m)

        # Serve per lo zoom
        vertice_superiore = lista[1][1].get_end()

        strutt = Tex("Struttura fine").scale(1).shift(3 * UP)
        autosimil = Tex("Autosimilarità").scale(1).next_to(strutt, 2 * LEFT)
        irreg = Tex("Irregolarità").scale(1).next_to(strutt, 2 * RIGHT)
        dimensione = MathTex(r"&\text{Se } C \text{ è un frattale, } \\ &\operatorname{dim}(C) \not \in \mathbb{N}").scale(1.5)

        self.play(Write(autosimil), Write(strutt), Write(irreg))
        self.play(autosimil.animate.set_color(YELLOW))
        # self.play(Write(autosimil))
        # self.wait(3)
        # self.play(FadeOut(autosimil))

        curva_finale = Group(*[linea for linea in lista[livelli]])
        # curva_finale.shift(2 * DOWN)

        self.play(FadeIn(curva_finale))

        self.zoomed_display.shift(2 * DOWN)
        self.zoomed_camera.frame.move_to(l.get_start())
        self.activate_zooming(animate=False)
        self.play(self.zoomed_camera.frame.animate.move_to(vertice_superiore))
        self.wait(1)
        self.play(self.zoomed_camera.frame.animate.move_to(l.get_end()))
        self.wait(1)
        # self.zoom_activated = False
        self.play(curva_finale.animate.shift(UP),self.zoomed_camera.frame.animate.shift(UP))
        self.wait(3)

        self.play(autosimil.animate.set_color(WHITE),strutt.animate.set_color(YELLOW))
        # self.play(Write(strutt))
        # self.wait(6)
        # self.play(FadeOut(strutt))

        axes = Axes(
            x_range = (-7, 7),
            y_range = (-1.5, 1.5),
            y_length = 1,
            tips = False
        ).shift(2 * DOWN)
        axes.add_coordinates(font_size = 24)

        self.wait(3)

        self.play(Write(axes))

        cos = axes.plot(lambda x: np.cos(x), color = RED)

        self.play(Write(cos))

        self.play(self.zoomed_camera.frame.animate.move_to(1.7 * DOWN))
        self.play(self.zoomed_camera.frame.animate.scale(0.5))

        self.wait(7)

        self.play(
            Uncreate(self.zoomed_camera.frame),FadeOut(self.zoomed_display),
            FadeOut(axes), FadeOut(cos))

        # self.clear()

        self.play(strutt.animate.set_color(WHITE),irreg.animate.set_color(YELLOW))

        self.play(curva_finale.animate.shift(DOWN).scale(2))

        # self.play(Write(irreg))
        # self.wait(6)
        # self.play(FadeOut(irreg))

        self.wait(6)
        self.clear()
        self.wait(0.5)

        self.play(Write(dimensione))
        self.wait(20)




# config.disable_caching = True