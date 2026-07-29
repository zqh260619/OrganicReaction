from manim import *
from manim.typing import Vector3D
import numpy as np
from typing import Iterable,Union,Callable
from enum import Enum

mytemplate = TexTemplate()
mytemplate.add_to_preamble(r"\usepackage{ctex}")

RNG=np.random.default_rng(seed=3)

#PARAMETERS
#structures
bond_length=1
"""键长"""
edge=0.25
"""键边距"""
ratio_transition_state=1.2
"""过渡态键长比例"""
default_charge_edge=0.07
"""默认电荷边距"""
#texts
title_height=3
"""标题高度"""
title_coordinate=[0,title_height,0]
"""标题坐标"""
title_size=60
"""标题大小"""
subtitle_height=2.3
"""副标题高度"""
subtitle_coordinate=[0,subtitle_height,0]
"""副标题坐标"""
subtitle_size=30
"""副标题大小"""
description_height=-2
"""描述性文本高度"""
description_coordinate=[0,description_height,0]
"""描述性文本坐标"""
txt_size=35
"""文字大小"""

#Mobject classes
class OutBond(Polygon):
    def __init__(self,*,start:Vector3D,direction:float,start_edge=False,end_edge=False,attributes:'AttributeHolder'):

        start_point=start+start_edge*attributes.edge_global*np.array([np.cos(direction),np.sin(direction),0])
        end_point=start+(attributes.length_global-end_edge*attributes.edge_global)*np.array([np.cos(direction),np.sin(direction),0])
        
        vertices=[start_point,
                  end_point + attributes.base_ratio_outbond*(attributes.length_global-(start_edge+end_edge)*attributes.edge_global)/2 * np.array(
                      [-np.sin(direction), np.cos(direction), 0]),
                  end_point - attributes.base_ratio_outbond*(attributes.length_global-(start_edge+end_edge)*attributes.edge_global)/2 * np.array(
                      [-np.sin(direction), np.cos(direction), 0]),]

        super().__init__(
            *vertices,
            color=attributes.color,
            fill_opacity=1,
            stroke_width=0
        )

class InBond(VGroup):
    def __init__(self,*,start:Vector3D,direction:float,start_edge=False,end_edge=False,attributes:'AttributeHolder'):
        
        start_point=start+start_edge*attributes.edge_global*np.array([np.cos(direction),np.sin(direction),0])
        end_point=start+(attributes.length_global-end_edge*attributes.edge_global)*np.array([np.cos(direction),np.sin(direction),0])
        end_point_1=end_point+attributes.base_ratio_inbond*(attributes.length_global-(start_edge+end_edge)*attributes.edge_global)/2*np.array(
            [-np.sin(direction),np.cos(direction),0])
        end_point_2=end_point-attributes.base_ratio_inbond*(attributes.length_global-(start_edge+end_edge)*attributes.edge_global)/2*np.array(
            [-np.sin(direction),np.cos(direction),0])

        num=attributes.num_inbond
        lines=[]
        for i in range(1,num+1):
            start_point_temp=end_point_1*i/num+start_point*(num-i)/num
            end_point_temp=end_point_2*i/num+start_point*(num-i)/num
            temp=Line(start=start_point_temp,end=end_point_temp,color=attributes.color,stroke_width=2)
            lines.append(temp)

        super().__init__(*lines)

class DashedBond(DashedLine):
    def __init__(self,*,start:Vector3D,direction:float,start_edge=False,end_edge=False,attributes:'AttributeHolder'):

        start_point=start+np.array([np.cos(direction),np.sin(direction),0])*attributes.edge_global*start_edge
        end_point=start+np.array([np.cos(direction),np.sin(direction),0])*\
            (attributes.length_global*attributes.ratio_transition_state_dashedbond-attributes.edge_global*end_edge)
        super().__init__(color=attributes.color,start=start_point,end=end_point,
                       dash_length=attributes.dashed_length_dashedbond,
                       dashed_ratio=attributes.dashed_ratio_dashedbond)

class NormalBond(Line):
    def __init__(self,*,start:Vector3D,direction:float,start_edge=False,end_edge=False,attributes:'AttributeHolder'):

        start_point=start+np.array([np.cos(direction),np.sin(direction),0])*start_edge*attributes.edge_global
        end_point=start+np.array([np.cos(direction),np.sin(direction),0])*(attributes.length_global-end_edge*attributes.edge_global)
        super().__init__(start=start_point,end=end_point,color=attributes.color)

