#manim {VideoCover.py} [SceneName] [-s]/*只保存最后一帧，即封面图*/ [-qk/-qh/-qm/-ql]/*分辨率(由高到低)*/
#manim VideoCover.py CollectionCover -sqh

"""生成 B 站视频合集封面（1920×1080）。

每个封面一个独立场景类，场景名即封面名，不要把不同封面塞进同一个类。
本场景（合集「有机化学机理动画」的总封面）：纯黑底，白色 LaTeX 文本与白色线框为主体，
只少量用彩色（青=电子流，琥珀=亲电试剂）。左上为两行大标题，右下为竖直苯环 + 推电子弯箭头指向 E⁺。
场景不含动画，只摆好一帧画面，封面图由 -s 保存最后一帧得到：
media/images/VideoCover/ 下的 CollectionCover_*.png
"""

from OrganicReactionTools import *

#封面固定为 1920×1080（-qh 也是该分辨率；这里显式声明，换质量档位后输出尺寸也不变）
config.pixel_width=1920
config.pixel_height=1080

class CollectionCover(Scene):
    def construct(self):

        #-----------------------配色-----------------------
        color_electrons=ManimColor("#3ad6ff")#电子流：第二行标题、强调条、推电子箭头
        color_electrophile=ManimColor("#ffc65c")#亲电试剂：E 与它的正电荷

        #-----------------------左侧标题-----------------------
        left=-6.45

        title1=Title(text=r"\text{有机化学}",pos=[0,2.53,0],color=WHITE,size=160)
        title1.move_to([left+title1.width/2,2.53,0])

        title2=Title(text=r"\text{机理动画}",pos=[0,0.61,0],color=color_electrons,size=160)
        title2.move_to([left+title2.width/2,0.61,0])

        bar=RoundedRectangle(corner_radius=0.06,width=2.8,height=0.13,color=color_electrons,fill_opacity=1,stroke_width=0)
        bar.move_to([left+bar.width/2,-0.87,0])

        #-----------------------右侧机理图示-----------------------
        ring_center=[4.00,-1.45,0]

        #竖直苯环（尖顶朝上）：苯环立起来后更窄更高，右侧留白更匀
        #参与进攻的 π 键取 C1=C2 这条右上边，箭头从它的中点朝环外推出去
        ring=Benzene(center=ring_center,first_c_angle=90*DEGREES,length_global=1.90,color=WHITE)
        ring.set_stroke(width=7.5)

        c1=ring.atomic_clusters["C1"]["pos"]
        c2=ring.atomic_clusters["C2"]["pos"]
        bond_mid=(c1+c2)/2

        #亲电试剂 E⁺：E 用结构式承载，正电荷用 API 的电荷类挂在 E 的右上角
        electrophile=StructuralFormula(name="E1",pos=[5.85,1.35,0],text=r"\mathrm{E}",font_size=88,color=color_electrophile,
                                       radius_positive=0.14,ratio_positive=0.65,stroke_width_positive=3.2,
                                       edge_charge=0.10)
        electrophile.add_charge(text="E1",pos=UR,charge_type=ChargeType.POSITIVE)

        #推电子弯箭头：起点落在环右上边（C1=C2 这个 π 键）的中点，越过环外指向 E⁺
        arrow=BezierArrow(start_anchor=bond_mid,start_handle=[5.12,0.72,0],
                          end_anchor=[5.40,1.05,0],end_handle=[4.82,0.66,0],
                          color=color_electrons,stroke_width=8,arrow_size=0.5)

        self.add(title1,title2,bar,ring,arrow,electrophile)
