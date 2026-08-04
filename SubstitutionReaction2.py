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

        E1_start=np.array([2*benzene.attributes.length_global,0,0])
        E1_target=benzene.atomic_clusters["C1"]["pos"]+np.array([np.cos(60*DEGREES),np.sin(60*DEGREES),0])*benzene.attributes.length_global
        E1_mob=AtomicCluster(text="E",pos=E1_start,attributes=benzene.attributes)
        benzene.atomic_clusters["E1"]={Mobject:E1_mob,"pos":E1_start,"adj":[],Bond:[]}
        benzene.add(E1_mob)
        benzene.add_charge(text="E1",pos=UR,charge_type=ChargeType.POSITIVE)

        E1_positive=benzene.charges["E1"]

        self.play(FadeIn(E1_mob),FadeIn(E1_positive))
        self.wait(0.5)
        shift=E1_target-E1_start
        self.play(E1_mob.animate.shift(shift),
                  E1_positive.animate.shift(shift),
                  run_time=1)
        benzene.atomic_clusters["E1"]["pos"]=E1_target

        C1_C6_double=benzene.atomic_clusters["C1"][Bond][1]
        C1_H1_normal=benzene.atomic_clusters["H1"][Bond][0]

        C1_C6_single=benzene.build_bond(start="C1",end="C6",bond_type=BondType.NORMAL_BOND)
        C1_E1_in=benzene.build_bond(start="C1",end="E1",bond_type=BondType.IN_BOND)
        C6_positive=benzene.build_charge(text="C6",pos=UL,charge_type=ChargeType.POSITIVE_COORDINATE)

        step_wheland=ElectronMigrationStep(
            replace=[(C1_C6_double,VGroup(C1_C6_single,C1_E1_in))],
            create=[C6_positive],
            fadeout=[E1_positive],
        )

        self.play(benzene.electron_migration(steps=[step_wheland],lag_ratio=0,run_time=1.2),
                  BondTypeTransform(bond=C1_H1_normal,
                                    target_type=BondType.OUT_BOND,
                                    angle=30*DEGREES,
                                    about_point=benzene.atomic_clusters["C1"]["pos"],
                                    sf=benzene,
                                    run_time=1.2))

        benzene.delete_bond(start="C1", end="C6")
        benzene.atomic_clusters["C1"][Bond].extend([C1_C6_single, C1_E1_in])
        benzene.atomic_clusters["C6"][Bond].append(C1_C6_single)
        benzene.atomic_clusters["E1"][Bond].append(C1_E1_in)
        benzene.atomic_clusters["C1"]["adj"].extend(["C6", "E1"])
        benzene.atomic_clusters["C6"]["adj"].append("C1")
        benzene.atomic_clusters["E1"]["adj"].append("C1")
        benzene.charges.pop("E1")
        benzene.charges["C6"] = C6_positive

        self.wait(1.5)

        C1_C6_double_new=benzene.build_bond(start="C6", end="C1", bond_type=BondType.DOUBLE_BOND,
                                             side=-1, start_side_edge=True, end_side_edge=True)
        H1_positive=benzene.build_charge(text="H1", pos=UR, charge_type=ChargeType.POSITIVE)

        step_elimination=ElectronMigrationStep(
            replace=[(VGroup(C1_H1_normal, C1_C6_single), C1_C6_double_new)],
            create=[H1_positive],
            fadeout=[C6_positive],
        )

        c1_pos=benzene.atomic_clusters["C1"]["pos"]
        ca, sa = np.cos(30*DEGREES), np.sin(30*DEGREES)
        dx, dy = E1_target[0]-c1_pos[0], E1_target[1]-c1_pos[1]
        E1_final=np.array([c1_pos[0]+dx*ca-dy*sa, c1_pos[1]+dx*sa+dy*ca, 0])
        arc=ArcBetweenPoints(E1_target, E1_final, angle=30*DEGREES)

        self.play(benzene.electron_migration(steps=[step_elimination], lag_ratio=0, run_time=1.5),
                  BondTypeTransform(bond=C1_E1_in,
                                    target_type=BondType.NORMAL_BOND,
                                    angle=30*DEGREES,
                                    about_point=c1_pos,
                                    run_time=1.2),
                  MoveAlongPath(E1_mob, arc, run_time=1.2))

        benzene.delete_bond(start="C1", end="H1")
        benzene.delete_bond(start="C1", end="C6")
        benzene.atomic_clusters["C1"][Bond].append(C1_C6_double_new)
        benzene.atomic_clusters["C6"][Bond].append(C1_C6_double_new)
        benzene.atomic_clusters["C1"]["adj"].append("C6")
        benzene.atomic_clusters["C6"]["adj"].append("C1")
        benzene.charges.pop("C6")
        benzene.charges["H1"] = H1_positive
        benzene.atomic_clusters["E1"]["pos"] = E1_final

        H1_target=np.array([-2*benzene.attributes.length_global,0,0])
        shift_h=H1_target-benzene.atomic_clusters["H1"][Mobject].get_center()
        self.play(benzene.atomic_clusters["H1"][Mobject].animate.shift(shift_h),
                  H1_positive.animate.shift(shift_h),
                  run_time=1)
        benzene.atomic_clusters["H1"]["pos"]=H1_target

        self.wait(1.5)
