from manim import *
import random

class TiffAnimation(Scene):
    def construct(self):
        title = Text("Quant'è lunga la costa?", font_size=42).set_color_by_gradient(BLUE, PURPLE, PINK)
        title.to_edge(UP)  # Posiziona il titolo in cima alla scena
        self.play(Write(title))
        # Lista dei fotogrammi in formato TIFF
        frame_files = [f"frame-{i:03d}.tiff" for i in range(10)]  # Modifica il range per il numero di fotogrammi disponibili

        # Perimetri: oscillazione attorno a 12,429 e crescita esponenziale più grande
        base_perimeter = 12429
        perimeters = []

        # Oscillazione attorno a 12,429 (diminuzione dell'oscillazione per i primi 7 frame)
        for i in range(8):
            # La variazione iniziale è ampia, ma diminuisce con ogni passaggio
            max_variation = 5000 / (4**i + 1)  # Maggiore variazione iniziale, minore man mano che i fotogrammi vanno avanti
            variation = random.uniform(-max_variation, 0)
            perimeters.append(base_perimeter + variation)

        # Crescita esponenziale forte per gli ultimi 3 fotogrammi
        for i in range(8, 10):
            # Aumento esponenziale con un fattore di crescita maggiore
            perimeters.append(base_perimeter + ( 250*(i - 6)))

        # Inizializza il primo fotogramma
        first_frame = ImageMobject(frame_files[0]).scale(0.6).shift(0.4 * UP)
        self.play(FadeIn(first_frame),run_time=2)

        # Inizializza la scritta per il perimetro
        perimeter_text = Text(f"Perimetro = {perimeters[0]:,.0f} KM", font_size=24)
        new_perimeter_text = Text(f"Perimetro = {int(perimeters[i]):,.0f} KM".replace(',', '.'), font_size=24)
        perimeter_text.next_to(first_frame, DOWN)  # Posiziona sotto l'immagine
        self.play(Write(perimeter_text),run_time=2)
        self.wait(0.5)

        # Trasforma i fotogrammi successivi e aggiorna il testo
        for i in range(1, len(frame_files)):
            next_frame = ImageMobject(frame_files[i]).scale(0.6).shift(0.4 * UP)  # Sposta leggermente in alto
            # Assicurati che 'perimeters[i]' sia un numero
            new_perimeter_text = Text(f"Perimetro = {int(perimeters[i]):,.0f} KM".replace(',', '.'), font_size=24)
            new_perimeter_text.next_to(next_frame, DOWN)  # Posiziona sotto il nuovo frame

            # Anima il cambiamento del fotogramma e del testo
            self.play(
                Transform(first_frame, next_frame), 
                Transform(perimeter_text, new_perimeter_text),
                run_time=0.5
            )
            self.wait(1)

        # Mantieni l'ultimo fotogramma visibile per un po'
        self.wait(1)
