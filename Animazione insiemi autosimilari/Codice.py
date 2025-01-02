import math
import numpy as np
from manim import *

class Similitudine(Scene):
    def construct(self):
        # Colori per il gradiente
        gradient_colors = [BLUE, PURPLE]
        
        # Titolo
        title = Text("Insiemi autosimilari", gradient=gradient_colors).scale(0.8).to_edge(UP)
        definizione = MathTex(
            r"\text{Si definisce una similitudine con fattore di riscalamento } r \in (0,1) ",
        ).scale(0.7).to_edge(UP).to_edge(LEFT, buff=0.5).next_to(title, DOWN, buff=0.5)
        # Equazioni e spiegazioni
        equations = MathTex(
            r"S_i : \mathbb{R}^n \to \mathbb{R}^n \\",
            r"x \mapsto r O_i(x) + b_i\hspace{1 cm} O_i \in \text{SO}(n), b_i \in \mathbb{R}^n \\ ",
        ).scale(0.7).next_to(definizione, DOWN, buff=0.5)
        
        # Spostare la seconda riga a destra
        equations[0].shift(LEFT*3.5)
        equations[1].shift(RIGHT*1.6)

        # Definizione della famiglia di similitudini
        famiglia = MathTex(
            r"\text{Sia ora }S = \{S_1, \dots, S_m\} \text{ una famiglia finita di similitudini con fattore di riscalamento } r.\\",
            r"\text{Dato } E \subseteq \mathbb{R}^n \;\text{si definisce } S(E) = \bigcup_{i=1}^m S_i(E) \text{ insieme autosimilare di E.}",
        ).scale(0.7).next_to(equations, DOWN, aligned_edge=LEFT, buff=0.5)
        famiglia.shift(LEFT*4.4)
        famiglia[0].shift(LEFT*0.1)
        famiglia[1].shift(LEFT*1.5)
     # Effetti di apparizione con runtime di 4 secondi
        self.play(Write(title, shift=UP, run_time=2))
        self.wait(0.5)
        self.play(Write(definizione, shift=UP, run_time=4))
        self.wait(1)
        self.play(Write(equations, shift=LEFT * 1.3, run_time=4))
        self.wait(1)
        self.play(Write(famiglia, shift=LEFT * 3, run_time=4))
        self.wait(2)
        self.clear()
        # Creazione del primo segmento (E)
        segmento_E = Line(start=LEFT, end=RIGHT, color=BLUE).scale(3).shift(UP * 2.5)  # Ingrandisci e trasla verso l'alto
        label_E = MathTex("E").next_to(segmento_E, UP)

        self.play(Create(segmento_E))  # Mostra E
        # Definizione dei punti di incollamento
        medio = (segmento_E.get_end() + segmento_E.get_start()) / 2
        punto = medio + DOWN * 3 + LEFT * segmento_E.get_length() / 3
        angoli = [0, PI / 3, -PI / 3, 0]  # Rotazioni per i segmenti
        scale_factors = 1/3  # Rimpicciolimento

        # Creazione dei segmenti sovrapposti ad E
        segmenti_sopra = VGroup()
        for _ in range(4):
            segmento = segmento_E.copy()
            segmenti_sopra.add(segmento)
            self.play(Create(segmento))

        self.wait(1)
        posizioni = []
        # Trasformazione dei segmenti sovrapposti in quelli sotto
        for i in range(4):
            segmento = segmenti_sopra[i]
            if(i == 0):
                self.play(
                segmento.animate.move_to(punto).rotate(angoli[i]).scale(scale_factors)
                )
            else:
                self.play(
                segmento.animate.move_to(posizioni[i-1]).rotate(angoli[i]).scale(scale_factors)
                )
            # Supponiamo che segment.get_end() ritorni un array numpy, come ad esempio [x, y]
            end_point = segmento.get_end()  # Un array numpy con le coordinate [x, y]

            if(i<3):
                dx = segmento.get_length()/2 * np.cos(angoli[i+1])
                dy = segmento.get_length()/2 * np.sin(angoli[i+1])
            else:
                dx = segmento.get_length()/2 * np.cos(angoli[i])
                dy = segmento.get_length()/2 * np.sin(angoli[i])
            new_end_point = end_point + np.array([dx, dy,0])

            # Aggiungiamo la nuova posizione alla lista posizioni
            posizioni.append(new_end_point)

        self.wait(1)

        # Aggiunta delle etichette alla fine
        nomi = ["S_1(E)", "S_2(E)", "S_3(E)", "S_4(E)"]
        for segmento, nome in zip(segmenti_sopra, nomi):
            label = MathTex(nome).scale(0.5).next_to(segmento, DOWN, buff=0.1)  # Riduci le scritte e posizionale più vicino
            self.play(Write(label))

        self.wait(2)