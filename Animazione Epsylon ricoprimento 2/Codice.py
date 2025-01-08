from manim import *
import random

class EpsilonRicoprimentoGenerale(Scene):
    def construct(self):
        self.wait(0.8)
        titolo = Text("Misura di Hausdorff p-dimensionale", font_size=48).to_edge(UP).set_color_by_gradient(BLUE, PURPLE, PINK) 
        self.play(Write(titolo))
        self.wait(0.5)
        
        limite = MathTex(
            r"H_p(A) = \lim_{\varepsilon \to 0} H_{p,\varepsilon(A)}", 
            font_size=44
        )
        
        # Rendere gialla la epsilon
        limite[0][15].set_color(YELLOW)  # Il carattere \varepsilon si trova all'indice 14
        limite[0][9].set_color(YELLOW)  # Il carattere \varepsilon si trova all'indice 9 

        # Mostrare la formula inizialmente
        self.play(Write(limite))
        self.wait(0.5)

        # Animare lo spostamento della formula verso l'alto
        self.play(limite.animate.shift(UP * 1.7), run_time=1)
        self.wait(1)
        # Parametri generali
        curve_color = BLUE
        ricoprimento_color = YELLOW
        figura_color = GREEN
        parentesi_color = RED
        scala_figura = 1.3  # Scala per adattare la figura
        curva_shift = DOWN * 1.5

        # Parametri personalizzabili
        num_radii = 5  # Numero di raggi
        min_radius = 0.05  # Raggio minimo
        max_radius = 1  # Raggio massimo
        num_points_range = (4, 14)  # Numero di punti delle figure, variabile

        # Definizione della curva generica
        curva = ParametricFunction(
            lambda t: np.array([t, 0.3 * np.sin(2 * PI * t), 0]),  # Curva generica (sinusoide)
            t_range=[-2, 2],
            color=curve_color,
            stroke_width=4
        ).scale(scala_figura).shift(curva_shift)

        # Funzione per ottenere un punto sulla curva
        def get_curve_point(t):
            """Restituisce un punto sulla curva data dalla funzione della curva."""
            return curva.function(t) * scala_figura + np.array([0, -1.5, 0])

        # Creazione dinamica dei raggi
        radii = [min_radius + (max_radius - min_radius) * i / (num_radii - 1) for i in range(num_radii)]
        
        # Funzione per calcolare il numero di cerchi in modo più proporzionale
        def calc_num_circles(raggio):
            if raggio < 0.3:
                return int(10 + (1 / raggio) * 9)  # Più cerchi per raggi piccoli
            elif raggio < 0.6:
                return int(7 + (1 / raggio) * 5)  # Numero medio di cerchi
            else:
                return int(5 + (1 / raggio) * 5)  # Meno cerchi per raggi grandi

        # Calcolare il numero di cerchi per ogni raggio
        num_sets = [calc_num_circles(raggio) for raggio in radii]
        
        # Generazione dei ranges per la posizione dei cerchi
        ranges = [
            np.linspace(-1.8, 1.8, num_sets[i])  # Spaziatura in base al numero di cerchi per ciascun raggio
            for i in range(num_radii)
        ]

        # Creazione dei cerchi tratteggiati per ogni intervallo
        ricoprimenti = VGroup()
        for i, raggio in enumerate(radii):
            ricoprimenti.add(*[
                DashedVMobject(
                    Circle(
                        radius=raggio,
                        color=ricoprimento_color,
                        stroke_width=2,
                    )
                ).move_to(get_curve_point(t))
                for t in ranges[i]
            ])

        # Generazione di figure randomiche contenute nei cerchi
        def crea_figura_randomica(cerchio, raggio):
            center = cerchio.get_center()
            max_size = raggio * 0.65  # Assicuriamoci che le figure siano contenute nel cerchio

            # Creare una figura deformata con punti interpolati
            num_points = random.randint(num_points_range[0], num_points_range[1])
            angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
            points = [
                center + np.array([
                    max_size * random.uniform(0.5, 1.5) * np.cos(a),  # Maggiore deformazione
                    max_size * random.uniform(0.5, 1.5) * np.sin(a),
                    0
                ])
                for a in angles
            ]
            return Polygon(*points, color=figura_color, fill_opacity=0.2).make_smooth()

        # Creare figure randomiche per ogni cerchio
        figure_randomiche = VGroup()
        for i, raggio in enumerate(radii):
            current_range = ricoprimenti.submobjects[sum(num_sets[:i]):sum(num_sets[:i+1])]
            figures = VGroup(*[
                crea_figura_randomica(cerchio, raggio)
                for cerchio in current_range
            ])
            figure_randomiche.add(figures)

        # Creazione delle parentesi tonde
        parentesi_A = MathTex("(").scale(1.0).set_color(parentesi_color).move_to(get_curve_point(-1.8))
        parentesi_B = MathTex(")").scale(1.0).set_color(parentesi_color).move_to(get_curve_point(1.8))

        # Animazioni
        self.play(Create(curva))  # Disegnare la curva
        self.wait(0.2)
        # Mostrare i punti A e B con le parentesi
        self.play(FadeIn(parentesi_A), FadeIn(parentesi_B))
        epsilon_text = MathTex(r"\varepsilon = {:.2f}".format(1), font_size=28, color=YELLOW).move_to(curva.get_left() + LEFT + 1.5* UP)
        self.play(FadeIn(epsilon_text))
        self.wait(0.5)
        # Mostrare cerchi e figure verdi per ogni intervallo, creando i cerchi prima e le figure dopo
        for i in range(len(radii)-1, -1, -1):  # Invertiamo l'ordine di creazione dei raggi
            current_circles = ricoprimenti.submobjects[sum(num_sets[:i]):sum(num_sets[:i+1])]
           # Aggiornare dinamicamente il testo di epsilon
            new_epsilon_text = MathTex(r"\varepsilon = {:.2f}".format(radii[i]), font_size=28, color=YELLOW).move_to(curva.get_left() + LEFT + 1.5* UP)
            self.play(Transform(epsilon_text, new_epsilon_text))
            current_figures = figure_randomiche.submobjects[i]

            # FadeOut dei cerchi e delle figure precedenti, se ci sono
            if i < len(radii) - 1:
                previous_circles = ricoprimenti.submobjects[sum(num_sets[:i+1]):sum(num_sets[:i+2])]
                previous_figures = figure_randomiche.submobjects[i + 1]
                self.play(FadeOut(VGroup(*previous_circles)), FadeOut(previous_figures), run_time=0.3)

            # Creare e fare comparire cerchi
            self.play(
                Create(VGroup(*current_circles)),
                run_time=0.4  # Rallentato rispetto a prima
            )

            # Creare le figure verdi **solo dopo** aver completato la creazione dei cerchi
            self.play(
                FadeIn(VGroup(*current_figures)),
                run_time=0.4
            )

        self.wait(0.5)  # Pausa finale