class DoubleBond(VGroup):
    def __init__(self,*,start:Vector3D,direction:float,start_edge=False,end_edge=False,attributes:'AttributeHolder',
                 side:int,start_side_edge:bool,end_side_edge:bool):

        """
        手平行于屏幕平面，手掌心向屏幕内侧，食指从start指向end，大拇指的方向为较短的键的位置。
        side=0时：双键左右对称，两侧一样长。
        side=1时：右手确定较短的键的位置。
        side=-1时：左手确定较短的键的位置。
        """

        super().__init__(color=attributes.color)

        direction_vector=np.array([np.cos(direction),np.sin(direction),0])
        normal_vector=np.array([-np.sin(direction),np.cos(direction),0])
        end=start+direction_vector*attributes.length_global

        if side==0:

            start1=start+direction_vector*start_edge*attributes.edge_global+0.5*normal_vector*attributes.length_global*attributes.edge_ratio_double
            start2=start+direction_vector*start_edge*attributes.edge_global-0.5*normal_vector*attributes.length_global*attributes.edge_ratio_double
            end1=end-direction_vector*end_edge*attributes.edge_global+0.5*normal_vector*attributes.length_global*attributes.edge_ratio_double
            end2=end-direction_vector*end_edge*attributes.edge_global-0.5*normal_vector*attributes.length_global*attributes.edge_ratio_double

        elif side==1:

            start1=start+direction_vector*start_edge*attributes.edge_global
            end1=end-direction_vector*end_edge*attributes.edge_global
            start2=start+direction_vector*(start_edge*attributes.edge_global+start_side_edge*attributes.edge_ratio_double)\
                +normal_vector*attributes.length_global*attributes.distance_double
            end2=end-direction_vector*(end_edge*attributes.edge_global+end_side_edge*attributes.edge_ratio_double)\
                +normal_vector*attributes.length_global*attributes.distance_double

        elif side==-1:

            start1=start+direction_vector*start_edge*attributes.edge_global
            end1=end-direction_vector*end_edge*attributes.edge_global
            start2=start+direction_vector*(start_edge*attributes.edge_global+start_side_edge*attributes.edge_ratio_double)\
                -normal_vector*attributes.length_global*attributes.distance_double
            end2=end-direction_vector*(end_edge*attributes.edge_global+end_side_edge*attributes.edge_ratio_double)\
                -normal_vector*attributes.length_global*attributes.distance_double

        bond1=Line(start=start1,end=end1,color=attributes.color)
        bond2=Line(start=start2,end=end2,color=attributes.color)

        self.add(bond1,bond2)

class TripleBond(VGroup):
    def __init__(self,*,start:Vector3D,direction:float,start_edge=False,end_edge=False,attributes:'AttributeHolder'):

        super().__init__(color=attributes.color)

        direction_vector=np.array([np.cos(direction),np.sin(direction),0])
        normal_vector=np.array([-np.sin(direction),np.cos(direction),0])
        end=start+direction_vector*attributes.length_global

        start1=start+direction_vector*start_edge*attributes.edge_global
        end1=end-direction_vector*end_edge*attributes.edge_global
        bond1=Line(start=start1,end=end1,color=attributes.color)

        start2=start+direction_vector*start_edge*attributes.edge_global-normal_vector*attributes.length_global*attributes.distance_triple
        end2=end-direction_vector*end_edge*attributes.edge_global-normal_vector*attributes.length_global*attributes.distance_triple
        bond2=Line(start=start2,end=end2,color=attributes.color)

        start3=start+direction_vector*start_edge*attributes.edge_global+normal_vector*attributes.length_global*attributes.distance_triple
        end3=end-direction_vector*end_edge*attributes.edge_global+normal_vector*attributes.length_global*attributes.distance_triple
        bond3=Line(start=start3,end=end3,color=attributes.color)

        self.add(bond1,bond2,bond3)

