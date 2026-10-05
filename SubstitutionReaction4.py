#manim SubstitutionReaction4.py test -pqh

from OrganicReactionTools import *

class test(Scene):
    def construct(self):
        
        title=Title(text=r"\text{一些常见的取代反应的机理}\quad\text{补}",pos=ORIGIN)
        subtitle=Subtitle(text=r"\text{芳环上的取代反应}",pos=[0,-0.7,0])
        self.play(Write(title),Write(subtitle))
        self.wait(1.5)
        self.play(FadeOut(title,subtitle))

        #-----------------------ANRORC mechanism-----------------------

        ANRORC_mechanism=Title(text=r"\mathrm{ANRORC}\text{（亲核加成}\mathrm{-}\text{开环}\mathrm{-}\text{闭环）}")
        self.play(Write(ANRORC_mechanism))
        self.wait(0.5)
