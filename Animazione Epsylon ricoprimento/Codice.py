from manim import *
import random
config.tex_template.add_to_preamble(r"\usepackage{xcolor}")
config.tex_template.add_to_preamble(r"\definecolor{mioverde}{RGB}{0,128,0}")
config.tex_template.add_to_preamble(r"\definecolor{miogiallo}{RGB}{255,255,0}")

class EpsilonRicoprimentoOttimizzato(Scene):
    def construct(self):
        # Prima riga - manteniamo le parti più unite per l'allineamento
        riga1 = MathTex(
            r"\text{Sia } (X, d) \text{ spazio metrico, } A \subseteq X \text{ fissato } ",
            r"\varepsilon",
            r"\in \mathbb{R} \text{ si definisce un }",
            r"\varepsilon",
            r"\text{-ricoprimento di } A:"
        )
        
        # Coloriamo le epsilon nella prima riga
        riga1[1].set_color(YELLOW)
        riga1[3].set_color(YELLOW)
        
        # Seconda riga - manteniamo U_ε come una singola unità
        riga2 = MathTex(
            r"\mathcal{U}_{\varepsilon}(A) := \{",
            r"U_i",
            r"\}_{i \in I} \subseteq X \text{ tale che } \bigcup_{i \in I} ",
            r"U_i",
            r"= A \ \land \sup_{x,y \in ",
            r"U_i",
            r"} d(x,y) := \text{diam}(",
            r"U_i",
            r") < ",
            r"\varepsilon"
        )
        
        # Coloriamo le U_i e l'epsilon nella seconda riga
        riga2[1].set_color(GREEN)
        riga2[3].set_color(GREEN)
        riga2[5].set_color(GREEN)
        riga2[7].set_color(GREEN)
        riga2[9].set_color(YELLOW)
        
        # Coloriamo l'epsilon nel pedice di U
        riga2[0][1].set_color(YELLOW)  # Questo indice potrebbe dover essere aggiustato
        
        # Arrangiamo le righe verticalmente
        testo_completo = VGroup(riga1, riga2).arrange(DOWN, aligned_edge=LEFT).scale(0.7)
        
        # Animiamo l'apparizione del testo
        self.play(
            Write(testo_completo),
            run_time=8
        )
        self.wait()

        # Spostare il testo verso l'alto
        self.play(testo_completo.animate.shift(UP * 2))
        self.wait(3)  

        # Parametri per la curva e il ricoprimento
        curve_color = BLUE
        ricoprimento_color = YELLOW
        figura_color = GREEN
        parentesi_color = RED
        epsilon_radius = 0.3  # Raggio dei cerchi tratteggiati leggermente ridotto
        scala_figura = 2.0  # Scala per adattare la figura

        # Creazione della curva
        curva = ParametricFunction(
            lambda t: np.array([t, 0.3 * np.sin(2 * PI * t), 0]),
            t_range=[-2, 2],
            color=curve_color,
            stroke_width=4
        ).scale(scala_figura).shift(DOWN * 2)

        # Intervallo della curva da coprire (da punto A a punto B)
        t_range_cover = [-0.95, 0.95]
        num_covering_sets = 15  # Numero di cerchi aumentato per coprire meglio la curva

        # Posizionamento degli insiemi di ricoprimento solo tra punto A e B
        x_positions = np.linspace(t_range_cover[0], t_range_cover[1], num_covering_sets)  # Distribuzione lungo la curva
        ricoprimenti = VGroup(*[
            DashedVMobject(
                Circle(
                    radius=epsilon_radius,
                    color=ricoprimento_color,
                    stroke_width=2,
                )
            ).scale(scala_figura).move_to(
                np.array([x * scala_figura, 0.3 * np.sin(2 * PI * x) * scala_figura - 2, 0])
            )
            for x in x_positions
        ])

        # Generazione di figure randomiche contenute nei cerchi
        def crea_figura_randomica(cerchio):
            center = cerchio.get_center()
            max_size = epsilon_radius * 0.90  # Assicuriamoci che le figure siano contenute nel cerchio

            # Creare una figura estremamente deformata con punti interpolati
            num_points = random.randint(4, 8)  # Numero di vertici della figura
            angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
            points = [
                center + np.array([
                    max_size * random.uniform(0.4, 2.3) * np.cos(a),  # Maggiore deformazione
                    max_size * random.uniform(0.4, 2.3) * np.sin(a),
                    0
                ])
                for a in angles
            ]
            return Polygon(*points, color=figura_color, fill_opacity=0.2).make_smooth()

        # Creare figure randomiche per ogni cerchio
        figure_randomiche = VGroup(*[crea_figura_randomica(cerchio) for cerchio in ricoprimenti])

        # Calcolo dei punti e delle tangenti per le parentesi
        def get_curve_point_and_angle(t):
            """Calcola il punto sulla curva e l'angolo della tangente in un dato t."""
            # Parametri della curva
            x = t
            y = 0.3 * np.sin(2 * PI * t)
            point = np.array([x * scala_figura, y * scala_figura - 2, 0])

            # Tangente della curva (approssimata)
            dx = 1  # Derivata della x rispetto a t
            dy = 0.6 * PI * np.cos(2 * PI * t)  # Derivata della y rispetto a t
            angle = np.arctan2(dy, dx)  # Calcola l'angolo della tangente
            return point, angle

        # Punti e angoli delle parentesi
        punto_A, angolo_A = get_curve_point_and_angle(t_range_cover[0]-0.05)
        punto_B, angolo_B = get_curve_point_and_angle(t_range_cover[1]+0.05)

        # Creazione delle parentesi tonde
        parentesi_A = MathTex("(").scale(1.0).set_color(parentesi_color).move_to(punto_A).rotate(angolo_A)
        parentesi_B = MathTex(")").scale(1.0).set_color(parentesi_color).move_to(punto_B).rotate(angolo_B)

        # Animazioni
        self.play(Create(curva))  # Disegnare la curva
        self.wait(0.5)

        # Mostrare i punti A e B con le parentesi
        self.play(FadeIn(parentesi_A), FadeIn(parentesi_B))
        self.wait(0.5)

        # Mostrare i cerchi tratteggiati
        self.play(LaggedStart(*[Create(cerchio) for cerchio in ricoprimenti], lag_ratio=0.2))
        self.wait(0.2)

        # Mostrare le figure randomiche
        self.play(LaggedStart(*[FadeIn(figura) for figura in figure_randomiche], lag_ratio=0.2))
        self.wait(0.4)
        
        # Formula della sommatoria
        formula = MathTex(
            r"H_{p,\varepsilon}(A) = \inf_{\mathcal{U_\varepsilon(A)}} \left\{ \sum_{j=1}^\infty"
            r" (\operatorname{diam} U_j)^p \ \mid \ U_j \in \mathcal{U_\varepsilon(A)}   \right\}",
            font_size=32
        ).shift(UP * 0.2)
        # Colora i caratteri epsilon di giallo
        formula[0][3].set_color(YELLOW)  # Primo epsilon
        formula[0][12].set_color(YELLOW)  # Secondo epsilon
        formula[0][38].set_color(YELLOW)  # Terzo epsilon

        # Colora i caratteri U_j di verde
        formula[0][34].set_color(GREEN)  
        formula[0][29].set_color(GREEN)  
        formula[0][35].set_color(GREEN)  
        formula[0][30].set_color(GREEN)  

        # Mostrare la formula
        self.play(Write(formula))
        self.wait(1)
        
        # **Animazione delle figure verdi che cambiano dinamicamente con Transform**
        n_secondi = 3  # Durata dell'animazione in secondi
        num_steps = n_secondi * 2  # Numero di iterazioni

        for _ in range(num_steps):
            # Creiamo nuove figure
            nuove_figure = VGroup(*[crea_figura_randomica(cerchio) for cerchio in ricoprimenti])

            # Trasformazione fluida delle figure
            self.play(
                Transform(figure_randomiche, nuove_figure),
                run_time=0.5
            )
            self.wait(0.5)  # Attende mezzo secondo per il cambio figura
        
        self.wait(2)
        self.clear() 
        self.wait(1)
