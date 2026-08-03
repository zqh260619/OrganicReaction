from manim import *
from manim.typing import Vector3D
import numpy as np
from typing import Callable, Optional
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

        direction=np.array([x-y for x,y in zip(end,start)])
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

        """此类中的魔法数字用于调整箭头的大小和位置，使得箭头与曲线不重叠且中心对齐，建议不要随意修改"""

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

class ElectronMigrationStep:
    """电子迁移步骤的描述。

    Attributes
    ----------
    replace : list[tuple[Mobject, Mobject]]
        要执行的 ReplacementTransform 列表，每项为 (source, target)。
        多对一：将多个 source 用 VGroup 包装。
        一对多：将多个 target 用 VGroup 包装，或使用 Mobject.copy()。
    create : list[Mobject]
        要在本步骤中 FadeIn 的新 Mobject 列表。
    lag_ratio : float
        步骤内部子动画之间的延迟比率（0~1），类似 AnimationGroup.lag_ratio。
    """
    def __init__(self,*,
                 replace:list[tuple[Mobject,Mobject]]|None=None,
                 create:list[Mobject]|None=None,
                 lag_ratio:float=0.0):
        self.replace=replace or []
        self.create=create or []
        self.lag_ratio=lag_ratio

class Locator:
    """原子定位器，封装新原子相对于邻接原子的位置计算。

    支持两种模式：
    - 角度模式：指定相对于邻接原子的极角（弧度或度）
    - 坐标模式：直接指定绝对坐标

    提供常用方向的工厂方法：Locator.up(), Locator.down(), Locator.left(), Locator.right()
    """
    def __init__(self,*,radians:float|None=None,degrees:float|None=None,coord:Vector3D|None=None):
        if coord is not None:
            self._mode='coord'
            self._coord=np.array(coord,dtype=float)
        elif degrees is not None:
            self._mode='angle'
            self._angle=degrees*DEGREES
        elif radians is not None:
            self._mode='angle'
            self._angle=radians
        else:
            self._mode='angle'
            self._angle=0.0

    @classmethod
    def up(cls)->'Locator':
        return cls(radians=PI/2)

    @classmethod
    def down(cls)->'Locator':
        return cls(radians=-PI/2)

    @classmethod
    def left(cls)->'Locator':
        return cls(radians=PI)

    @classmethod
    def right(cls)->'Locator':
        return cls(radians=0)

    def get_coord(self,sf:'StructuralFormula',adjacency:str)->Vector3D:
        """根据 StructuralFormula 和邻接原子名计算新原子的坐标。"""
        if self._mode=='coord':
            return self._coord.copy()
        else:
            a=sf.attributes.length_global
            return a*np.array([np.cos(self._angle),np.sin(self._angle),0])+sf.atomic_clusters[adjacency]["pos"]

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
        self.side=side
        self.start_side_edge=start_side_edge
        self.end_side_edge=end_side_edge
        angle_vector=self.end-self.start
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
                 name:str|None=None,
                 pos:Vector3D|None=None,
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

        if name is not None:
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
                 direction:float|None=None,
                 text:str|None=None,
                 bond_type:BondType|None=None,
                 adjacency:str|None=None,
                 pos:Vector3D|None=None,
                 side:int|None=None,
                 start_side_edge:bool|None=None,
                 end_side_edge:bool|None=None):

        if name in self.atomic_clusters:
            raise ValueError(f"原子 '{name}' 已经存在于结构中，不能重复添加。")

        if not self.atomic_clusters:
            if pos is None:
                raise ValueError("向空结构式添加第一个原子时必须提供 pos 参数。")
            if text is not None:
                self.atomic_clusters[name]={Mobject:AtomicCluster(text=text,pos=pos,attributes=self.attributes),
                                            "pos":pos,
                                            "adj":[],
                                            Bond:[]}
                self.add(self.atomic_clusters[name][Mobject])
            else:
                self.atomic_clusters[name]={Mobject:None,"pos":pos,"adj":[],Bond:[]}
            return

        if adjacency is None:
            raise ValueError("向非空结构式添加原子时必须提供 adjacency 参数。")
        if direction is None:
            raise ValueError("向非空结构式添加原子时必须提供 direction 参数。")
        if bond_type is None:
            raise ValueError("向非空结构式添加原子时必须提供 bond_type 参数。")
        if adjacency not in self.atomic_clusters:
            raise ValueError(f"邻接原子 '{adjacency}' 不存在于结构中。")

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
                                                     start=self.atomic_clusters[adjacency][Mobject] or self.atomic_clusters[adjacency]["pos"],
                                                     end=self.atomic_clusters[name][Mobject] or self.atomic_clusters[name]["pos"],
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

        if text not in self.atomic_clusters:
            raise ValueError(f"原子 '{text}' 不存在于结构中。")
        if text in self.charges:
            raise ValueError(f"原子 '{text}' 上已经存在电荷，不能重复添加。")

        self.charges[text]=Charge(charge_type=charge_type,text=self.atomic_clusters[text][Mobject] or self.atomic_clusters[text]["pos"],pos=pos,attributes=self.attributes)

        self.add(self.charges[text])

    def add_bond(self,*,
                 start:str,
                 end:str,
                 bond_type:BondType,
                 side:int|None=None,
                 start_side_edge:bool|None=None,
                 end_side_edge:bool|None=None):

        if start not in self.atomic_clusters:
            raise ValueError(f"原子 '{start}' 不存在于结构中。")
        if end not in self.atomic_clusters:
            raise ValueError(f"原子 '{end}' 不存在于结构中。")
        if start == end:
            raise ValueError(f"不能在同一原子 '{start}' 之间创建键。")
        if end in self.atomic_clusters[start]["adj"]:
            raise ValueError(f"原子 '{start}' 和 '{end}' 之间已经存在键，不能重复创建。")

        if bond_type==BondType.DOUBLE_BOND:
            bond=Bond(bond_type=bond_type,
                      start=self.atomic_clusters[start][Mobject] or self.atomic_clusters[start]["pos"],
                      end=self.atomic_clusters[end][Mobject] or self.atomic_clusters[end]["pos"],
                      start_edge=(self.atomic_clusters[start][Mobject]!=None),
                      end_edge=(self.atomic_clusters[end][Mobject]!=None),
                      attributes=self.attributes,
                      side=side,
                      start_side_edge=start_side_edge,
                      end_side_edge=end_side_edge)

        else:
            bond=Bond(bond_type=bond_type,
                      start=self.atomic_clusters[start][Mobject] or self.atomic_clusters[start]["pos"],
                      end=self.atomic_clusters[end][Mobject] or self.atomic_clusters[end]["pos"],
                      start_edge=(self.atomic_clusters[start][Mobject]!=None),
                      end_edge=(self.atomic_clusters[end][Mobject]!=None),
                      attributes=self.attributes)

        self.add(bond)

        self.atomic_clusters[start][Bond].append(bond)
        self.atomic_clusters[end][Bond].append(bond)
        self.atomic_clusters[start]["adj"].append(end)
        self.atomic_clusters[end]["adj"].append(start)

    def build_bond(self,*,
                   start:str,
                   end:str,
                   bond_type:BondType,
                   side:int|None=None,
                   start_side_edge:bool|None=None,
                   end_side_edge:bool|None=None)->Bond:
        """创建化学键对象但不添加到结构式中。

        Parameters
        ----------
        start : str
            起始原子名。
        end : str
            终止原子名。
        bond_type : BondType
            键的类型。
        side : int | None
            双键的左右不对称参数（仅对 DOUBLE_BOND 有效）。
        start_side_edge : bool | None
            起始端是否使用 side 边距。
        end_side_edge : bool | None
            终止端是否使用 side 边距。

        Returns
        -------
        Bond
            创建的化学键对象（未添加到 StructuralFormula 中）。
        """
        if start not in self.atomic_clusters:
            raise ValueError(f"原子 '{start}' 不存在于结构中。")
        if end not in self.atomic_clusters:
            raise ValueError(f"原子 '{end}' 不存在于结构中。")

        if bond_type==BondType.DOUBLE_BOND:
            return Bond(bond_type=bond_type,
                        start=self.atomic_clusters[start][Mobject] or self.atomic_clusters[start]["pos"],
                        end=self.atomic_clusters[end][Mobject] or self.atomic_clusters[end]["pos"],
                        start_edge=(self.atomic_clusters[start][Mobject]!=None),
                        end_edge=(self.atomic_clusters[end][Mobject]!=None),
                        attributes=self.attributes,
                        side=side,
                        start_side_edge=start_side_edge,
                        end_side_edge=end_side_edge)
        else:
            return Bond(bond_type=bond_type,
                        start=self.atomic_clusters[start][Mobject] or self.atomic_clusters[start]["pos"],
                        end=self.atomic_clusters[end][Mobject] or self.atomic_clusters[end]["pos"],
                        start_edge=(self.atomic_clusters[start][Mobject]!=None),
                        end_edge=(self.atomic_clusters[end][Mobject]!=None),
                        attributes=self.attributes)

    def build_charge(self,*,
                     text:str,
                     pos:Vector3D,
                     charge_type:ChargeType)->Charge:
        """创建电荷对象但不添加到结构式中。

        Parameters
        ----------
        text : str
            电荷所附着的原子名。
        pos : Vector3D
            电荷相对于原子文本的位置（方向向量，如 UR, DOWN 等）。
        charge_type : ChargeType
            电荷类型。

        Returns
        -------
        Charge
            创建的电荷对象（未添加到 StructuralFormula 中）。
        """
        if text not in self.atomic_clusters:
            raise ValueError(f"原子 '{text}' 不存在于结构中。")
        return Charge(charge_type=charge_type,
                      text=self.atomic_clusters[text][Mobject] or self.atomic_clusters[text]["pos"],
                      pos=pos,
                      attributes=self.attributes)

    def delete_atom(self,*,
                    names:str|list[str],
                    anim:type[Animation]=FadeOut)->Animation:

        if isinstance(names,str):
            names=[names]

        for name in names:
            if name not in self.atomic_clusters:
                raise ValueError(f"原子 '{name}' 不存在于结构中。")

        deletes=[]

        for name in names:

            if self.atomic_clusters[name][Mobject]!=None:
                deletes.append(self.atomic_clusters[name][Mobject])
                self.remove(self.atomic_clusters[name][Mobject])
            for bond in self.atomic_clusters[name][Bond]:
                deletes.append(bond)
                self.remove(bond)
            if name in self.charges:
                deletes.append(self.charges[name])
                self.remove(self.charges[name])
                self.charges.pop(name)
            for adjacency in self.atomic_clusters[name]["adj"]:
                self.atomic_clusters[adjacency][Bond]=[bond for bond in self.atomic_clusters[adjacency][Bond] if bond not in self.atomic_clusters[name][Bond]]
                self.atomic_clusters[adjacency]["adj"].remove(name)
            self.atomic_clusters.pop(name)

        return anim(*deletes)

    def delete_bond(self,*,
                    start:str,
                    end:str,
                    anim:type[Animation]=FadeOut)->Animation:

        if start not in self.atomic_clusters:
            raise ValueError(f"原子 '{start}' 不存在于结构中。")
        if end not in self.atomic_clusters:
            raise ValueError(f"原子 '{end}' 不存在于结构中。")

        target=None
        for bond in self.atomic_clusters[start][Bond]:
            if bond in self.atomic_clusters[end][Bond]:
                target=bond
                break

        if target is None:
            raise ValueError(f"原子 '{start}' 和 '{end}' 之间不存在键。")

        self.remove(target)

        assert target in self.atomic_clusters[start][Bond],f"内部错误：键不在 '{start}' 的键列表中"
        assert target in self.atomic_clusters[end][Bond],f"内部错误：键不在 '{end}' 的键列表中"
        assert end in self.atomic_clusters[start]["adj"],f"内部错误：'{end}' 不在 '{start}' 的邻接列表中"
        assert start in self.atomic_clusters[end]["adj"],f"内部错误：'{start}' 不在 '{end}' 的邻接列表中"

        self.atomic_clusters[start][Bond]=[b for b in self.atomic_clusters[start][Bond] if b is not target]
        self.atomic_clusters[end][Bond]=[b for b in self.atomic_clusters[end][Bond] if b is not target]
        self.atomic_clusters[start]["adj"]=[a for a in self.atomic_clusters[start]["adj"] if a!=end]
        self.atomic_clusters[end]["adj"]=[a for a in self.atomic_clusters[end]["adj"] if a!=start]

        return anim(target)

    def rotate_atoms(self,*,
                     atom_names:str|list[str],
                     center:str|Vector3D,
                     angle:float,
                     about_edge:bool=True,
                     run_time:float=1.0,
                     rate_func:Callable[[float],float]=smooth,
                     **kwargs)->Animation:
        """旋转一个或多个原子及其相连的化学键。

        Parameters
        ----------
        atom_names : str | list[str]
            要旋转的原子在字典中的键（单个字符串或字符串列表）。
        center : str | Vector3D
            旋转中心，可以是原子名称字符串（以其坐标为中心）或 Vector3D 坐标。
        angle : float
            旋转角度（弧度制），逆时针为正。
        about_edge : bool
            当 center 为原子名时生效。
            True（默认）：以原子的键端点坐标（pos）为旋转中心。
            False：以原子文本标签的视觉中心为旋转中心。
        run_time : float
            动画持续时间（秒）。
        rate_func : Callable[[float],float]
            动画速率函数。
        **kwargs
            传递给 Animation 的额外参数。

        Returns
        -------
        Animation
            可直接用于 self.play() 的 RotateAtoms 动画实例。
        """
        if isinstance(atom_names,str):
            atom_names=[atom_names]
        for name in atom_names:
            if name not in self.atomic_clusters:
                raise ValueError(f"原子 '{name}' 不存在于结构中。")
        if isinstance(center,str) and center not in self.atomic_clusters:
            raise ValueError(f"旋转中心原子 '{center}' 不存在于结构中。")

        return RotateAtoms(structural_formula=self,
                           atom_names=atom_names,
                           center=center,
                           angle=angle,
                           about_edge=about_edge,
                           run_time=run_time,
                           rate_func=rate_func,
                           **kwargs)

    def electron_migration(self,*,
                           steps:list[ElectronMigrationStep],
                           lag_ratio:float=0.0,
                           run_time:float=1.0,
                           **kwargs)->"ElectronMigration":
        """创建电子迁移动画。

        指定一系列 ElectronMigrationStep，每个步骤描述一组化学键/电荷的变换。
        步骤之间通过 lag_ratio 控制延迟比率（0 表示所有步骤同时开始，1 表示依次执行）。

        Parameters
        ----------
        steps : list[ElectronMigrationStep]
            电子迁移步骤列表。
        lag_ratio : float
            步骤之间的延迟比率（0~1）。
        run_time : float
            每个步骤内子动画的运行时间（秒）。
        **kwargs
            传递给 ElectronMigration 的额外参数。

        Returns
        -------
        ElectronMigration
            可直接用于 self.play() 的动画实例。
        """
        return ElectronMigration(sf=self,
                                 steps=steps,
                                 lag_ratio=lag_ratio,
                                 run_time=run_time,
                                 **kwargs)

