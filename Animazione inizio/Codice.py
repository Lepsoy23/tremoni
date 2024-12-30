from manim import *

class Inizio(Scene):
    def construct(self):
        # Carica l'immagine PNG
        image = ImageMobject("Image.png")
        
        # Ingrandisci l'immagine se necessario
        image.scale(3)
        
        # Posiziona l'immagine al centro dello schermo
        image.move_to(ORIGIN)
        
        # Anima l'apparizione dell'immagine con FadeIn
        self.play(ScaleInPlace(image, run_time=2))
        
        # Mantieni l'immagine visibile per alcuni secondi
        self.wait(2)
