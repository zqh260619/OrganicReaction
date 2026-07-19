#manim {SubstitutionReaction1.py} [SceneName] [-p]/*预览*/ [-qk/-qh/-qm/-ql]/*分辨率(由高到低)*/
#manim SubstitutionReaction1.py test -pqh

from OrganicReactionTools import *

class test(Scene):
    def construct(self):

        text0=Text("一些常见的取代反应机理",color=WHITE,font_size=title_size)
        self.play(Write(text0))
        self.wait(1.5)
        self.play(FadeOut(text0))

        #-----------------------SN2 reaction-----------------------

        SN2_reaction=MathTex(r"S_N2\text{（双分子亲核取代）}",color=WHITE,font_size=title_size,tex_template=mytemplate)
        SN2_reaction.move_to([0,title_height,0])
        self.play(Write(SN2_reaction))
        self.wait(0.5)

        #bond1  C1-H1
        angle1=120*DEGREES
        end_point1=[(length-edge)*np.cos(angle1),(length-edge)*np.sin(angle1),0]
        bond1=Line(color=WHITE,start=[0,0,0],end=end_point1)
        #bond2  C1-Br1
        end_point2=[length-edge,0,0]
        bond2=Line(color=WHITE,start=[0,0,0],end=end_point2)
        #bond3  C1-H2
        angle3=-120*DEGREES
        bond3=OutBond(direction=angle3,length=length-edge)
        #bond4  C1-H3
        angle4=-150*DEGREES
        bond4=InBond(direction=angle4,length=length-edge)


        Br1=MathTex(r"Br",color=WHITE,font_size=txt_size)
        Br1.move_to([length,0,0])

        H1=MathTex(r"H",color=WHITE,font_size=txt_size)
        H1.move_to([length*np.cos(angle1),length*np.sin(angle1),0])

        H2=MathTex(r"H",color=WHITE,font_size=txt_size)
        H2.move_to([length*np.cos(angle3),length*np.sin(angle3),0])

        H3=MathTex(r"H",color=WHITE,font_size=txt_size)
        H3.move_to([length*np.cos(angle4),length*np.sin(angle4),0])

        self.play(Create(bond1),
                  Create(bond2),
                  Create(bond3),
                  Create(bond4),
                  Write(Br1),
                  Write(H1),
                  Write(H2),
                  Write(H3))
        self.wait(1)

        OH1=MathTex(r"HO",color=WHITE,font_size=txt_size)
        OH1.move_to([-2*length,0,0])
        OH1_negative=NegativeCharge(text=OH1,pos=UR,edge=default_charge_edge)

        self.play(Create(OH1),Create(OH1_negative))

        self.wait(1)

        #dashedbond5    C1-Br1
        dashedbond5=DashedLine(color=WHITE,
                               start=[0,0,0],
                               end=[length*ratio_transition_state-edge,0,0],
                               dash_length=0.1)
        #-------DEFAULT_DASH_LENGTH=0.05--------#

        #dashedbond6    C1-OH1
        dashedbond6=DashedLine(color=WHITE,
                               start=[0,0,0],
                               end=[-length*ratio_transition_state+edge,0,0],
                               dash_length=0.1)

        #H1_path_1
        H1_path_1=Arc(radius=1,start_angle=120*DEGREES,angle=-30*DEGREES,arc_center=ORIGIN)

        #H2_path_1
        H2_path_1=Arc(radius=1,start_angle=-120*DEGREES,angle=45*DEGREES,arc_center=ORIGIN)

        #H3_path_1
        H3_path_1=Arc(radius=1,start_angle=-150*DEGREES,angle=45*DEGREES,arc_center=ORIGIN)

        #bracket for transition state
        transition_bracket=VGroup(BracketBetweenPoints(start=[-1.8,1.3,0],end=[-1.8,-1.3,0],
                                                     color=WHITE),
                                  BracketBetweenPoints(start=[1.8,-1.3,0],end=[1.8,1.3,0],
                                                     color=WHITE))

        #ddagger for transition state
        ddagger=MathTex(r"\ddagger",color=WHITE,font_size=txt_size)
        ddagger.move_to([1.9,1.35,0])

        #delta negative charge for OH1
        delta_negative_OH1=MathTex(r"\delta^-",color=WHITE,font_size=txt_size*0.9)
        delta_negative_OH1.move_to([-ratio_transition_state*length,0.35,0])

        #delta negative charge for Br1
        delta_negative_Br1=MathTex(r"\delta^-",color=WHITE,font_size=txt_size*0.9)
        delta_negative_Br1.move_to([ratio_transition_state*length,0.35,0])

        self.play(ReplacementTransform(bond2.copy(),dashedbond5),
                  ReplacementTransform(bond2,delta_negative_Br1),
                  Br1.animate.shift([(ratio_transition_state-1)*length,0,0]),
                  ReplacementTransform(OH1_negative.copy(),dashedbond6),
                  ReplacementTransform(OH1_negative,delta_negative_OH1),
                  OH1.animate.shift([(1.9-ratio_transition_state)*length,0,0]),
                  bond1.animate.rotate(about_point=ORIGIN,angle=-30*DEGREES),
                  MoveAlongPath(H1,H1_path_1),
                  bond3.animate.rotate(about_point=ORIGIN,angle=45*DEGREES),
                  MoveAlongPath(H2,H2_path_1),
                  bond4.animate.rotate(about_point=ORIGIN,angle=45*DEGREES),
                  MoveAlongPath(H3,H3_path_1),
                  AnimationGroup(*[Create(x) for x in transition_bracket],lag_ratio=0),
                  Create(ddagger))

        self.wait(0.5)

        #bond7 C1-OH1
        end_point7=[-length+edge,0,0]
        bond7=Line(color=WHITE,start=[0,0,0],end=end_point7)

        Br1_temp=Br1.copy()
        Br1_temp.shift([(2-ratio_transition_state)*length,0,0])
        Br1_negative=NegativeCharge(text=Br1_temp,pos=UL,edge=default_charge_edge)

        #H1_path_2
        H1_path_2=Arc(radius=1,start_angle=90*DEGREES,angle=-30*DEGREES,arc_center=ORIGIN)

        #H2_path_2
        H2_path_2=Arc(radius=1,start_angle=-75*DEGREES,angle=15*DEGREES,arc_center=ORIGIN)

        #H3_path_2
        H3_path_2=Arc(radius=1,start_angle=-105*DEGREES,angle=75*DEGREES,arc_center=ORIGIN)

        self.play(OH1.animate.shift([(ratio_transition_state-1)*length,0,0]),
                  ReplacementTransform(dashedbond6,bond7),
                  ReplacementTransform(delta_negative_OH1,bond7),
                  Br1.animate.shift([(2-ratio_transition_state)*length,0,0]),
                  ReplacementTransform(dashedbond5,Br1_negative),
                  ReplacementTransform(delta_negative_Br1,Br1_negative),
                  FadeOut(transition_bracket),
                  FadeOut(ddagger),
                  bond1.animate.rotate(about_point=ORIGIN,angle=-30*DEGREES),
                  MoveAlongPath(H1,H1_path_2),
                  bond3.animate.rotate(about_point=ORIGIN,angle=15*DEGREES),
                  MoveAlongPath(H2,H2_path_2),
                  bond4.animate.rotate(about_point=ORIGIN,angle=75*DEGREES),
                  MoveAlongPath(H3,H3_path_2))

        #text
        text1=Text("产物全部构型翻转",color=WHITE,font_size=txt_size)
        text1.move_to([0,description_height,0])
        self.play(Write(text1))

        self.wait(1)

        self.play(FadeOut(bond1),
                  FadeOut(bond3),
                  FadeOut(bond4),
                  FadeOut(bond7),
                  FadeOut(H1),
                  FadeOut(H2),
                  FadeOut(H3),
                  FadeOut(Br1),
                  FadeOut(OH1),
                  FadeOut(Br1_negative),
                  FadeOut(SN2_reaction),
                  FadeOut(text1))

        self.wait(1.5)

        #-----------------------SN1 reaction-----------------------

        SN1_reaction=MathTex(r"S_N1\text{（单分子亲核取代）}",color=WHITE,font_size=title_size,tex_template=mytemplate)
        SN1_reaction.move_to([0,title_height,0])
        self.play(Write(SN1_reaction))
        self.wait(0.5)

        #bond8  C2-R1
        angle8=120*DEGREES
        end_point8=[(length-edge)*np.cos(angle8),(length-edge)*np.sin(angle8),0]
        bond8=Line(color=WHITE,start=[0,0,0],end=end_point8)

        #bond9  C2-X1
        end_point9=[length-edge,0,0]
        bond9=Line(color=WHITE,start=[0,0,0],end=end_point9)

        #bond10 C2-R2
        angle10=-120*DEGREES
        bond10=OutBond(direction=angle10,length=length-edge)

        #bond11 C2-R3
        angle11=-150*DEGREES
        bond11=InBond(direction=angle11,length=length-edge)

        R1=MathTex(r"R_1",color=WHITE,font_size=txt_size)
        R1.move_to([length*np.cos(angle8),length*np.sin(angle8),0])

        X1=MathTex(r"X",color=WHITE,font_size=txt_size)
        X1.move_to([length,0,0])

        R2=MathTex(r"R_2",color=WHITE,font_size=txt_size)
        R2.move_to([length*np.cos(angle10),length*np.sin(angle10),0])

        R3=MathTex(r"R_3",color=WHITE,font_size=txt_size)
        R3.move_to([length*np.cos(angle11),length*np.sin(angle11),0])

        self.play(Create(bond8),
                  Create(bond9),
                  Create(bond10),
                  Create(bond11),
                  Write(R1),
                  Write(X1),
                  Write(R2),
                  Write(R3))

        self.wait(1)

        #X1_negative
        X1_negative=NegativeCharge(text=X1,pos=UL,edge=default_charge_edge)
        X1_negative.shift([length,0,0])

        #C2_positive
        C2_positive=PositiveChargeByCoordinate(position=[0.2,0.2,0])

        #R1_path_1
        R1_path_1=Arc(radius=1,start_angle=120*DEGREES,angle=-30*DEGREES,arc_center=ORIGIN)

        #R2_path_1
        R2_path_1=Arc(radius=1,start_angle=-120*DEGREES,angle=45*DEGREES,arc_center=ORIGIN)

        #R3_path_1
        R3_path_1=Arc(radius=1,start_angle=-150*DEGREES,angle=45*DEGREES,arc_center=ORIGIN)

        self.play(X1.animate.shift([length,0,0]),
                  Create(C2_positive),
                  ReplacementTransform(bond9,X1_negative),
                  MoveAlongPath(R1,R1_path_1),
                  MoveAlongPath(R2,R2_path_1),
                  MoveAlongPath(R3,R3_path_1),
                  bond8.animate.rotate(about_point=ORIGIN,angle=-30*DEGREES),
                  bond10.animate.rotate(about_point=ORIGIN,angle=45*DEGREES),
                  bond11.animate.rotate(about_point=ORIGIN,angle=45*DEGREES))

        self.wait(1)

        self.play(FadeOut(X1),
                  FadeOut(X1_negative))

        #bond8_copy
        bond8_copy=bond8.copy()

        #bond10_copy
        bond10_copy=bond10.copy()

        #bond11_copy
        bond11_copy=bond11.copy()

        R1_copy=R1.copy()
        R2_copy=R2.copy()
        R3_copy=R3.copy()

        C2_positive_copy=C2_positive.copy()

        self.play(bond8.animate.shift([2,0,0]),
                  bond10.animate.shift([2,0,0]),
                  bond11.animate.shift([2,0,0]),
                  R1.animate.shift([2,0,0]),
                  R2.animate.shift([2,0,0]),
                  R3.animate.shift([2,0,0]),
                  C2_positive.animate.shift([2,0,0]),
                  bond8_copy.animate.shift([-2,0,0]),
                  bond10_copy.animate.shift([-2,0,0]),
                  bond11_copy.animate.shift([-2,0,0]),
                  R1_copy.animate.shift([-2,0,0]),
                  R2_copy.animate.shift([-2,0,0]),
                  R3_copy.animate.shift([-2,0,0]),
                  C2_positive_copy.animate.shift([-2,0,0]))
         
        self.wait(1)

        #Nu1
        Nu1=MathTex(r"Nu",color=WHITE,font_size=txt_size)
        Nu1.move_to([2+2*length,0,0])
        Nu1_negative=NegativeCharge(text=Nu1,pos=UL,edge=default_charge_edge)

        #Nu1_copy
        Nu1_copy=MathTex(r"Nu",color=WHITE,font_size=txt_size)
        Nu1_copy.move_to([-2-2*length,0,0])
        Nu1_negative_copy=NegativeCharge(text=Nu1_copy,pos=UR,edge=default_charge_edge)

        self.play(Write(Nu1),
                  Create(Nu1_negative),
                  Write(Nu1_copy),
                  Create(Nu1_negative_copy))

        self.wait(1)

        #bond12 C2-Nu1
        bond12=Line(color=WHITE,start=[2,0,0],end=[2+length-edge,0,0])

        #bond12_copy C2_copy-Nu1_copy
        bond12_copy=Line(color=WHITE,start=[-2,0,0],end=[-2-length+edge,0,0])

        #R1_path_2
        R1_path_2=Arc(radius=1,start_angle=90*DEGREES,angle=30*DEGREES,arc_center=[2,0,0])

        #R2_path_2
        R2_path_2=Arc(radius=1,start_angle=-75*DEGREES,angle=-30*DEGREES,arc_center=[2,0,0])

        #R3_path_2
        R3_path_2=Arc(radius=1,start_angle=-105*DEGREES,angle=-30*DEGREES,arc_center=[2,0,0])

        #R1_copy_path_2
        R1_copy_path_2=Arc(radius=1,start_angle=90*DEGREES,angle=-30*DEGREES,arc_center=[-2,0,0])

        #R2_copy_path_2
        R2_copy_path_2=Arc(radius=1,start_angle=-75*DEGREES,angle=15*DEGREES,arc_center=[-2,0,0])

        #R3_copy_path_2
        R3_copy_path_2=Arc(radius=1,start_angle=-105*DEGREES,angle=75*DEGREES,arc_center=[-2,0,0])

        self.play(FadeOut(C2_positive),
                  ReplacementTransform(Nu1_negative,bond12),
                  Nu1.animate.shift([-length,0,0]),
                  FadeOut(C2_positive_copy),
                  ReplacementTransform(Nu1_negative_copy,bond12_copy),
                  Nu1_copy.animate.shift([length,0,0]),
                  MoveAlongPath(R1,R1_path_2),
                  MoveAlongPath(R2,R2_path_2),
                  MoveAlongPath(R3,R3_path_2),
                  MoveAlongPath(R1_copy,R1_copy_path_2),
                  MoveAlongPath(R2_copy,R2_copy_path_2),
                  MoveAlongPath(R3_copy,R3_copy_path_2),
                  bond8.animate.rotate(about_point=[2,0,0],angle=30*DEGREES),
                  bond10.animate.rotate(about_point=[2,0,0],angle=-30*DEGREES),
                  bond11.animate.rotate(about_point=[2,0,0],angle=-30*DEGREES),
                  bond8_copy.animate.rotate(about_point=[-2,0,0],angle=-30*DEGREES),
                  bond10_copy.animate.rotate(about_point=[-2,0,0],angle=15*DEGREES),
                  bond11_copy.animate.rotate(about_point=[-2,0,0],angle=75*DEGREES))

        #text
        text2=Text("两边进攻的机会相等",color=WHITE,font_size=txt_size)
        text2.move_to([0,description_height,0])

        #text
        text3=Text("产物完全外消旋化",color=WHITE,font_size=txt_size)
        text3.move_to([0,description_height,0])
        self.play(Write(text2))
        self.wait(0.5)
        self.play(ReplacementTransform(text2,text3))

        self.wait(1.5)

        self.play(FadeOut(bond8),
                  FadeOut(bond10),
                  FadeOut(bond11),
                  FadeOut(bond12),
                  FadeOut(R1),
                  FadeOut(R2),
                  FadeOut(R3),
                  FadeOut(Nu1),
                  FadeOut(Nu1_negative),
                  FadeOut(bond8_copy),
                  FadeOut(bond10_copy),
                  FadeOut(bond11_copy),
                  FadeOut(bond12_copy),
                  FadeOut(R1_copy),
                  FadeOut(R2_copy),
                  FadeOut(R3_copy),
                  FadeOut(Nu1_copy),
                  FadeOut(Nu1_negative_copy),
                  FadeOut(SN1_reaction),
                  FadeOut(text3))

        #-----------------------Ion pair reaction-----------------------

        
        self.wait(0.5)

        #text
        text3=MathTex(r"\text{然而绝大多}sp^3C\text{上的亲核取代反应并不是完全的}S_N1\text{或}S_N2",
                      color=WHITE,font_size=txt_size,tex_template=mytemplate)
        text3.move_to([0,0,0])
        text4=MathTex(r"\text{以}\alpha-\text{甲基苄氯水解为例（40\%水-丙酮）}",
                      color=WHITE,font_size=txt_size,tex_template=mytemplate)
        text4.move_to([0,0,0])
        text5=MathTex(r"&\text{产物95\%外消旋化，}\\&\text{既不是完全构型翻转，也不是完全外消旋化}",
                      color=WHITE,font_size=txt_size,tex_template=mytemplate)
        text5.move_to([0,0,0])
        text6=MathTex(r"\text{因此机理介于}S_N1\text{和}S_N2\text{之间}",
                      color=WHITE,font_size=txt_size,tex_template=mytemplate)
        text6.move_to([0,0,0])

        self.play(Write(text3))
        self.wait(2)

        self.play(ReplacementTransform(text3,text4))
        self.wait(2)

        self.play(ReplacementTransform(text4,text5))
        self.wait(3)

        self.play(ReplacementTransform(text5,text6))
        self.wait(2)

        self.play(FadeOut(text6))
        
        Ion_pair_reaction=MathTex(r"\text{离子对机理}",color=WHITE,font_size=title_size,tex_template=mytemplate)
        Ion_pair_reaction.move_to([0,title_height,0])
        self.play(Write(Ion_pair_reaction))

        self.wait(0.5)

        #bond13  C3-R4
        angle13=120*DEGREES
        end_point13=[(length-edge)*np.cos(angle13),(length-edge)*np.sin(angle13),0]
        bond13=Line(color=WHITE,start=[0,0,0],end=end_point13)

        #bond14  C3-X2
        end_point14=[length-edge,0,0]
        bond14=Line(color=WHITE,start=[0,0,0],end=end_point14)

        #bond15 C3-R5
        angle15=-120*DEGREES
        bond15=OutBond(direction=angle15,length=length-edge)

        #bond16 C3-R6
        angle16=-150*DEGREES
        bond16=InBond(direction=angle16,length=length-edge)

        R4=MathTex(r"R_1",color=WHITE,font_size=txt_size)
        R4.move_to([length*np.cos(angle13),length*np.sin(angle13),0])

        X2=MathTex(r"X",color=WHITE,font_size=txt_size)
        X2.move_to([length,0,0])

        R5=MathTex(r"R_2",color=WHITE,font_size=txt_size)
        R5.move_to([length*np.cos(angle15),length*np.sin(angle15),0])

        R6=MathTex(r"(H)R_3",color=WHITE,font_size=txt_size)
        R6.move_to([length*np.cos(angle16)-0.25,length*np.sin(angle16),0])

        self.play(Create(bond13),
                  Create(bond14),
                  Create(bond15),
                  Create(bond16),
                  Create(R4),
                  Create(X2),
                  Create(R5),
                  Create(R6))

        self.wait(1)

        #X2_negative
        X2_negative=NegativeCharge(text=X2,pos=UL,edge=default_charge_edge)

        #C3_positive
        C3_postive=PositiveChargeByCoordinate(position=[0.2,0.2,0])

        #R4_path_1
        R4_path_1=Arc(radius=1,start_angle=120*DEGREES,angle=-30*DEGREES,arc_center=ORIGIN)

        #R5_path_1
        R5_path_1=Arc(radius=1,start_angle=-120*DEGREES,angle=45*DEGREES,arc_center=ORIGIN)

        #R6_path_1
        R6_path_1=Arc(radius=1,start_angle=-150*DEGREES,angle=45*DEGREES,arc_center=[-0.25,0,0])

        #Nu2
        Nu2=MathTex(r"Nu",color=WHITE,font_size=txt_size)
        Nu2.move_to([0,2*length,0])

        #Nu2_negative
        Nu2_negative=NegativeCharge(text=Nu2,pos=UR,edge=default_charge_edge)

        self.play(FadeIn(C3_postive),
                  ReplacementTransform(bond14,X2_negative),
                  MoveAlongPath(R4,R4_path_1),
                  MoveAlongPath(R5,R5_path_1),
                  MoveAlongPath(R6,R6_path_1),
                  bond13.animate.rotate(about_point=[0,0,0],angle=-30*DEGREES),
                  bond15.animate.rotate(about_point=[0,0,0],angle=45*DEGREES),
                  bond16.animate.rotate(about_point=[0,0,0],angle=45*DEGREES))

        #S1
        S1=MathTex(r"S",color=0x77DDFF,font_size=txt_size)
        S1.move_to([1.7,1.1,0]).set_opacity(0.3)

        #S2
        S2=MathTex(r"S",color=0x77DDFF,font_size=txt_size)
        S2.move_to([-0.5,-1.3,0]).set_opacity(0.3)

        #S3
        S3=MathTex(r"S",color=0x77DDFF,font_size=txt_size)
        S3.move_to([-1.3,-0.9,0]).set_opacity(0.3)

        #S4
        S4=MathTex(r"S",color=0x77DDFF,font_size=txt_size)
        S4.move_to([1.6,-0.7,0]).set_opacity(0.3)

        #S5
        S5=MathTex(r"S",color=0x77DDFF,font_size=txt_size)
        S5.move_to([-1.4,0.4,0]).set_opacity(0.3)

        #S6
        S6=MathTex(r"S",color=0x77DDFF,font_size=txt_size)
        S6.move_to([1.6,0.2,0]).set_opacity(0.3)

        #S7
        S7=MathTex(r"S",color=0x77DDFF,font_size=txt_size)
        S7.move_to([0.8,-2.0,0]).set_opacity(0.3)

        #S8
        S8=MathTex(r"S",color=0x77DDFF,font_size=txt_size)
        S8.move_to([0.7,1.0,0]).set_opacity(0.3)

        #S9
        S9=MathTex(r"S",color=0x77DDFF,font_size=txt_size)
        S9.move_to([-1.9,-0.7,0]).set_opacity(0.3)

        #S10
        S10=MathTex(r"S",color=0x77DDFF,font_size=txt_size)
        S10.move_to([-0.6,-1.7,0]).set_opacity(0.3)

        #S11
        S11=MathTex(r"S",color=0x77DDFF,font_size=txt_size)
        S11.move_to([-1.5,2.0,0]).set_opacity(0.3)

        #S12
        S12=MathTex(r"S",color=0x77DDFF,font_size=txt_size)
        S12.move_to([0.8,-0.6,0]).set_opacity(0.3)

        #S13
        S13=MathTex(r"S",color=0x77DDFF,font_size=txt_size)
        S13.move_to([-1.6,0.6,0]).set_opacity(0.3)

        #S14
        S14=MathTex(r"S",color=0x77DDFF,font_size=txt_size)
        S14.move_to([1.4,-1.8,0]).set_opacity(0.3)

        #S15
        S15=MathTex(r"S",color=0x77DDFF,font_size=txt_size)
        S15.move_to([-0.4,0.7,0]).set_opacity(0.3)

        self.play(Write(Nu2),
                  Write(Nu2_negative),
                  Write(S1),
                  Write(S2),
                  Write(S3),
                  Write(S4),
                  Write(S5),
                  Write(S6),
                  Write(S7),
                  Write(S8),
                  Write(S9),
                  Write(S10),
                  Write(S11),
                  Write(S12),
                  Write(S13),
                  Write(S14),
                  Write(S15))

        self.wait(1)

        #pionts of bezier arrow for Nu2
        start1=np.array([0.3,2.0,0])
        start_handle_1=np.array([1.0,1.5,0])
        end1=np.array([0.4,0.1,0])
        end_handle_1=np.array([1.2,0.7,0])
        start2=np.array([-0.3,2.0,0])
        start_handle_2=np.array([-1.0,1.5,0])
        end2=np.array([-0.4,0.1,0])
        end_handle_2=np.array([-1.2,0.7,0])

        #arrow1 & 2
        arrow1=BezierArrow(start_anchor=start1,
                           start_handle=start_handle_1,
                           end_handle=end_handle_1,
                           end_anchor=end1,
                           color=WHITE,
                           stroke_width=2,
                           arrow_size=0.3,
                           opacity=0.1)
        arrow2=BezierArrow(start_anchor=start2,
                           start_handle=start_handle_2,
                           end_handle=end_handle_2,
                           end_anchor=end2,
                           color=WHITE,
                           stroke_width=2,
                           arrow_size=0.3,
                           opacity=0.9)
        arrow2.set_stroke(opacity=0.9)

        #text
        text7=MathTex(r"\text{左侧进攻}",
                      color=WHITE,font_size=txt_size/2,tex_template=mytemplate)
        text7.move_to([-1.3,1.5,0])
        text8=MathTex(r"\text{右侧进攻}",
                      color=WHITE,font_size=txt_size/2,tex_template=mytemplate)
        text8.move_to([1.3,1.5,0])
        text9=MathTex(r"S\text{代表溶剂分子}",
                      color=WHITE,font_size=txt_size,tex_template=mytemplate)
        text9.move_to([0,description_height,0])
        
        self.play(Create(arrow1),
                  Create(arrow2),
                  Write(text7),
                  Write(text8),
                  Write(text9))

        self.wait(1)

        #animation of Solvent molecules
        Solvent_anim=brownian_motion([S1,S2,S3,S4,S5,S6,S7,S8,S9,S10,S11,S12,S13,S14,S15],8,9.0)

        #animation of X2
        X2_anim=ApplyMethod(X2.shift,[5,0,0],rate_func=smoothstep,run_time=9.0)
        X2_negative_anim=ApplyMethod(X2_negative.shift,[5,0,0],rate_func=smoothstep,run_time=9.0)

        #text
        text10=MathTex(r"\text{一开始两个离子紧密贴合在一起，形成紧密离子对}",
                       color=WHITE,font_size=txt_size,tex_template=mytemplate)
        text10.move_to([0,description_height,0])
        text11=MathTex(r"\text{左侧位阻小，易进攻；右侧位阻大，难进攻}",
                       color=WHITE,font_size=txt_size,tex_template=mytemplate)
        text11.move_to([0,description_height,0])
        text12=MathTex(r"\text{溶剂介入，离子对解离}",
                       color=WHITE,font_size=txt_size,tex_template=mytemplate)
        text12.move_to([0,description_height,0])
        text13=MathTex(r"\text{空间位阻解除，两侧进攻概率趋于等同}",
                       color=WHITE,font_size=txt_size,tex_template=mytemplate)
        text13.move_to([0,description_height,0]) 

        anims=merging_timeline(Solvent_anim,{
            0:[X2_anim,
               X2_negative_anim,
               Transform(text9, text10),
               OpacityEffect(mobject=arrow1,initial_opacity=0.1,final_opacity=0.5,run_time=9.0,func=linear),
               OpacityEffect(mobject=arrow2,initial_opacity=0.9,final_opacity=0.5,run_time=9.0,func=linear)],
            3:[FadeOut(text9,run_time=0),Transform(text10, text11)],
            6:[FadeOut(text10,run_time=0),Transform(text11, text12)],
            8:[FadeOut(text11,run_time=0),Transform(text12,text13)]
        })
        
        play_timeline(self,anims)

        self.wait(2)
