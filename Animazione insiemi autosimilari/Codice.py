from manim import *

class Similitudini(Scene):
    def construct(self):
        formula0 = MathTex(r"\text{Similitudine con fattore di risclamento } r ")
        # Prima formula
        formula1 = MathTex(r"S_i: \mathbb{R}^n \rightarrow \mathbb{R}^n \\ x \mapsto r_i O(x) + b_i \\ \text{con } O \text{ trasformazione ortogonale e } b_i \in \mathbb{R}^n")
        
        # Seconda formula
        formula2 = MathTex(r"S = (S_1, ..., S_m) \text{ famiglia finita di similitudini con fattore di riscalamento } r_i \\ \text{dato } E \in \mathbb{R}^n, S(E) = \bigcup_{i=1}^m S_i(E)")
        
        # Posizionamento e dimensione delle formule
        formula0.scale(0.7)
        formula1.scale(0.7)  # Riduci la dimensione del 10%
        formula2.scale(0.7)
        VGroup(formula0, formula1, formula2).arrange(DOWN, buff=1)

        # Animazione con pausa
        self.play(Write(formula0))
        self.play(Write(formula1))
        self.wait(2)  # Pausa di 2 secondi
        self.play(Write(formula2))

if __name__ == "__main__":
    scene = Similitudini()
    scene.render()