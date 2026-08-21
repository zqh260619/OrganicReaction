#manim SubstitutionReaction3.py test -pqh

from OrganicReactionTools import *

class test(Scene):
    def construct(self):
        
        title=Title(text=r"\text{一些常见的取代反应机理}\quad\text{完}",pos=ORIGIN)
        subtitle=Subtitle(text=r"\text{羰基上的取代反应}",pos=[0,-0.7,0])
        self.play(Write(title),Write(subtitle))
        self.wait(1.5)
        self.play(FadeOut(title,subtitle))

        #-----------------------Addition-elimination mechanism-----------------------

        Addition_elimination_mechanism=Title(text=r"\text{加成-消除机理}")
        self.play(Write(Addition_elimination_mechanism))
        self.wait(0.5)

        acetyl_L=StructuralFormula(name="C1",pos=ORIGIN,text=None)
        acetyl_L.add_atom(name="O1",direction=90*DEGREES,text=r"\mathrm{O}",
                          bond_type=BondType.DOUBLE_BOND,adjacency="C1",side=0)
        acetyl_L.add_atom(name="CH3",direction=210*DEGREES,text=None,
                          bond_type=BondType.NORMAL_BOND,adjacency="C1")
        acetyl_L.add_atom(name="L",direction=330*DEGREES,text=r"\mathrm{L}",
                          bond_type=BondType.NORMAL_BOND,adjacency="C1")

        #右侧亲核试剂 Nu^-
        Nu_pos=np.array([3*acetyl_L.attributes.length_global,0,0])
        Nu_sf=StructuralFormula(name="Nu",pos=Nu_pos,text=r"\mathrm{Nu}")
        Nu_sf.add_charge(text="Nu",pos=UL,charge_type=ChargeType.NEGATIVE)

        #先显示中间底物，再显示右侧亲核试剂
        self.play(Create(acetyl_L))
        self.wait(0.5)
        self.play(Create(Nu_sf))
        self.wait(1.5)
