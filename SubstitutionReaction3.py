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

        Addition_elimination_mechanism=Title(text=r"\text{加成}-\text{消除机理}")
        self.play(Write(Addition_elimination_mechanism))
        self.wait(0.5)

        #descriptions
        text1=Description(text=r"\text{芳香环上可以发生亲核加成}\mathrm{-}\text{消除机理的取代反应，羧酸及其衍生物上同样可以}")
        text2=Description(text=r"\mathrm{L}\text{是离去基团，}\mathrm{Nu^-}\text{是亲核试剂}")
        text3=Description(text=r"\text{碳氧双键有极性，双键的电子更偏向氧原子，}\\\text{这使得氧原子上带部分负电，碳原子上带部分正电}")
        text4=Description(text=r"\text{条件分别为酸催化和碱催化时，有着不同的机理，但是其内在的逻辑是类似的}")

        acetyl_L=StructuralFormula(name="C1",pos=ORIGIN,text=None)
        acetyl_L.add_atom(name="O1",direction=90*DEGREES,text=r"\mathrm{O}",
                          bond_type=BondType.DOUBLE_BOND,adjacency="C1",side=0)
        acetyl_L.add_atom(name="CH3",direction=210*DEGREES,text=None,
                          bond_type=BondType.NORMAL_BOND,adjacency="C1")
        acetyl_L.add_atom(name="L",direction=330*DEGREES,text=r"\mathrm{L}",
                          bond_type=BondType.NORMAL_BOND,adjacency="C1")

        #先显示中间底物
        self.play(Write(text1))
        self.play(Create(acetyl_L))
        self.wait(1.5)

        #右侧亲核试剂 Nu^-（先独立显示，进攻时再并入乙酰基结构）
        Nu_start=np.array([3*acetyl_L.attributes.length_global,0,0])
        Nu_mob=AtomicCluster(text=r"\mathrm{Nu}",pos=Nu_start,attributes=acetyl_L.attributes)
        acetyl_L.register_atom(name="Nu",mobject=Nu_mob)
        acetyl_L.add_charge(text="Nu",pos=UL,charge_type=ChargeType.NEGATIVE)
        Nu_negative=acetyl_L.charges["Nu"]

        self.play(FadeIn(Nu_mob),FadeIn(Nu_negative),ReplacementTransform(text1,text2))
        self.wait(1)

        #C=O键左侧的极性键箭头：从C指向O
        delta_positive_C=MathTex(r"\delta^+",color=WHITE,font_size=txt_size*0.9)
        delta_positive_C.move_to(acetyl_L.atomic_clusters["C1"]["pos"]+np.array([0,-0.35,0]))
        delta_negative_O=MathTex(r"\delta^-",color=WHITE,font_size=txt_size*0.9)
        delta_negative_O.move_to(acetyl_L.atomic_clusters["O1"]["pos"]+np.array([0,0.35,0]))

        polarity_arrow=BondPolarityArrow(start=acetyl_L.atomic_clusters["C1"]["pos"],
                                         end=acetyl_L.atomic_clusters["O1"]["pos"],
                                         attributes=acetyl_L.attributes,
                                         side=1,
                                         length=bond_length*0.8,
                                         offset=0.2)
        self.play(FadeIn(polarity_arrow),FadeIn(delta_positive_C),FadeIn(delta_negative_O),ReplacementTransform(text2,text3))
        self.wait(2)
        self.play(FadeOut(polarity_arrow,delta_positive_C,delta_negative_O))
        self.play(ReplacementTransform(text3,text4))
        self.wait(2)

        #碱催化的机理
        subtitle1=Subtitle(text=r"\text{碱催化}")
        self.play(Write(subtitle1))

        #descriptions
        text5=Description(text=r"\text{带负电的}\mathrm{Nu^-}\text{首先进攻带部分正电的羰基碳，}\\\text{发生亲核加成，形成一个带负电的四面体中间体}")
        text6=Description(text=r"\text{接着发生消除，}\mathrm{L^-}\text{离去，碳氧双键恢复，生成取代产物}")

        self.play(ReplacementTransform(text4,text5))

        #Nu^-进攻羰基碳：Nu移动到中心碳的右侧
        Nu_target=acetyl_L.atomic_clusters["C1"]["pos"]+np.array([np.cos(0*DEGREES),np.sin(0*DEGREES),0])*acetyl_L.attributes.length_global
        shift_Nu=Nu_target-Nu_start
        self.play(Nu_mob.animate.shift(shift_Nu),
                  Nu_negative.animate.shift(shift_Nu),
                  run_time=1)
        acetyl_L.atomic_clusters["Nu"]["pos"]=Nu_target

        #Nu的负电荷变为C-Nu InBond；C=O双键变为原位单键并生成O^-；同时C-L键顺时针旋转30°变为OutBond
        C1_O1_double=acetyl_L.atomic_clusters["O1"][Bond][0]
        C1_L_normal=acetyl_L.atomic_clusters["L"][Bond][0]

        C1_Nu_in=acetyl_L.build_bond(start="C1",end="Nu",bond_type=BondType.IN_BOND)
        C1_O1_single=acetyl_L.build_bond(start="C1",end="O1",bond_type=BondType.NORMAL_BOND)
        O1_negative=acetyl_L.build_charge(text="O1",pos=UR,charge_type=ChargeType.NEGATIVE)

        step_attack=ElectronMigrationStep(
            replace=[(Nu_negative,C1_Nu_in),
                     (C1_O1_double,VGroup(C1_O1_single,O1_negative))],
        )

        self.play(acetyl_L.electron_migration(steps=[step_attack],run_time=1.5),
                  BondTypeTransform(bond=C1_L_normal,
                                    target_type=BondType.OUT_BOND,
                                    angle=-30*DEGREES,
                                    about_point=acetyl_L.atomic_clusters["C1"]["pos"],
                                    sf=acetyl_L,
                                    run_time=1.5))

        #C-Nu键顺时针旋转30°
        self.play(acetyl_L.rotate_atoms(atom_names="Nu",
                                        center="C1",
                                        angle=-30*DEGREES,
                                        run_time=0.8))

        self.wait(1.5)

        #L^-离去，碳氧双键恢复
        C1_O1_double_new=acetyl_L.build_bond(start="C1",end="O1",bond_type=BondType.DOUBLE_BOND,side=0)
        L_negative=acetyl_L.build_charge(text="L",pos=UL,charge_type=ChargeType.NEGATIVE)
        C1_Nu_normal=acetyl_L.build_bond(start="C1",end="Nu",bond_type=BondType.NORMAL_BOND)

        step_elimination=ElectronMigrationStep(
            replace=[(VGroup(C1_O1_single,O1_negative),C1_O1_double_new),
                     (C1_L_normal,L_negative),
                     (C1_Nu_in,C1_Nu_normal)],
        )

        self.play(ReplacementTransform(text5,text6))
        self.play(acetyl_L.electron_migration(steps=[step_elimination],run_time=1.5))
        self.wait(1)

        #L^-从下方沿一条弧线移动到左侧
        L_mob=acetyl_L.atomic_clusters["L"][Mobject]
        L_start=L_mob.get_center()
        L_final=np.array([-2*acetyl_L.attributes.length_global,0,0])
        arc_L=ArcBetweenPoints(L_start,L_final,angle=-120*DEGREES)
        L_charge_offset=L_negative.get_center()-L_mob.get_center()
        arc_L_negative=arc_L.copy().shift(L_charge_offset)

        self.play(MoveAlongPath(L_mob,arc_L,run_time=1.5),
                  MoveAlongPath(L_negative,arc_L_negative,run_time=1.5))
        acetyl_L.atomic_clusters["L"]["pos"]=L_final
        self.wait(1.5)
        self.play(FadeOut(text6))

        #快速倒放：回到Nu^-进攻羰基前
        self.play(MoveAlongPath(L_mob,arc_L.reverse_points(),run_time=0.3),
                  MoveAlongPath(L_negative,arc_L_negative.reverse_points(),run_time=0.3))
        acetyl_L.atomic_clusters["L"]["pos"]=L_start

        #倒放消除步骤：恢复四面体中间体
        C1_O1_single_rev=acetyl_L.build_bond(start="C1",end="O1",bond_type=BondType.NORMAL_BOND)
        O1_negative_rev=acetyl_L.build_charge(text="O1",pos=UR,charge_type=ChargeType.NEGATIVE)
        C1_Nu_in_rev=acetyl_L.build_bond(start="C1",end="Nu",bond_type=BondType.IN_BOND)
        C1_L_out_rev=acetyl_L.build_bond(start="C1",end="L",bond_type=BondType.OUT_BOND)

        step_reverse_elimination=ElectronMigrationStep(
            replace=[(C1_O1_double_new,VGroup(C1_O1_single_rev,O1_negative_rev)),
                     (C1_Nu_normal,C1_Nu_in_rev),
                     (L_negative,C1_L_out_rev)],
        )
        self.play(acetyl_L.electron_migration(steps=[step_reverse_elimination],run_time=0.3))

        #倒放C-Nu键旋转（先逆时针旋转；正放0.8s，倒放0.16s）
        self.play(acetyl_L.rotate_atoms(atom_names="Nu",
                                        center="C1",
                                        angle=30*DEGREES,
                                        run_time=0.16))

        #倒放加成步骤：C-L键边变形边旋转，同时进行逆向电子转移
        Nu_negative_rev=acetyl_L.build_charge(text="Nu",pos=UL,charge_type=ChargeType.NEGATIVE)
        C1_O1_double_rev=acetyl_L.build_bond(start="C1",end="O1",bond_type=BondType.DOUBLE_BOND,side=0)
        L_rewind_end=acetyl_L.atomic_clusters["C1"]["pos"]+np.array([np.cos(330*DEGREES),np.sin(330*DEGREES),0])*acetyl_L.attributes.length_global
        arc_L_rot_reverse=ArcBetweenPoints(L_start,L_rewind_end,angle=30*DEGREES)


        step_reverse_attack=ElectronMigrationStep(
            replace=[(C1_Nu_in_rev,Nu_negative_rev),
                     (VGroup(C1_O1_single_rev,O1_negative_rev),C1_O1_double_rev)],
        )

        self.play(acetyl_L.electron_migration(steps=[step_reverse_attack],run_time=0.3),
                  BondTypeTransform(bond=C1_L_out_rev,
                                    target_type=BondType.NORMAL_BOND,
                                    angle=30*DEGREES,
                                    about_point=acetyl_L.atomic_clusters["C1"]["pos"],
                                    sf=acetyl_L,
                                    run_time=0.3),
                  MoveAlongPath(L_mob,arc_L_rot_reverse,run_time=0.3))
        acetyl_L.atomic_clusters["L"]["pos"]=L_rewind_end

        #Nu^-移回初始位置
        shift_Nu_back=Nu_start-Nu_mob.get_center()
        self.play(Nu_mob.animate.shift(shift_Nu_back),
                  Nu_negative_rev.animate.shift(shift_Nu_back),
                  run_time=0.2)
        acetyl_L.atomic_clusters["Nu"]["pos"]=Nu_start

        #倒放Nu^-的出现：淡出，回到Nu^-显示之前
        self.play(FadeOut(Nu_mob,Nu_negative_rev),run_time=0.2)
        self.wait(1.5)

        #酸催化的机理
        subtitle2=Subtitle(text=r"\text{酸催化}")
        self.play(ReplacementTransform(subtitle1,subtitle2))

        #descriptions
        text7=Description(text=r"\text{在有}\mathrm{H^+}\text{的条件下，首先带部分负电的氧被质子化}")
        text8=Description(text=r"\text{带正电的氧对碳氧双键的电子的吸引力更强，使得碳更具正电性}")
        text9=Description(text=r"\text{此时存在这种共振式，可以看出碳的正电性相较于质子化之前大大增加，}\\\text{因此也更易被亲核试剂进攻}")
        text10=Description(text=r"\text{接着}\mathrm{NuH}\text{进攻活化的带正电的碳，}\\\text{随后被体系中的碱夺去质子，得到不带电荷的四面体中间体}")
        text11=Description(text=r"\text{最后发生消除反应}")
        text12=Description(text=r"\text{如果}\mathrm{L}\text{是卤素原子}\mathrm{X}\text{，作为一个好的离去基团，}\\\mathrm{X^-}\text{会直接离去，羰基上的质子被碱拔除}")
        text13=Description(text=r"\text{如果}\mathrm{L}\text{不是卤素原子，那么}\mathrm{L}\text{会先被质子化，形成一个好的离去基团}")
        text14=Description(text=r"\text{然后以}\mathrm{HL}\text{的形式离去，羰基上的质子被碱拔除}")

        #右侧出现H^+，O的右上30°方向出现孤对电子
        O_pos=acetyl_L.atomic_clusters["O1"]["pos"]
        lone_pair_direction=np.array([np.cos(30*DEGREES),np.sin(30*DEGREES),0])
        acetyl_L.add_charge(text="O1",pos=lone_pair_direction,charge_type=ChargeType.PAIR)
        lone_pair=acetyl_L.charges["O1"]

        H_pos=O_pos+lone_pair_direction*acetyl_L.attributes.length_global
        H_mob=AtomicCluster(text=r"\mathrm{H}",pos=H_pos,attributes=acetyl_L.attributes)
        acetyl_L.register_atom(name="H",mobject=H_mob)
        acetyl_L.add_charge(text="H",pos=UR,charge_type=ChargeType.POSITIVE)
        H_positive=acetyl_L.charges["H"]

        self.play(FadeIn(text7))
        self.play(FadeIn(H_mob),FadeIn(H_positive),FadeIn(lone_pair))
        self.wait(1)

        #孤对电子进攻H^+：变为O-H键，O带正电荷，H^+的电荷消失
        O_H_bond=acetyl_L.build_bond(start="O1",end="H",bond_type=BondType.NORMAL_BOND)
        O_positive=acetyl_L.build_charge(text="O1",pos=UL,charge_type=ChargeType.POSITIVE)

        step_protonation=ElectronMigrationStep(
            replace=[(lone_pair,O_H_bond)],
            create=[O_positive],
            fadeout=[H_positive],
        )

        self.play(acetyl_L.electron_migration(steps=[step_protonation],run_time=1.0))
        self.play(ReplacementTransform(text7,text8))
        self.wait(1.5)

        #碳氧双键变为C-O单键和O上的孤对电子，O的正电荷消失，C上出现正电荷
        C1_O1_single_oxy=acetyl_L.build_bond(start="C1",end="O1",bond_type=BondType.NORMAL_BOND)
        O_lone_pair=acetyl_L.build_charge(text="O1",pos=np.array([np.cos(150*DEGREES),np.sin(150*DEGREES),0]),charge_type=ChargeType.PAIR)
        C1_positive=acetyl_L.build_charge(text="C1",pos=np.array([np.cos(30*DEGREES),np.sin(30*DEGREES),0]),charge_type=ChargeType.POSITIVE_COORDINATE)

        step_oxocarbocation=ElectronMigrationStep(
            replace=[(C1_O1_double_rev,VGroup(C1_O1_single_oxy,O_lone_pair))],
            create=[C1_positive],
            fadeout=[O_positive],
        )

        self.play(ReplacementTransform(text8,text9))
        self.play(acetyl_L.electron_migration(steps=[step_oxocarbocation],run_time=1.0))
        self.wait(2)

        #右侧出现Nu-H：H在Nu右上30°，Nu左侧有一对孤对电子
        acetyl_L.delete_charge(text="Nu")

        Nu_mob=acetyl_L.atomic_clusters["Nu"][Mobject]
        direction30=np.array([np.cos(60*DEGREES),np.sin(60*DEGREES),0])
        H2_pos=Nu_mob.get_center()+direction30*acetyl_L.attributes.length_global
        H2_mob=AtomicCluster(text=r"\mathrm{H}",pos=H2_pos,attributes=acetyl_L.attributes)
        acetyl_L.register_atom(name="H2",mobject=H2_mob,adjacency="Nu",bond_type=BondType.NORMAL_BOND)
        Nu_H2_bond=acetyl_L.bond_lookup.between("Nu","H2")
        acetyl_L.add_charge(text="Nu",pos=LEFT,charge_type=ChargeType.PAIR)
        Nu_lone_pair=acetyl_L.charges["Nu"]

        self.play(ReplacementTransform(text9,text10))
        self.play(FadeIn(Nu_mob),FadeIn(H2_mob),FadeIn(Nu_H2_bond),FadeIn(Nu_lone_pair))
        self.wait(0.5)

        #Nu-H的孤对电子进攻碳正离子：Nu移动到中心碳右侧
        Nu_target2=acetyl_L.atomic_clusters["C1"]["pos"]+np.array([np.cos(0*DEGREES),np.sin(0*DEGREES),0])*acetyl_L.attributes.length_global
        H2_pos_before=acetyl_L.atomic_clusters["H2"]["pos"]
        shift_NuH=Nu_target2-Nu_mob.get_center()
        self.play(Nu_mob.animate.shift(shift_NuH),
                  H2_mob.animate.shift(shift_NuH),
                  Nu_H2_bond.animate.shift(shift_NuH),
                  Nu_lone_pair.animate.shift(shift_NuH),
                  run_time=1)
        acetyl_L.atomic_clusters["Nu"]["pos"]=Nu_target2
        acetyl_L.atomic_clusters["H2"]["pos"]=H2_pos_before+shift_NuH

        #孤对电子变为C-Nu InBond；C-L键顺时针旋转30°并变为OutBond
        C1_Nu_in2=acetyl_L.build_bond(start="C1",end="Nu",bond_type=BondType.IN_BOND)
        Nu_positive=acetyl_L.build_charge(text="Nu",pos=DR,charge_type=ChargeType.POSITIVE)
        C1_L_current=acetyl_L.bond_lookup.between("C1","L")
        L_forward_start=acetyl_L.atomic_clusters["L"]["pos"]
        L_forward_end=acetyl_L.atomic_clusters["C1"]["pos"]+np.array([np.cos(300*DEGREES),np.sin(300*DEGREES),0])*acetyl_L.attributes.length_global
        arc_L_forward2=ArcBetweenPoints(L_forward_start,L_forward_end,angle=-30*DEGREES)

        step_nu_attack2=ElectronMigrationStep(
            replace=[(Nu_lone_pair,C1_Nu_in2)],
            create=[Nu_positive],
            fadeout=[C1_positive],
        )

        self.play(acetyl_L.electron_migration(steps=[step_nu_attack2],run_time=1.5),
                  BondTypeTransform(bond=C1_L_current,
                                    target_type=BondType.OUT_BOND,
                                    angle=-30*DEGREES,
                                    about_point=acetyl_L.atomic_clusters["C1"]["pos"],
                                    sf=acetyl_L,
                                    run_time=1.5),
                  MoveAlongPath(L_mob,arc_L_forward2,run_time=1.5))
        acetyl_L.atomic_clusters["L"]["pos"]=L_forward_end

        #紧接着C-Nu键顺时针旋转30°
        self.play(acetyl_L.rotate_atoms(atom_names=["Nu","H2"],
                                        center="C1",
                                        angle=-30*DEGREES,
                                        run_time=0.8))
        self.wait(1.5)

        #右边出现OH_2，O（OH_2标签）左侧有一对孤对电子
        OH2_pos=H2_mob.get_center()+np.array([acetyl_L.attributes.length_global,0,0])
        OH2_mob=AtomicCluster(text=r"\mathrm{OH_2}",pos=OH2_pos,text_offset=np.array([0.2,-0.03,0]),
                              attributes=acetyl_L.attributes)
        acetyl_L.register_atom(name="OH2",mobject=OH2_mob)
        acetyl_L.add_charge(text="OH2",pos=LEFT,charge_type=ChargeType.PAIR)
        OH2_lone_pair=acetyl_L.charges["OH2"]

        self.play(FadeIn(OH2_mob),FadeIn(OH2_lone_pair))
        self.wait(0.5)

        #孤对电子进攻Nu上的H：Nu-H变为Nu右上30°的孤对电子，Nu^+消失，OH_2带正电荷
        OH2_H2_bond=acetyl_L.build_bond(start="OH2",end="H2",bond_type=BondType.NORMAL_BOND)
        Nu_lone_pair_after=acetyl_L.build_charge(text="Nu",pos=direction30,charge_type=ChargeType.PAIR)
        OH2_positive=acetyl_L.build_charge(text="OH2",pos=UL,charge_type=ChargeType.POSITIVE)

        step_deprotonation=ElectronMigrationStep(
            replace=[(OH2_lone_pair,OH2_H2_bond),
                     (Nu_H2_bond,Nu_lone_pair_after)],
            create=[OH2_positive],
            fadeout=[Nu_positive],
        )

        self.play(acetyl_L.electron_migration(steps=[step_deprotonation],run_time=1.5))

        #随后Nu上的孤对电子消失
        self.play(FadeOut(Nu_lone_pair_after))
        acetyl_L.delete_charge(text="Nu")

        #右侧水合氢离子消失
        self.play(FadeOut(OH2_mob,OH2_positive,H2_mob,OH2_H2_bond))
        self.wait(1.5)
        self.play(ReplacementTransform(text10,text11))
        self.wait(2)
        acetyl_L.delete_atom(names=["OH2","H2"])

        #整个分子分为左右两种情况，分别向左向右平移三个单位
        left_shift=np.array([-3,0,0],dtype=float)
        right_shift=np.array([3,0,0],dtype=float)
        right_mol=acetyl_L.copy()
        right_mol.shift(right_shift)

        self.play(acetyl_L.animate.shift(left_shift),
                  ReplacementTransform(acetyl_L.copy(),right_mol),
                  run_time=1.5)
        for data in acetyl_L.atomic_clusters.values():
            data["pos"]=np.array(data["pos"],dtype=float)+left_shift
        for data in right_mol.atomic_clusters.values():
            data["pos"]=np.array(data["pos"],dtype=float)+right_shift

        #左边的L变为X
        left_L_mob=acetyl_L.atomic_clusters["L"][Mobject]
        X_mob=AtomicCluster(text=r"\mathrm{X}",pos=left_L_mob.get_center(),attributes=acetyl_L.attributes)
        self.play(ReplacementTransform(text11,text12))
        self.play(ReplacementTransform(left_L_mob,X_mob),run_time=0.8)
        self.wait(1.5)
        acetyl_L.remove(left_L_mob)
        acetyl_L.atomic_clusters["L"][Mobject]=X_mob
        acetyl_L.add(X_mob)

        #左边：氧上的孤对电子和C-O单键变为双键，C-X键变为X^-，O左上30°出现正电荷
        direction150=np.array([np.cos(150*DEGREES),np.sin(150*DEGREES),0])
        left_C1_O1_single=acetyl_L.bond_lookup.between("C1","O1")
        left_O_lone_pair=acetyl_L.charges["O1"]
        left_C1_X_bond=acetyl_L.bond_lookup.between("C1","L")

        left_C1_O1_double=acetyl_L.build_bond(start="C1",end="O1",bond_type=BondType.DOUBLE_BOND,side=0)
        left_X_negative=acetyl_L.build_charge(text="L",pos=UL,charge_type=ChargeType.NEGATIVE)
        left_O_positive=acetyl_L.build_charge(text="O1",pos=direction150,charge_type=ChargeType.POSITIVE)

        left_step_restore=ElectronMigrationStep(
            replace=[(VGroup(left_C1_O1_single,left_O_lone_pair),left_C1_O1_double),
                     (left_C1_X_bond,left_X_negative)],
            create=[left_O_positive],
        )
        self.play(acetyl_L.electron_migration(steps=[left_step_restore],run_time=1.5))

        #X^-及X原子消失
        left_X_mob=acetyl_L.atomic_clusters["L"][Mobject]
        self.play(FadeOut(left_X_negative,left_X_mob))
        acetyl_L.delete_charge(text="L")
        acetyl_L.delete_atom(names=["L"])
        self.wait(0.5)

        #左边：OH2夺取羰基O上的H
        left_H_mob=acetyl_L.atomic_clusters["H"][Mobject]
        left_O1_H_bond=acetyl_L.bond_lookup.between("O1","H")
        left_OH2_pos=left_H_mob.get_center()+np.array([acetyl_L.attributes.length_global,0,0])
        left_OH2_mob=AtomicCluster(text=r"\mathrm{OH_2}",pos=left_OH2_pos,text_offset=np.array([0.2,-0.03,0]),
                                   attributes=acetyl_L.attributes)
        acetyl_L.register_atom(name="OH2",mobject=left_OH2_mob)
        acetyl_L.add_charge(text="OH2",pos=LEFT,charge_type=ChargeType.PAIR)
        left_OH2_lone_pair=acetyl_L.charges["OH2"]

        self.play(FadeIn(left_OH2_mob),FadeIn(left_OH2_lone_pair))
        self.wait(0.5)

        left_OH2_H_bond=acetyl_L.build_bond(start="OH2",end="H",bond_type=BondType.NORMAL_BOND)
        left_O_lone_pair_after=acetyl_L.build_charge(text="O1",pos=direction30,charge_type=ChargeType.PAIR)
        left_OH2_positive=acetyl_L.build_charge(text="OH2",pos=UL,charge_type=ChargeType.POSITIVE)

        left_step_deprotonation=ElectronMigrationStep(
            replace=[(left_OH2_lone_pair,left_OH2_H_bond),
                     (left_O1_H_bond,left_O_lone_pair_after)],
            create=[left_OH2_positive],
            fadeout=[left_O_positive],
        )
        self.play(acetyl_L.electron_migration(steps=[left_step_deprotonation],run_time=1.5))

        #羰基O上的孤对电子消失，左侧水合氢离子消失
        self.play(FadeOut(left_O_lone_pair_after))
        acetyl_L.delete_charge(text="O1")
        self.play(FadeOut(left_OH2_mob,left_OH2_positive,left_H_mob,left_OH2_H_bond))
        acetyl_L.delete_atom(names=["OH2","H"])
        self.wait(0.5)
        self.play(ReplacementTransform(text12,text13))

        #右边：L右侧出现孤对电子，H^+进攻生成L-H，L下方出现正电荷
        right_L_mob=right_mol.atomic_clusters["L"][Mobject]
        right_L_pos=right_mol.atomic_clusters["L"]["pos"]
        right_mol.add_charge(text="L",pos=RIGHT,charge_type=ChargeType.PAIR)
        right_L_lone_pair=right_mol.charges["L"]

        right_Hplus_pos=right_L_pos+np.array([right_mol.attributes.length_global,0,0])
        right_Hplus_mob=AtomicCluster(text=r"\mathrm{H}",pos=right_Hplus_pos,attributes=right_mol.attributes)
        right_mol.register_atom(name="HplusR",mobject=right_Hplus_mob)
        right_mol.add_charge(text="HplusR",pos=UR,charge_type=ChargeType.POSITIVE)
        right_Hplus_positive=right_mol.charges["HplusR"]

        self.play(FadeIn(right_L_lone_pair),FadeIn(right_Hplus_mob),FadeIn(right_Hplus_positive))
        self.wait(1.5)

        right_L_H_bond=right_mol.build_bond(start="L",end="HplusR",bond_type=BondType.NORMAL_BOND)
        right_L_positive=right_mol.build_charge(text="L",pos=DOWN,charge_type=ChargeType.POSITIVE)

        right_step_protonation=ElectronMigrationStep(
            replace=[(right_L_lone_pair,right_L_H_bond)],
            create=[right_L_positive],
            fadeout=[right_Hplus_positive],
        )
        self.play(right_mol.electron_migration(steps=[right_step_protonation],run_time=1.5))

        #右边：其余流程与左边相同
        right_C1_O1_single=right_mol.bond_lookup.between("C1","O1")
        right_O_lone_pair=right_mol.charges["O1"]
        right_C1_L_bond=right_mol.bond_lookup.between("C1","L")
        right_C1_O1_double=right_mol.build_bond(start="C1",end="O1",bond_type=BondType.DOUBLE_BOND,side=0)
        right_L_lone_pair_after=right_mol.build_charge(text="L",pos=LEFT,charge_type=ChargeType.PAIR)
        right_O_positive=right_mol.build_charge(text="O1",pos=direction150,charge_type=ChargeType.POSITIVE)

        right_step_restore=ElectronMigrationStep(
            replace=[(VGroup(right_C1_O1_single,right_O_lone_pair),right_C1_O1_double),
                     (right_C1_L_bond,right_L_lone_pair_after)],
            create=[right_O_positive],
            fadeout=[right_L_positive],
        )
        self.play(ReplacementTransform(text13,text14))
        self.play(right_mol.electron_migration(steps=[right_step_restore],run_time=1.5))

        #L-H^+离去基团消失
        self.play(FadeOut(right_L_mob,right_L_H_bond,right_Hplus_mob,right_L_lone_pair_after))
        right_mol.delete_atom(names=["L","HplusR"])
        self.wait(0.5)

        #右边：OH2夺取羰基O上的H
        right_H_mob=right_mol.atomic_clusters["H"][Mobject]
        right_O1_H_bond=right_mol.bond_lookup.between("O1","H")
        right_OH2_pos=right_H_mob.get_center()+np.array([right_mol.attributes.length_global,0,0])
        right_OH2_mob=AtomicCluster(text=r"\mathrm{OH_2}",pos=right_OH2_pos,text_offset=np.array([0.2,-0.03,0]),
                                    attributes=right_mol.attributes)
        right_mol.register_atom(name="OH2",mobject=right_OH2_mob)
        right_mol.add_charge(text="OH2",pos=LEFT,charge_type=ChargeType.PAIR)
        right_OH2_lone_pair=right_mol.charges["OH2"]

        self.play(FadeIn(right_OH2_mob),FadeIn(right_OH2_lone_pair))
        self.wait(0.5)

        right_OH2_H_bond=right_mol.build_bond(start="OH2",end="H",bond_type=BondType.NORMAL_BOND)
        right_O_lone_pair_after=right_mol.build_charge(text="O1",pos=direction30,charge_type=ChargeType.PAIR)
        right_OH2_positive=right_mol.build_charge(text="OH2",pos=UL,charge_type=ChargeType.POSITIVE)

        right_step_deprotonation=ElectronMigrationStep(
            replace=[(right_OH2_lone_pair,right_OH2_H_bond),
                     (right_O1_H_bond,right_O_lone_pair_after)],
            create=[right_OH2_positive],
            fadeout=[right_O_positive],
        )
        self.play(right_mol.electron_migration(steps=[right_step_deprotonation],run_time=1.5))

        #羰基O上的孤对电子消失，右侧水合氢离子消失
        self.play(FadeOut(right_O_lone_pair_after))
        right_mol.delete_charge(text="O1")
        self.play(FadeOut(right_OH2_mob,right_OH2_positive,right_H_mob,right_OH2_H_bond))
        right_mol.delete_atom(names=["OH2","H"])
        self.wait(1.5)
        self.play(FadeOut(*self.mobjects),run_time=1)

        #-----------------------alpha-H substitution-----------------------
        alpha_H_substitution=Title(text=r"\text{羰基活泼}\mathrm{\alpha-H}\text{的亲电取代}")
        self.play(Write(alpha_H_substitution))

        #显示一个丙酮分子
        acetone=StructuralFormula(name="C1",pos=ORIGIN,text=r"\mathrm{C}")
        acetone.add_atom(name="O1",direction=90*DEGREES,text=r"\mathrm{O}",
                         bond_type=BondType.DOUBLE_BOND,adjacency="C1",side=0)
        acetone.add_atom(name="C2",direction=210*DEGREES,text=None,
                         bond_type=BondType.NORMAL_BOND,adjacency="C1")
        acetone.add_atom(name="C3",direction=330*DEGREES,text=r"\mathrm{C}",
                         bond_type=BondType.NORMAL_BOND,adjacency="C1")
        acetone.add_atom(name="H1",direction=30*DEGREES,text=r"\mathrm{H}",
                         bond_type=BondType.NORMAL_BOND,adjacency="C3")
        acetone.add_atom(name="H2",direction=330*DEGREES,text=r"\mathrm{H}",
                         bond_type=BondType.NORMAL_BOND,adjacency="C3")
        acetone.add_atom(name="H3",direction=270*DEGREES,text=r"\mathrm{H}",
                         bond_type=BondType.NORMAL_BOND,adjacency="C3")

        self.play(Create(acetone))
        self.wait(1.5)

        #诱导效应：O=C键、C-αC键、三个αC-H键依次向前一个原子略平移
        O_C_bond=acetone.bond_lookup.between("O1","C1")
        C_alphaC_bond=acetone.bond_lookup.between("C1","C3")
        C3_H1_bond=acetone.bond_lookup.between("C3","H1")
        C3_H2_bond=acetone.bond_lookup.between("C3","H2")
        C3_H3_bond=acetone.bond_lookup.between("C3","H3")

        shift_amount=0.08
        O_pos=acetone.atomic_clusters["O1"]["pos"]
        C1_pos=acetone.atomic_clusters["C1"]["pos"]
        C3_pos=acetone.atomic_clusters["C3"]["pos"]
        H1_pos=acetone.atomic_clusters["H1"]["pos"]
        H2_pos=acetone.atomic_clusters["H2"]["pos"]
        H3_pos=acetone.atomic_clusters["H3"]["pos"]

        O_C_direction=(O_pos-C1_pos)/np.linalg.norm(O_pos-C1_pos)
        C_alphaC_direction=(C1_pos-C3_pos)/np.linalg.norm(C1_pos-C3_pos)
        C3_H1_direction=(C3_pos-H1_pos)/np.linalg.norm(C3_pos-H1_pos)
        C3_H2_direction=(C3_pos-H2_pos)/np.linalg.norm(C3_pos-H2_pos)
        C3_H3_direction=(C3_pos-H3_pos)/np.linalg.norm(C3_pos-H3_pos)

        O_C_shift=O_C_direction*shift_amount
        C_alphaC_shift=C_alphaC_direction*shift_amount
        C3_H1_shift=C3_H1_direction*shift_amount
        C3_H2_shift=C3_H2_direction*shift_amount
        C3_H3_shift=C3_H3_direction*shift_amount

        def shorten_bond(bond,shift,direction):
            target=bond.copy()
            center=bond.get_center()
            def func(p):
                rel=p-center
                along=np.dot(rel,direction)
                return center+shift+direction*(along*0.8)+(rel-direction*along)
            target.apply_function(func)
            return target

        O_C_bond_original=O_C_bond.copy()
        C_alphaC_bond_original=C_alphaC_bond.copy()
        C3_H1_bond_original=C3_H1_bond.copy()
        C3_H2_bond_original=C3_H2_bond.copy()
        C3_H3_bond_original=C3_H3_bond.copy()

        O_C_bond_short=shorten_bond(O_C_bond,O_C_shift,O_C_direction)
        C_alphaC_bond_short=shorten_bond(C_alphaC_bond,C_alphaC_shift,C_alphaC_direction)
        C3_H1_bond_short=shorten_bond(C3_H1_bond,C3_H1_shift,C3_H1_direction)
        C3_H2_bond_short=shorten_bond(C3_H2_bond,C3_H2_shift,C3_H2_direction)
        C3_H3_bond_short=shorten_bond(C3_H3_bond,C3_H3_shift,C3_H3_direction)

        self.play(Transform(O_C_bond,O_C_bond_short),run_time=0.8,rate_func=smoothererstep)
        self.play(Transform(C_alphaC_bond,C_alphaC_bond_short),run_time=0.8,rate_func=smoothererstep)
        self.play(Transform(C3_H1_bond,C3_H1_bond_short),
                  Transform(C3_H2_bond,C3_H2_bond_short),
                  Transform(C3_H3_bond,C3_H3_bond_short),
                  run_time=0.8,rate_func=smoothererstep)

        self.wait(1.5)

        self.play(Transform(O_C_bond,O_C_bond_original),
                  Transform(C_alphaC_bond,C_alphaC_bond_original),
                  Transform(C3_H1_bond,C3_H1_bond_original),
                  Transform(C3_H2_bond,C3_H2_bond_original),
                  Transform(C3_H3_bond,C3_H3_bond_original),
                  run_time=1.0,rate_func=smoothererstep)
        self.wait(1.0)