class NegativeCharge(VGroup):
    def __init__(self,*,text:MathTex,pos:Vector3D,attributes:'AttributeHolder'):

        position=text.get_corner(pos)+pos*attributes.edge_charge

        circle=Circle(radius=attributes.radius_negative,color=attributes.color,arc_center=position,
                      stroke_width=attributes.stroke_width_negative)

        line_start=[position[0]-attributes.radius_negative*attributes.ratio_negative,position[1],position[2]]
        line_end=[position[0]+attributes.radius_negative*attributes.ratio_negative,position[1],position[2]]
        line=Line(start=line_start,end=line_end,color=attributes.color,stroke_width=attributes.stroke_width_negative)

        super().__init__(circle,line)

class PositiveCharge(VGroup):
    def __init__(self,*,text:MathTex,pos:Vector3D,attributes:'AttributeHolder'):

        position=text.get_corner(pos)+pos*attributes.edge_charge

        circle=Circle(radius=attributes.radius_positive,color=attributes.color,arc_center=position,
                      stroke_width=attributes.stroke_width_positive)

        line1_start=[position[0]-attributes.radius_positive*attributes.ratio_positive,position[1],position[2]]
        line1_end=[position[0]+attributes.radius_positive*attributes.ratio_positive,position[1],position[2]]
        line1=Line(start=line1_start,end=line1_end,color=attributes.color,stroke_width=attributes.stroke_width_positive)

        line2_start=[position[0],position[1]-attributes.radius_positive*attributes.ratio_positive,position[2]]
        line2_end=[position[0],position[1]+attributes.radius_positive*attributes.ratio_positive,position[2]]
        line2=Line(start=line2_start,end=line2_end,color=attributes.color,stroke_width=attributes.stroke_width_positive)

        super().__init__(circle,line1,line2)

class SingleCharge(Circle):
    def __init__(self,*,text:MathTex,pos:Vector3D,attributes:'AttributeHolder'):

        position=text.get_corner(pos)+pos*attributes.edge_charge

        super().__init__(radius=attributes.radius_single,color=attributes.color,arc_center=position,fill_opacity=1)

class NegativeChargeByCoordinate(VGroup):
    def __init__(self,*,position:Vector3D,attributes:'AttributeHolder'):

        circle=Circle(radius=attributes.radius_negative,color=attributes.color,arc_center=position,
                      stroke_width=attributes.stroke_width_negative)

        line_start=[position[0]-attributes.radius_negative*attributes.ratio_negative,position[1],position[2]]
        line_end=[position[0]+attributes.radius_negative*attributes.ratio_negative,position[1],position[2]]
        line=Line(start=line_start,end=line_end,color=attributes.color,stroke_width=attributes.stroke_width_negative)

        super().__init__(circle,line)

class PositiveChargeByCoordinate(VGroup):
    def __init__(self,*,position:Vector3D,attributes:'AttributeHolder'):

        circle=Circle(radius=attributes.radius_positive,color=attributes.color,arc_center=position,
                      stroke_width=attributes.stroke_width_positive)

        line1_start=[position[0]-attributes.radius_positive*attributes.ratio_positive,position[1],position[2]]
        line1_end=[position[0]+attributes.radius_positive*attributes.ratio_positive,position[1],position[2]]
        line1=Line(start=line1_start,end=line1_end,color=attributes.color,stroke_width=attributes.stroke_width_positive)

        line2_start=[position[0],position[1]-attributes.radius_positive*attributes.ratio_positive,position[2]]
        line2_end=[position[0],position[1]+attributes.radius_positive*attributes.ratio_positive,position[2]]
        line2=Line(start=line2_start,end=line2_end,color=attributes.color,stroke_width=attributes.stroke_width_positive)

        super().__init__(circle,line1,line2)

class SingleChargeByCoordinate(Circle):
    def __init__(self,*,position:Vector3D,attributes:'AttributeHolder'):

        super().__init__(radius=attributes.radius_single,color=attributes.color,arc_center=position,fill_opacity=1)

class BracketBetweenPoints(VGroup):
    def __init__(self,*,start:Vector3D,end:Vector3D,ratio_edge=0.1,**kwargs):

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

