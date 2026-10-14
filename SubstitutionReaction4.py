#manim SubstitutionReaction4.py test -pqh

from OrganicReactionTools import *

class test(Scene):
    def construct(self):
        
        title=Title(text=r"\text{一些不常见的取代反应的机理}\quad\text{补}",pos=ORIGIN)
        subtitle=Subtitle(text=r"\text{芳环上的取代反应}",pos=[0,-0.7,0])
        self.play(Write(title),Write(subtitle))
        self.wait(1.5)
        self.play(FadeOut(title,subtitle))

        #-----------------------VNS mechanism-----------------------

        VNS_mechanism=Title(text=r"\mathrm{VNS}\text{（间接芳香亲核取代）}")
        self.play(Write(VNS_mechanism))
        self.wait(0.5)
