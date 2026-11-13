#manim SubstitutionReaction4.py test -pqh

from OrganicReactionTools import *

class test(Scene):
    def construct(self):
        
        title=Title(text=r"\text{一些常见的取代反应的机理}\quad\text{补}",pos=ORIGIN)
        subtitle=Subtitle(text=r"\text{芳环上的取代反应}",pos=[0,-0.7,0])
        self.play(Write(title),Write(subtitle))
        self.wait(1.5)
        self.play(FadeOut(title,subtitle))

        #descriptions
        text1=Description(text=r"\text{当我们需要把一个亲核的基团连到苯环上时，第一时间想到的应该是}\mathrm{SNAr}")
        text2=Description(text=r"\text{可是在}\mathrm{SNAr}\text{中，被取代的位点需要有一个可离去的基团}")
        text3=Description(text=r"\text{然而}\mathrm{H^-}\text{是一个极差的离去基团，}\\\text{因此}\mathrm{SNAr}\text{面对没有离去基团的苯环时就会显得无能为力}")

        #SNAr反应式：亲核试剂Nu取代芳环上邻位于硝基的X，X以负离子形式离去
        #反应式整体缩到 0.8 倍，键线宽按同一比例调细
        scale_equation=0.8
        bond_width=3.2
        substrate=Benzene(center=ORIGIN,c_names=["C1","C2","C3","C4","C5","C6"],bond_stroke_width=bond_width)
        substrate.add_atom(name="N1",direction=90*DEGREES,text=r"\mathrm{N}",
                           bond_type=BondType.NORMAL_BOND,adjacency="C1")
        substrate.add_atom(name="O1",direction=150*DEGREES,text=r"\mathrm{O}",
                           bond_type=BondType.NORMAL_BOND,adjacency="N1")
        substrate.add_atom(name="O2",direction=30*DEGREES,text=r"\mathrm{O}",
                           bond_type=BondType.DOUBLE_BOND,adjacency="N1",side=0)
        substrate.add_charge(text="N1",pos=LEFT,charge_type=ChargeType.POSITIVE)
        substrate.add_charge(text="O1",pos=UR,charge_type=ChargeType.NEGATIVE)
        substrate.add_atom(name="X",direction=30*DEGREES,text=r"\mathrm{X}",
                           bond_type=BondType.NORMAL_BOND,adjacency="C2")

        product=Benzene(center=ORIGIN,c_names=["C1","C2","C3","C4","C5","C6"],bond_stroke_width=bond_width)
        product.add_atom(name="N1",direction=90*DEGREES,text=r"\mathrm{N}",
                         bond_type=BondType.NORMAL_BOND,adjacency="C1")
        product.add_atom(name="O1",direction=150*DEGREES,text=r"\mathrm{O}",
                         bond_type=BondType.NORMAL_BOND,adjacency="N1")
        product.add_atom(name="O2",direction=30*DEGREES,text=r"\mathrm{O}",
                         bond_type=BondType.DOUBLE_BOND,adjacency="N1",side=0)
        product.add_charge(text="N1",pos=LEFT,charge_type=ChargeType.POSITIVE)
        product.add_charge(text="O1",pos=UR,charge_type=ChargeType.NEGATIVE)
        #Nu 是较宽的原子（团）符号，标签沿键方向外移，避免键与文字重合
        product.add_atom(name="Nu",direction=30*DEGREES,text=r"\mathrm{Nu}",
                         bond_type=BondType.NORMAL_BOND,adjacency="C2",
                         text_offset=0.15*np.array([np.cos(30*DEGREES),np.sin(30*DEGREES),0]))

        #左侧的Nu^-与右侧的X^-独立显示，负电荷都挂在右上角
        Nu_mob=AtomicCluster(text=r"\mathrm{Nu}",pos=ORIGIN,attributes=substrate.attributes)
        Nu_charge=Charge(charge_type=ChargeType.NEGATIVE,text=Nu_mob,pos=UR,attributes=substrate.attributes)
        Nu_negative=VGroup(Nu_mob,Nu_charge)
        X_mob=AtomicCluster(text=r"\mathrm{X}",pos=ORIGIN,attributes=substrate.attributes)
        X_charge=Charge(charge_type=ChargeType.NEGATIVE,text=X_mob,pos=UR,attributes=substrate.attributes)
        X_negative=VGroup(X_mob,X_charge)

        plus1=MathTex("+",font_size=txt_size)
        plus2=MathTex("+",font_size=txt_size)
        reaction_arrow=ReactionArrow(start=ORIGIN,above="",length=1.4,stroke_width=1.6)

        #横向排开：各对象只沿x平移，苯环中心与箭头始终在同一水平线上
        buff=0.35
        plus1.shift(RIGHT*(substrate.get_right()[0]+buff-plus1.get_left()[0]))
        Nu_negative.shift(RIGHT*(plus1.get_right()[0]+buff-Nu_negative.get_left()[0]))
        reaction_arrow.shift(RIGHT*(Nu_negative.get_right()[0]+buff-reaction_arrow.arrow.get_start()[0]))
        product.shift(RIGHT*(reaction_arrow.arrow.get_end()[0]+buff-product.get_left()[0]))
        plus2.shift(RIGHT*(product.get_right()[0]+buff-plus2.get_left()[0]))
        X_negative.shift(RIGHT*(plus2.get_right()[0]+buff-X_negative.get_left()[0]))
        #整组缩放，后面新建的 H 与红叉也按同一比例
        reaction_group=VGroup(substrate,plus1,Nu_negative,reaction_arrow,product,plus2,X_negative)
        reaction_group.scale(scale_equation)
        reaction_group.move_to(ORIGIN)

        self.play(FadeIn(reaction_group),run_time=1.5)
        self.wait(2)

        #X变形为H：没有可离去的基团，产物一侧消失，同时在箭头中间打上红叉表示反应无法直接进行
        X_leaving_mob=substrate.atomic_clusters["X"][Mobject]
        H_mob=AtomicCluster(text=r"\mathrm{H}",pos=X_leaving_mob.get_center(),
                            attributes=substrate.attributes)
        H_mob.scale(scale_equation)
        cross_frame=Square(side_length=0.6*scale_equation).move_to(reaction_arrow.arrow.get_center())
        refusal_cross=Cross(cross_frame,stroke_color=RED,stroke_width=6)

        self.play(ReplacementTransform(X_leaving_mob,H_mob),
                  FadeOut(product,plus2,X_negative),
                  Create(refusal_cross),
                  run_time=1.5)
        self.wait(2)

        substrate.remove(X_leaving_mob)
        substrate.atomic_clusters["X"][Mobject]=H_mob
        substrate.add(H_mob)

        reaction_group.remove(product,plus2,X_negative)

        #反应式与红叉一起退出
        self.play(FadeOut(reaction_group,refusal_cross),run_time=1)
        self.wait(0.5)

        #-----------------------VNS mechanism-----------------------

        #descriptions
        text4=Description(text=r"\text{但是在1978年，J.Goli\'nski和M.Makosza发现，在碱性条件下}\\\text{氯甲基苯基砜可以在硝基芳香化合物的邻位或对位取代氢原子，}\\\text{形成苯基砜甲基取代产物}")
        text5=Description(text=r"\text{进一步的实验表明，在邻位或者对位卤代的硝基苯中，}\\\text{氢被取代的反应速率快于卤素原子被取代}")
        text6=Description(text=r"\text{这个反应的机理就是}\mathrm{VNS}\text{机理}")
        text7=Description(text=r"\mathrm{VNS}\text{机理，全称}\mathrm{Vicarious\ Nucleophilic\ Substitution}\text{，}\\\text{翻译为中文就是间接亲核取代反应}")
        text8=Description(text=r"\text{意思就是底物中的氢不是被直接取代的，而是通过一种间接的方式离去}")

        #VNS反应式：硝基苯与氯甲基苯基砜在KOH/DMSO中反应，再经酸处理，生成苯基砜甲基在硝基邻位、对位的两种产物
        #两个箭头要等长、且长度要盖过上方较宽的氯甲基苯基砜，整式因此更宽，第二式再缩一点；键线宽按同一比例收，观感与第一式一致
        scale_vns=0.72
        bond_width_vns=bond_width*scale_vns/scale_equation
        substrate_vns=Benzene(center=ORIGIN,c_names=["C1","C2","C3","C4","C5","C6"],bond_stroke_width=bond_width_vns)
        substrate_vns.add_atom(name="N1",direction=90*DEGREES,text=r"\mathrm{N}",
                               bond_type=BondType.NORMAL_BOND,adjacency="C1")
        substrate_vns.add_atom(name="O1",direction=150*DEGREES,text=r"\mathrm{O}",
                               bond_type=BondType.NORMAL_BOND,adjacency="N1")
        substrate_vns.add_atom(name="O2",direction=30*DEGREES,text=r"\mathrm{O}",
                               bond_type=BondType.DOUBLE_BOND,adjacency="N1",side=0)
        substrate_vns.add_charge(text="N1",pos=LEFT,charge_type=ChargeType.POSITIVE)
        substrate_vns.add_charge(text="O1",pos=UR,charge_type=ChargeType.NEGATIVE)

        #第一个箭头上方：氯甲基苯基砜，中心C无文本标签，左下30°连Cl、右下30°连S，S的右上60°/左下60°为双键O、右下30°为Ph
        sulfone_vns=StructuralFormula(name="C1",pos=ORIGIN,text=None,bond_stroke_width=bond_width_vns)
        sulfone_vns.add_atom(name="Cl1",direction=210*DEGREES,text=r"\mathrm{Cl}",
                             bond_type=BondType.NORMAL_BOND,adjacency="C1")
        sulfone_vns.add_atom(name="S1",direction=330*DEGREES,text=r"\mathrm{S}",
                             bond_type=BondType.NORMAL_BOND,adjacency="C1")
        sulfone_vns.add_atom(name="O1",direction=60*DEGREES,text=r"\mathrm{O}",
                             bond_type=BondType.DOUBLE_BOND,adjacency="S1",side=0)
        sulfone_vns.add_atom(name="O2",direction=240*DEGREES,text=r"\mathrm{O}",
                             bond_type=BondType.DOUBLE_BOND,adjacency="S1",side=0)
        #Ph 是较宽的原子（团）符号，标签沿键方向外移，避免键与文字重合
        sulfone_vns.add_atom(name="Ph1",direction=330*DEGREES,text=r"\mathrm{Ph}",
                             bond_type=BondType.NORMAL_BOND,adjacency="S1",
                             text_offset=0.15*np.array([np.cos(330*DEGREES),np.sin(330*DEGREES),0]))

        #两个箭头等长（长度盖过上方较宽的氯甲基苯基砜）：第一个下方KOH/DMSO，第二个上方H3O+
        #箭头上下方的条件文字比默认字号大一号（整式缩到 0.72 后仍清楚）
        arrow_font_size=32
        arrow_length=sulfone_vns.width+0.1
        arrow1_vns=ReactionArrow(start=ORIGIN,above=sulfone_vns,below=r"\mathrm{KOH/DMSO}",length=arrow_length,
                                 font_size=arrow_font_size)
        arrow2_vns=ReactionArrow(start=ORIGIN,above=r"\mathrm{H_3O^+}",length=arrow_length,font_size=arrow_font_size)

        #SO2Ph 标签整体右移，使键正对首字符S的中心，而不是整段文字的中心
        SO2Ph_label=MathTex(r"\mathrm{SO_2Ph}",font_size=substrate_vns.attributes.font_size,tex_template=mytemplate)
        SO2Ph_first=MathTex(r"\mathrm{S}",font_size=substrate_vns.attributes.font_size,tex_template=mytemplate)
        SO2Ph_offset=RIGHT*(SO2Ph_label.width/2-SO2Ph_first.width/2)

        #产物一：苯基砜甲基在硝基邻位（C2），SO2Ph朝右下30°连出
        product_ortho_vns=Benzene(center=ORIGIN,c_names=["C1","C2","C3","C4","C5","C6"],bond_stroke_width=bond_width_vns)
        product_ortho_vns.add_atom(name="N1",direction=90*DEGREES,text=r"\mathrm{N}",
                                   bond_type=BondType.NORMAL_BOND,adjacency="C1")
        product_ortho_vns.add_atom(name="O1",direction=150*DEGREES,text=r"\mathrm{O}",
                                   bond_type=BondType.NORMAL_BOND,adjacency="N1")
        product_ortho_vns.add_atom(name="O2",direction=30*DEGREES,text=r"\mathrm{O}",
                                   bond_type=BondType.DOUBLE_BOND,adjacency="N1",side=0)
        product_ortho_vns.add_charge(text="N1",pos=LEFT,charge_type=ChargeType.POSITIVE)
        product_ortho_vns.add_charge(text="O1",pos=UR,charge_type=ChargeType.NEGATIVE)
        product_ortho_vns.add_atom(name="CH2",direction=30*DEGREES,text=None,
                                   bond_type=BondType.NORMAL_BOND,adjacency="C2")
        product_ortho_vns.add_atom(name="SO2Ph",direction=330*DEGREES,text=r"\mathrm{SO_2Ph}",
                                   bond_type=BondType.NORMAL_BOND,adjacency="CH2",
                                   text_offset=SO2Ph_offset)

        #产物二：苯基砜甲基在硝基对位（C4）
        product_para_vns=Benzene(center=ORIGIN,c_names=["C1","C2","C3","C4","C5","C6"],bond_stroke_width=bond_width_vns)
        product_para_vns.add_atom(name="N1",direction=90*DEGREES,text=r"\mathrm{N}",
                                  bond_type=BondType.NORMAL_BOND,adjacency="C1")
        product_para_vns.add_atom(name="O1",direction=150*DEGREES,text=r"\mathrm{O}",
                                  bond_type=BondType.NORMAL_BOND,adjacency="N1")
        product_para_vns.add_atom(name="O2",direction=30*DEGREES,text=r"\mathrm{O}",
                                  bond_type=BondType.DOUBLE_BOND,adjacency="N1",side=0)
        product_para_vns.add_charge(text="N1",pos=LEFT,charge_type=ChargeType.POSITIVE)
        product_para_vns.add_charge(text="O1",pos=UR,charge_type=ChargeType.NEGATIVE)
        product_para_vns.add_atom(name="CH2",direction=270*DEGREES,text=None,
                                  bond_type=BondType.NORMAL_BOND,adjacency="C4")
        product_para_vns.add_atom(name="SO2Ph",direction=330*DEGREES,text=r"\mathrm{SO_2Ph}",
                                  bond_type=BondType.NORMAL_BOND,adjacency="CH2",
                                  text_offset=SO2Ph_offset)

        plus_vns=MathTex("+",font_size=txt_size)

        #横向排开：各对象只沿x平移，苯环中心与箭头始终在同一水平线上；两种产物之间用加号连接
        buff=0.3
        substrate_vns.shift(RIGHT*(-5.0))
        arrow1_vns.shift(RIGHT*(substrate_vns.get_right()[0]+buff-arrow1_vns.get_left()[0]))
        arrow2_vns.shift(RIGHT*(arrow1_vns.get_right()[0]+buff-arrow2_vns.get_left()[0]))
        product_ortho_vns.shift(RIGHT*(arrow2_vns.get_right()[0]+buff-product_ortho_vns.get_left()[0]))
        plus_vns.shift(RIGHT*(product_ortho_vns.get_right()[0]+buff-plus_vns.get_left()[0]))
        product_para_vns.shift(RIGHT*(plus_vns.get_right()[0]+buff-product_para_vns.get_left()[0]))
        reaction_group_vns=VGroup(substrate_vns,arrow1_vns,arrow2_vns,
                                  product_ortho_vns,plus_vns,product_para_vns)
        reaction_group_vns.scale(scale_vns)
        reaction_group_vns.move_to(ORIGIN)

        self.play(FadeIn(reaction_group_vns),run_time=1.5)
        self.wait(2)

        #标题用三个独立字母拼成，坐标写死（由 test.py 的 TestVNSExpand 标定：总宽与整体排版的 VNS 一致）
        VNS_mechanism=VGroup(MathTex(r"\mathrm{V}",font_size=title_size,tex_template=mytemplate),
                             MathTex(r"\mathrm{N}",font_size=title_size,tex_template=mytemplate),
                             MathTex(r"\mathrm{S}",font_size=title_size,tex_template=mytemplate))
        VNS_mechanism[0].move_to([-0.4164,3.0,0])
        VNS_mechanism[1].move_to([0.0879,3.0,0])
        VNS_mechanism[2].move_to([0.5043,3.0,0])
        V_letter,N_letter,S_letter=VNS_mechanism
        self.play(Write(VNS_mechanism))
        self.wait(0.5)

        #反应式淡出，标题保留
        self.play(FadeOut(reaction_group_vns),run_time=1)
        self.wait(0.5)

        #VNS拆成三个字母，移到画面纵向中心，再分别扩展成三个单词（坐标写死，由 test.py 的 TestVNSExpand 标定）
        words=VGroup(MathTex(r"\mathrm{V}",r"\mathrm{icarious}",arg_separator="",font_size=title_size,tex_template=mytemplate),
                     MathTex(r"\mathrm{N}",r"\mathrm{ucleophilic}",arg_separator="",font_size=title_size,tex_template=mytemplate),
                     MathTex(r"\mathrm{S}",r"\mathrm{ubstitution}",arg_separator="",font_size=title_size,tex_template=mytemplate))
        words[0].move_to([-3.4697,0,0])
        words[1].move_to([-0.1384,-0.0673,0])
        words[2].move_to([3.6081,0.0072,0])

        #三个字母移到各词首字母的位置（词距 0.263、基线 -0.2313）
        self.play(V_letter.animate.move_to([-4.566,0,0]),
                  N_letter.animate.move_to([-1.653,-0.0072,0]),
                  S_letter.animate.move_to([2.0085,0.0072,0]),
                  run_time=1.5)
        self.wait(1)

        self.play(Write(words[0][1]),Write(words[1][1]),Write(words[2][1]),run_time=2)
        self.wait(2)

        #三个字母飞回标题位置（画面只保留 VNS），其余字母同时淡出
        self.play(V_letter.animate.move_to([-0.4164,3.0,0]),
                  N_letter.animate.move_to([0.0879,3.0,0]),
                  S_letter.animate.move_to([0.5043,3.0,0]),
                  FadeOut(words[0][1]),FadeOut(words[1][1]),FadeOut(words[2][1]),
                  run_time=1.5)
        self.wait(1.5)

        #descriptions
        text9=Description(text=r"\text{首先体系中的碱夺取}\mathrm{ClCH_2SO_2Ph}\text{的酸性}\mathrm{\alpha-H}\text{，形成碳负离子}")
        text10=Description(text=r"\text{然后这个碳负离子进攻苯环上硝基的邻位或者对位（此处以邻位为例），}\\\text{形成}\mathrm{\sigma}\text{-络合物}")
        text11=Description(text=r"\text{接着发生}\mathrm{\beta}\text{-消除，生成一分子的}\mathrm{HX}\text{，环恢复芳香性}")
        text12=Description(text=r"\text{最后将体系酸化，碳负离子被质子化，得到产物}")

        #氯甲基苯基砜：中心 C 带标签（便于楔形键收在字母边缘），左上150°、正下方270° 各连一个 H，右下330° 连 Cl，右上30° 连 SO2Ph
        sulfone_mob=StructuralFormula(name="C1",pos=ORIGIN,text=r"\mathrm{C}")
        sulfone_mob.add_atom(name="H1",direction=150*DEGREES,text=r"\mathrm{H}",
                             bond_type=BondType.NORMAL_BOND,adjacency="C1")
        sulfone_mob.add_atom(name="H2",direction=270*DEGREES,text=r"\mathrm{H}",
                             bond_type=BondType.NORMAL_BOND,adjacency="C1")
        sulfone_mob.add_atom(name="Cl1",direction=330*DEGREES,text=r"\mathrm{Cl}",
                             bond_type=BondType.NORMAL_BOND,adjacency="C1")
        #SO2Ph 标签沿用产物里的位移，让键正对首字符 S 的中心
        sulfone_mob.add_atom(name="S1",direction=30*DEGREES,text=r"\mathrm{SO_2Ph}",
                             bond_type=BondType.NORMAL_BOND,adjacency="C1",text_offset=SO2Ph_offset)

        self.play(Create(sulfone_mob),run_time=1.5)
        self.wait(2)

        #左上角 H 的左侧显示 HO-（负电荷在 O 的右上）
        H1_pos=sulfone_mob.atomic_clusters["H1"]["pos"]
        HO_pos=H1_pos+np.array([-sulfone_mob.attributes.length_global,0,0])
        #HO 标签整体左移：键要正对右侧 O 的中心，而不是整段文字的中心
        HO_label=MathTex(r"\mathrm{HO}",font_size=sulfone_mob.attributes.font_size,tex_template=mytemplate)
        HO_oxygen=MathTex(r"\mathrm{O}",font_size=sulfone_mob.attributes.font_size,tex_template=mytemplate)
        HO_offset=LEFT*(HO_label.width/2-HO_oxygen.width/2)
        HO_mob=AtomicCluster(text=r"\mathrm{HO}",pos=HO_pos,text_offset=HO_offset,attributes=sulfone_mob.attributes)
        sulfone_mob.register_atom(name="HO",mobject=HO_mob)
        sulfone_mob.add_charge(text="HO",pos=UR,charge_type=ChargeType.NEGATIVE)
        HO_negative=sulfone_mob.charges["HO"]

        self.add(HO_mob,HO_negative)
        self.play(FadeIn(HO_mob),FadeIn(HO_negative),run_time=0.8)
        self.wait(0.5)

        #负电荷进攻H：O-H成键、C-H键断裂并在C上留下负电荷（碳负离子）
        C1_H1_bond=sulfone_mob.bond_lookup.between("C1","H1")
        HO_H1_bond=sulfone_mob.build_bond(start="HO",end="H1",bond_type=BondType.NORMAL_BOND)
        C1_negative=sulfone_mob.build_charge(text="C1",pos=DL,charge_type=ChargeType.NEGATIVE)

        step_ho_attack=ElectronMigrationStep(
            replace=[(HO_negative,HO_H1_bond),
                     (C1_H1_bond,C1_negative)],
        )
        self.play(sulfone_mob.electron_migration(steps=[step_ho_attack],run_time=1.5))
        self.wait(1)

        #生成H2O：HO-与那个H合并成一个水分子（碳负离子留在原处）
        H1_mob=sulfone_mob.atomic_clusters["H1"][Mobject]
        H2O_mob=AtomicCluster(text=r"\mathrm{H_2O}",pos=HO_pos+np.array([0.1,0.35,0]),attributes=sulfone_mob.attributes)
        self.play(ReplacementTransform(VGroup(HO_mob,H1_mob,HO_H1_bond),H2O_mob),run_time=1.5)
        sulfone_mob.remove(HO_mob,H1_mob,HO_H1_bond)
        self.wait(2)

        #H2O 消失，碳负离子右移让出位置
        self.play(FadeOut(H2O_mob),run_time=1)
        sulfone_mob.remove(H2O_mob)
        self.wait(0.5)
        self.play(sulfone_mob.animate.shift(RIGHT*1.0),run_time=1.5)
        for atom_vns in sulfone_mob.atomic_clusters.values():
            atom_vns["pos"]=np.array(atom_vns["pos"])+RIGHT*1.0
        self.wait(0.5)

        #硝基苯：硝基在正上方（C1 正上方 90°），硝基右侧的邻位 C2 上显示一个 H
        nitrobenzene_mob=Benzene(center=np.array([-1.9,-0.4,0]),c_names=["C1","C2","C3","C4","C5","C6"])
        nitrobenzene_mob.add_atom(name="N1",direction=90*DEGREES,text=r"\mathrm{N}",
                                  bond_type=BondType.NORMAL_BOND,adjacency="C1")
        nitrobenzene_mob.add_atom(name="O1",direction=150*DEGREES,text=r"\mathrm{O}",
                                  bond_type=BondType.NORMAL_BOND,adjacency="N1")
        nitrobenzene_mob.add_atom(name="O2",direction=30*DEGREES,text=r"\mathrm{O}",
                                  bond_type=BondType.DOUBLE_BOND,adjacency="N1",side=0)
        nitrobenzene_mob.add_charge(text="N1",pos=LEFT,charge_type=ChargeType.POSITIVE)
        nitrobenzene_mob.add_charge(text="O1",pos=UR,charge_type=ChargeType.NEGATIVE)
        nitrobenzene_mob.add_atom(name="H1",direction=30*DEGREES,text=r"\mathrm{H}",
                                  bond_type=BondType.NORMAL_BOND,adjacency="C2")

        self.play(Create(nitrobenzene_mob),run_time=2.5)
        self.wait(2)

        self.play(sulfone_mob.rotate_atoms(atom_names=["C1","H2","Cl1","S1"],center="C1",
                                           angle=30*DEGREES,run_time=1.5))
        self.wait(1)

        #碳负离子进攻苯环：先让两只分子就位——碳负离子的碳 C1 落在硝基苯 C2 的正右侧、相距一个键长
        nitro_shift=RIGHT*0.58
        C1_live=np.array(sulfone_mob.atomic_clusters["C1"][Mobject].get_center())
        C2_pos=np.array(nitrobenzene_mob.atomic_clusters["C2"]["pos"])+nitro_shift
        C1_target=C2_pos+RIGHT

        attack_shift=C1_target-C1_live
        self.play(nitrobenzene_mob.animate.shift(nitro_shift),
                  sulfone_mob.animate.shift(attack_shift),run_time=1.5)
        for atom_vns in sulfone_mob.atomic_clusters.values():
            atom_vns["pos"]=np.array(atom_vns["pos"])+attack_shift
        for atom_vns in nitrobenzene_mob.atomic_clusters.values():
            atom_vns["pos"]=np.array(atom_vns["pos"])+nitro_shift
        self.wait(1)

        #这一连串电子转移放在同一个转移动画里：
        #负电荷 → C-C 键（OutBond，朝向观察者）；环右上双键 → C-N 变双键；N=O 双键 → O 上变成负电荷；
        #同时苯环上的 C-H 逆时针转 15°（30°→45°）并变成 InBond（背离观察者）
        #end_edge=True：楔形粗端停在 C 标签边缘，两个角不会顶在键的交点上
        cc_bond=OutBond(start=C2_pos,direction=0*DEGREES,
                        start_edge=False,end_edge=True,attributes=sulfone_mob.attributes)

        ring_H1_bond=nitrobenzene_mob.bond_lookup.between("C2","H1")
        ring_H1_mob=nitrobenzene_mob.atomic_clusters["H1"][Mobject]
        ring_H1_target=C2_pos+np.array([np.cos(45*DEGREES),np.sin(45*DEGREES),0])
        nitrobenzene_mob.atomic_clusters["H1"]["pos"]=ring_H1_target
        ring_H1_bond_in=nitrobenzene_mob.build_bond(start="C2",end="H1",bond_type=BondType.IN_BOND)
        ring_H1_mob_new=ring_H1_mob.copy().move_to(ring_H1_target)

        C1_C2_double=nitrobenzene_mob.bond_lookup.between("C1","C2")
        C1_N1_single=nitrobenzene_mob.bond_lookup.between("C1","N1")
        N1_O2_double=nitrobenzene_mob.bond_lookup.between("N1","O2")

        C1_C2_single=nitrobenzene_mob.build_bond(start="C1",end="C2",bond_type=BondType.NORMAL_BOND)
        C1_N1_double=nitrobenzene_mob.build_bond(start="C1",end="N1",bond_type=BondType.DOUBLE_BOND,side=0)
        N1_O2_single=nitrobenzene_mob.build_bond(start="N1",end="O2",bond_type=BondType.NORMAL_BOND)
        O2_negative=nitrobenzene_mob.build_charge(text="O2",pos=UR,charge_type=ChargeType.NEGATIVE)

        #C-H 逆时针转 15°（30°→45°）并变成 InBond：作为一个独立动画与电子转移同时开始（不塞进 electron_migration）。
        step_attack=ElectronMigrationStep(
            replace=[(C1_negative,cc_bond),
                     BondLinePair(source=VGroup(C1_C2_double,C1_N1_single),
                                  target=VGroup(C1_C2_single,C1_N1_double)),
                     (N1_O2_double,VGroup(N1_O2_single,O2_negative))],
        )
        ring_H1_turn=AnimationGroup(ReplacementTransform(ring_H1_bond,ring_H1_bond_in,run_time=1),
                                    ReplacementTransform(ring_H1_mob,ring_H1_mob_new,run_time=1),
                                    lag_ratio=0)
        attack_migration=nitrobenzene_mob.electron_migration(steps=[step_attack],run_time=2.0)
        self.play(attack_migration,Succession(ring_H1_turn,Wait(attack_migration.run_time-1)))
        sulfone_mob.remove(C1_negative)
        nitrobenzene_mob.atomic_clusters["C2"][Bond].remove(ring_H1_bond)
        nitrobenzene_mob.atomic_clusters["H1"][Bond].remove(ring_H1_bond)
        nitrobenzene_mob.register_bond(start="C2",end="H1",bond=ring_H1_bond_in)
        nitrobenzene_mob.atomic_clusters["H1"][Mobject]=ring_H1_mob_new
        self.wait(2)

        #消除 HCl：先在苯环上 H 的正上方显示 OH-（负电荷在 O 的左上）
        ring_H1_pos=np.array(nitrobenzene_mob.atomic_clusters["H1"]["pos"])
        OH_pos=ring_H1_pos+UP*1.0
        #OH 标签整体右移，让键正对左侧 O 的中心
        OH_label=MathTex(r"\mathrm{OH}",font_size=nitrobenzene_mob.attributes.font_size,tex_template=mytemplate)
        OH_oxygen=MathTex(r"\mathrm{O}",font_size=nitrobenzene_mob.attributes.font_size,tex_template=mytemplate)
        OH_offset=RIGHT*(OH_label.width/2-OH_oxygen.width/2)
        OH_mob=AtomicCluster(text=r"\mathrm{OH}",pos=OH_pos,text_offset=OH_offset,
                             attributes=nitrobenzene_mob.attributes)
        nitrobenzene_mob.register_atom(name="OH",mobject=OH_mob)
        nitrobenzene_mob.add_charge(text="OH",pos=UL,charge_type=ChargeType.NEGATIVE)
        OH_negative=nitrobenzene_mob.charges["OH"]

        self.add(OH_mob,OH_negative)
        self.play(FadeIn(OH_mob),FadeIn(OH_negative),run_time=0.8)
        self.wait(0.5)

        #OH- 的负电荷变成 H-OH 键；环上 C-H 与 C-C 楔形键变成 C=C（side=0）；C-Cl 的电子给 Cl（右上负电荷）
        C2_H1_bond=nitrobenzene_mob.bond_lookup.between("C2","H1")
        C1_Cl1_bond=sulfone_mob.bond_lookup.between("C1","Cl1")
        H_OH_bond=nitrobenzene_mob.build_bond(start="H1",end="OH",bond_type=BondType.NORMAL_BOND)
        C2_C1_double=DoubleBond(start=C2_pos,direction=0*DEGREES,start_edge=False,end_edge=True,
                                attributes=nitrobenzene_mob.attributes,side=0)
        Cl1_negative=sulfone_mob.build_charge(text="Cl1",pos=UR,charge_type=ChargeType.NEGATIVE)

        step_elimination=ElectronMigrationStep(
            replace=[(OH_negative,H_OH_bond),
                     (VGroup(C2_H1_bond,cc_bond),C2_C1_double),
                     (C1_Cl1_bond,Cl1_negative)],
        )
        self.play(nitrobenzene_mob.electron_migration(steps=[step_elimination],run_time=1.5))
        sulfone_mob.atomic_clusters["C1"][Bond].remove(C1_Cl1_bond)
        sulfone_mob.atomic_clusters["Cl1"][Bond].remove(C1_Cl1_bond)
        sulfone_mob.register_charge(name="Cl1",charge=Cl1_negative)
        sulfone_mob.remove(C1_Cl1_bond)
        for line_vns in C2_C1_double.submobjects:
            nitrobenzene_mob.remove(line_vns)
        nitrobenzene_mob.remove(ring_H1_bond,ring_H1_mob)

        #H-OH 与 Cl- 离开
        ring_H1_mob=nitrobenzene_mob.atomic_clusters["H1"][Mobject]
        Cl1_mob=sulfone_mob.atomic_clusters["Cl1"][Mobject]
        self.play(FadeOut(OH_mob,H_OH_bond,ring_H1_mob,Cl1_mob,Cl1_negative),run_time=1)
        nitrobenzene_mob.remove(OH_mob,H_OH_bond,ring_H1_mob,Cl1_negative)
        sulfone_mob.remove(Cl1_mob)

        #连出去的那个 C=C 及其外侧的对象（碳负离子的碳、H、SO2Ph）一起绕苯环右上角的 C 逆时针转 30°
        self.play(sulfone_mob.rotate_atoms(atom_names=["C1","H2","S1"],center=C2_pos,
                                          angle=30*DEGREES,run_time=1.5),
                  Rotate(C2_C1_double,angle=30*DEGREES,about_point=C2_pos,run_time=1.5))
        self.wait(1.5)

        #恢复芳香性：右侧 O 的负电荷 + N-O 键 → N=O；C=N 与环上 C-C → C-N 与环上 C=C；
        #环外 C=C → 环外 C-C + 环外 C 上的负电荷
        sulfone_mob.charges.pop("C1",None)
        sulfone_mob.charges.pop("Cl1",None)

        N1_O2_single=nitrobenzene_mob.bond_lookup.between("N1","O2")
        O2_negative=nitrobenzene_mob.charges["O2"]
        N1_O2_double=nitrobenzene_mob.build_bond(start="N1",end="O2",bond_type=BondType.DOUBLE_BOND,side=0)

        C1_N1_double=nitrobenzene_mob.bond_lookup.between("C1","N1")
        C1_N1_single=nitrobenzene_mob.build_bond(start="C1",end="N1",bond_type=BondType.NORMAL_BOND)

        C1_C2_single=nitrobenzene_mob.bond_lookup.between("C1","C2")
        C1_C2_double=nitrobenzene_mob.build_bond(start="C1",end="C2",bond_type=BondType.DOUBLE_BOND,side=-1,
                                                 start_side_edge=True,end_side_edge=True)

        C2_C1_single=NormalBond(start=C2_pos,direction=30*DEGREES,start_edge=False,end_edge=True,
                                attributes=nitrobenzene_mob.attributes)
        C1_sub_negative=sulfone_mob.build_charge(text="C1",pos=RIGHT,charge_type=ChargeType.NEGATIVE)

        #C=N 与环 C-C 是键级整体互换，用 BondLinePair 把两侧的键拆成线段按最小位移配对：
        #C=N 靠 C2 一侧的 π 线自己走过去、成为环 C=C 的内侧短线，两条 σ 线原地不动。
        step_rearomatization=ElectronMigrationStep(
            replace=[(VGroup(N1_O2_single,O2_negative),N1_O2_double),
                     BondLinePair(source=VGroup(C1_N1_double,C1_C2_single),
                                  target=VGroup(C1_N1_single,C1_C2_double)),
                     (C2_C1_double,VGroup(C2_C1_single,C1_sub_negative))],
        )
        self.play(nitrobenzene_mob.electron_migration(steps=[step_rearomatization],run_time=2.0))
        sulfone_mob.register_charge(name="C1",charge=C1_sub_negative)
        nitrobenzene_mob.remove(C1_sub_negative,C2_C1_single)
        nitrobenzene_mob.charges.pop("C1",None)
        self.wait(2)

        #酸化：碳负离子右下出现 H-OH2+，左侧的 H 在 C 的右下 60°（H3O+ 的 H 就是待转移的那个质子）
        C1_pos=np.array(sulfone_mob.atomic_clusters["C1"]["pos"])
        acid_direction=np.array([np.cos(300*DEGREES),np.sin(300*DEGREES),0])
        H3O_H_pos=C1_pos+acid_direction*sulfone_mob.attributes.length_global
        H3O_O_pos=H3O_H_pos+acid_direction*sulfone_mob.attributes.length_global
        H3O_H_mob=AtomicCluster(text=r"\mathrm{H}",pos=H3O_H_pos,attributes=sulfone_mob.attributes)
        #OH_2 标签整体右移：H-O 键要正对左侧 O 的中心，而不是整段文字的中心
        H3O_O_label=MathTex(r"\mathrm{OH_2}",font_size=sulfone_mob.attributes.font_size,tex_template=mytemplate)
        H3O_O_char=MathTex(r"\mathrm{O}",font_size=sulfone_mob.attributes.font_size,tex_template=mytemplate)
        H3O_O_offset=RIGHT*(H3O_O_label.width/2-H3O_O_char.width/2)
        H3O_O_mob=AtomicCluster(text=r"\mathrm{OH_2}",pos=H3O_O_pos,text_offset=H3O_O_offset,
                                attributes=sulfone_mob.attributes)
        sulfone_mob.register_atom(name="H3",mobject=H3O_H_mob)
        sulfone_mob.register_atom(name="O3",mobject=H3O_O_mob)
        H3O_bond=sulfone_mob.build_bond(start="H3",end="O3",bond_type=BondType.NORMAL_BOND)
        #正电荷放在 OH_2 的左下：左上被进键的 H-O 键占住，正左方要留给 H-O 键断裂后生成的孤对电子
        sulfone_mob.add_charge(text="O3",pos=DL,charge_type=ChargeType.POSITIVE)
        H3O_positive=sulfone_mob.charges["O3"]

        self.add(H3O_H_mob,H3O_O_mob,H3O_bond,H3O_positive)
        self.play(FadeIn(H3O_H_mob),FadeIn(H3O_O_mob),FadeIn(H3O_bond),FadeIn(H3O_positive),run_time=0.8)
        self.wait(0.5)

        #负电荷变成 C-H 键；H-O 键的电子变成 O 左侧的孤对电子，正电荷同时消失
        C1_H3_bond=sulfone_mob.build_bond(start="C1",end="H3",bond_type=BondType.NORMAL_BOND)
        H3O_lone_pair=sulfone_mob.build_charge(text="O3",pos=LEFT,charge_type=ChargeType.PAIR)
        step_acidification=ElectronMigrationStep(
            replace=[(C1_sub_negative,C1_H3_bond),
                     (H3O_bond,H3O_lone_pair)],
            fadeout=[H3O_positive],
        )
        self.play(sulfone_mob.electron_migration(steps=[step_acidification],run_time=1.5))
        self.wait(1)

        #剩下的水（OH_2，连同 O 上的孤对电子）退场
        self.play(FadeOut(H3O_O_mob,H3O_lone_pair),run_time=1)
        sulfone_mob.remove(H3O_O_mob,H3O_lone_pair)
        sulfone_mob.charges.pop("O3",None)
        self.wait(2)

        #画面上的对象一起淡出
        self.play(*[FadeOut(mob) for mob in self.mobjects],run_time=1.5)