class BezierArrow(VGroup):
    def __init__(self,*,start_anchor:Vector3D,start_handle:Vector3D,end_anchor:Vector3D,end_handle:Vector3D,
                 color=WHITE,stroke_width=2,arrow_size=-1.0,opacity=1.0,**kwargs):

        if arrow_size==-1:
            arrow_size=np.sqrt((start_anchor[0]-end_anchor[0])**2+(start_anchor[1]-end_anchor[1])**2)*0.15

        angle=np.arctan2(end_anchor[1]-end_handle[1],end_anchor[0]-end_handle[0])

        end_anchor=np.array(end_anchor)
        end_handle=np.array(end_handle)

        self.tip=ArrowTriangleFilledTip(color=color,fill_opacity=opacity)
        self.tip.scale(arrow_size).rotate(angle+PI).move_to(end_anchor)

        end_anchor-=arrow_size*(1/8.9*np.array([np.cos(np.arctan2(end_anchor[1]-end_handle[1],end_anchor[0]-end_handle[0])),
                                           np.sin(np.arctan2(end_anchor[1]-end_handle[1],end_anchor[0]-end_handle[0])),
                                           0])+np.array([0,0.0363,0]))
        end_handle-=arrow_size*(1/8.9*np.array([np.cos(np.arctan2(end_anchor[1]-end_handle[1],end_anchor[0]-end_handle[0])),
                                           np.sin(np.arctan2(end_anchor[1]-end_handle[1],end_anchor[0]-end_handle[0])),
                                           0])+np.array([0,0.0363,0]))

        self.bezier=CubicBezier(start_anchor=start_anchor,start_handle=start_handle,end_handle=end_handle,end_anchor=end_anchor,
                      color=color,stroke_width=stroke_width,**kwargs)
        self.bezier.set_stroke(opacity=opacity)

        super().__init__(self.bezier,self.tip)

class LightArrow(VGroup):
    def __init__(self,*,end:Vector3D,length:float=1.5,pos:Vector3D=UL,color=YELLOW,mark:bool=True,width=1,end_edge:float=0,**kwargs):

        self.length=length
        self.start=[end[0]+pos[0]*length,end[1]+pos[1]*length,0]
        self.end=[end[0]+pos[0]*end_edge,end[1]+pos[1]*end_edge,0]

        arrow=Arrow(start=self.start,end=self.end,stroke_width=width,color=color,tip_length=0.1,**kwargs)

        if mark==True:
            text=MathTex(r"h\nu",color=color,font_size=15,**kwargs)
            text.move_to([end[0]+pos[0]*(length/2-0.1*np.sqrt(2)),end[1]+pos[1]*(length/2-0.1*np.sqrt(2))+0.2,0])
            super().__init__(arrow,text)
        else:
            super().__init__(arrow)

class BondType(Enum):
    NORMAL_BOND=NormalBond
    IN_BOND=InBond
    OUT_BOND=OutBond
    DASHED_BOND=DashedBond
    DOUBLE_BOND=DoubleBond
    TRIPLE_BOND=TripleBond

class ChargeType(Enum):
    POSITIVE=PositiveCharge
    NEGATIVE=NegativeCharge
    SINGLE=SingleCharge
    POSITIVE_COORDINATE=PositiveChargeByCoordinate
    NEGATIVE_COORDINATE=NegativeChargeByCoordinate
    SINGLE_COORDINATE=SingleChargeByCoordinate

class AtomicCluster(MathTex):
    def __init__(self,*,
                 text:str,
                 pos:Vector3D,
                 attributes:'AttributeHolder'):

        super().__init__(text,color=attributes.color,font_size=attributes.font_size)
        self.move_to(pos)

class AttributeHolder:
    def __init__(self,*,
                 base_ratio_outbond:float,
                 base_ratio_inbond:float,
                 num_inbond:int,
                 dashed_length_dashedbond:float,
                 dashed_ratio_dashedbond:float,
                 ratio_transition_state_dashedbond:float,
                 length_global:float,
                 color:ManimColor,
                 edge_global:float,
                 font_size:float,
                 radius_negative:float,
                 ratio_negative:float,
                 stroke_width_negative:float,
                 edge_charge:float,
                 radius_positive:float,
                 ratio_positive:float,
                 stroke_width_positive:float,
                 radius_single:float,
                 distance_double:float,
                 edge_ratio_double:float,
                 distance_triple:float):

        self.base_ratio_outbond=base_ratio_outbond
        self.base_ratio_inbond=base_ratio_inbond
        self.num_inbond=num_inbond
        self.dashed_length_dashedbond=dashed_length_dashedbond
        self.dashed_ratio_dashedbond=dashed_ratio_dashedbond
        self.ratio_transition_state_dashedbond=ratio_transition_state_dashedbond
        self.length_global=length_global
        self.color=color
        self.edge_global=edge_global
        self.font_size=font_size
        self.radius_negative=radius_negative
        self.ratio_negative=ratio_negative
        self.stroke_width_negative=stroke_width_negative
        self.edge_charge=edge_charge
        self.radius_positive=radius_positive
        self.ratio_positive=ratio_positive
        self.stroke_width_positive=stroke_width_positive
        self.radius_single=radius_single
        self.distance_double=distance_double
        self.edge_ratio_double=edge_ratio_double
        self.distance_triple=distance_triple

