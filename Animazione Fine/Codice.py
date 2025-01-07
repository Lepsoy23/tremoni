from manim import *

class Fine(Scene):
    def construct(self):
        # Carica l'immagine PNG
        image = ImageMobject("Image.png")
        
        # Posiziona l'immagine al centro dello schermo
        image.move_to(ORIGIN)
        
        # Anima l'apparizione dell'immagine con FadeIn
        self.play(FadeIn(image), run_time=2)
        
        # Mantieni l'immagine visibile per alcuni secondi
        self.wait(2)