def _rotate_point_2d(point:Vector3D,center:Vector3D,angle:float)->Vector3D:
    """绕 center 在 XY 平面内旋转 point，角度 angle（弧度）"""
    dx=point[0]-center[0]
    dy=point[1]-center[1]
    cos_a=np.cos(angle)
    sin_a=np.sin(angle)
    return np.array([center[0]+dx*cos_a-dy*sin_a,
                     center[1]+dx*sin_a+dy*cos_a,
                     point[2]])

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

class RotateAtoms(Animation):
    """绕指定中心旋转一个或多个原子，相连化学键跟随伸缩。"""
    def __init__(self,*,
                 structural_formula:'StructuralFormula',
                 atom_names:str|list[str],
                 center:str|Vector3D,
                 angle:float,
                 about_edge:bool=True,
                 run_time:float=1.0,
                 rate_func:Callable[[float],float]=smooth,
                 **kwargs):

        self.sf=structural_formula
        if isinstance(atom_names,str):
            atom_names=[atom_names]
        self.atom_names=atom_names
        self.angle=angle

        # 确定旋转中心点坐标
        if isinstance(center,str):
            if about_edge:
                self.center_point=np.copy(structural_formula.atomic_clusters[center]["pos"])
            else:
                mobj=structural_formula.atomic_clusters[center][Mobject]
                if mobj is not None:
                    self.center_point=np.copy(mobj.get_center())
                else:
                    self.center_point=np.copy(structural_formula.atomic_clusters[center]["pos"])
        else:
            self.center_point=np.array(center,dtype=float)

        # 存储旋转原子的初始位置
        self.initial_positions={}
        for name in atom_names:
            self.initial_positions[name]=np.copy(structural_formula.atomic_clusters[name]["pos"])

        # 建立 键→所连两原子名 的映射
        self.bond_to_atoms={}
        for name in atom_names:
            for bond in structural_formula.atomic_clusters[name][Bond]:
                if bond not in self.bond_to_atoms:
                    atoms=[]
                    for n,data in structural_formula.atomic_clusters.items():
                        if bond in data[Bond]:
                            atoms.append(n)
                    self.bond_to_atoms[bond]=atoms

        # 存储电荷相对于其原子的偏移量
        self.charge_offsets={}
        for name in atom_names:
            if name in structural_formula.charges:
                charge_center=structural_formula.charges[name].get_center()
                atom_pos=structural_formula.atomic_clusters[name]["pos"]
                self.charge_offsets[name]=charge_center-atom_pos

        super().__init__(mobject=structural_formula,run_time=run_time,rate_func=rate_func,**kwargs)

    def _rebuild_bond(self,bond:'Bond'):
        """根据原子当前位置原地更新键的几何体（不删建，避免残留）。"""
        a1,a2=self.bond_to_atoms[bond]
        bond.start=self.sf.atomic_clusters[a1]["pos"]
        bond.end=self.sf.atomic_clusters[a2]["pos"]
        angle_vector=bond.end-bond.start
        bond.direction=np.arctan2(angle_vector[1],angle_vector[0])

        attrs=self.sf.attributes
        d=bond.direction
        dv=np.array([np.cos(d),np.sin(d),0])
        nv=np.array([-np.sin(d),np.cos(d),0])
        se=bond.start_edge
        ee=bond.end_edge
        start=bond.start
        end=start+dv*attrs.length_global

        bt=bond.bond_type
        geo=bond.submobjects[0]  # 键几何体的外层 VGroup/Line/Polygon

        if bt==BondType.NORMAL_BOND:
            sp=start+dv*se*attrs.edge_global
            ep=start+dv*(attrs.length_global-ee*attrs.edge_global)
            geo.put_start_and_end_on(sp,ep)

        elif bt==BondType.DASHED_BOND:
            sp=start+dv*attrs.edge_global*se
            ep=start+dv*(attrs.length_global*attrs.ratio_transition_state_dashedbond-attrs.edge_global*ee)
            geo.put_start_and_end_on(sp,ep)

        elif bt==BondType.OUT_BOND:
            sp=start+se*attrs.edge_global*dv
            ep=start+(attrs.length_global-ee*attrs.edge_global)*dv
            offset=attrs.base_ratio_outbond*(attrs.length_global-(se+ee)*attrs.edge_global)/2
            vertices=[sp,ep+offset*nv,ep-offset*nv]
            geo.set_points_as_corners(vertices)

        elif bt==BondType.IN_BOND:
            sp=start+se*attrs.edge_global*dv
            ep=start+(attrs.length_global-ee*attrs.edge_global)*dv
            half=attrs.base_ratio_inbond*(attrs.length_global-(se+ee)*attrs.edge_global)/2
            ep1=ep+half*nv
            ep2=ep-half*nv
            num=attrs.num_inbond
            for i in range(num):
                t=(i+1)/num
                s=(num-(i+1))/num
                geo.submobjects[i].put_start_and_end_on(ep1*t+sp*s,ep2*t+sp*s)

        elif bt==BondType.TRIPLE_BOND:
            s1=start+dv*se*attrs.edge_global
            e1=end-dv*ee*attrs.edge_global
            s2=s1-nv*attrs.length_global*attrs.distance_triple
            e2=e1-nv*attrs.length_global*attrs.distance_triple
            s3=s1+nv*attrs.length_global*attrs.distance_triple
            e3=e1+nv*attrs.length_global*attrs.distance_triple
            geo.submobjects[0].put_start_and_end_on(s1,e1)
            geo.submobjects[1].put_start_and_end_on(s2,e2)
            geo.submobjects[2].put_start_and_end_on(s3,e3)

        elif bt==BondType.DOUBLE_BOND:
            side=bond.side
            sse=bond.start_side_edge
            ese=bond.end_side_edge
            if side==0:
                s1=start+dv*se*attrs.edge_global+0.5*nv*attrs.length_global*attrs.edge_ratio_double
                s2=start+dv*se*attrs.edge_global-0.5*nv*attrs.length_global*attrs.edge_ratio_double
                e1=end-dv*ee*attrs.edge_global+0.5*nv*attrs.length_global*attrs.edge_ratio_double
                e2=end-dv*ee*attrs.edge_global-0.5*nv*attrs.length_global*attrs.edge_ratio_double
            elif side==1:
                s1=start+dv*se*attrs.edge_global
                e1=end-dv*ee*attrs.edge_global
                s2=start+dv*(se*attrs.edge_global+sse*attrs.edge_ratio_double)+nv*attrs.length_global*attrs.distance_double
                e2=end-dv*(ee*attrs.edge_global+ese*attrs.edge_ratio_double)+nv*attrs.length_global*attrs.distance_double
            else:  # side==-1
                s1=start+dv*se*attrs.edge_global
                e1=end-dv*ee*attrs.edge_global
                s2=start+dv*(se*attrs.edge_global+sse*attrs.edge_ratio_double)-nv*attrs.length_global*attrs.distance_double
                e2=end-dv*(ee*attrs.edge_global+ese*attrs.edge_ratio_double)-nv*attrs.length_global*attrs.distance_double
            geo.submobjects[0].put_start_and_end_on(s1,e1)
            geo.submobjects[1].put_start_and_end_on(s2,e2)

    def interpolate_mobject(self,alpha:float):
        current_angle=self.angle*self.rate_func(alpha)

        # 更新原子位置
        for name in self.atom_names:
            new_pos=_rotate_point_2d(self.initial_positions[name],self.center_point,current_angle)
            self.sf.atomic_clusters[name]["pos"]=new_pos
            mobj=self.sf.atomic_clusters[name][Mobject]
            if mobj is not None:
                mobj.move_to(new_pos)

        # 重建受影响的键
        for bond in self.bond_to_atoms:
            self._rebuild_bond(bond)

        # 更新电荷位置
        for name in self.atom_names:
            if name in self.charge_offsets:
                new_charge_pos=self.sf.atomic_clusters[name]["pos"]+self.charge_offsets[name]
                self.sf.charges[name].move_to(new_charge_pos)

