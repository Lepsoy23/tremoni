from manim import *

class Costa(Scene):
    def construct(self):
        self.show_additional_elements()
    def show_additional_elements(self):
        # Gestione delle immagini SVG
        coast = SVGMobject("britain_coast.svg")
        coast.set_fill(color=BLUE, opacity=0.5)  # Riempi di blu chiaro con opacità
        coast.set_stroke(color=WHITE, width=2)   # Bordi bianchi per la costa
        coast.scale(2.5)
        coast.move_to(LEFT * 3)

        coastSmooth = SVGMobject("smooth_coast.svg")
        coastSmooth.set_fill(color=BLUE, opacity=0.5)
        coastSmooth.set_stroke(color=WHITE, width=2)
        coastSmooth.scale(2.5)
        coastSmooth.move_to(RIGHT * 3)

        # Aggiunta dei titoli
        title_fractale = Text("Frattale", font_size=36).next_to(coast, UP, buff=0.5)
        title_smooth = Text("Smooth", font_size=36).next_to(coastSmooth, UP, buff=0.5)

        # Disegna le immagini e i titoli
        self.play(Write(title_fractale), Write(title_smooth))
        self.play(
            DrawBorderThenFill(coast),
            DrawBorderThenFill(coastSmooth),
            run_time=4
        )

        # Aggiungi una pausa prima di far scomparire le immagini
        self.wait(1)

        # Fai scomparire i titoli e le immagini
        self.play(FadeOut(title_fractale), FadeOut(title_smooth))
        self.play(FadeOut(coast), FadeOut(coastSmooth))

        # Formula matematica
        formula = MathTex(
            r"H_{p,\delta}(A) = \inf_{\mathcal{B}} \left\{ \sum_{j=1}^\infty"
            r" (\operatorname{diam} B_j)^p \;:\; A \subseteq \bigcup_{j=1}^\infty B_j"
            r" \;\wedge\; \operatorname{diam} B_j \leq \delta \right\}",
            font_size=36
        )
        formula.move_to(ORIGIN)

        # Mostra la formula
        self.play(Write(formula))
        self.wait(3)

        # Rimuovi la formula
        self.play(Unwrite(formula))