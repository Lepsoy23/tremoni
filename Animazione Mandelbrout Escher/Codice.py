from manim import *

class Inizio(Scene):
    def construct(self):
        # Testo iniziale con etimologia di "frattale" e colore sfumato
        etymology_text = Text(
            "Frattale: dal latino 'fractus', che significa rotto o spezzato.\n",
            font_size=36
        )
        etymology_text.set_color_by_gradient(BLUE, PURPLE, PINK)  # Applica il gradiente
        etymology_text.move_to(ORIGIN)  # Posiziona al centro dello schermo

        # Anima la scritta con effetto di scrittura
        self.play(Write(etymology_text), run_time=4)
        self.wait(1)

        # Rimuove la scritta
        self.play(FadeOut(etymology_text))
        self.wait(0)

        # Creazione della linea del tempo con un intervallo di 40 anni e una freccia alla fine
        timeline = NumberLine(
            x_range=[1870, 1950, 40],  # Range temporale modificato da 1870 a 1950 con intervallo di 40 anni
            length=10,  # Lunghezza della linea
            include_numbers=False,  # Disattiviamo i numeri per aggiungere etichette personalizzate
            include_tip=True,  # Aggiunge la freccia alla fine
            tip_length=0.2,  # Lunghezza della freccia
            tick_size=0.05  # Dimensione delle stanghette
        )
        timeline.to_edge(DOWN)  # Posiziona la linea in basso

        # Personalizza il colore delle stanghette
        for tick in timeline.get_tick_marks():
            tick.set_color(WHITE)  # Rende tutte le stanghette bianche

        # Aggiungiamo le etichette personalizzate sull'asse x con intervallo di 40 anni
        labels = [1870, 1910, 1950]  # Valori con intervalli di 40 anni
        label_objects = VGroup(*[
            Text(str(label), font_size=20).next_to(timeline.n2p(label), DOWN)
            for label in labels
        ])

        # Disegna la linea del tempo e le etichette
        self.play(Create(timeline), Write(label_objects))
        self.wait(0)

        # Aggiungi la data di nascita di Escher sulla linea temporale
        birth_year_escher = 1898
        birth_marker_escher = Line(
            start=timeline.n2p(birth_year_escher) + UP * 0.1,
            end=timeline.n2p(birth_year_escher) + DOWN * 0.1,
            color=WHITE  # Colore del marker
        )
        birth_label_escher = Text("1898", font_size=24)
        birth_label_escher.next_to(timeline.n2p(birth_year_escher), DOWN)

        # Disegna il marker e la data di nascita di Escher
        self.play(Create(birth_marker_escher), Write(birth_label_escher))
        self.wait(1)

        # Carica l'immagine di Escher
        face_image_escher = ImageMobject("Escher.jpg")
        
        # Ridimensiona e posiziona l'immagine sopra la data di nascita
        face_image_escher.set_height(4)  # Dimensione della figura
        face_image_escher.move_to(birth_marker_escher.get_top() + UP * 2.5 + LEFT )  # Posiziona sopra la data di nascita
        self.play(FadeIn(face_image_escher), run_time=3)

        # Aggiungi la data di nascita di Mandelbrot sulla linea temporale
        birth_year_mandelbrot = 1924
        birth_marker_mandelbrot = Line(
            start=timeline.n2p(birth_year_mandelbrot) + UP * 0.1,
            end=timeline.n2p(birth_year_mandelbrot) + DOWN * 0.1,
            color=WHITE  # Colore del marker
        )
        birth_label_mandelbrot = Text("1924", font_size=24)
        birth_label_mandelbrot.next_to(timeline.n2p(birth_year_mandelbrot), DOWN)

        # Disegna il marker e la data di nascita di Mandelbrot
        self.play(Create(birth_marker_mandelbrot), Write(birth_label_mandelbrot))
        self.wait(0)

        # Carica il file SVG di Mandelbrot
        face_svg_mandelbrot = ImageMobject("Mandelbrout.jpg")
        
        # Ridimensiona e posiziona l'immagine sopra la data di nascita
        face_svg_mandelbrot.set_height(4)  # Dimensione della figura
        face_svg_mandelbrot.move_to(birth_marker_mandelbrot.get_top() + UP * 2.5 + RIGHT )  # Posiziona sopra la data di nascita
        self.play(FadeIn(face_svg_mandelbrot), run_time=3)

        # Pausa finale per visualizzare tutto
        self.wait(20)
