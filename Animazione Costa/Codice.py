from manim import *

class TiffAnimation(Scene):
    def construct(self):
        # Lista dei fotogrammi in formato TIFF
        frame_files = [f"frame-{i:03d}.tiff" for i in range(10)]  # Modifica il range per il numero di fotogrammi disponibili

        # Inizializza il primo fotogramma
        first_frame = ImageMobject(frame_files[0]).scale(1)  # Scala impostata a 0.5
        self.add(first_frame)
        self.wait(0.5)

        # Trasforma i fotogrammi successivi
        for i in range(1, len(frame_files)):
            next_frame = ImageMobject(frame_files[i]).scale(1)  # Scala impostata a 0.5
            self.play(Transform(first_frame, next_frame), run_time=0.5)
            self.wait(0.5)  # Pausa tra un frame e l'altro

        # Mantieni l'ultimo fotogramma visibile per un po'
        self.wait(2)
