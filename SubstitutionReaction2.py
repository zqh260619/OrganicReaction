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

        step_elimination1=ElectronMigrationStep(
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
        self.play(benzene1.electron_migration(steps=[step_elimination1], lag_ratio=0, run_time=1.5),
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

        self.play(FadeOut(text5,benzene1))

        #----------------------Bromination of benzene-----------------------

        #descriptions
        text6=Description(text=r"\text{接下来以}\mathrm{FeBr_3}\text{催化的苯的溴化反应为例}")
        text7=Description(text=r"\text{首先，}\mathrm{Br_2}\text{与}\mathrm{FeBr_3}\text{结合，}\mathrm{Br_2}\text{异裂}")
        text8=Description(text=r"\text{同时生成一个}\mathrm{Br^+}\text{和一个}\mathrm{FeBr_4^-}")
        text9=Description(text=r"\text{接下来，}\mathrm{Br^+}\text{进攻苯环的}\mathrm{\pi}\text{电子}")
        text10=Description(text=r"\text{随后，}\mathrm{H^+}\text{离去，形成产物溴苯}")
        text11=Description(text=r"\text{最后，}\mathrm{H^+}\text{与}\mathrm{FeBr_4^-}\text{结合，生成}\mathrm{HBr}\text{，}\mathrm{FeBr_3}\text{催化剂再生}")

        benzene2=StructuralFormula(name="C7",pos=[0,0.5*bond_length,0],text=None)
        benzene2.add_atom(name="C8",direction=-30*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C7")
        benzene2.add_atom(name="C9",direction=-90*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C8",
                         side=-1,start_side_edge=True,end_side_edge=True)
        benzene2.add_atom(name="C10",direction=-150*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C9")
        benzene2.add_atom(name="C11",direction=150*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C10",
                         side=-1,start_side_edge=True,end_side_edge=True)
        benzene2.add_atom(name="C12",direction=90*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C11")
        benzene2.add_bond(start="C12",end="C7",bond_type=BondType.DOUBLE_BOND,side=-1,start_side_edge=True,end_side_edge=True)
        benzene2.add_atom(name="H2",direction=90*DEGREES,text="\mathrm{H}",bond_type=BondType.NORMAL_BOND,adjacency="C7")

        self.play(Write(text6))
        self.play(Create(benzene2))

        self.wait(1.5)

        Br2_start=np.array([2*benzene2.attributes.length_global,0,0])
        Br2_target=benzene2.atomic_clusters["C7"]["pos"]+np.array([np.cos(60*DEGREES),np.sin(60*DEGREES),0])*benzene2.attributes.length_global

        Br2_mob=AtomicCluster(text="\mathrm{Br}",pos=Br2_start,attributes=benzene2.attributes)
        benzene2.atomic_clusters["Br2"]={Mobject:Br2_mob,"pos":Br2_start,"adj":[],Bond:[]}
        benzene2.add(Br2_mob)

        Br3_mob=AtomicCluster(text="\mathrm{Br}",pos=np.array([3*benzene2.attributes.length_global,0,0]),attributes=benzene2.attributes)
        Br2_Br3_bond=NormalBond(start=Br2_mob.get_center(),direction=0,start_edge=True,end_edge=True,attributes=benzene2.attributes)

        FeBr3_anchor=np.array([4.0*benzene2.attributes.length_global,0,0])
        FeBr3_start=FeBr3_anchor+np.array([1.5,0,0])
        FeBr3_mob=AtomicCluster(text=r"\mathrm{FeBr_3}",pos=FeBr3_start,attributes=benzene2.attributes,
                                text_offset=np.array([0.3,-0.03,0]))

        self.play(FadeIn(Br2_mob),FadeIn(Br3_mob),FadeIn(Br2_Br3_bond),ReplacementTransform(text6,text7))
        self.wait(1)
        self.play(FadeIn(FeBr3_mob))
        self.wait(0.5)

        self.play(FeBr3_mob.animate.shift(FeBr3_anchor-FeBr3_start),run_time=1)

        Br3_FeBr3_bond=NormalBond(start=Br3_mob.get_center(),direction=0,start_edge=True,end_edge=True,attributes=benzene2.attributes)
        FeBr4_negative=Charge(charge_type=ChargeType.NEGATIVE,text=FeBr3_mob,pos=UL,attributes=benzene2.attributes)

        benzene2.add_charge(text="Br2",pos=UR,charge_type=ChargeType.POSITIVE)
        Br2_positive=benzene2.charges["Br2"]

        self.play(ReplacementTransform(Br2_Br3_bond,Br3_FeBr3_bond),
                  FadeIn(Br2_positive),
                  FadeIn(FeBr4_negative),
                  run_time=1.5)
        self.play(ReplacementTransform(text7,text8))
        self.wait(2)
        self.play(ReplacementTransform(text8,text9))

        shift=Br2_target-Br2_start
        self.play(Br2_mob.animate.shift(shift),
                  Br2_positive.animate.shift(shift),
                  FadeOut(FeBr3_mob),
                  FadeOut(Br3_mob),
                  FadeOut(Br3_FeBr3_bond),
                  FadeOut(FeBr4_negative),
                  run_time=1)
        benzene2.atomic_clusters["Br2"]["pos"]=Br2_target

        C7_C12_double=benzene2.atomic_clusters["C7"][Bond][1]
        C7_H2_normal=benzene2.atomic_clusters["H2"][Bond][0]

        C7_C12_single=benzene2.build_bond(start="C7",end="C12",bond_type=BondType.NORMAL_BOND)
        C7_Br2_in=benzene2.build_bond(start="C7",end="Br2",bond_type=BondType.IN_BOND)
        C12_positive=benzene2.build_charge(text="C12",pos=UL,charge_type=ChargeType.POSITIVE_COORDINATE)

        step_wheland2=ElectronMigrationStep(
            replace=[(C7_C12_double,VGroup(C7_C12_single,C7_Br2_in))],
            create=[C12_positive],
            fadeout=[Br2_positive],
        )

        self.play(benzene2.electron_migration(steps=[step_wheland2],lag_ratio=0,run_time=1.2),
                  BondTypeTransform(bond=C7_H2_normal,
                                    target_type=BondType.OUT_BOND,
                                    angle=30*DEGREES,
                                    about_point=benzene2.atomic_clusters["C7"]["pos"],
                                    sf=benzene2,
                                    run_time=1.2))

        benzene2.delete_bond(start="C7", end="C12")
        benzene2.atomic_clusters["C7"][Bond].extend([C7_C12_single, C7_Br2_in])
        benzene2.atomic_clusters["C12"][Bond].append(C7_C12_single)
        benzene2.atomic_clusters["Br2"][Bond].append(C7_Br2_in)
        benzene2.atomic_clusters["C7"]["adj"].extend(["C12", "Br2"])
        benzene2.atomic_clusters["C12"]["adj"].append("C7")
        benzene2.atomic_clusters["Br2"]["adj"].append("C7")
        benzene2.charges.pop("Br2")
        benzene2.charges["C12"] = C12_positive

        self.wait(2.5)

        C7_C12_double_new=benzene2.build_bond(start="C12", end="C7", bond_type=BondType.DOUBLE_BOND,
                                             side=-1, start_side_edge=True, end_side_edge=True)
        H2_positive=benzene2.build_charge(text="H2", pos=UR, charge_type=ChargeType.POSITIVE)

        step_elimination2=ElectronMigrationStep(
            replace=[(VGroup(C7_H2_normal, C7_C12_single), C7_C12_double_new)],
            create=[H2_positive],
            fadeout=[C12_positive],
        )

        c7_pos=benzene2.atomic_clusters["C7"]["pos"]
        ca, sa = np.cos(30*DEGREES), np.sin(30*DEGREES)
        dx, dy = Br2_target[0]-c7_pos[0], Br2_target[1]-c7_pos[1]
        Br2_final=np.array([c7_pos[0]+dx*ca-dy*sa, c7_pos[1]+dx*sa+dy*ca, 0])
        arc2=ArcBetweenPoints(Br2_target, Br2_final, angle=30*DEGREES)

        self.play(benzene2.electron_migration(steps=[step_elimination2], lag_ratio=0, run_time=1.5),
                  BondTypeTransform(bond=C7_Br2_in,
                                    target_type=BondType.NORMAL_BOND,
                                    angle=30*DEGREES,
                                    about_point=c7_pos,
                                    run_time=1.2),
                  MoveAlongPath(Br2_mob, arc2, run_time=1.2),
                  ReplacementTransform(text9,text10))

        benzene2.delete_bond(start="C7", end="H2")
        benzene2.delete_bond(start="C7", end="C12")
        benzene2.atomic_clusters["C7"][Bond].append(C7_C12_double_new)
        benzene2.atomic_clusters["C12"][Bond].append(C7_C12_double_new)
        benzene2.atomic_clusters["C7"]["adj"].append("C12")
        benzene2.atomic_clusters["C12"]["adj"].append("C7")
        benzene2.charges.pop("C12")
        benzene2.charges["H2"] = H2_positive
        benzene2.atomic_clusters["Br2"]["pos"] = Br2_final

        H2_target=np.array([-2*benzene2.attributes.length_global,0,0])
        shift_h2=H2_target-benzene2.atomic_clusters["H2"][Mobject].get_center()
        self.play(benzene2.atomic_clusters["H2"][Mobject].animate.shift(shift_h2),
                  H2_positive.animate.shift(shift_h2),
                  run_time=1)
        benzene2.atomic_clusters["H2"]["pos"]=H2_target

        self.wait(1.5)

        self.play(ReplacementTransform(text10,text11))

        FeBr4_sf=StructuralFormula(name="Br3Fe",pos=np.array([-5*benzene2.attributes.length_global,0,0]),
                                   text=r"\mathrm{Br_3Fe}",text_offset=np.array([-0.3,-0.03,0]))
        Br4_mob=AtomicCluster(text="\mathrm{Br}",pos=np.array([-4*benzene2.attributes.length_global,0,0]),attributes=FeBr4_sf.attributes)
        FeBr4_sf.atomic_clusters["Br4"]={Mobject:Br4_mob,"pos":np.array([-4*benzene2.attributes.length_global,0,0]),"adj":["Br3Fe"],Bond:[]}
        FeBr4_sf.add(Br4_mob)

        Br3Fe_Br4_bond=Bond(bond_type=BondType.NORMAL_BOND,
                            start=np.array([-5*benzene2.attributes.length_global,0,0]),
                            end=np.array([-4*benzene2.attributes.length_global,0,0]),
                            start_edge=True,end_edge=True,
                            attributes=FeBr4_sf.attributes)
        FeBr4_sf.atomic_clusters["Br3Fe"][Bond].append(Br3Fe_Br4_bond)
        FeBr4_sf.atomic_clusters["Br4"][Bond].append(Br3Fe_Br4_bond)
        FeBr4_sf.atomic_clusters["Br3Fe"]["adj"].append("Br4")
        FeBr4_sf.add(Br3Fe_Br4_bond)

        FeBr4_sf.add_charge(text="Br3Fe",pos=UR,charge_type=ChargeType.NEGATIVE)

        self.play(Create(FeBr4_sf))
        self.wait(1)

        H2_final=np.array([-3*benzene2.attributes.length_global,0,0])
        shift_h3=H2_final-benzene2.atomic_clusters["H2"]["pos"]
        self.play(benzene2.atomic_clusters["H2"][Mobject].animate.shift(shift_h3),
                  H2_positive.animate.shift(shift_h3),
                  run_time=1)
        benzene2.atomic_clusters["H2"]["pos"]=H2_final

        H_Br4_bond=Bond(bond_type=BondType.NORMAL_BOND,
                        start=H2_final,
                        end=FeBr4_sf.atomic_clusters["Br3Fe"]["pos"],
                        start_edge=True,end_edge=True,
                        attributes=benzene2.attributes)

        self.play(ReplacementTransform(Br3Fe_Br4_bond,H_Br4_bond),
                  FadeOut(H2_positive),
                  FadeOut(FeBr4_sf.charges["Br3Fe"]),
                  run_time=1.5)

        FeBr4_sf.delete_bond(start="Br3Fe",end="Br4")
        benzene2.charges.pop("H2")
        FeBr4_negative2=FeBr4_sf.charges.pop("Br3Fe")
        benzene2.remove(H2_positive)
        FeBr4_sf.remove(FeBr4_negative2)

        self.wait(1.5)

        self.play(FadeOut(benzene2,FeBr4_sf,H_Br4_bond,text11))

        #----------------------Nitration of benzene-----------------------

        benzene3=StructuralFormula(name="C13",pos=[0,0.5*bond_length,0],text=None)
        benzene3.add_atom(name="C14",direction=-30*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C13")
        benzene3.add_atom(name="C15",direction=-90*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C14",
                         side=-1,start_side_edge=True,end_side_edge=True)
        benzene3.add_atom(name="C16",direction=-150*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C15")
        benzene3.add_atom(name="C17",direction=150*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C16",
                         side=-1,start_side_edge=True,end_side_edge=True)
        benzene3.add_atom(name="C18",direction=90*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C17")
        benzene3.add_bond(start="C18",end="C13",bond_type=BondType.DOUBLE_BOND,side=-1,start_side_edge=True,end_side_edge=True)
        benzene3.add_atom(name="H3",direction=90*DEGREES,text="\mathrm{H}",bond_type=BondType.NORMAL_BOND,adjacency="C13")

        self.play(Create(benzene3))

        self.wait(0.5)

        N_start=np.array([3*benzene3.attributes.length_global,0,0])
        N_target=benzene3.atomic_clusters["C13"]["pos"]+np.array([np.cos(60*DEGREES),np.sin(60*DEGREES),0])*benzene3.attributes.length_global

        N_mob=AtomicCluster(text="\mathrm{N}",pos=N_start,attributes=benzene3.attributes)
        O1_pos=N_start+np.array([np.cos(90*DEGREES),np.sin(90*DEGREES),0])*benzene3.attributes.length_global
        O2_pos=N_start+np.array([np.cos(-30*DEGREES),np.sin(-30*DEGREES),0])*benzene3.attributes.length_global
        O3_pos=N_start+np.array([np.cos(-150*DEGREES),np.sin(-150*DEGREES),0])*benzene3.attributes.length_global
        O1_mob=AtomicCluster(text="\mathrm{O}",pos=O1_pos,attributes=benzene3.attributes)
        O2_mob=AtomicCluster(text="\mathrm{O}",pos=O2_pos,attributes=benzene3.attributes)
        O3_mob=AtomicCluster(text="\mathrm{O}",pos=O3_pos,attributes=benzene3.attributes)
        H4_pos=O3_pos+np.array([np.cos(150*DEGREES),np.sin(150*DEGREES),0])*benzene3.attributes.length_global
        H4_mob=AtomicCluster(text="\mathrm{H}",pos=H4_pos,attributes=benzene3.attributes)
        lone_pair=Charge(charge_type=ChargeType.PAIR,text=O3_mob,pos=DOWN,attributes=benzene3.attributes)

        benzene3.atomic_clusters["N"]={Mobject:N_mob,"pos":N_start,"adj":[],Bond:[]}
        benzene3.atomic_clusters["O1"]={Mobject:O1_mob,"pos":O1_pos,"adj":[],Bond:[]}
        benzene3.atomic_clusters["O2"]={Mobject:O2_mob,"pos":O2_pos,"adj":[],Bond:[]}
        benzene3.atomic_clusters["O3"]={Mobject:O3_mob,"pos":O3_pos,"adj":[],Bond:[]}
        benzene3.atomic_clusters["H4"]={Mobject:H4_mob,"pos":H4_pos,"adj":[],Bond:[]}

        benzene3.add_bond(start="N",end="O1",bond_type=BondType.NORMAL_BOND)
        benzene3.add_bond(start="N",end="O2",bond_type=BondType.DOUBLE_BOND,side=0)
        benzene3.add_bond(start="N",end="O3",bond_type=BondType.NORMAL_BOND)
        benzene3.add_bond(start="O3",end="H4",bond_type=BondType.NORMAL_BOND)

        N_O1_single_gen=benzene3.atomic_clusters["N"][Bond][0]
        N_O2_bond=benzene3.atomic_clusters["N"][Bond][1]
        N_O3_bond=benzene3.atomic_clusters["N"][Bond][2]
        O3_H_bond=benzene3.atomic_clusters["H4"][Bond][0]

        benzene3.add(N_mob)
        benzene3.add(O1_mob)
        benzene3.add(O2_mob)
        benzene3.add(O3_mob)
        benzene3.add(H4_mob)
        benzene3.add(lone_pair)
        benzene3.add_charge(text="N",pos=UR,charge_type=ChargeType.POSITIVE)
        benzene3.add_charge(text="O1",pos=UR,charge_type=ChargeType.NEGATIVE)
        N_positive=benzene3.charges["N"]
        O1_negative=benzene3.charges["O1"]

        self.play(FadeIn(N_mob),FadeIn(O1_mob),FadeIn(O2_mob),FadeIn(O3_mob),FadeIn(H4_mob),
                  FadeIn(lone_pair),FadeIn(N_O1_single_gen),FadeIn(N_O2_bond),FadeIn(N_O3_bond),
                  FadeIn(O3_H_bond),FadeIn(N_positive),FadeIn(O1_negative))
        self.wait(1)

        H5_pos=O3_pos+np.array([0,-1*benzene3.attributes.length_global,0])
        H5_mob=AtomicCluster(text="\mathrm{H}",pos=H5_pos,attributes=benzene3.attributes)
        O4_pos=H5_pos+np.array([1*benzene3.attributes.length_global,0,0])
        O4_mob=AtomicCluster(text="\mathrm{O}",pos=O4_pos,attributes=benzene3.attributes)
        SO3H_pos=np.array([O4_pos[0]+1*benzene3.attributes.length_global,O4_pos[1],0])
        SO3H_mob=AtomicCluster(text=r"\mathrm{SO_3H}",pos=SO3H_pos,attributes=benzene3.attributes,
                               text_offset=np.array([0.3,-0.03,0]))

        benzene3.atomic_clusters["H5"]={Mobject:H5_mob,"pos":H5_pos,"adj":[],Bond:[]}
        benzene3.atomic_clusters["O4"]={Mobject:O4_mob,"pos":O4_pos,"adj":[],Bond:[]}
        benzene3.atomic_clusters["SO3H"]={Mobject:SO3H_mob,"pos":SO3H_pos,"adj":[],Bond:[]}

        benzene3.add_bond(start="H5",end="O4",bond_type=BondType.NORMAL_BOND)

        O4_SO3H_bond=Bond(bond_type=BondType.NORMAL_BOND,
                          start=O4_pos,
                          end=SO3H_pos,
                          start_edge=True,end_edge=True,
                          attributes=benzene3.attributes)
        benzene3.atomic_clusters["O4"][Bond].append(O4_SO3H_bond)
        benzene3.atomic_clusters["SO3H"][Bond].append(O4_SO3H_bond)
        benzene3.atomic_clusters["O4"]["adj"].append("SO3H")
        benzene3.atomic_clusters["SO3H"]["adj"].append("O4")
        benzene3.add(O4_SO3H_bond)

        H_O_bond=benzene3.atomic_clusters["H5"][Bond][0]

        benzene3.add(H5_mob)
        benzene3.add(O4_mob)
        benzene3.add(SO3H_mob)

        self.play(FadeIn(H5_mob),FadeIn(O4_mob),FadeIn(SO3H_mob),FadeIn(H_O_bond),FadeIn(O4_SO3H_bond))
        self.wait(0.5)

        O3_H2_bond=benzene3.build_bond(start="O3",end="H5",bond_type=BondType.NORMAL_BOND)
        O3_positive=benzene3.build_charge(text="O3",pos=DR,charge_type=ChargeType.POSITIVE)
        O4_negative=Charge(charge_type=ChargeType.NEGATIVE,text=O4_mob,pos=UL,attributes=benzene3.attributes)

        step_protonation=ElectronMigrationStep(
            replace=[(lone_pair,O3_H2_bond),
                     (H_O_bond,O4_negative)],
            create=[O3_positive],
        )

        self.play(benzene3.electron_migration(steps=[step_protonation],lag_ratio=0,run_time=1.5))

        benzene3.atomic_clusters["O3"][Bond].append(O3_H2_bond)
        benzene3.atomic_clusters["H5"][Bond].remove(H_O_bond)
        benzene3.atomic_clusters["H5"][Bond].append(O3_H2_bond)
        benzene3.atomic_clusters["O4"][Bond].remove(H_O_bond)
        benzene3.atomic_clusters["H5"]["adj"].remove("O4")
        benzene3.atomic_clusters["H5"]["adj"].append("O3")
        benzene3.atomic_clusters["O4"]["adj"].remove("H5")
        benzene3.atomic_clusters["O3"]["adj"].append("H5")
        benzene3.charges["O3"] = O3_positive

        self.wait(1)

        self.play(FadeOut(O4_mob),FadeOut(SO3H_mob),FadeOut(O4_negative),FadeOut(O4_SO3H_bond))
        benzene3.remove(O4_mob,SO3H_mob,O4_negative,O4_SO3H_bond)

        N_O1_bond=benzene3.build_bond(start="N",end="O1",bond_type=BondType.DOUBLE_BOND,side=0)
        O3_lone_pair2=Charge(charge_type=ChargeType.PAIR,text=O3_mob,pos=UR,attributes=benzene3.attributes)

        step_dehydration=ElectronMigrationStep(
            replace=[(VGroup(N_O1_single_gen,O1_negative),N_O1_bond),
                     (N_O3_bond,O3_lone_pair2)],
            fadeout=[O3_positive],
        )

        self.play(benzene3.electron_migration(steps=[step_dehydration],lag_ratio=0,run_time=1.5))

        benzene3.atomic_clusters["N"][Bond].remove(N_O1_single_gen)
        benzene3.atomic_clusters["N"][Bond].append(N_O1_bond)
        benzene3.atomic_clusters["O1"][Bond].remove(N_O1_single_gen)
        benzene3.atomic_clusters["O1"][Bond].append(N_O1_bond)
        benzene3.atomic_clusters["N"][Bond].remove(N_O3_bond)
        benzene3.atomic_clusters["O3"][Bond].remove(N_O3_bond)
        benzene3.atomic_clusters["N"]["adj"].remove("O3")
        benzene3.atomic_clusters["O3"]["adj"].remove("N")
        benzene3.charges.pop("O1")
        benzene3.charges.pop("O3")

        self.wait(1)

        self.play(benzene3.rotate_atoms(atom_names="O1",center="N",angle=30*DEGREES,run_time=1.2),
                  benzene3.rotate_atoms(atom_names="O2",center="N",angle=-30*DEGREES,run_time=1.2),
                  FadeOut(O3_mob),FadeOut(H4_mob),FadeOut(H5_mob),
                  FadeOut(O3_H_bond),FadeOut(O3_H2_bond),FadeOut(O3_lone_pair2),
                  run_time=1.2)
        benzene3.remove(O3_mob,H4_mob,H5_mob,O3_H_bond,O3_H2_bond,O3_lone_pair2)

        self.wait(1)

        shift3=N_target-N_start
        self.play(N_mob.animate.shift(shift3),
                  O1_mob.animate.shift(shift3),
                  O2_mob.animate.shift(shift3),
                  N_positive.animate.shift(shift3),
                  N_O1_bond.animate.shift(shift3),
                  N_O2_bond.animate.shift(shift3),
                  run_time=1)
        benzene3.atomic_clusters["N"]["pos"]=N_target
        benzene3.atomic_clusters["O1"]["pos"]=benzene3.atomic_clusters["O1"]["pos"]+shift3
        benzene3.atomic_clusters["O2"]["pos"]=benzene3.atomic_clusters["O2"]["pos"]+shift3
        N_O1_bond.start=N_target
        N_O1_bond.end=benzene3.atomic_clusters["O1"]["pos"]
        N_O2_bond.start=N_target
        N_O2_bond.end=benzene3.atomic_clusters["O2"]["pos"]

        C13_C18_double=benzene3.atomic_clusters["C13"][Bond][1]
        C13_H3_normal=benzene3.atomic_clusters["H3"][Bond][0]

        C13_C18_single=benzene3.build_bond(start="C13",end="C18",bond_type=BondType.NORMAL_BOND)
        C13_N_in=benzene3.build_bond(start="C13",end="N",bond_type=BondType.IN_BOND)
        N_O1_single=benzene3.build_bond(start="N",end="O1",bond_type=BondType.NORMAL_BOND)
        C18_positive=benzene3.build_charge(text="C18",pos=UL,charge_type=ChargeType.POSITIVE_COORDINATE)
        O1_negative=benzene3.build_charge(text="O1",pos=UR,charge_type=ChargeType.NEGATIVE)

        step_wheland3=ElectronMigrationStep(
            replace=[(C13_C18_double,VGroup(C13_C18_single,C13_N_in)),
                     (N_O1_bond,VGroup(N_O1_single,O1_negative))],
            create=[C18_positive],
        )

        wheland_em=benzene3.electron_migration(steps=[step_wheland3],run_time=1.2)
        benzene3.remove(C13_C18_double,N_O1_bond)
        self.add(wheland_em.mobject)
        self.play(wheland_em,
                  BondTypeTransform(bond=C13_H3_normal,
                                    target_type=BondType.OUT_BOND,
                                    angle=30*DEGREES,
                                    about_point=benzene3.atomic_clusters["C13"]["pos"],
                                    sf=benzene3,
                                    run_time=1.2),
                  benzene3.rotate_atoms(atom_names="O2",center="N",angle=60*DEGREES,run_time=1.2))

        benzene3.delete_bond(start="C13", end="C18")
        benzene3.atomic_clusters["C13"][Bond].extend([C13_C18_single, C13_N_in])
        benzene3.atomic_clusters["C18"][Bond].append(C13_C18_single)
        benzene3.atomic_clusters["N"][Bond].remove(N_O1_bond)
        benzene3.atomic_clusters["N"][Bond].append(N_O1_single)
        benzene3.atomic_clusters["O1"][Bond].remove(N_O1_bond)
        benzene3.atomic_clusters["O1"][Bond].append(N_O1_single)
        benzene3.atomic_clusters["N"][Bond].append(C13_N_in)
        benzene3.atomic_clusters["C13"]["adj"].extend(["C18", "N"])
        benzene3.atomic_clusters["C18"]["adj"].append("C13")
        benzene3.atomic_clusters["N"]["adj"].append("C13")
        benzene3.charges["C18"] = C18_positive
        benzene3.charges["O1"] = O1_negative

        self.wait(2.5)

        C13_C18_double_new=benzene3.build_bond(start="C18", end="C13", bond_type=BondType.DOUBLE_BOND,
                                              side=-1, start_side_edge=True, end_side_edge=True)
        H3_positive=benzene3.build_charge(text="H3", pos=UR, charge_type=ChargeType.POSITIVE)

        elim_source=VGroup(C13_H3_normal, C13_C18_single)
        step_elimination3=ElectronMigrationStep(
            replace=[(elim_source, C13_C18_double_new)],
            create=[H3_positive],
            fadeout=[C18_positive],
        )

        em_anim=benzene3.electron_migration(steps=[step_elimination3], lag_ratio=0, run_time=1.5)
        benzene3.remove(C13_H3_normal, C13_C18_single, C18_positive)
        self.add(em_anim.mobject)

        c13_pos=benzene3.atomic_clusters["C13"]["pos"]
        c13_n_btt=BondTypeTransform(bond=C13_N_in,
                                    target_type=BondType.NORMAL_BOND,
                                    angle=30*DEGREES,
                                    about_point=c13_pos,
                                    run_time=1.2)
        benzene3.atomic_clusters["N"][Bond].remove(C13_N_in)
        nitro_rot=benzene3.rotate_atoms(atom_names=["N","O1","O2"],center="C13",angle=30*DEGREES,run_time=1.2)
        benzene3.atomic_clusters["N"][Bond].append(C13_N_in)

        self.play(em_anim,
                  c13_n_btt,
                  nitro_rot)

        benzene3.delete_bond(start="C13", end="H3")
        benzene3.delete_bond(start="C13", end="C18")
        benzene3.atomic_clusters["C13"][Bond].append(C13_C18_double_new)
        benzene3.atomic_clusters["C18"][Bond].append(C13_C18_double_new)
        benzene3.atomic_clusters["C13"]["adj"].append("C18")
        benzene3.atomic_clusters["C18"]["adj"].append("C13")
        benzene3.charges.pop("C18")
        benzene3.charges["H3"] = H3_positive

        H3_target=np.array([-2*benzene3.attributes.length_global,0,0])
        shift_h4=H3_target-benzene3.atomic_clusters["H3"][Mobject].get_center()
        self.play(benzene3.atomic_clusters["H3"][Mobject].animate.shift(shift_h4),
                  H3_positive.animate.shift(shift_h4),
                  run_time=1)
        benzene3.atomic_clusters["H3"]["pos"]=H3_target

        self.wait(1.5)
