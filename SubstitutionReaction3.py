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

        #先显示中间底物
        self.play(Create(acetyl_L))
        self.wait(0.5)

        #右侧亲核试剂 Nu^-（先独立显示，进攻时再并入乙酰基结构）
        Nu_start=np.array([3*acetyl_L.attributes.length_global,0,0])
        Nu_mob=AtomicCluster(text=r"\mathrm{Nu}",pos=Nu_start,attributes=acetyl_L.attributes)
        acetyl_L.register_atom(name="Nu",mobject=Nu_mob)
        acetyl_L.add_charge(text="Nu",pos=UL,charge_type=ChargeType.NEGATIVE)
        Nu_negative=acetyl_L.charges["Nu"]

        self.play(FadeIn(Nu_mob),FadeIn(Nu_negative))
        self.wait(0.5)
        
        #碱催化的机理

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

        #更新结构式内部数据
        acetyl_L.delete_bond(start="C1",end="O1")
        acetyl_L.atomic_clusters["C1"][Bond].append(C1_O1_single)
        acetyl_L.atomic_clusters["O1"][Bond].append(C1_O1_single)
        acetyl_L.atomic_clusters["C1"]["adj"].append("O1")
        acetyl_L.atomic_clusters["O1"]["adj"].append("C1")

        acetyl_L.atomic_clusters["C1"][Bond].append(C1_Nu_in)
        acetyl_L.atomic_clusters["Nu"][Bond].append(C1_Nu_in)
        acetyl_L.atomic_clusters["C1"]["adj"].append("Nu")
        acetyl_L.atomic_clusters["Nu"]["adj"].append("C1")

        acetyl_L.charges.pop("Nu")
        acetyl_L.charges["O1"]=O1_negative

        #C-Nu键顺时针旋转30°
        self.play(acetyl_L.rotate_atoms(atom_names="Nu",
                                        center="C1",
                                        angle=-30*DEGREES,
                                        run_time=0.8))

        self.wait(1.5)