class Bond(VGroup):
    def __init__(self,*,
                 bond_type:BondType,
                 start:AtomicCluster|Vector3D,
                 end:AtomicCluster|Vector3D,
                 start_edge=False,
                 end_edge=True,
                 attributes:AttributeHolder,
                 side:int|None=None,
                 start_side_edge:bool|None=None,
                 end_side_edge:bool|None=None):

        super().__init__(color=attributes.color)

        self.bond_type=bond_type
        self.start=start
        self.end=end
        if isinstance(start,AtomicCluster):
            self.start=self.start.get_center()
        if isinstance(end,AtomicCluster):
            self.end=self.end.get_center()
        self.start_edge=start_edge
        self.end_edge=end_edge
        angle_vector=end-start
        self.direction=np.arctan2(angle_vector[1],angle_vector[0])

        if bond_type==BondType.DOUBLE_BOND:
            bond=self.bond_type.value(start=self.start,direction=self.direction,
                                      start_edge=self.start_edge,end_edge=self.end_edge,
                                      attributes=attributes,
                                      side=side,start_side_edge=start_side_edge,end_side_edge=end_side_edge)
        else:
            bond=self.bond_type.value(start=self.start,direction=self.direction,
                                      start_edge=self.start_edge,end_edge=self.end_edge,
                                      attributes=attributes)

        self.add(bond)

class Charge(VGroup):
    def __init__(self,*,
                 charge_type:ChargeType,
                 text:AtomicCluster|Vector3D,
                 pos:Vector3D,
                 attributes:AttributeHolder):

        super().__init__(color=attributes.color)

        self.charge_type=charge_type
        self.text=text

        if isinstance(text,AtomicCluster):
            charge=self.charge_type.value(text=text,pos=pos,attributes=attributes)
        else:
            charge=self.charge_type.value(position=pos*attributes.edge_charge+text,attributes=attributes)

        self.add(charge)

