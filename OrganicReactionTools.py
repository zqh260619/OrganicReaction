from os import wait

from manim import *
from manim.typing import Vector3D
import numpy as np
from typing import Iterable, Union

mytemplate = TexTemplate()
mytemplate.add_to_preamble(r"\usepackage{ctex}")

#parameters
length=1
"""键长"""
edge=0.25
"""键边距"""
txt_size=35
"""文字大小"""
title_size=60
"""标题大小"""
ratio_transition_state=1.2
"""过渡态键长比例"""
title_height=3
"""标题高度"""
description_height=-2
"""描述性文本高度"""
default_charge_edge=0.07
"""默认电荷边距"""


class OutBond(Polygon):
    def __init__(self,*,start_point=ORIGIN,direction=0.0,length=1.0,
                 base_ratio=0.2,color=WHITE):

        """

        direction: angle in radians

        """
        
        end_point=start_point+length*np.array([np.cos(direction),np.sin(direction),0])
        
        vertices=[start_point,
                  end_point + base_ratio*length/2 * np.array(
                      [-np.sin(direction), np.cos(direction), 0]),
                  end_point - base_ratio*length/2 * np.array(
                      [-np.sin(direction), np.cos(direction), 0]),]

        super().__init__(
            *vertices,
            color=color,
            fill_opacity=1,
            stroke_width=0
        )
        

class InBond(VGroup):
    def __init__(self,*,start_point=ORIGIN,direction=0.0,length=1.0,base_ratio=0.2,
                 color=WHITE,num=5):
        
        """

        <length> means the length from start(including edge) to end(excluding edge)

        """

        end_point=start_point+length*np.array([np.cos(direction),np.sin(direction),0])
        end_point_1=end_point+base_ratio*length/2*np.array(
            [-np.sin(direction),np.cos(direction),0])
        end_point_2=end_point-base_ratio*length/2*np.array(
            [-np.sin(direction),np.cos(direction),0])

        lines=[]
        for i in range(1,num+1):
            start_point_temp=end_point_1*i/num+start_point*(num-i)/num
            end_point_temp=end_point_2*i/num+start_point*(num-i)/num
            temp=Line(start=start_point_temp,end=end_point_temp,color=color,stroke_width=2)
            lines.append(temp)

        super().__init__(*lines)

class NegativeCharge(VGroup):
    def __init__(self,*,color=WHITE,text:MathTex,radius=0.05,
                 ratio=0.6,stroke_width=1.2,pos:Vector3D,edge:float):

        position=text.get_corner(pos)+pos*edge

        circle=Circle(radius=radius,color=color,arc_center=position,
                      stroke_width=stroke_width)

        line_start=[position[0]-radius*ratio,position[1],position[2]]
        line_end=[position[0]+radius*ratio,position[1],position[2]]
        line=Line(start=line_start,end=line_end,color=color,stroke_width=stroke_width)

        super().__init__(circle,line)

class PositiveCharge(VGroup):
    def __init__(self,*,color=WHITE,text:MathTex,radius=0.05,
                 ratio=0.6,stroke_width=1.2,pos:Vector3D,edge:float):

        position=text.get_corner(pos)+pos*edge

        circle=Circle(radius=radius,color=color,arc_center=position,
                      stroke_width=stroke_width)

        line1_start=[position[0]-radius*ratio,position[1],position[2]]
        line1_end=[position[0]+radius*ratio,position[1],position[2]]
        line1=Line(start=line1_start,end=line1_end,color=color,stroke_width=stroke_width)

        line2_start=[position[0],position[1]-radius*ratio,position[2]]
        line2_end=[position[0],position[1]+radius*ratio,position[2]]
        line2=Line(start=line2_start,end=line2_end,color=color,stroke_width=stroke_width)

        super().__init__(circle,line1,line2)

class NegativeChargeByCoordinate(VGroup):
    def __init__(self,*,color=WHITE,radius=0.05,
                 ratio=0.6,stroke_width=1.2,position:Vector3D):

        circle=Circle(radius=radius,color=color,arc_center=position,
                      stroke_width=stroke_width)

        line_start=[position[0]-radius*ratio,position[1],position[2]]
        line_end=[position[0]+radius*ratio,position[1],position[2]]
        line=Line(start=line_start,end=line_end,color=color,stroke_width=stroke_width)

        super().__init__(circle,line)

class PositiveChargeByCoordinate(VGroup):
    def __init__(self,*,color=WHITE,radius=0.05,
                 ratio=0.6,stroke_width=1.2,position:Vector3D):

        circle=Circle(radius=radius,color=color,arc_center=position,
                      stroke_width=stroke_width)

        line1_start=[position[0]-radius*ratio,position[1],position[2]]
        line1_end=[position[0]+radius*ratio,position[1],position[2]]
        line1=Line(start=line1_start,end=line1_end,color=color,stroke_width=stroke_width)

        line2_start=[position[0],position[1]-radius*ratio,position[2]]
        line2_end=[position[0],position[1]+radius*ratio,position[2]]
        line2=Line(start=line2_start,end=line2_end,color=color,stroke_width=stroke_width)

        super().__init__(circle,line1,line2)

class BracketBetweenPoints(VGroup):
    def __init__(self,*,start=ORIGIN,end=ORIGIN,ratio_edge=0.1,**kwargs):

        """
        According to the left bracket
        the upper end is the starting point
        the lower end is the ending point
        """

        direction=[x-y for x,y in zip(end,start)]
        direction/=np.sqrt(direction[0]**2+direction[1]**2)
        edge_direction=[-direction[1],direction[0],0]

        main=Line(start=start,end=end,**kwargs)

        end1=[x+y*ratio_edge for x,y in zip(start,edge_direction)]
        edge_start=Line(start=start,end=end1,**kwargs)

        end2=[x+y*ratio_edge for x,y in zip(end,edge_direction)]
        edge_end=Line(start=end,end=end2,**kwargs)

        super().__init__(edge_start,main,edge_end)

def play_timeline(scene:Scene,timeline:dict[float,Union[Iterable[Animation],Animation]]):
    pretime=0
    ending=0
    for time,animation in sorted(timeline.items()):
        to_wait=time-pretime
        if to_wait>0:
            scene.wait(to_wait)
        pretime=time
        if not isinstance(animation,Iterable):
            animation=[animation]
        for anim in animation:
            turn_animation_into_updater(anim)
            scene.add(anim.mobject)
            ending=max(ending,anim.run_time+time)
    if ending>pretime:
        wait(ending-pretime)
