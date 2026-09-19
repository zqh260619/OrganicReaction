"""电荷类、Charge 包装器与 ChargeType 枚举。"""

from manim import VGroup, Circle, Line
from manim.typing import Vector3D
import numpy as np
from enum import Enum

from .parameters import MathTex
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
    """孤对电子电荷：两个与 SingleCharge 形状相同的圆点。

    两个圆点中心位于电荷锚点（文本角点向外偏移 edge_charge 处）两侧，
    且两个圆点中心的连线始终垂直于文本中心到两个圆点中点的连线。
    """
    def __init__(self,*,text:MathTex,pos:Vector3D,attributes:'AttributeHolder'):

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
    """PairCharge 的坐标版本。

    position：两个圆点的中点（电荷锚点）。
    直接构造时两个圆点水平排列在 position 两侧；通过 Charge
    包装器（add_charge / build_charge）构造时，会自动旋转到
    与"原子 pos → 两圆点中点"连线垂直的方向。
    """
    def __init__(self,*,position:Vector3D,attributes:'AttributeHolder'):

        half=attributes.distance_pair/2

        circle1=Circle(radius=attributes.radius_single,color=attributes.color,
                       arc_center=position+np.array([half,0.,0.]),fill_opacity=1)
        circle2=Circle(radius=attributes.radius_single,color=attributes.color,
                       arc_center=position-np.array([half,0.,0.]),fill_opacity=1)

        super().__init__(circle1,circle2)

class PartialCharge(VGroup):
    """部分电荷：由 delta_count 个 δ 和上标正负号组成。

    使用 anchor_mode 控制文本定位方式：

    - "border"（默认）：电荷文本边框上与 pos 相反方向的点，与原子
      文本在 pos 方向的角点重合。例如 pos=UR 时，δδ+ 的左下角与
      原子文本的右上角重合。该模式忽略 edge_charge。
    - "center"：电荷文本中心位于原子文本角点向外偏移 edge_charge
      的位置，保持原有中心对齐行为。

    可通过 Charge 包装器使用：

        Charge(
            charge_type=ChargeType.PARTIAL,
            text=atom,
            pos=UR,
            attributes=attributes,
            delta_count=2,
            sign="+",
            anchor_mode="border",
        )

    Parameters
    ----------
    text : MathTex | None
        电荷所附着的原子文本（或 AtomicCluster）。
    pos : Vector3D | None
        电荷相对原子文本的方向向量，如 UR、DOWN 等。
    position : Vector3D | None
        坐标模式下电荷的位置。
    attributes : AttributeHolder
        样式属性（取 color、font_size_partial、edge_charge）。
    delta_count : int
        δ 的数目，必须为大于等于 1 的整数，默认 1。
    sign : str
        上标正负号，取 "+" 或 "-"，默认 "+"。
    anchor_mode : str
        定位模式，取 "border" 或 "center"，默认 "border"。
    """
    def __init__(self,*,
                 text:MathTex|None=None,
                 pos:Vector3D|None=None,
                 position:Vector3D|None=None,
                 attributes:'AttributeHolder',
                 delta_count:int=1,
                 sign:str="+",
                 anchor_mode:str="border"):

        if not isinstance(delta_count,int) or delta_count<1:
            raise ValueError(f"delta_count 必须为大于等于 1 的整数，实际为 {delta_count}。")
        if sign not in ("+","-"):
            raise ValueError(f"sign 只能取 '+' 或 '-'，实际为 {sign!r}。")
        if anchor_mode not in ("border","center"):
            raise ValueError(f"anchor_mode 只能取 'border' 或 'center'，实际为 {anchor_mode!r}。")
        if anchor_mode=="border" and pos is None:
            raise ValueError("anchor_mode='border' 需要提供 pos 方向。")

        if position is None:
            if text is None or pos is None:
                raise ValueError("PartialCharge 需要提供 position，或同时提供 text 与 pos。")
            corner=np.array(text.get_corner(pos),dtype=float)
            if anchor_mode=="center":
                target=corner+np.array(pos,dtype=float)*attributes.edge_charge
            else:
                target=corner
        else:
            target=np.array(position,dtype=float)

        tex_string=r"\delta"*delta_count+"^{"+sign+"}"
        font_size=attributes.font_size_partial
        charge_text=MathTex(tex_string,color=attributes.color,font_size=font_size)

        if anchor_mode=="border":
            opposite=-np.array(pos,dtype=float)
            if np.linalg.norm(opposite)==0:
                raise ValueError("anchor_mode='border' 需要非零的 pos 方向。")
            charge_text.shift(target-charge_text.get_corner(opposite))
        else:
            charge_text.move_to(target)

        super().__init__(charge_text)

        self.delta_count=delta_count
        self.sign=sign
        self.anchor_mode=anchor_mode
        self.position=target
        self.font_size=font_size
        self.charge_text=charge_text

