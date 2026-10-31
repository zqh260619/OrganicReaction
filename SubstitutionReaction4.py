#manim SubstitutionReaction4.py test -pqh

from OrganicReactionTools import *

class test(Scene):
    def construct(self):
        
        title=Title(text=r"\text{一些不常见的取代反应的机理}\quad\text{补}",pos=ORIGIN)
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

        #标题用三个独立字母拼成（间距与整体排版的 VNS 一致），后面才能拆开并各自扩展成单词
        VNS_mechanism=VGroup(MathTex(r"\mathrm{V}",font_size=title_size,tex_template=mytemplate),
                             MathTex(r"\mathrm{N}",font_size=title_size,tex_template=mytemplate),
                             MathTex(r"\mathrm{S}",font_size=title_size,tex_template=mytemplate))
        VNS_mechanism.arrange(RIGHT,buff=0)
        title_buff=(MathTex(r"\mathrm{VNS}",font_size=title_size,tex_template=mytemplate).width-VNS_mechanism.width)/2
        VNS_mechanism.arrange(RIGHT,buff=title_buff).move_to(title_coordinate)
        V_letter,N_letter,S_letter=VNS_mechanism
        self.play(Write(VNS_mechanism))
        self.wait(0.5)

        #反应式淡出，标题保留
        self.play(FadeOut(reaction_group_vns),run_time=1)
        self.wait(0.5)

        #VNS拆成三个字母，移到画面纵向中心，再分别扩展成三个单词；
        #每个单词拆成“首字母 + 其余字母”两个子对象（arg_separator="" 保持同一行排版），
        #只写其余字母，首字母不参与 Write，避免重复绘制产生边缘闪光
        words=VGroup(MathTex(r"\mathrm{V}",r"\mathrm{icarious}",arg_separator="",font_size=title_size,tex_template=mytemplate),
                     MathTex(r"\mathrm{N}",r"\mathrm{ucleophilic}",arg_separator="",font_size=title_size,tex_template=mytemplate),
                     MathTex(r"\mathrm{S}",r"\mathrm{ubstitution}",arg_separator="",font_size=title_size,tex_template=mytemplate))

        #三个单词按基线对齐（不是包围盒中心：否则 "Nucleophilic" 因 p 的降部会整体上移）
        letters_vns=(V_letter,N_letter,S_letter)
        #单词间距取正常 LaTeX 词间距：同字号下“两词带空格整块宽 − 两词各自宽”= 墨迹间隙
        word_space=(MathTex(r"\mathrm{Vicarious}\ \mathrm{Nucleophilic}",font_size=title_size,tex_template=mytemplate).width
                    -words[0].width-words[1].width)
        words.arrange(RIGHT,buff=word_space)
        baseline_y=-float(np.mean([letter.height for letter in letters_vns]))/2
        for word in words:
            word.shift(UP*(baseline_y-word[0].get_bottom()[1]))
        words.shift(LEFT*float(np.mean([word.get_center()[0] for word in words])))

        #先把三个字母移到各自单词首字母的位置（word[0] 就是首字母子对象），三个字母因此落在同一水平线上
        self.play(V_letter.animate.move_to(words[0][0].get_center()),
                  N_letter.animate.move_to(words[1][0].get_center()),
                  S_letter.animate.move_to(words[2][0].get_center()),
                  run_time=1.5)
        self.wait(1)

        #字母已就位且不再移动：只写每个单词的其余字母（word[1]），首字母完全不参与 Write
        self.play(Write(words[0][1]),Write(words[1][1]),Write(words[2][1]),run_time=2)
        self.wait(2)