class BondTypeTransform(Transform):
    """化学键类型变换+旋转动画（独立动画类）。

    通过 Transform 底层点插值，同时实现：
    1. 化学键类型的形状变换（如 NormalBond → DoubleBond）
    2. 化学键绕指定点的旋转

    两者同时开始、同时结束，整个过程中键的几何体平滑过渡。
    如果提供了 sf（StructuralFormula），关联的原子文本和电荷也会逐帧同步旋转。

    Parameters
    ----------
    bond : Bond
        要变换的化学键对象。
    target_type : BondType
        目标化学键类型。
    angle : float
        旋转角度（弧度）。
    about_point : Vector3D, optional
        旋转中心点，默认为键的起点（绕起点原子旋转另一端）。
    sf : StructuralFormula, optional
        所属的结构式对象。提供后，动画每帧同步旋转原子的 Mobject 和电荷。
    **kwargs
        传递给 Transform 的额外参数（如 run_time, rate_func 等）。
    """

    def __init__(self, *,
                 bond: Bond,
                 target_type: BondType,
                 angle: float,
                 about_point: Optional[Vector3D] = None,
                 sf: Optional['StructuralFormula'] = None,
                 **kwargs):

        self._bond = bond
        self._target_type = target_type
        self._angle = angle
        self._sf = sf

        if about_point is None:
            about_point = np.array(bond.start)
        self._about_point = np.array(about_point, dtype=float)

        # 保存初始起止位置
        self._initial_start = np.array(bond.start, dtype=float)
        self._initial_end = np.array(bond.end, dtype=float)

        # ----- 获取 StructuralFormula 中关联的原子信息（用于逐帧同步）-----
        self._atom1_name: Optional[str] = None
        self._atom2_name: Optional[str] = None
        self._atom1_mobj: Optional[Mobject] = None
        self._atom2_mobj: Optional[Mobject] = None
        self._atom1_init_pos: Optional[np.ndarray] = None
        self._atom2_init_pos: Optional[np.ndarray] = None
        self._charge_offsets: dict[str, np.ndarray] = {}

        if sf is not None:
            for name, data in sf.atomic_clusters.items():
                if bond in data[Bond]:
                    if self._atom1_name is None:
                        self._atom1_name = name
                    else:
                        self._atom2_name = name
                        break

            if self._atom1_name is not None:
                self._atom1_mobj = sf.atomic_clusters[self._atom1_name].get(Mobject)
                self._atom1_init_pos = np.array(
                    sf.atomic_clusters[self._atom1_name]["pos"], dtype=float
                )
                if self._atom1_name in sf.charges:
                    c = sf.charges[self._atom1_name]
                    self._charge_offsets[self._atom1_name] = (
                        c.get_center() - self._atom1_init_pos
                    )

            if self._atom2_name is not None:
                self._atom2_mobj = sf.atomic_clusters[self._atom2_name].get(Mobject)
                self._atom2_init_pos = np.array(
                    sf.atomic_clusters[self._atom2_name]["pos"], dtype=float
                )
                if self._atom2_name in sf.charges:
                    c = sf.charges[self._atom2_name]
                    self._charge_offsets[self._atom2_name] = (
                        c.get_center() - self._atom2_init_pos
                    )

        # 获取属性持有者
        attrs = sf.attributes if sf is not None else DEFAULT_ATTRIBUTES

        # 构建目标键（与源键相同起止位置，但类型不同）
        target_bond = Bond(
            bond_type=target_type,
            start=np.array(bond.start, dtype=float),
            end=np.array(bond.end, dtype=float),
            start_edge=bond.start_edge,
            end_edge=bond.end_edge,
            attributes=attrs,
            side=bond.side if (target_type == BondType.DOUBLE_BOND and bond.side is not None) else (0 if target_type == BondType.DOUBLE_BOND else None),
            start_side_edge=bond.start_side_edge if (target_type == BondType.DOUBLE_BOND and bond.start_side_edge is not None) else (False if target_type == BondType.DOUBLE_BOND else None),
            end_side_edge=bond.end_side_edge if (target_type == BondType.DOUBLE_BOND and bond.end_side_edge is not None) else (False if target_type == BondType.DOUBLE_BOND else None),
        )

        # 旋转目标键：其内部点位直接体现终态
        target_bond.rotate(angle, about_point=self._about_point)

        super().__init__(mobject=bond, target_mobject=target_bond, **kwargs)

    # ---- 逐帧旋转辅助 ----
    @staticmethod
    def _rotate_point(pt: np.ndarray, center: np.ndarray, rad: float) -> np.ndarray:
        dx = pt[0] - center[0]
        dy = pt[1] - center[1]
        cos_a = np.cos(rad)
        sin_a = np.sin(rad)
        return np.array([
            center[0] + dx * cos_a - dy * sin_a,
            center[1] + dx * sin_a + dy * cos_a,
            pt[2],
        ])

    def _move_atoms_to_alpha(self, alpha: float) -> None:
        """根据 alpha 旋转原子 Mobject 和电荷到当前位置。"""
        cur_angle = self.rate_func(alpha) * self._angle

        if self._atom1_mobj is not None and self._atom1_init_pos is not None:
            new_pos = self._rotate_point(self._atom1_init_pos, self._about_point, cur_angle)
            self._atom1_mobj.move_to(new_pos)
            if self._atom1_name in self._charge_offsets:
                self._sf.charges[self._atom1_name].move_to(
                    new_pos + self._charge_offsets[self._atom1_name]
                )

        if self._atom2_mobj is not None and self._atom2_init_pos is not None:
            new_pos = self._rotate_point(self._atom2_init_pos, self._about_point, cur_angle)
            self._atom2_mobj.move_to(new_pos)
            if self._atom2_name in self._charge_offsets:
                self._sf.charges[self._atom2_name].move_to(
                    new_pos + self._charge_offsets[self._atom2_name]
                )

    def interpolate_mobject(self, alpha: float) -> None:
        """每帧：先做键几何插值，再旋转原子 Mobject。"""
        super().interpolate_mobject(alpha)
        if self._sf is not None:
            self._move_atoms_to_alpha(alpha)

    def finish(self) -> None:
        """动画结束：更新 Bond 的元数据及 StructuralFormula 内部状态。"""
        super().finish()

        # 更新键类型
        self._bond.bond_type = self._target_type

        # 用旋转公式从初始位置计算旋转后的起止点
        new_start = self._rotate_point(self._initial_start, self._about_point, self._angle)
        new_end = self._rotate_point(self._initial_end, self._about_point, self._angle)

        self._bond.start = new_start
        self._bond.end = new_end
        angle_vec = new_end - new_start
        self._bond.direction = np.arctan2(angle_vec[1], angle_vec[0])

        # 同步 StructuralFormula 内部数据（pos 字段）
        if self._sf is not None:
            self._sync_structural_formula()

    def _sync_structural_formula(self) -> None:
        """更新 StructuralFormula 中原子位置数据（非 Mobject，已在 interpolate 中处理）。"""
        sf = self._sf

        if self._atom1_name is not None:
            sf.atomic_clusters[self._atom1_name]["pos"] = self._bond.start
        if self._atom2_name is not None:
            sf.atomic_clusters[self._atom2_name]["pos"] = self._bond.end


