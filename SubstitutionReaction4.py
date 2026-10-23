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
        substrate=Benzene(center=ORIGIN,c_names=["C1","C2","C3","C4","C5","C6"])
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

        product=Benzene(center=ORIGIN,c_names=["C1","C2","C3","C4","C5","C6"])
        product.add_atom(name="N1",direction=90*DEGREES,text=r"\mathrm{N}",
                         bond_type=BondType.NORMAL_BOND,adjacency="C1")
        product.add_atom(name="O1",direction=150*DEGREES,text=r"\mathrm{O}",
                         bond_type=BondType.NORMAL_BOND,adjacency="N1")
        product.add_atom(name="O2",direction=30*DEGREES,text=r"\mathrm{O}",
                         bond_type=BondType.DOUBLE_BOND,adjacency="N1",side=0)
        product.add_charge(text="N1",pos=LEFT,charge_type=ChargeType.POSITIVE)
        product.add_charge(text="O1",pos=UR,charge_type=ChargeType.NEGATIVE)
        product.add_atom(name="Nu",direction=30*DEGREES,text=r"\mathrm{Nu}",
                         bond_type=BondType.NORMAL_BOND,adjacency="C2")

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
        reaction_arrow=ReactionArrow(start=ORIGIN,above="",length=1.4)

        #横向排开：各对象只沿x平移，苯环中心与箭头始终在同一水平线上
        buff=0.35
        plus1.shift(RIGHT*(substrate.get_right()[0]+buff-plus1.get_left()[0]))
        Nu_negative.shift(RIGHT*(plus1.get_right()[0]+buff-Nu_negative.get_left()[0]))
        reaction_arrow.shift(RIGHT*(Nu_negative.get_right()[0]+buff-reaction_arrow.arrow.get_start()[0]))
        product.shift(RIGHT*(reaction_arrow.arrow.get_end()[0]+buff-product.get_left()[0]))
        plus2.shift(RIGHT*(product.get_right()[0]+buff-plus2.get_left()[0]))
        X_negative.shift(RIGHT*(plus2.get_right()[0]+buff-X_negative.get_left()[0]))
        reaction_group=VGroup(substrate,plus1,Nu_negative,reaction_arrow,product,plus2,X_negative)
        reaction_group.move_to(ORIGIN)

        self.play(FadeIn(reaction_group),run_time=1.5)
        self.wait(2)

        #X变形为H：没有可离去的基团，产物一侧消失，同时在箭头中间打上红叉表示反应无法直接进行
        X_leaving_mob=substrate.atomic_clusters["X"][Mobject]
        H_mob=AtomicCluster(text=r"\mathrm{H}",pos=X_leaving_mob.get_center(),
                            attributes=substrate.attributes)
        #Cross 按参照物的对角线画叉，直接套在细长箭头上会被压成扁叉，所以用一个不显示的小方框当参照物
        cross_frame=Square(side_length=0.6).move_to(reaction_arrow.arrow.get_center())
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

        #反应式与红叉一起退出
        self.play(FadeOut(reaction_group,refusal_cross),run_time=1)
        self.wait(0.5)

        #-----------------------VNS mechanism-----------------------

        VNS_mechanism=Title(text=r"\mathrm{VNS}\text{（间接芳香亲核取代）}")
        self.play(Write(VNS_mechanism))
        self.wait(0.5)
