#manim SubstitutionReaction4.py test -pqh

from OrganicReactionTools import *

class test(Scene):
    def construct(self):
        
        title=Title(text=r"\text{一些常见的取代反应的机理}\quad\text{补}",pos=ORIGIN)
        subtitle=Subtitle(text=r"\text{芳环上的取代反应}",pos=[0,-0.7,0])
        self.play(Write(title),Write(subtitle))
        self.wait(1.5)
        self.play(FadeOut(title,subtitle))

        #SNAr反应式：亲核试剂Nu取代芳环上邻位于硝基的X，X以负离子形式离去
        #反应式整体缩到 0.8 倍，键线宽按同一比例调细（原来顶得太满、线条也太粗）
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
        #上下都不放对象的反应箭头：above 传空串只为通过「至少一侧有内容」的校验
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
        #Cross 按参照物的对角线画叉，直接套在细长箭头上会被压成扁叉，所以用一个不显示的小方框当参照物
        cross_frame=Square(side_length=0.6*scale_equation).move_to(reaction_arrow.arrow.get_center())
        refusal_cross=Cross(cross_frame,stroke_color=RED,stroke_width=6)

        self.play(ReplacementTransform(X_leaving_mob,H_mob),
                  FadeOut(product,plus2,X_negative),
                  Create(refusal_cross),
                  run_time=1.5)
        self.wait(2)

        #对原子表的修改放在播放之后，避免新标签在形变前闪现
        substrate.remove(X_leaving_mob)
        substrate.atomic_clusters["X"][Mobject]=H_mob
        substrate.add(H_mob)

        #这三个对象已在上面被 FadeOut 过，manim 收尾会把它们的透明度复原成 1；
        #从组里摘掉，否则最后整组淡出时它们会被重新加回场景而闪现
        reaction_group.remove(product,plus2,X_negative)

        #反应式与红叉一起退出
        self.play(FadeOut(reaction_group,refusal_cross),run_time=1)
        self.wait(0.5)

        #-----------------------VNS mechanism-----------------------

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
        #每个单词拆成“首字母 + 其余字母”两段（arg_separator="" 保持同一行排版），
        #只写其余字母，首字母不参与 Write，避免重复绘制产生边缘闪光
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

        #只写每个单词的其余字母（word[1]），首字母完全不参与 Write
        self.play(Write(words[0][1]),Write(words[1][1]),Write(words[2][1]),run_time=2)
        self.wait(2)

        #三个字母飞回标题位置（画面只保留 VNS），其余字母同时淡出
        self.play(V_letter.animate.move_to([-0.4164,3.0,0]),
                  N_letter.animate.move_to([0.0879,3.0,0]),
                  S_letter.animate.move_to([0.5043,3.0,0]),
                  FadeOut(words[0][1]),FadeOut(words[1][1]),FadeOut(words[2][1]),
                  run_time=1.5)
        self.wait(1.5)

        #氯甲基苯基砜：中心 C 不带标签，左上150°、右下330° 各连一个 H，正下方270° 连 Cl，右上30° 连 SO2Ph
        sulfone_mob=StructuralFormula(name="C1",pos=ORIGIN,text=None)
        sulfone_mob.add_atom(name="H1",direction=150*DEGREES,text=r"\mathrm{H}",
                             bond_type=BondType.NORMAL_BOND,adjacency="C1")
        sulfone_mob.add_atom(name="H2",direction=330*DEGREES,text=r"\mathrm{H}",
                             bond_type=BondType.NORMAL_BOND,adjacency="C1")
        sulfone_mob.add_atom(name="Cl1",direction=270*DEGREES,text=r"\mathrm{Cl}",
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
        C1_negative=sulfone_mob.build_charge(text="C1",pos=UL,charge_type=ChargeType.NEGATIVE_COORDINATE)

        step_ho_attack=ElectronMigrationStep(
            replace=[(HO_negative,HO_H1_bond),
                     (C1_H1_bond,C1_negative)],
        )
        self.play(sulfone_mob.electron_migration(steps=[step_ho_attack],run_time=1.5))
        self.wait(1)

        #生成H2O：HO-与那个H合并成一个水分子（碳负离子留在原处）
        H1_mob=sulfone_mob.atomic_clusters["H1"][Mobject]
        H2O_mob=AtomicCluster(text=r"\mathrm{H_2O}",pos=HO_pos+np.array([0.1,0.35,0]),attributes=sulfone_mob.attributes)
        self.play(ReplacementTransform(VGroup(HO_mob,H1_mob),H2O_mob),FadeOut(HO_H1_bond),run_time=1.5)
        #把这一段的残留对象从结构式里摘掉：它们已被就地变形、且 FadeOut 收尾会把透明度复原，
        #留在组里的话会在 H2O 淡出后随结构式重新画出来
        sulfone_mob.remove(HO_mob,H1_mob,HO_H1_bond)
        self.wait(2)

        #H2O 消失，碳负离子右移让出位置
        self.play(FadeOut(H2O_mob),run_time=1)
        sulfone_mob.remove(H2O_mob)
        self.wait(0.5)
        self.play(sulfone_mob.animate.shift(RIGHT*1.0),run_time=1.5)
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

        #硝基苯出现得慢一些：2.25 s 绘制 + 3 s 停留 = 5.25 s，约为原来（1.5+2）的 1.5 倍
        self.play(Create(nitrobenzene_mob),run_time=2.5)
        self.wait(2)

        #碳负离子进攻苯环：先让两只分子就位——碳负离子的碳 C1 落在硝基苯 C2 的右下30°、相距一个键长
        nitro_shift=RIGHT*0.58
        C1_live=np.array(sulfone_mob.bond_lookup.between("C1","H2").submobjects[0].get_start())
        C2_pos=np.array(nitrobenzene_mob.atomic_clusters["C2"]["pos"])+nitro_shift
        C1_target=C2_pos+np.array([np.cos(330*DEGREES),np.sin(330*DEGREES),0])

        self.play(nitrobenzene_mob.animate.shift(nitro_shift),
                  sulfone_mob.animate.shift(C1_target-C1_live),run_time=1.5)
        #位移后手动同步原子坐标数据（move/shift 不会更新 pos，后面建键要用）
        for atom_vns in nitrobenzene_mob.atomic_clusters.values():
            atom_vns["pos"]=np.array(atom_vns["pos"])+nitro_shift
        self.wait(1)

        #这一连串电子转移放在同一个转移动画里：
        #碳负离子的负电荷 → C-C 单键；环右上双键 → C-N 变双键；N=O 双键 → O 上变成负电荷
        cc_direction=np.arctan2(C2_pos[1]-C1_target[1],C2_pos[0]-C1_target[0])
        cc_bond=NormalBond(start=C1_target,direction=cc_direction,
                           start_edge=False,end_edge=False,attributes=sulfone_mob.attributes)

        C1_C2_double=nitrobenzene_mob.bond_lookup.between("C1","C2")
        C1_N1_single=nitrobenzene_mob.bond_lookup.between("C1","N1")
        N1_O2_double=nitrobenzene_mob.bond_lookup.between("N1","O2")

        C1_C2_single=nitrobenzene_mob.build_bond(start="C1",end="C2",bond_type=BondType.NORMAL_BOND)
        C1_N1_double=nitrobenzene_mob.build_bond(start="C1",end="N1",bond_type=BondType.DOUBLE_BOND,side=0)
        N1_O2_single=nitrobenzene_mob.build_bond(start="N1",end="O2",bond_type=BondType.NORMAL_BOND)
        O2_negative=nitrobenzene_mob.build_charge(text="O2",pos=UR,charge_type=ChargeType.NEGATIVE)

        step_attack=ElectronMigrationStep(
            replace=[(C1_negative,cc_bond),
                     (VGroup(C1_C2_double,C1_N1_single),VGroup(C1_C2_single,C1_N1_double)),
                     (N1_O2_double,VGroup(N1_O2_single,O2_negative))],
        )
        self.play(nitrobenzene_mob.electron_migration(steps=[step_attack],run_time=2.0))
        self.wait(2)
