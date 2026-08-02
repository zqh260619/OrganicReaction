#manim SubstitutionReaction2.py test -pqh

from OrganicReactionTools import *

class test(Scene):
    def construct(self):

        title=Title(text=r"\text{一些常见的取代反应机理}\quad\text{续}",pos=ORIGIN)
        self.play(Write(title))
        self.wait(1.5)
        self.play(FadeOut(title))

        #-----------------------SEAr reaction-----------------------

        SEAr_reaction=Title(text=r"\mathrm{S_EAr}\text{（芳香亲电取代）}")
        self.play(Write(SEAr_reaction))
        self.wait(2)

        benzene=StructuralFormula(name="C1",pos=[0,0.5*bond_length,0],text=None)
        benzene.add_atom(name="C2",direction=-30*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C1")
        benzene.add_atom(name="C3",direction=-90*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C2",
                         side=-1,start_side_edge=True,end_side_edge=True)
        benzene.add_atom(name="C4",direction=-150*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C3")
        benzene.add_atom(name="C5",direction=150*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C4",
                         side=-1,start_side_edge=True,end_side_edge=True)
        benzene.add_atom(name="C6",direction=90*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C5")
        benzene.add_bond(start="C6",end="C1",bond_type=BondType.DOUBLE_BOND,side=-1,start_side_edge=True,end_side_edge=True)
        benzene.add_atom(name="E",direction=90*DEGREES,text="E",bond_type=BondType.NORMAL_BOND,adjacency="C1")

        self.play(Create(benzene))

        self.wait(2)