class StructuralFormula(VGroup):
    def __init__(self,*,
                 base_ratio_outbond=0.2,
                 base_ratio_inbond=0.2,
                 num_inbond=5,
                 dashed_length_dashedbond=0.1,
                 dashed_ratio_dashedbond=0.5,
                 ratio_transition_state_dashedbond=bond_length*ratio_transition_state,
                 length_global=bond_length,
                 color=WHITE,
                 edge_global=edge,
                 font_size=txt_size,
                 radius_negative=0.05,
                 ratio_negative=0.6,
                 stroke_width_negative=1.2,
                 edge_charge=default_charge_edge,
                 radius_positive=0.05,
                 ratio_positive=0.6,
                 stroke_width_positive=1.2,
                 radius_single=0.01,
                 distance_double=0.12,
                 edge_ratio_double=0.08,
                 distance_triple=0.12,
                 name:str,
                 pos:Vector3D,
                 text:str|None=None,
                 ):

        self.attributes=AttributeHolder(base_ratio_outbond=base_ratio_outbond,
                                        base_ratio_inbond=base_ratio_inbond,
                                        num_inbond=num_inbond,
                                        dashed_length_dashedbond=dashed_length_dashedbond,
                                        dashed_ratio_dashedbond=dashed_ratio_dashedbond,
                                        ratio_transition_state_dashedbond=ratio_transition_state_dashedbond,
                                        length_global=length_global,
                                        color=color,
                                        edge_global=edge_global,
                                        font_size=font_size,
                                        radius_negative=radius_negative,
                                        ratio_negative=ratio_negative,
                                        stroke_width_negative=stroke_width_negative,
                                        edge_charge=edge_charge,
                                        radius_positive=radius_positive,
                                        ratio_positive=ratio_positive,
                                        stroke_width_positive=stroke_width_positive,
                                        radius_single=radius_single,
                                        distance_double=distance_double,
                                        edge_ratio_double=edge_ratio_double,
                                        distance_triple=distance_triple)

        super().__init__(color=self.attributes.color)

        self.atomic_clusters={}

        if text!=None:
            self.atomic_clusters[name]={Mobject:AtomicCluster(text=text,pos=pos,attributes=self.attributes),
                                        "pos":pos,
                                        "adj":[],
                                        Bond:[]}
            self.add(self.atomic_clusters[name][Mobject])
        else:
            self.atomic_clusters[name]={Mobject:None,"pos":pos,"adj":[],Bond:[]}

        self.charges={}

    def add_atom(self,*,
                 name:str,
                 direction:float,
                 text:str|None=None,
                 bond_type:BondType,
                 adjacency:str,
                 side:int|None=None,
                 start_side_edge:bool|None=None,
                 end_side_edge:bool|None=None):

        pos=self.attributes.length_global*np.array([np.cos(direction),np.sin(direction),0])+self.atomic_clusters[adjacency]["pos"]

        if text!=None:
            self.atomic_clusters[name]={Mobject:AtomicCluster(text=text,pos=pos,attributes=self.attributes),
                                        "pos":pos,
                                        "adj":[adjacency],
                                        Bond:[]}
        else:
            self.atomic_clusters[name]={Mobject:None,
                                        "pos":pos,
                                        "adj":[adjacency],
                                        Bond:[]}

        self.atomic_clusters[name][Bond].append(Bond(bond_type=bond_type,
                                                     start=self.atomic_clusters[adjacency]["pos"],
                                                     end=self.atomic_clusters[name]["pos"],
                                                     start_edge=(self.atomic_clusters[adjacency][Mobject]!=None),
                                                     end_edge=(self.atomic_clusters[name][Mobject]!=None),
                                                     attributes=self.attributes,
                                                     side=side,
                                                     start_side_edge=start_side_edge,
                                                     end_side_edge=end_side_edge))

        self.atomic_clusters[adjacency]["adj"].append(name)
        self.atomic_clusters[adjacency][Bond].append(self.atomic_clusters[name][Bond][0])
        self.add(self.atomic_clusters[name][Bond][0])

        if text!=None:
            self.add(self.atomic_clusters[name][Mobject])

    def add_charge(self,*,
                   text:str,
                   pos:Vector3D,
                   charge_type:ChargeType):

        self.charges[text]=Charge(charge_type=charge_type,text=self.atomic_clusters[text]["pos"],pos=pos,attributes=self.attributes)
            
        self.add(self.charges[text])

    def add_bond(self,*,
                 start:str,
                 end:str,
                 bond_type:BondType,
                 side:int|None=None,
                 start_side_edge:bool|None=None,
                 end_side_edge:bool|None=None):

        if bond_type==BondType.DOUBLE_BOND:
            bond=Bond(bond_type=bond_type,
                      start=self.atomic_clusters[start]["pos"],
                      end=self.atomic_clusters[end]["pos"],
                      start_edge=(self.atomic_clusters[start][Mobject]!=None),
                      end_edge=(self.atomic_clusters[end][Mobject]!=None),
                      attributes=self.attributes,
                      side=side,
                      start_side_edge=start_side_edge,
                      end_side_edge=end_side_edge)

        else:
            bond=Bond(bond_type=bond_type,
                      start=self.atomic_clusters[start]["pos"],
                      end=self.atomic_clusters[end]["pos"],
                      start_edge=(self.atomic_clusters[start][Mobject]!=None),
                      end_edge=(self.atomic_clusters[end][Mobject]!=None),
                      attributes=self.attributes)

        self.add(bond)

        self.atomic_clusters[start][Bond].append(bond)
        self.atomic_clusters[end][Bond].append(bond)