class ElectronMigration(AnimationGroup):
    """电子迁移动画，管理化学键与电荷之间的动态变换序列。

    每个步骤内部可以有多个并行的子动画（ReplacementTransform / FadeIn），
    步骤之间通过 lag_ratio 控制延迟比率。

    Parameters
    ----------
    sf : StructuralFormula
        动画所操作的结构式对象。
    *steps : ElectronMigrationStep
        迁移步骤序列。
    lag_ratio : float
        步骤之间的延迟比率（0~1），默认为 0（所有步骤同时开始）。
    run_time : float
        每个步骤内子动画的运行时间。
    **kwargs
        传递给 AnimationGroup 的额外参数。
    """
    def __init__(self,*,
                 sf:'StructuralFormula',
                 steps:list[ElectronMigrationStep],
                 lag_ratio:float=0.0,
                 run_time:float=1.0,
                 **kwargs):

        self.sf=sf
        self.steps=steps
        self._all_sources:list[Mobject]=[]
        self._all_targets:list[Mobject]=[]
        self._all_creates:list[Mobject]=[]

        for step in steps:
            for source,target in step.replace:
                self._all_sources.append(source)
                self._all_targets.append(target)
            for obj in step.create:
                self._all_creates.append(obj)

        step_anims=[]
        for step in steps:
            sub_anims=[]
            for source,target in step.replace:
                sub_anims.append(ReplacementTransform(source,target,run_time=run_time))
            for obj in step.create:
                sub_anims.append(FadeIn(obj,run_time=run_time))
            step_anims.append(AnimationGroup(*sub_anims,lag_ratio=step.lag_ratio))

        super().__init__(*step_anims,lag_ratio=lag_ratio,**kwargs)

    def begin(self):
        """动画开始：从 StructuralFormula 中移除 source 对象（它们保留在 Scene 中）。"""
        for source in self._all_sources:
            if isinstance(source,VGroup) and not isinstance(source,(Bond,Charge)):
                for submob in source.submobjects:
                    self.sf.remove(submob)
            else:
                self.sf.remove(source)
        super().begin()

    def finish(self):
        """动画结束：将 target 和新创建的对象加入 StructuralFormula。"""
        super().finish()
        for target in self._all_targets:
            if isinstance(target,VGroup) and not isinstance(target,(Bond,Charge)):
                for submob in target.submobjects:
                    self.sf.add(submob)
            else:
                self.sf.add(target)
        for obj in self._all_creates:
            self.sf.add(obj)

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

def merging_timeline(timeline1:dict[float,list[Animation]|Animation],timeline2:dict[float,list[Animation]|Animation]):
    rslt=timeline1.copy()
    for time,anims in timeline2.items():
        if time in rslt:
            if not isinstance(rslt[time],list):
                rslt[time]=[rslt[time]]
            if not isinstance(anims,list):
                anims=[anims]
            rslt[time].extend(anims)
        else:
            rslt[time]=anims
    return rslt

def brownian_motion(items:Mobject|list,num:int,time:float=1.0):
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
