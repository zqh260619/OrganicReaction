#manim SubstitutionReaction2.py test -pqh

from OrganicReactionTools import *

class test(Scene):
    def construct(self):

        title=Title(text=r"\text{一些常见的取代反应机理}\quad\text{续}",pos=ORIGIN)
        subtitle=Subtitle(text=r"\text{苯环上取代反应}",pos=[0,-0.7,0])
        self.play(Write(title),Write(subtitle))
        self.wait(1.5)
        self.play(FadeOut(title,subtitle))

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

        #descriptions
        text12=Description(text=r"\text{另一经典反应是苯的硝化反应，反应需要浓}\mathrm{HNO_3}\text{和浓}\mathrm{H_2SO_4}\text{，}\\\text{其中浓}\mathrm{H_2SO_4}\text{作催化剂}")
        text13=Description(text=r"\mathrm{HNO_3}\text{分子的羟基}\mathrm{O}\text{先被浓}\mathrm{H_2SO_4}\text{质子化}")
        text14=Description(text=r"\text{然后快速脱去一个水分子，形成}\mathrm{NO_2^+}")
        text15=Description(text=r"\text{接着}\mathrm{NO_2^+}\text{进攻苯环，形成中间体}")
        text16=Description(text=r"\text{最后中间体的}\mathrm{H^+}\text{被体系中的}\mathrm{HSO_4^-}\text{拔除，催化剂再生}")

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

        self.play(Write(text12))
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
        benzene3.add_charge(text="N",pos=LEFT,charge_type=ChargeType.POSITIVE)
        benzene3.add_charge(text="O1",pos=UR,charge_type=ChargeType.NEGATIVE)
        N_positive=benzene3.charges["N"]
        O1_negative=benzene3.charges["O1"]

        self.play(FadeIn(N_mob),FadeIn(O1_mob),FadeIn(O2_mob),FadeIn(O3_mob),FadeIn(H4_mob),
                  FadeIn(lone_pair),FadeIn(N_O1_single_gen),FadeIn(N_O2_bond),FadeIn(N_O3_bond),
                  FadeIn(O3_H_bond),FadeIn(N_positive),FadeIn(O1_negative))

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
        self.play(ReplacementTransform(text12,text13))
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

        self.play(ReplacementTransform(text13,text14))

        N_O1_bond=benzene3.build_bond(start="N",end="O1",bond_type=BondType.DOUBLE_BOND,side=0)
        pair_dir=np.array([np.cos(30*DEGREES),np.sin(30*DEGREES),0])
        O3_lone_pair2=Charge(charge_type=ChargeType.PAIR_COORDINATE,
                             text=O3_mob.get_center()+pair_dir*0.21,
                             pos=pair_dir,
                             attributes=benzene3.attributes)

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

        self.play(benzene3.rotate_atoms(atom_names="O1",center="N",angle=30*DEGREES,run_time=1.2),
                  benzene3.rotate_atoms(atom_names="O2",center="N",angle=-30*DEGREES,run_time=1.2),
                  FadeOut(O3_mob),FadeOut(H4_mob),FadeOut(H5_mob),
                  FadeOut(O3_H_bond),FadeOut(O3_H2_bond),FadeOut(O3_lone_pair2),
                  run_time=1.2)
        benzene3.remove(O3_mob,H4_mob,H5_mob,O3_H_bond,O3_H2_bond,O3_lone_pair2)

        self.wait(0.5)
        self.play(ReplacementTransform(text14,text15))

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
        self.play(ReplacementTransform(text15,text16))

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

        H3_pos=benzene3.atomic_clusters["H3"]["pos"]
        O5_pos=H3_pos+np.array([-1*benzene3.attributes.length_global,0,0])
        O5_mob=AtomicCluster(text="\mathrm{O}",pos=O5_pos,attributes=benzene3.attributes)
        HO3S_pos=O5_pos+np.array([-1*benzene3.attributes.length_global,0,0])
        HO3S_mob=AtomicCluster(text=r"\mathrm{HO_3S}",pos=HO3S_pos,attributes=benzene3.attributes,
                               text_offset=np.array([-0.35,0,0]))

        benzene3.atomic_clusters["O5"]={Mobject:O5_mob,"pos":O5_pos,"adj":[],Bond:[]}
        benzene3.atomic_clusters["HO3S"]={Mobject:HO3S_mob,"pos":HO3S_pos,"adj":[],Bond:[]}

        HO3S_O5_bond=Bond(bond_type=BondType.NORMAL_BOND,
                          start=HO3S_pos,
                          end=O5_pos,
                          start_edge=True,end_edge=True,
                          attributes=benzene3.attributes)
        benzene3.atomic_clusters["HO3S"][Bond].append(HO3S_O5_bond)
        benzene3.atomic_clusters["O5"][Bond].append(HO3S_O5_bond)
        benzene3.atomic_clusters["HO3S"]["adj"].append("O5")
        benzene3.atomic_clusters["O5"]["adj"].append("HO3S")
        benzene3.add(HO3S_O5_bond)
        benzene3.add(O5_mob)
        benzene3.add(HO3S_mob)
        O5_negative=Charge(charge_type=ChargeType.NEGATIVE,text=O5_mob,pos=UR,attributes=benzene3.attributes)
        benzene3.add(O5_negative)

        self.play(FadeIn(O5_mob),FadeIn(HO3S_mob),FadeIn(HO3S_O5_bond),FadeIn(O5_negative))
        self.wait(1)

        O5_H_bond=benzene3.build_bond(start="O5",end="H3",bond_type=BondType.NORMAL_BOND)
        C13_C18_double_new=benzene3.build_bond(start="C18", end="C13", bond_type=BondType.DOUBLE_BOND,
                                              side=-1, start_side_edge=True, end_side_edge=True)

        elim_source=VGroup(C13_H3_normal, C13_C18_single)
        step_elimination3=ElectronMigrationStep(
            replace=[(O5_negative,O5_H_bond),
                     (elim_source, C13_C18_double_new)],
            fadeout=[C18_positive],
        )

        em_anim=benzene3.electron_migration(steps=[step_elimination3], lag_ratio=0, run_time=1.5)
        benzene3.remove(O5_negative, C13_H3_normal, C13_C18_single, C18_positive)
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

        benzene3.atomic_clusters["O5"][Bond].append(O5_H_bond)
        benzene3.atomic_clusters["O5"]["adj"].append("H3")
        benzene3.atomic_clusters["H3"][Bond].append(O5_H_bond)
        benzene3.atomic_clusters["H3"]["adj"].append("O5")

        benzene3.delete_bond(start="C13", end="H3")
        benzene3.delete_bond(start="C13", end="C18")
        benzene3.atomic_clusters["C13"][Bond].append(C13_C18_double_new)
        benzene3.atomic_clusters["C18"][Bond].append(C13_C18_double_new)
        benzene3.atomic_clusters["C13"]["adj"].append("C18")
        benzene3.atomic_clusters["C18"]["adj"].append("C13")
        benzene3.charges.pop("C18")

        H3_target=np.array([-2*benzene3.attributes.length_global,0,0])
        shift_h4=H3_target-benzene3.atomic_clusters["H3"][Mobject].get_center()
        self.play(benzene3.atomic_clusters["H3"][Mobject].animate.shift(shift_h4),
                  O5_mob.animate.shift(shift_h4),
                  HO3S_mob.animate.shift(shift_h4),
                  O5_H_bond.animate.shift(shift_h4),
                  HO3S_O5_bond.animate.shift(shift_h4),
                  run_time=1)
        benzene3.atomic_clusters["H3"]["pos"]=H3_target
        benzene3.atomic_clusters["O5"]["pos"]=benzene3.atomic_clusters["O5"]["pos"]+shift_h4
        benzene3.atomic_clusters["HO3S"]["pos"]=benzene3.atomic_clusters["HO3S"]["pos"]+shift_h4
        O5_H_bond.start=benzene3.atomic_clusters["O5"]["pos"]
        O5_H_bond.end=H3_target
        HO3S_O5_bond.start=benzene3.atomic_clusters["HO3S"]["pos"]
        HO3S_O5_bond.end=benzene3.atomic_clusters["O5"]["pos"]

        self.wait(1.5)

        self.play(FadeOut(benzene3,text16,SEAr_reaction,O5_H_bond,C13_C18_double_new),run_time=1)
        self.wait(1)

        #----------------------SNAr Reaction-----------------------

        SNAr_reaction=Title(text=r"\mathrm{S_NAr}\text{（芳香亲核取代）}")
        self.play(Write(SNAr_reaction))

        #消除-加成机理
        a_d_mechanism=Subtitle(text=r"\text{加成-消除机理}")
        self.play(Write(a_d_mechanism))
        self.wait(1)

        #descriptions
        text17=Description(text=r"\text{在加成-消除机理中，苯环上必须有一个强吸电子基团（}\mathrm{EWG}\text{）在邻对位}")
        text18=Description(text=r"\mathrm{EWG}\text{分为两类，一类是共轭类}\mathrm{EWG}\text{，另一种是诱导类}\mathrm{EWG}")
        text19=Description(text=r"\text{前者包括硝基、氰基，或者羰基等，后者包括三氟甲基等}")
        text20=Description(text=r"\text{此处以酮羰基为例演示此机理}")
        text21=Description(text=r"\mathrm{X}\text{为一个好的离去基团，通常是卤素原子}")
        text22=Description(text=r"\mathrm{Nu^-}\text{为亲核试剂，通常为醇负离子、氨、一/二级胺或者硫醇盐}")
        text23=Description(text=r"\text{首先，}\mathrm{Nu^-}\text{进攻离去基团所在的碳，}\mathrm{sp^2}\text{碳变为}\mathrm{sp^3}\text{碳，芳香性被破坏}")
        text24=Description(text=r"\text{负电荷可以离域，从而被酮羰基稳定}")
        text25=Description(text=r"\text{随后，}\mathrm{X^-}\text{离去，芳香性恢复，生成取代产物}")

        self.play(Write(text17))

        #苯环连接EWG
        benzene_ewg=StructuralFormula(name="C19",pos=[0,-0.7,0],text=None)
        benzene_ewg.add_atom(name="C20",direction=-30*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C19")
        benzene_ewg.add_atom(name="C21",direction=-90*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C20",
                             side=-1,start_side_edge=True,end_side_edge=True)
        benzene_ewg.add_atom(name="C22",direction=-150*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C21")
        benzene_ewg.add_atom(name="C23",direction=150*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C22",
                             side=-1,start_side_edge=True,end_side_edge=True)
        benzene_ewg.add_atom(name="C24",direction=90*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C23")
        benzene_ewg.add_bond(start="C24",end="C19",bond_type=BondType.DOUBLE_BOND,side=-1,start_side_edge=True,end_side_edge=True)
        benzene_ewg.add_atom(name="EWG",direction=90*DEGREES,text=r"\mathrm{EWG}",bond_type=BondType.NORMAL_BOND,adjacency="C19")

        self.play(Create(benzene_ewg))
        self.wait(1)

        #分裂为两个相同的分子
        ewg_left_shift=np.array([-1.5,0,0],dtype=float)
        ewg_right_shift=np.array([5,0,0],dtype=float)
        right_mol=benzene_ewg.copy()
        right_mol.shift(ewg_right_shift)

        self.play(ReplacementTransform(text17,text18))
        self.play(benzene_ewg.animate.shift(ewg_left_shift),
                  ReplacementTransform(benzene_ewg.copy(),right_mol),
                  run_time=1.5)

        for data in benzene_ewg.atomic_clusters.values():
            data["pos"]=np.array(data["pos"],dtype=float)+ewg_left_shift
        for data in right_mol.atomic_clusters.values():
            data["pos"]=np.array(data["pos"],dtype=float)+ewg_right_shift

        self.wait(0.5)

        gong_e=Description(text=r"\text{共轭类}",pos=[-1.5,1.5,0])
        you_dao=Description(text=r"\text{诱导类}",pos=[5,1.5,0])
        self.play(Write(gong_e),Write(you_dao))
        self.wait(1)

        #共轭类：硝基苯、氰基苯、乙酰基苯
        nitro_sf=StructuralFormula(name="C25",pos=[-4.5,-0.7,0],text=None)
        nitro_sf.add_atom(name="C26",direction=-30*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C25")
        nitro_sf.add_atom(name="C27",direction=-90*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C26",
                          side=-1,start_side_edge=True,end_side_edge=True)
        nitro_sf.add_atom(name="C28",direction=-150*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C27")
        nitro_sf.add_atom(name="C29",direction=150*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C28",
                          side=-1,start_side_edge=True,end_side_edge=True)
        nitro_sf.add_atom(name="C30",direction=90*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C29")
        nitro_sf.add_bond(start="C30",end="C25",bond_type=BondType.DOUBLE_BOND,side=-1,start_side_edge=True,end_side_edge=True)
        nitro_sf.add_atom(name="N",direction=90*DEGREES,text=r"\mathrm{N}",bond_type=BondType.NORMAL_BOND,adjacency="C25")
        nitro_sf.add_atom(name="O1",direction=150*DEGREES,text=r"\mathrm{O}",bond_type=BondType.NORMAL_BOND,adjacency="N")
        nitro_sf.add_atom(name="O2",direction=30*DEGREES,text=r"\mathrm{O}",bond_type=BondType.DOUBLE_BOND,adjacency="N",side=0)
        nitro_sf.add_charge(text="N",pos=LEFT,charge_type=ChargeType.POSITIVE)
        nitro_sf.add_charge(text="O1",pos=UR,charge_type=ChargeType.NEGATIVE)

        cyano_sf=StructuralFormula(name="C31",pos=[-1.5,-0.7,0],text=None)
        cyano_sf.add_atom(name="C32",direction=-30*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C31")
        cyano_sf.add_atom(name="C33",direction=-90*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C32",
                          side=-1,start_side_edge=True,end_side_edge=True)
        cyano_sf.add_atom(name="C34",direction=-150*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C33")
        cyano_sf.add_atom(name="C35",direction=150*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C34",
                          side=-1,start_side_edge=True,end_side_edge=True)
        cyano_sf.add_atom(name="C36",direction=90*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C35")
        cyano_sf.add_bond(start="C36",end="C31",bond_type=BondType.DOUBLE_BOND,side=-1,start_side_edge=True,end_side_edge=True)

        CN_bond_end=cyano_sf.atomic_clusters["C31"]["pos"]+np.array([0,1,0],dtype=float)
        #分成两个字符串构建，使C成为独立的子对象，便于把C精确对齐到键的正上方
        CN_mob=MathTex(r"\mathrm{C}",r"\mathrm{N}",color=cyano_sf.attributes.color,
                       font_size=cyano_sf.attributes.font_size,tex_template=mytemplate)
        CN_mob.move_to(CN_bond_end)
        CN_mob.shift(CN_bond_end-CN_mob.submobjects[0].get_center())

        cyano_sf.atomic_clusters["CN"]={Mobject:CN_mob,"pos":CN_bond_end,"adj":["C31"],Bond:[]}
        C31_CN_bond=Bond(bond_type=BondType.NORMAL_BOND,
                         start=cyano_sf.atomic_clusters["C31"]["pos"],
                         end=CN_bond_end,
                         start_edge=False,end_edge=True,
                         attributes=cyano_sf.attributes)
        cyano_sf.atomic_clusters["C31"][Bond].append(C31_CN_bond)
        cyano_sf.atomic_clusters["CN"][Bond].append(C31_CN_bond)
        cyano_sf.atomic_clusters["C31"]["adj"].append("CN")
        cyano_sf.add(C31_CN_bond)
        cyano_sf.add(CN_mob)

        acetyl_sf=StructuralFormula(name="C37",pos=[1.5,-0.7,0],text=None)
        acetyl_sf.add_atom(name="C38",direction=-30*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C37")
        acetyl_sf.add_atom(name="C39",direction=-90*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C38",
                           side=-1,start_side_edge=True,end_side_edge=True)
        acetyl_sf.add_atom(name="C40",direction=-150*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C39")
        acetyl_sf.add_atom(name="C41",direction=150*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C40",
                           side=-1,start_side_edge=True,end_side_edge=True)
        acetyl_sf.add_atom(name="C42",direction=90*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C41")
        acetyl_sf.add_bond(start="C42",end="C37",bond_type=BondType.DOUBLE_BOND,side=-1,start_side_edge=True,end_side_edge=True)
        acetyl_sf.add_atom(name="C43",direction=90*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C37")
        acetyl_sf.add_atom(name="O",direction=30*DEGREES,text=r"\mathrm{O}",bond_type=BondType.DOUBLE_BOND,adjacency="C43",side=0)
        acetyl_sf.add_atom(name="C44",direction=150*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C43")

        #诱导类：三氟甲基苯
        cf3_sf=StructuralFormula(name="C45",pos=[5,-0.7,0],text=None)
        cf3_sf.add_atom(name="C46",direction=-30*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C45")
        cf3_sf.add_atom(name="C47",direction=-90*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C46",
                        side=-1,start_side_edge=True,end_side_edge=True)
        cf3_sf.add_atom(name="C48",direction=-150*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C47")
        cf3_sf.add_atom(name="C49",direction=150*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C48",
                        side=-1,start_side_edge=True,end_side_edge=True)
        cf3_sf.add_atom(name="C50",direction=90*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C49")
        cf3_sf.add_bond(start="C50",end="C45",bond_type=BondType.DOUBLE_BOND,side=-1,start_side_edge=True,end_side_edge=True)
        cf3_sf.add_atom(name="C51",direction=90*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C45")
        cf3_sf.add_atom(name="F1",direction=150*DEGREES,text=r"\mathrm{F}",bond_type=BondType.OUT_BOND,adjacency="C51")
        cf3_sf.add_atom(name="F2",direction=120*DEGREES,text=r"\mathrm{F}",bond_type=BondType.IN_BOND,adjacency="C51")
        cf3_sf.add_atom(name="F3",direction=30*DEGREES,text=r"\mathrm{F}",bond_type=BondType.NORMAL_BOND,adjacency="C51")

        #左边的分子变为三个分子
        #只对苯环之外的对象做变形：源分子的竖直键与EWG文本（及其副本）
        #变换为目标分子苯环之外的全部对象（多出的化学键、文本标签、电荷全部由EWG变换而来）；
        #硝基苯与乙酰基苯的苯环从中间苯环的位置平移而来（形状完全相同，ReplacementTransform表现为纯平移）
        nitro_ring=VGroup(*nitro_sf.submobjects[:6])
        acetyl_ring=VGroup(*acetyl_sf.submobjects[:6])
        nitro_out=VGroup(*nitro_sf.submobjects[6:])
        acetyl_out=VGroup(*acetyl_sf.submobjects[6:])
        cyano_out=VGroup(*cyano_sf.submobjects[6:])

        self.play(ReplacementTransform(text18,text19))
        self.play(ReplacementTransform(VGroup(*benzene_ewg.submobjects[6:]),cyano_out),
                  ReplacementTransform(VGroup(*[o.copy() for o in benzene_ewg.submobjects[6:]]),nitro_out),
                  ReplacementTransform(VGroup(*[b.copy() for b in benzene_ewg.submobjects[:6]]),nitro_ring),
                  ReplacementTransform(VGroup(*[o.copy() for o in benzene_ewg.submobjects[6:]]),acetyl_out),
                  ReplacementTransform(VGroup(*[b.copy() for b in benzene_ewg.submobjects[:6]]),acetyl_ring),
                  run_time=1.5)

        self.remove(benzene_ewg)
        #scene.remove不解散分组，需显式移除被重组后遗留在场景中的六根苯环键
        self.remove(*benzene_ewg.submobjects[:6])
        self.add(cyano_sf)
        self.add(nitro_sf)
        self.add(acetyl_sf)
        self.wait(1)

        #右边的分子变为三氟甲基苯
        #同样苯环保持不动：竖直键与EWG文本及其副本变换为苯环之外的C-F键与F文本
        cf3_out=VGroup(*cf3_sf.submobjects[6:])

        self.play(ReplacementTransform(VGroup(*right_mol.submobjects[6:]),cf3_out),run_time=1.5)

        self.remove(right_mol)
        #scene.remove不解散分组，需显式移除被重组后遗留在场景中的六根苯环键
        self.remove(*right_mol.submobjects[:6])
        self.add(cf3_sf)
        self.wait(2)

        #其他分子与描述性文本消失（标题、副标题不变），乙酰基苯移动到中间
        #目标位置：横坐标0，纵坐标比第一部分第二部分的苯环位置（顶碳y=0.5）低0.2
        acetyl_target=np.array([0,0.3,0],dtype=float)
        acetyl_shift=acetyl_target-acetyl_sf.atomic_clusters["C37"]["pos"]

        self.play(FadeOut(nitro_sf,cyano_sf,cf3_sf,gong_e,you_dao),
                  acetyl_sf.animate.shift(acetyl_shift),
                  run_time=1.5)

        acetyl_bonds=set()
        for data in acetyl_sf.atomic_clusters.values():
            data["pos"]=np.array(data["pos"],dtype=float)+acetyl_shift
            for bond in data[Bond]:
                acetyl_bonds.add(bond)
        for bond in acetyl_bonds:
            bond.start=np.array(bond.start,dtype=float)+acetyl_shift
            bond.end=np.array(bond.end,dtype=float)+acetyl_shift

        self.wait(0.5)

        #底部的"前者包括……"文本变换为text20
        self.play(ReplacementTransform(text19,text20))
        self.wait(1)

        #在乙酰基苯右上角的碳（C38，乙酰基的邻位）上添加离去基团X，使用NormalBond连接
        acetyl_sf.add_atom(name="X",direction=30*DEGREES,text=r"\mathrm{X}",bond_type=BondType.NORMAL_BOND,adjacency="C38")
        X_mob=acetyl_sf.atomic_clusters["X"][Mobject]
        C38_X_bond=acetyl_sf.atomic_clusters["X"][Bond][0]

        #右侧出现Nu^-（负电荷用API的Charge类表示）
        Nu_pos=np.array([3.5,-0.2,0],dtype=float)
        Nu_mob=AtomicCluster(text=r"\mathrm{Nu}",pos=Nu_pos,attributes=acetyl_sf.attributes)
        Nu_charge=Charge(charge_type=ChargeType.NEGATIVE,text=Nu_mob,pos=UR,attributes=acetyl_sf.attributes)
        acetyl_sf.atomic_clusters["Nu"]={Mobject:Nu_mob,"pos":Nu_pos,"adj":[],Bond:[]}
        acetyl_sf.add(Nu_mob)

        self.play(FadeIn(X_mob),FadeIn(C38_X_bond),FadeIn(Nu_mob),FadeIn(Nu_charge))
        self.play(ReplacementTransform(text20,text21))
        self.wait(2)
        self.play(ReplacementTransform(text21,text22))
        self.wait(1)

        #Nu^-依次变换为RO^-、NH3、NH2R、NHR2、RS^-，最后回到Nu^-
        RO_mob=AtomicCluster(text=r"\mathrm{RO}",pos=Nu_pos,attributes=acetyl_sf.attributes)
        RO_charge=Charge(charge_type=ChargeType.NEGATIVE,text=RO_mob,pos=UR,attributes=acetyl_sf.attributes)
        NH3_mob=AtomicCluster(text=r"\mathrm{NH_3}",pos=Nu_pos,attributes=acetyl_sf.attributes)
        NH2R_mob=AtomicCluster(text=r"\mathrm{NH_2R}",pos=Nu_pos,attributes=acetyl_sf.attributes)
        NHR2_mob=AtomicCluster(text=r"\mathrm{NHR_2}",pos=Nu_pos,attributes=acetyl_sf.attributes)
        RS_mob=AtomicCluster(text=r"\mathrm{RS}",pos=Nu_pos,attributes=acetyl_sf.attributes)
        RS_charge=Charge(charge_type=ChargeType.NEGATIVE,text=RS_mob,pos=UR,attributes=acetyl_sf.attributes)
        Nu_final=AtomicCluster(text=r"\mathrm{Nu}",pos=Nu_pos,attributes=acetyl_sf.attributes)
        Nu_final_charge=Charge(charge_type=ChargeType.NEGATIVE,text=Nu_final,pos=UR,attributes=acetyl_sf.attributes)

        self.play(ReplacementTransform(Nu_mob,RO_mob),
                  ReplacementTransform(Nu_charge,RO_charge))
        self.wait(0.5)
        self.play(ReplacementTransform(RO_mob,NH3_mob),
                  FadeOut(RO_charge))
        self.wait(0.5)
        self.play(ReplacementTransform(NH3_mob,NH2R_mob))
        self.wait(0.5)
        self.play(ReplacementTransform(NH2R_mob,NHR2_mob))
        self.wait(0.5)
        self.play(ReplacementTransform(NHR2_mob,RS_mob),
                  FadeIn(RS_charge))
        self.wait(0.5)
        self.play(ReplacementTransform(RS_mob,Nu_final),
                  ReplacementTransform(RS_charge,Nu_final_charge))
        acetyl_sf.atomic_clusters["Nu"][Mobject]=Nu_final
        acetyl_sf.charges["Nu"]=Nu_final_charge
        acetyl_sf.add(Nu_final_charge)
        self.add(acetyl_sf)
        self.wait(1)
        self.play(ReplacementTransform(text22,text23))

        #Nu^-进攻X所在的碳C38：移动到C38右侧一个单位处
        Nu_target=acetyl_sf.atomic_clusters["C38"]["pos"]+np.array([1,0,0],dtype=float)
        Nu_shift=Nu_target-Nu_pos
        self.play(Nu_final.animate.shift(Nu_shift),
                  Nu_final_charge.animate.shift(Nu_shift),
                  run_time=1)
        acetyl_sf.atomic_clusters["Nu"]["pos"]=Nu_target

        #负电荷变换为C-Nu的OutBond；
        #然后C38与其下方C39的双键变换为原位的单键和C39右下角的负电荷；
        #同时C-X键逆时针旋转30°并变换为InBond
        C38_C39_double=acetyl_sf.atomic_clusters["C38"][Bond][1]
        C38_Nu_out=acetyl_sf.build_bond(start="C38",end="Nu",bond_type=BondType.OUT_BOND)
        C38_C39_single=acetyl_sf.build_bond(start="C38",end="C39",bond_type=BondType.NORMAL_BOND)
        C39_negative=Charge(charge_type=ChargeType.NEGATIVE_COORDINATE,
                            text=acetyl_sf.atomic_clusters["C39"]["pos"],
                            pos=DR,attributes=acetyl_sf.attributes)

        step_attack=ElectronMigrationStep(
            replace=[(Nu_final_charge,C38_Nu_out),
                     (C38_C39_double,VGroup(C38_C39_single,C39_negative))],
            lag_ratio=0.5,
        )

        em_anim=acetyl_sf.electron_migration(steps=[step_attack],lag_ratio=0,run_time=1.2)
        acetyl_sf.remove(Nu_final_charge,C38_C39_double)
        self.add(em_anim.mobject)
        self.play(em_anim,
                  BondTypeTransform(bond=C38_X_bond,
                                    target_type=BondType.IN_BOND,
                                    angle=30*DEGREES,
                                    about_point=acetyl_sf.atomic_clusters["C38"]["pos"],
                                    sf=acetyl_sf,
                                    run_time=1.8))

        acetyl_sf.atomic_clusters["C38"][Bond].remove(C38_C39_double)
        acetyl_sf.atomic_clusters["C39"][Bond].remove(C38_C39_double)
        acetyl_sf.atomic_clusters["C38"][Bond].extend([C38_C39_single,C38_Nu_out])
        acetyl_sf.atomic_clusters["C39"][Bond].append(C38_C39_single)
        acetyl_sf.atomic_clusters["Nu"][Bond].append(C38_Nu_out)
        acetyl_sf.atomic_clusters["C38"]["adj"].append("Nu")
        acetyl_sf.atomic_clusters["Nu"]["adj"].append("C38")
        acetyl_sf.charges.pop("Nu")
        acetyl_sf.charges["C39"]=C39_negative
        self.add(acetyl_sf)
        self.wait(1)

        self.play(ReplacementTransform(text23,text24))

        #负电荷在苯环上迁移：右下C39→左下C41→上方C37→O→回到上方C37
        #第一步：C39的负电荷与C39-C40单键变为C39-C40双键；C40-C41双键变为C40-C41单键和C41左下的负电荷
        C39_C40_single=next(b for b in acetyl_sf.atomic_clusters["C39"][Bond] if b in acetyl_sf.atomic_clusters["C40"][Bond])
        C40_C41_double=next(b for b in acetyl_sf.atomic_clusters["C40"][Bond] if b in acetyl_sf.atomic_clusters["C41"][Bond])
        C39_C40_double=acetyl_sf.build_bond(start="C39",end="C40",bond_type=BondType.DOUBLE_BOND,side=-1,start_side_edge=True,end_side_edge=True)
        C40_C41_single=acetyl_sf.build_bond(start="C40",end="C41",bond_type=BondType.NORMAL_BOND)
        C41_negative=Charge(charge_type=ChargeType.NEGATIVE_COORDINATE,
                            text=acetyl_sf.atomic_clusters["C41"]["pos"],pos=DL,attributes=acetyl_sf.attributes)
        step_mig1=ElectronMigrationStep(
            replace=[(VGroup(C39_negative,C39_C40_single),C39_C40_double),
                     (C40_C41_double,VGroup(C40_C41_single,C41_negative))],
            lag_ratio=0)
        em_mig1=acetyl_sf.electron_migration(steps=[step_mig1],lag_ratio=0,run_time=1.2)
        acetyl_sf.remove(C39_negative,C39_C40_single,C40_C41_double)
        self.add(em_mig1.mobject)
        self.play(em_mig1)

        acetyl_sf.atomic_clusters["C39"][Bond].remove(C39_C40_single)
        acetyl_sf.atomic_clusters["C40"][Bond].remove(C39_C40_single)
        acetyl_sf.atomic_clusters["C39"][Bond].append(C39_C40_double)
        acetyl_sf.atomic_clusters["C40"][Bond].append(C39_C40_double)
        acetyl_sf.atomic_clusters["C40"][Bond].remove(C40_C41_double)
        acetyl_sf.atomic_clusters["C41"][Bond].remove(C40_C41_double)
        acetyl_sf.atomic_clusters["C40"][Bond].append(C40_C41_single)
        acetyl_sf.atomic_clusters["C41"][Bond].append(C40_C41_single)
        acetyl_sf.charges.pop("C39")
        acetyl_sf.charges["C41"]=C41_negative
        self.add(acetyl_sf)
        self.wait(0.5)

        #第二步：C41的负电荷与C41-C42单键变为C41-C42双键；C42-C37双键变为C42-C37单键和C37右上方的负电荷
        C41_C42_single=next(b for b in acetyl_sf.atomic_clusters["C41"][Bond] if b in acetyl_sf.atomic_clusters["C42"][Bond])
        C42_C37_double=next(b for b in acetyl_sf.atomic_clusters["C42"][Bond] if b in acetyl_sf.atomic_clusters["C37"][Bond])
        C41_C42_double=acetyl_sf.build_bond(start="C41",end="C42",bond_type=BondType.DOUBLE_BOND,side=-1,start_side_edge=True,end_side_edge=True)
        C42_C37_single=acetyl_sf.build_bond(start="C42",end="C37",bond_type=BondType.NORMAL_BOND)
        C37_negative=Charge(charge_type=ChargeType.NEGATIVE_COORDINATE,
                            text=acetyl_sf.atomic_clusters["C37"]["pos"],pos=UR,attributes=acetyl_sf.attributes)
        step_mig2=ElectronMigrationStep(
            replace=[(VGroup(C41_negative,C41_C42_single),C41_C42_double),
                     (C42_C37_double,VGroup(C42_C37_single,C37_negative))],
            lag_ratio=0)
        em_mig2=acetyl_sf.electron_migration(steps=[step_mig2],lag_ratio=0,run_time=1.2)
        acetyl_sf.remove(C41_negative,C41_C42_single,C42_C37_double)
        self.add(em_mig2.mobject)
        self.play(em_mig2)

        acetyl_sf.atomic_clusters["C41"][Bond].remove(C41_C42_single)
        acetyl_sf.atomic_clusters["C42"][Bond].remove(C41_C42_single)
        acetyl_sf.atomic_clusters["C41"][Bond].append(C41_C42_double)
        acetyl_sf.atomic_clusters["C42"][Bond].append(C41_C42_double)
        acetyl_sf.atomic_clusters["C42"][Bond].remove(C42_C37_double)
        acetyl_sf.atomic_clusters["C37"][Bond].remove(C42_C37_double)
        acetyl_sf.atomic_clusters["C42"][Bond].append(C42_C37_single)
        acetyl_sf.atomic_clusters["C37"][Bond].append(C42_C37_single)
        acetyl_sf.charges.pop("C41")
        acetyl_sf.charges["C37"]=C37_negative
        self.add(acetyl_sf)
        self.wait(0.5)

        #第三步：C37的负电荷与C37-C43单键变为C37-C43双键；C43-O双键变为C43-O单键和O右上方的负电荷
        C37_C43_single=next(b for b in acetyl_sf.atomic_clusters["C37"][Bond] if b in acetyl_sf.atomic_clusters["C43"][Bond])
        C43_O_double=next(b for b in acetyl_sf.atomic_clusters["C43"][Bond] if b in acetyl_sf.atomic_clusters["O"][Bond])
        C37_C43_double=acetyl_sf.build_bond(start="C37",end="C43",bond_type=BondType.DOUBLE_BOND,side=-1,start_side_edge=True,end_side_edge=True)
        C43_O_single=acetyl_sf.build_bond(start="C43",end="O",bond_type=BondType.NORMAL_BOND)
        O_negative=Charge(charge_type=ChargeType.NEGATIVE,text=acetyl_sf.atomic_clusters["O"][Mobject],
                          pos=UR,attributes=acetyl_sf.attributes)
        step_mig3=ElectronMigrationStep(
            replace=[(VGroup(C37_negative,C37_C43_single),C37_C43_double),
                     (C43_O_double,VGroup(C43_O_single,O_negative))],
            lag_ratio=0)
        em_mig3=acetyl_sf.electron_migration(steps=[step_mig3],lag_ratio=0,run_time=1.2)
        acetyl_sf.remove(C37_negative,C37_C43_single,C43_O_double)
        self.add(em_mig3.mobject)
        self.play(em_mig3)

        acetyl_sf.atomic_clusters["C37"][Bond].remove(C37_C43_single)
        acetyl_sf.atomic_clusters["C43"][Bond].remove(C37_C43_single)
        acetyl_sf.atomic_clusters["C37"][Bond].append(C37_C43_double)
        acetyl_sf.atomic_clusters["C43"][Bond].append(C37_C43_double)
        acetyl_sf.atomic_clusters["C43"][Bond].remove(C43_O_double)
        acetyl_sf.atomic_clusters["O"][Bond].remove(C43_O_double)
        acetyl_sf.atomic_clusters["C43"][Bond].append(C43_O_single)
        acetyl_sf.atomic_clusters["O"][Bond].append(C43_O_single)
        acetyl_sf.charges.pop("C37")
        acetyl_sf.charges["O"]=O_negative
        self.add(acetyl_sf)
        self.wait(0.5)

        #第四步：O的负电荷与C43-O单键变为C43-O双键；C37-C43双键变为C37-C43单键和C37右上方的负电荷，回到上方C37
        C43_O_double_new=acetyl_sf.build_bond(start="C43",end="O",bond_type=BondType.DOUBLE_BOND,side=0)
        C37_C43_single_new=acetyl_sf.build_bond(start="C37",end="C43",bond_type=BondType.NORMAL_BOND)
        C37_negative_final=Charge(charge_type=ChargeType.NEGATIVE_COORDINATE,
                                  text=acetyl_sf.atomic_clusters["C37"]["pos"],pos=UR,attributes=acetyl_sf.attributes)
        step_mig4=ElectronMigrationStep(
            replace=[(VGroup(O_negative,C43_O_single),C43_O_double_new),
                     (C37_C43_double,VGroup(C37_C43_single_new,C37_negative_final))],
            lag_ratio=0)
        em_mig4=acetyl_sf.electron_migration(steps=[step_mig4],lag_ratio=0,run_time=1.2)
        acetyl_sf.remove(O_negative,C43_O_single,C37_C43_double)
        self.add(em_mig4.mobject)
        self.play(em_mig4)

        acetyl_sf.atomic_clusters["C43"][Bond].remove(C43_O_single)
        acetyl_sf.atomic_clusters["O"][Bond].remove(C43_O_single)
        acetyl_sf.atomic_clusters["C43"][Bond].append(C43_O_double_new)
        acetyl_sf.atomic_clusters["O"][Bond].append(C43_O_double_new)
        acetyl_sf.atomic_clusters["C37"][Bond].remove(C37_C43_double)
        acetyl_sf.atomic_clusters["C43"][Bond].remove(C37_C43_double)
        acetyl_sf.atomic_clusters["C37"][Bond].append(C37_C43_single_new)
        acetyl_sf.atomic_clusters["C43"][Bond].append(C37_C43_single_new)
        acetyl_sf.charges.pop("O")
        acetyl_sf.charges["C37"]=C37_negative_final
        self.add(acetyl_sf)
        self.wait(1)

        self.play(ReplacementTransform(text24,text25))

        #X离去：上方C37的负电荷与C37-C38单键变为右上方的C37=C38双键；
        #C-X键变为X右上方的负电荷；
        #同时C-Nu键逆时针旋转30°并变换为NormalBond
        C37_C38_single=next(b for b in acetyl_sf.atomic_clusters["C37"][Bond] if b in acetyl_sf.atomic_clusters["C38"][Bond])
        C37_C38_double=acetyl_sf.build_bond(start="C37",end="C38",bond_type=BondType.DOUBLE_BOND,side=-1,start_side_edge=True,end_side_edge=True)
        X_negative=Charge(charge_type=ChargeType.NEGATIVE,text=acetyl_sf.atomic_clusters["X"][Mobject],
                          pos=UR,attributes=acetyl_sf.attributes)

        step_elim=ElectronMigrationStep(
            replace=[(VGroup(C37_negative_final,C37_C38_single),C37_C38_double),
                     (C38_X_bond,X_negative)],
            lag_ratio=0)

        em_elim=acetyl_sf.electron_migration(steps=[step_elim],lag_ratio=0,run_time=1.5)
        acetyl_sf.remove(C37_negative_final,C37_C38_single,C38_X_bond)
        self.add(em_elim.mobject)
        self.play(em_elim,
                  BondTypeTransform(bond=C38_Nu_out,
                                    target_type=BondType.NORMAL_BOND,
                                    angle=30*DEGREES,
                                    about_point=acetyl_sf.atomic_clusters["C38"]["pos"],
                                    sf=acetyl_sf,
                                    run_time=1.5))

        acetyl_sf.atomic_clusters["C37"][Bond].remove(C37_C38_single)
        acetyl_sf.atomic_clusters["C38"][Bond].remove(C37_C38_single)
        acetyl_sf.atomic_clusters["C37"][Bond].append(C37_C38_double)
        acetyl_sf.atomic_clusters["C38"][Bond].append(C37_C38_double)
        acetyl_sf.atomic_clusters["C38"][Bond].remove(C38_X_bond)
        acetyl_sf.atomic_clusters["X"][Bond].remove(C38_X_bond)
        acetyl_sf.atomic_clusters["C38"]["adj"].remove("X")
        acetyl_sf.atomic_clusters["X"]["adj"].remove("C38")
        acetyl_sf.charges.pop("C37")
        acetyl_sf.charges["X"]=X_negative
        self.add(acetyl_sf)
        self.wait(1)

        #接着X^-消失
        self.play(FadeOut(X_mob,X_negative))
        acetyl_sf.remove(X_mob,X_negative)
        acetyl_sf.atomic_clusters.pop("X")
        acetyl_sf.charges.pop("X")
        self.add(acetyl_sf)
        self.wait(1)

        #苯炔机理之前：淡出除标题和副标题外的所有对象
        #Scene.replace的BFS会把已加入结构式的键从结构式中剥离，这里重新加回，确保FadeOut覆盖全部
        acetyl_sf.add(C38_Nu_out,C39_C40_double,C41_C42_double,C43_O_double_new,C37_C38_double)
        self.play(FadeOut(text25,acetyl_sf),run_time=1)
        self.wait(1)

        #苯炔机理
        benzyne_mechanism=Subtitle(text=r"\text{苯炔机理}")
        self.play(ReplacementTransform(a_d_mechanism,benzyne_mechanism))

        #descriptions
        text26=Description(text=r"\text{如果苯环上没有合适的EWG，那么就可以进行苯炔机理，但是需要强碱和非质子溶剂}")
        text27=Description(text=r"\text{强碱通常使用}\mathrm{NaNH_2}\text{、}\mathrm{n-BuLi}\text{或}\mathrm{LDA}\text{等，此处以}\mathrm{NaNH_2}\text{为例，溶剂一般为液氨}")
        text28=Description(text=r"\text{底物卤代苯中卤素的邻位必须有一个氢}")
        text29=Description(text=r"\text{首先，}\mathrm{NH_2^-}\text{进攻卤素邻位的氢，同时卤素离子离去}")
        text30=Description(text=r"\text{此时生成极不稳定的中间体苯炔，三键被强行塞入环内，张力极大，能量高}")
        text31=Description(text=r"\text{苯炔生成后立刻被}\mathrm{NH_2^-}\text{进攻，生成的碳负离子立即夺取}\mathrm{NH_3}\text{的氢，生成取代产物}")

        #苯炔机理演示：中心显示苯环（纵坐标与第一、二部分的苯环相同），上方C连接EWG，右上C连接X
        benzene_bz=StructuralFormula(name="C52",pos=[0,0.5,0],text=None)
        benzene_bz.add_atom(name="C53",direction=-30*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C52")
        benzene_bz.add_atom(name="C54",direction=-90*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C53",
                            side=-1,start_side_edge=True,end_side_edge=True)
        benzene_bz.add_atom(name="C55",direction=-150*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C54")
        benzene_bz.add_atom(name="C56",direction=150*DEGREES,text=None,bond_type=BondType.DOUBLE_BOND,adjacency="C55",
                            side=-1,start_side_edge=True,end_side_edge=True)
        benzene_bz.add_atom(name="C57",direction=90*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C56")
        benzene_bz.add_bond(start="C57",end="C52",bond_type=BondType.DOUBLE_BOND,side=-1,start_side_edge=True,end_side_edge=True)
        benzene_bz.add_atom(name="EWG",direction=90*DEGREES,text=r"\mathrm{EWG}",bond_type=BondType.NORMAL_BOND,adjacency="C52")
        benzene_bz.add_atom(name="X",direction=30*DEGREES,text=r"\mathrm{X}",bond_type=BondType.NORMAL_BOND,adjacency="C53")

        self.play(Create(benzene_bz),run_time=2)
        self.wait(1)

        #在EWG的位置显示红色叉，表示实际上没有EWG
        EWG_bz_mob=benzene_bz.atomic_clusters["EWG"][Mobject]
        C52_EWG_bond=benzene_bz.atomic_clusters["EWG"][Bond][0]
        red_cross=Cross(EWG_bz_mob,stroke_color=RED,stroke_width=6)
        self.play(Create(red_cross))
        self.wait(1)

        #EWG、C-EWG键、红叉消失，X基苯不消失
        self.play(FadeOut(EWG_bz_mob,C52_EWG_bond,red_cross),run_time=1)
        benzene_bz.remove(EWG_bz_mob,C52_EWG_bond)
        benzene_bz.atomic_clusters.pop("EWG")
        benzene_bz.atomic_clusters["C52"]["adj"].remove("EWG")
        benzene_bz.atomic_clusters["C52"][Bond].remove(C52_EWG_bond)
        self.add(benzene_bz)
        self.wait(1)

        #左侧显示LDA的结构1秒后消失：中间N，左上、左下各连一个异丙基（键线式），右侧连Li，所有键角120°
        LDA_sf=StructuralFormula(name="N",pos=[-4.5,0,0],text=r"\mathrm{N}")
        LDA_sf.add_atom(name="C1",direction=120*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="N")
        LDA_sf.add_atom(name="C2",direction=60*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C1")
        LDA_sf.add_atom(name="C3",direction=180*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C1")
        LDA_sf.add_atom(name="C4",direction=240*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="N")
        LDA_sf.add_atom(name="C5",direction=180*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C4")
        LDA_sf.add_atom(name="C6",direction=300*DEGREES,text=None,bond_type=BondType.NORMAL_BOND,adjacency="C4")
        LDA_sf.add_atom(name="Li",direction=0*DEGREES,text=r"\mathrm{Li}",bond_type=BondType.NORMAL_BOND,adjacency="N")
        LDA=Description(text=r"\mathrm{LDA}",pos=[-5.0,-2.0,0])

        self.play(Create(LDA_sf),Write(LDA))
        self.wait(1.5)
        self.play(FadeOut(LDA_sf,LDA),run_time=1)
        self.wait(0.5)

        #右侧显示NH2^-（文本像前面的长文本一样用text_offset位移），负电荷在左上角
        NH2_start=np.array([4.5,-1.5,0],dtype=float)
        NH2_mob=AtomicCluster(text=r"\mathrm{NH_2}",pos=NH2_start,text_offset=np.array([0.2,-0.03,0]),
                              attributes=benzene_bz.attributes)
        NH2_charge=Charge(charge_type=ChargeType.NEGATIVE,text=NH2_mob,pos=UL,attributes=benzene_bz.attributes)
        benzene_bz.atomic_clusters["NH2"]={Mobject:NH2_mob,"pos":NH2_start,"adj":[],Bond:[]}
        benzene_bz.add(NH2_mob)

        self.play(FadeIn(NH2_mob),FadeIn(NH2_charge))
        self.wait(0.5)

        #右下的C（C54）上显示一个H（在FadeIn之前才加入结构式，避免提前闪现）
        benzene_bz.add_atom(name="H",direction=-30*DEGREES,text=r"\mathrm{H}",bond_type=BondType.NORMAL_BOND,adjacency="C54")
        H_mob=benzene_bz.atomic_clusters["H"][Mobject]
        C54_H_bond=benzene_bz.atomic_clusters["H"][Bond][0]
        self.play(FadeIn(H_mob),FadeIn(C54_H_bond))
        self.wait(0.5)

        #NH2^-进攻H：pos移动到H右侧一个单位处（pos而非文本标签中心）
        H_pos=benzene_bz.atomic_clusters["H"]["pos"]
        NH2_target=H_pos+np.array([1,0,0],dtype=float)
        NH2_shift=NH2_target-NH2_start
        self.play(NH2_mob.animate.shift(NH2_shift),
                  NH2_charge.animate.shift(NH2_shift),
                  run_time=1)
        benzene_bz.atomic_clusters["NH2"]["pos"]=NH2_target

        #负电荷变为NH2-H单键；C-H键与右侧C53=C54双键合并为原位的C53≡C54三键；C-X变为X上的负电荷
        C53_C54_double=next(b for b in benzene_bz.atomic_clusters["C53"][Bond] if b in benzene_bz.atomic_clusters["C54"][Bond])
        C53_X_bond=benzene_bz.atomic_clusters["X"][Bond][0]
        NH2_H_bond=Bond(bond_type=BondType.NORMAL_BOND,
                        start=NH2_target,end=H_pos,
                        start_edge=True,end_edge=True,
                        attributes=benzene_bz.attributes)
        C53_C54_triple=benzene_bz.build_bond(start="C53",end="C54",bond_type=BondType.TRIPLE_BOND)
        X_negative=Charge(charge_type=ChargeType.NEGATIVE,text=benzene_bz.atomic_clusters["X"][Mobject],
                          pos=UR,attributes=benzene_bz.attributes)

        step_bz=ElectronMigrationStep(
            replace=[(NH2_charge,NH2_H_bond),
                     (VGroup(C54_H_bond,C53_C54_double),C53_C54_triple),
                     (C53_X_bond,X_negative)]
            )

        em_bz=benzene_bz.electron_migration(steps=[step_bz],lag_ratio=0,run_time=1.5)
        benzene_bz.remove(NH2_charge,C54_H_bond,C53_C54_double,C53_X_bond)
        self.add(em_bz.mobject)
        self.play(em_bz)

        benzene_bz.atomic_clusters["NH2"][Bond].append(NH2_H_bond)
        benzene_bz.atomic_clusters["H"][Bond].append(NH2_H_bond)
        benzene_bz.atomic_clusters["NH2"]["adj"].append("H")
        benzene_bz.atomic_clusters["H"]["adj"].append("NH2")
        benzene_bz.atomic_clusters["C54"][Bond].remove(C54_H_bond)
        benzene_bz.atomic_clusters["H"][Bond].remove(C54_H_bond)
        benzene_bz.atomic_clusters["C54"]["adj"].remove("H")
        benzene_bz.atomic_clusters["H"]["adj"].remove("C54")
        benzene_bz.atomic_clusters["C53"][Bond].remove(C53_C54_double)
        benzene_bz.atomic_clusters["C54"][Bond].remove(C53_C54_double)
        benzene_bz.atomic_clusters["C53"][Bond].append(C53_C54_triple)
        benzene_bz.atomic_clusters["C54"][Bond].append(C53_C54_triple)
        benzene_bz.atomic_clusters["C53"][Bond].remove(C53_X_bond)
        benzene_bz.atomic_clusters["X"][Bond].remove(C53_X_bond)
        benzene_bz.atomic_clusters["C53"]["adj"].remove("X")
        benzene_bz.atomic_clusters["X"]["adj"].remove("C53")
        benzene_bz.charges["X"]=X_negative
        #Scene.replace的BFS会把直接加入结构式的键/电荷剥离，重新加回
        benzene_bz.add(NH2_H_bond,C53_C54_triple,X_negative)
        self.add(benzene_bz)
        self.wait(1)