class PartialChargeByCoordinate(PartialCharge):
    """部分电荷的坐标版本：直接以 position 指定电荷位置。

    anchor_mode="border" 时，还需要通过 pos 指定方向，用于确定
    与 position 对齐的边框点。
    """
    def __init__(self,*,
                 position:Vector3D,
                 attributes:'AttributeHolder',
                 delta_count:int=1,
                 sign:str="+",
                 anchor_mode:str="border",
                 pos:Vector3D|None=None):

        super().__init__(position=position,
                         attributes=attributes,
                         delta_count=delta_count,
                         sign=sign,
                         anchor_mode=anchor_mode,
                         pos=pos)

class ChargeType(Enum):
    POSITIVE=PositiveCharge
    NEGATIVE=NegativeCharge
    SINGLE=SingleCharge
    PAIR=PairCharge
    PARTIAL=PartialCharge
    PARTIAL_COORDINATE=PartialChargeByCoordinate
    POSITIVE_COORDINATE=PositiveChargeByCoordinate
    NEGATIVE_COORDINATE=NegativeChargeByCoordinate
    SINGLE_COORDINATE=SingleChargeByCoordinate
    PAIR_COORDINATE=PairChargeByCoordinate

class Charge(VGroup):
    def __init__(self,*,
                 charge_type:ChargeType,
                 text:AtomicCluster|Vector3D,
                 pos:Vector3D,
                 attributes:AttributeHolder,
                 atom_name:str|None=None,
                 delta_count:int=1,
                 sign:str="+",
                 anchor_mode:str="border"):

        super().__init__(color=attributes.color)

        self.charge_type=charge_type
        self.text=text
        self.atom_name=atom_name

        partial_kwargs={}
        if charge_type in (ChargeType.PARTIAL,ChargeType.PARTIAL_COORDINATE):
            partial_kwargs={"delta_count":delta_count,"sign":sign,"anchor_mode":anchor_mode}

        is_partial=charge_type in (ChargeType.PARTIAL,ChargeType.PARTIAL_COORDINATE)

        if isinstance(text,AtomicCluster):
            charge=self.charge_type.value(text=text,pos=pos,attributes=attributes,**partial_kwargs)
        else:
            if is_partial and anchor_mode=="border":
                # border 模式忽略 edge_charge，position 直接作为对齐点
                coordinate_position=np.array(text,dtype=float)
            else:
                coordinate_position=pos*attributes.edge_charge+text

            charge_kwargs=dict(partial_kwargs)
            if is_partial:
                charge_kwargs["pos"]=pos

            charge=self.charge_type.value(position=coordinate_position,
                                          attributes=attributes,**charge_kwargs)
            if charge_type==ChargeType.PAIR_COORDINATE:
                # 将默认水平取向的两圆点旋转到与"原子 pos → 两圆点中点"方向（即 pos）垂直
                charge.rotate(np.arctan2(pos[1],pos[0])+np.pi/2)

        self.add(charge)
