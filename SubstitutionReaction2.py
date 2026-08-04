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
        self.wait(1)

        benzene=StructuralFormula(name="C1",pos=[0,0.5*bond_length,0],text=None)
        benzene.add_atom(name="C2",direction=-30*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C1")
        benzene.add_atom(name="C3",direction=-90*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C2",
                         side=-1,start_side_edge=True,end_side_edge=True)
        benzene.add_atom(name="C4",direction=-150*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C3")
        benzene.add_atom(name="C5",direction=150*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C4",
                         side=-1,start_side_edge=True,end_side_edge=True)
        benzene.add_atom(name="C6",direction=90*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C5")
        benzene.add_bond(start="C6",end="C1",bond_type=BondType.DOUBLE_BOND,side=-1,start_side_edge=True,end_side_edge=True)
        benzene.add_atom(name="H1",direction=90*DEGREES,text="H",bond_type=BondType.NORMAL_BOND,adjacency="C1")

        self.play(Create(benzene))

        self.wait(0.5)

        benzene.add_atom(name="E1",direction=60*DEGREES,text="E",bond_type=BondType.IN_BOND,adjacency="C1")
        benzene.add_charge(text="E1",pos=UR,charge_type=ChargeType.POSITIVE)

        bond_temp1=benzene.atomic_clusters["E1"][Bond][0]
        benzene.atomic_clusters["C1"][Bond].remove(bond_temp1)
        benzene.atomic_clusters["E1"][Bond].remove(bond_temp1)
        benzene.remove(bond_temp1)
        benzene.atomic_clusters["C1"]["adj"].remove("E1")
        benzene.atomic_clusters["E1"]["adj"].remove("C1")

        C1_C6_double=benzene.atomic_clusters["C1"][Bond][1]
        E1_positive=benzene.charges["E1"]
        C1_H1_normal=benzene.atomic_clusters["H1"][Bond][0]

        self.play(FadeIn(benzene.atomic_clusters["E1"][Mobject]),
                  FadeIn(E1_positive))
        self.wait(0.5)

        C1_C6_single=benzene.build_bond(start="C1",end="C6",bond_type=BondType.NORMAL_BOND)
        C1_E1_in=benzene.build_bond(start="C1",end="E1",bond_type=BondType.IN_BOND)
        C6_positive=benzene.build_charge(text="C6",pos=UL,charge_type=ChargeType.POSITIVE_COORDINATE)

        step_wheland=ElectronMigrationStep(
            replace=[(C1_C6_double,VGroup(C1_C6_single,C1_E1_in))],
            create=[C6_positive],
            fadeout=[E1_positive],
        )

        self.play(benzene.electron_migration(steps=[step_wheland],run_time=1.5),
                  BondTypeTransform(bond=C1_H1_normal,
                                    target_type=BondType.OUT_BOND,
                                    angle=30*DEGREES,
                                    about_point=benzene.atomic_clusters["C1"]["pos"],
                                    sf=benzene,
                                    run_time=1.5))

        for name in ["C1","C6"]:
            benzene.atomic_clusters[name][Bond]=[b for b in benzene.atomic_clusters[name][Bond] if b is not C1_C6_double]
        benzene.atomic_clusters["C1"][Bond].append(C1_C6_single)
        benzene.atomic_clusters["C1"][Bond].append(C1_E1_in)
        benzene.atomic_clusters["C6"][Bond].append(C1_C6_single)
        benzene.atomic_clusters["E1"][Bond].append(C1_E1_in)
        benzene.atomic_clusters["C1"]["adj"].append("E1")
        benzene.atomic_clusters["E1"]["adj"].append("C1")
        del benzene.charges["E1"]
        benzene.charges["C6"]=C6_positive

        self.wait(1.5)
