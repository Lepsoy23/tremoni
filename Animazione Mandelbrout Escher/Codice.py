from manim import *

class SVGFaceScene(Scene):
    def construct(self):
        # Carica il file SVG (assicurati che il file sia nella directory corretta)
        face_svg = SVGMobject("Mandelbrout.svg")
        
        # Ridimensiona e centra l'SVG
        face_svg.set_height(4)  # Regola l'altezza dell'immagine
        face_svg.set_color(YELLOW)  # Colora il contorno di giallo
        
        # Anima la creazione dell'immagine gradualmente, come se venisse "disegnata"
        self.play(DrawBorderThenFill(face_svg), run_time=4)  # Disegna in 32 secondi
        
        # Pausa per visualizzare l'immagine finale
        self.wait(2)
