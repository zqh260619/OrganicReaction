#manim SubstitutionReaction3.py test -pqh

from OrganicReactionTools import *

class test(Scene):
    def construct(self):
        
        title=Title(text=r"\text{一些常见的取代反应机理}\quad\text{完}",pos=ORIGIN)
        subtitle=Subtitle(text=r"\text{羰基上的取代反应}",pos=[0,-0.7,0])
        self.play(Write(title),Write(subtitle))
        self.wait(1.5)
        self.play(FadeOut(title,subtitle))
