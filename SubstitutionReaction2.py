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

        #descriptions
        text1=Description(text=r"\mathrm{E^+}\text{为亲电试剂，通常为卤素阳离子或硝基阳离子等}")
        text2=Description(text=r"\text{首先，亲电试剂}\mathrm{E^+}\text{进攻苯环的}\mathrm{\pi}\text{电子}")
        text3=Description(text=r"\text{对应的碳由}\mathrm{sp^2}\text{杂化变为}\mathrm{sp^3}\text{杂化，苯环失去芳香性，此中间体能量较高}")
        text4=Description(text=r"\text{随后，}\mathrm{H^+}\text{离去，生成产物}")
        text5=Description(text=r"\text{此时苯环恢复芳香性，能量降低，反应存在强大的热力学驱动力}")

        benzene1=StructuralFormula(name="C1",pos=[0,0.5*bond_length,0],text=None)
        benzene1.add_atom(name="C2",direction=-30*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C1")
        benzene1.add_atom(name="C3",direction=-90*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C2",
                         side=-1,start_side_edge=True,end_side_edge=True)
        benzene1.add_atom(name="C4",direction=-150*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C3")
        benzene1.add_atom(name="C5",direction=150*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C4",
                         side=-1,start_side_edge=True,end_side_edge=True)
        benzene1.add_atom(name="C6",direction=90*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C5")
        benzene1.add_bond(start="C6",end="C1",bond_type=BondType.DOUBLE_BOND,side=-1,start_side_edge=True,end_side_edge=True)
        benzene1.add_atom(name="H1",direction=90*DEGREES,text="\mathrm{H}",bond_type=BondType.NORMAL_BOND,adjacency="C1")

        self.play(Create(benzene1))

        self.wait(0.5)

        #苯进攻亲电试剂E+，形成Wheland中间体

        E1_start=np.array([2*benzene1.attributes.length_global,0,0])
        E1_target=benzene1.atomic_clusters["C1"]["pos"]+np.array([np.cos(60*DEGREES),np.sin(60*DEGREES),0])*benzene1.attributes.length_global
        E1_mob=AtomicCluster(text="\mathrm{E}",pos=E1_start,attributes=benzene1.attributes)
        benzene1.atomic_clusters["E1"]={Mobject:E1_mob,"pos":E1_start,"adj":[],Bond:[]}
        benzene1.add(E1_mob)
        benzene1.add_charge(text="E1",pos=UR,charge_type=ChargeType.POSITIVE)

        E1_positive=benzene1.charges["E1"]

        self.play(FadeIn(E1_mob),FadeIn(E1_positive),Write(text1))
        self.wait(2)
        self.play(ReplacementTransform(text1,text2))
        self.wait(2)
        shift=E1_target-E1_start
        self.play(E1_mob.animate.shift(shift),
                  E1_positive.animate.shift(shift),
                  run_time=1)
        benzene1.atomic_clusters["E1"]["pos"]=E1_target

        C1_C6_double=benzene1.atomic_clusters["C1"][Bond][1]
        C1_H1_normal=benzene1.atomic_clusters["H1"][Bond][0]

        C1_C6_single=benzene1.build_bond(start="C1",end="C6",bond_type=BondType.NORMAL_BOND)
        C1_E1_in=benzene1.build_bond(start="C1",end="E1",bond_type=BondType.IN_BOND)
        C6_positive=benzene1.build_charge(text="C6",pos=UL,charge_type=ChargeType.POSITIVE_COORDINATE)

        step_wheland=ElectronMigrationStep(
            replace=[(C1_C6_double,VGroup(C1_C6_single,C1_E1_in))],
            create=[C6_positive],
            fadeout=[E1_positive],
        )

        self.play(benzene1.electron_migration(steps=[step_wheland],lag_ratio=0,run_time=1.2),
                  BondTypeTransform(bond=C1_H1_normal,
                                    target_type=BondType.OUT_BOND,
                                    angle=30*DEGREES,
                                    about_point=benzene1.atomic_clusters["C1"]["pos"],
                                    sf=benzene1,
                                    run_time=1.2))
        self.play(ReplacementTransform(text2,text3))

        benzene1.delete_bond(start="C1", end="C6")
        benzene1.atomic_clusters["C1"][Bond].extend([C1_C6_single, C1_E1_in])
        benzene1.atomic_clusters["C6"][Bond].append(C1_C6_single)
        benzene1.atomic_clusters["E1"][Bond].append(C1_E1_in)
        benzene1.atomic_clusters["C1"]["adj"].extend(["C6", "E1"])
        benzene1.atomic_clusters["C6"]["adj"].append("C1")
        benzene1.atomic_clusters["E1"]["adj"].append("C1")
        benzene1.charges.pop("E1")
        benzene1.charges["C6"] = C6_positive

        self.wait(2.5)

        #H1离去，生成产物

        C1_C6_double_new=benzene1.build_bond(start="C6", end="C1", bond_type=BondType.DOUBLE_BOND,
                                             side=-1, start_side_edge=True, end_side_edge=True)
        H1_positive=benzene1.build_charge(text="H1", pos=UR, charge_type=ChargeType.POSITIVE)

        step_elimination=ElectronMigrationStep(
            replace=[(VGroup(C1_H1_normal, C1_C6_single), C1_C6_double_new)],
            create=[H1_positive],
            fadeout=[C6_positive],
        )

        c1_pos=benzene1.atomic_clusters["C1"]["pos"]
        ca, sa = np.cos(30*DEGREES), np.sin(30*DEGREES)
        dx, dy = E1_target[0]-c1_pos[0], E1_target[1]-c1_pos[1]
        E1_final=np.array([c1_pos[0]+dx*ca-dy*sa, c1_pos[1]+dx*sa+dy*ca, 0])
        arc=ArcBetweenPoints(E1_target, E1_final, angle=30*DEGREES)

        self.play(ReplacementTransform(text3,text4))
        self.play(benzene1.electron_migration(steps=[step_elimination], lag_ratio=0, run_time=1.5),
                  BondTypeTransform(bond=C1_E1_in,
                                    target_type=BondType.NORMAL_BOND,
                                    angle=30*DEGREES,
                                    about_point=c1_pos,
                                    run_time=1.2),
                  MoveAlongPath(E1_mob, arc, run_time=1.2))

        benzene1.delete_bond(start="C1", end="H1")
        benzene1.delete_bond(start="C1", end="C6")
        benzene1.atomic_clusters["C1"][Bond].append(C1_C6_double_new)
        benzene1.atomic_clusters["C6"][Bond].append(C1_C6_double_new)
        benzene1.atomic_clusters["C1"]["adj"].append("C6")
        benzene1.atomic_clusters["C6"]["adj"].append("C1")
        benzene1.charges.pop("C6")
        benzene1.charges["H1"] = H1_positive
        benzene1.atomic_clusters["E1"]["pos"] = E1_final

        H1_target=np.array([-2*benzene1.attributes.length_global,0,0])
        shift_h=H1_target-benzene1.atomic_clusters["H1"][Mobject].get_center()
        self.play(benzene1.atomic_clusters["H1"][Mobject].animate.shift(shift_h),
                  H1_positive.animate.shift(shift_h),
                  run_time=1)
        benzene1.atomic_clusters["H1"]["pos"]=H1_target

        self.wait(1.5)
        self.play(ReplacementTransform(text4,text5))
        self.wait(2)
