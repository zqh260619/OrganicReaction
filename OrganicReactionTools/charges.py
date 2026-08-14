"""电荷类、Charge 包装器与 ChargeType 枚举。"""

from manim import VGroup, Circle, Line, MathTex
from manim.typing import Vector3D
import numpy as np
from enum import Enum

from .attributes import AttributeHolder
from .atoms import AtomicCluster

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

class PairCharge(VGroup):
    def __init__(self,*,text:MathTex,pos:Vector3D,attributes:'AttributeHolder'):

        """孤对电子电荷：两个与 SingleCharge 形状相同的圆点。

        两个圆点中心位于电荷锚点（文本角点向外偏移 edge_charge 处）两侧，
        且两个圆点中心的连线始终垂直于文本中心到两个圆点中点的连线。
        """

        position=text.get_corner(pos)+pos*attributes.edge_charge

        direction=position-text.get_center()
        norm=np.linalg.norm(direction)
        if norm==0:
            direction=np.array(pos,dtype=float)
            norm=np.linalg.norm(direction)
        if norm==0:
            direction=np.array([1.,0.,0.])
        else:
            direction=direction/norm

        normal=np.array([-direction[1],direction[0],0])
        half=attributes.distance_pair/2

        circle1=Circle(radius=attributes.radius_single,color=attributes.color,
                       arc_center=position+normal*half,fill_opacity=1)
        circle2=Circle(radius=attributes.radius_single,color=attributes.color,
                       arc_center=position-normal*half,fill_opacity=1)

        super().__init__(circle1,circle2)

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

class PairChargeByCoordinate(VGroup):
    def __init__(self,*,position:Vector3D,direction:Vector3D,attributes:'AttributeHolder'):

        """PairCharge 的坐标版本。

        position：两个圆点的中点（电荷锚点）。
        direction：文本中心指向两个圆点中点的方向向量，
        两个圆点中心的连线始终垂直于该方向。
        """

        direction=np.array(direction,dtype=float)
        norm=np.linalg.norm(direction)
        if norm==0:
            direction=np.array([1.,0.,0.])
        else:
            direction=direction/norm

        normal=np.array([-direction[1],direction[0],0])
        half=attributes.distance_pair/2

        circle1=Circle(radius=attributes.radius_single,color=attributes.color,
                       arc_center=position+normal*half,fill_opacity=1)
        circle2=Circle(radius=attributes.radius_single,color=attributes.color,
                       arc_center=position-normal*half,fill_opacity=1)

        super().__init__(circle1,circle2)

class ChargeType(Enum):
    POSITIVE=PositiveCharge
    NEGATIVE=NegativeCharge
    SINGLE=SingleCharge
    PAIR=PairCharge
    POSITIVE_COORDINATE=PositiveChargeByCoordinate
    NEGATIVE_COORDINATE=NegativeChargeByCoordinate
    SINGLE_COORDINATE=SingleChargeByCoordinate
    PAIR_COORDINATE=PairChargeByCoordinate

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
            if charge_type==ChargeType.PAIR_COORDINATE:
                charge=self.charge_type.value(position=pos*attributes.edge_charge+text,direction=pos,attributes=attributes)
            else:
                charge=self.charge_type.value(position=pos*attributes.edge_charge+text,attributes=attributes)

        self.add(charge)
