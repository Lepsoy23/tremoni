from pdb import run
from manim import *

class PropositionWithGraph(Scene):
    def construct(self):
        # Titolo "Proposizione" al centro
        title = Tex("Proposizione").scale(0.8).to_edge(UP).shift(LEFT * 4.6)

        # Testo della proposizione traslato in basso sotto il titolo e leggermente a destra
        proposition = MathTex(
            r"\text{Siano } s,\ t \in  \mathbb{R} \text{ tale che } 0 \leq s < t < \infty, \, E \subset \mathbb{R}^n", r"\\",
            r"I) \ \mathcal{H}^s(E) < \infty \implies \mathcal{H}^t(E) = 0", r"\\",
            r"II) \ \mathcal{H}^t(E) > 0 \implies \mathcal{H}^s(E) = \infty"
        ).scale(0.7).next_to(title, DOWN, buff=0.5).shift(RIGHT*2.5)

        self.play(Write(title))
        self.play(Write(proposition),run_time=8)
        self.wait(1)

        # Assi del grafico con frecce migliorate e valori dell'asse y rimossi
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            axis_config={
                "include_numbers": False,  # Rimuovi valori sugli assi
                "include_ticks": False,    # Rimuovi i simboli delle tacche
                "font_size": 20,
                "tip_length": 0.05,  # Freccia degli assi più piccola e visibile
                "stroke_width": 2,  # Rende gli assi più chiari
            },
            x_length=4.5,
            y_length=3
        ).to_corner(DR)

        # Etichetta dell'asse x
        x_label = MathTex(r"s").scale(0.7).next_to(axes.x_axis.get_end(), DOWN)

        # Grafico con salto in s*
        vertical_line = DashedLine(
            start=axes.c2p(3, 0), end=axes.c2p(3, 3.5), color=YELLOW
        )
        graph_left = axes.plot(lambda x: 3.5, color=BLUE, x_range=[0, 3])  # Valore costante fino a s*
        graph_right = axes.plot(lambda x: 0, color=BLUE, x_range=[3, 5])  # Valore costante dopo s*

        # Punto di discontinuità a metà tra 0 e infinito
        discontinuity = Dot(axes.c2p(3, 1.75), color=RED)  # Posizionato a metà altezza

        # Punto critico ed etichetta
        s_star_label = MathTex(r"s^*=dim_H(E)").scale(0.6).next_to(axes.c2p(3, 0), DOWN)
        infinity_label = MathTex(r"\infty").scale(0.7).next_to(axes.c2p(0, 3.5), LEFT)
        measureHausdorff = MathTex(r"H^{s^*}(E)").scale(0.7).next_to(axes.c2p(0, 1.75), LEFT)


        # Disegna grafico e annotazioni
        self.play(Create(axes), Write(x_label))
        self.play(Create(graph_left), Create(vertical_line), Create(graph_right))
        self.play(Create(discontinuity), Write(s_star_label), Write(infinity_label),Write(measureHausdorff))

        # Finalizza la scena
        self.wait(10)
        definition = MathTex( 
            r" \text{Si definisce la dimensione di Hausdorﬀ di E come:}", r"\\",
            r"\dim_H(E) := \inf\{ s : \mathcal{H}^s(E) = 0\} \hspace{2.85 cm}", r"\\",
            r"= \sup\{ s : \mathcal{H}^s(E) = \infty \}  \hspace{2.65 cm}"
        ).scale(0.6).to_edge(LEFT).shift(DOWN*1.5)

        self.play(Write(definition),run_time=8)
        self.wait(2)