#Animation classes
class OpacityEffect(Animation):
    def __init__(self,*,mobject:Mobject,initial_opacity:float,final_opacity:float,run_time:float,func:Callable[[float],float]=linear,**kwargs):
        self.initial_opacity=initial_opacity
        self.final_opacity=final_opacity
        self.func=func
        super().__init__(mobject=mobject,run_time=run_time,**kwargs)

    def interpolate_mobject(self, alpha:float):
        opacity=self.func(alpha)*(self.final_opacity-self.initial_opacity)+self.initial_opacity
        if isinstance(self.mobject,BezierArrow):
            self.mobject.tip.set_fill(opacity=opacity)
            self.mobject.bezier.set_stroke(opacity=opacity)
        else:
            self.mobject.set_opacity(opacity)

#Text classes
class Title(MathTex):
    def __init__(self,*,text:str,pos:Vector3D=title_coordinate,color=WHITE,size=title_size):

        super().__init__(text,color=color,tex_template=mytemplate,font_size=size)

        self.move_to(pos)

class Subtitle(MathTex):
    def __init__(self,*,text:str,pos:Vector3D=subtitle_coordinate,color=WHITE,size=subtitle_size):

        super().__init__(text,color=color,tex_template=mytemplate,font_size=size)

        self.move_to(pos)

class Description(MathTex):
    def __init__(self,*,text:str,pos:Vector3D=description_coordinate,color=WHITE,size=txt_size):

        super().__init__(text,color=color,tex_template=mytemplate,font_size=size)

        self.move_to(pos)
        
#functions
def play_timeline(scene:Scene,timeline:dict[float,Animation]):

    # Inspired by github.com/abul4fia/manim-play-timeline's timeline implementation

    pretime=0
    ending=0
    for time,animation in sorted(timeline.items()):
        to_wait=time-pretime
        if to_wait>0:
            scene.wait(to_wait)
        pretime=time
        for anim in animation:
            turn_animation_into_updater(anim)
            scene.add(anim.mobject)
            ending=max(ending,anim.run_time+time)
    if ending>time:
        scene.wait(ending-pretime)

def merging_timeline(timeline1:dict[float,Union[Iterable[Animation],Animation]],timeline2:dict[float,Union[Iterable[Animation],Animation]]):
    rslt=timeline1.copy()
    for time,anims in timeline2.items():
        if time in rslt:
            if not isinstance(rslt[time],Iterable):
                rslt[time]=[rslt[time]]
            if not isinstance(anims,Iterable):
                anims=[anims]
            rslt[time].extend(anims)
        else:
            rslt[time]=anims
    return rslt

def brownian_motion(items:Union[Mobject,list],num:int,time:float=1.0):
    if isinstance(items,list):
        temp={}
        for item in items:
            temp=merging_timeline(temp,brownian_motion(item,num,time))
        return temp
    else:
        node=[]
        while len(node)<num:
            temp_node=RNG.uniform(0,time)
            node.append(temp_node)
        node=sorted(node)
        node.append(time)

        rslt={}
        destination=items.get_center()
        for i in range(num):
            dx=np.array([RNG.uniform(-0.5,0.5),RNG.uniform(-0.5,0.5),0])
            destination+=dx
            if np.abs(destination[0])>5 or np.abs(destination[1])>3:
                destination[0]=destination[0]/7*6
                destination[1]=destination[1]/4*3
            if i == 0:
                rslt[0] = [ApplyMethod(
                    items.shift,
                    dx,
                    run_time=node[i],
                    rate_func=smooth)]
            else:
                rslt[node[i-1]] = [ApplyMethod(
                    items.shift,
                    dx,
                    run_time=node[i] - node[i-1],
                    rate_func=smooth)]
        return rslt

#default settings
DEFAULT_ATTRIBUTES=AttributeHolder(base_ratio_outbond=0.2,
                                   base_ratio_inbond=0.2,
                                   num_inbond=5,
                                   dashed_length_dashedbond=0.1,
                                   dashed_ratio_dashedbond=0.5,
                                   ratio_transition_state_dashedbond=bond_length*ratio_transition_state,
                                   length_global=bond_length,
                                   color=WHITE,
                                   edge_global=edge,
                                   font_size=txt_size,
                                   radius_negative=0.05,
                                   ratio_negative=0.6,
                                   stroke_width_negative=1.2,
                                   edge_charge=default_charge_edge,
                                   radius_positive=0.05,
                                   ratio_positive=0.6,
                                   stroke_width_positive=1.2,
                                   radius_single=0.01,
                                   distance_double=0.12,
                                   edge_ratio_double=0.08,
                                   distance_triple=0.12)
