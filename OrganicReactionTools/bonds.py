"""化学键类、Bond 包装器、BondType 枚举与键查找器 BondLookup。"""

from manim import Polygon, VGroup, Line, DashedLine
from manim.typing import Vector3D
import numpy as np
from enum import Enum

from .attributes import AttributeHolder
from .atoms import AtomicCluster

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

class BondType(Enum):
    NORMAL_BOND=NormalBond
    IN_BOND=InBond
    OUT_BOND=OutBond
    DASHED_BOND=DashedBond
    DOUBLE_BOND=DoubleBond
    TRIPLE_BOND=TripleBond

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
                 end_side_edge:bool|None=None,
                 atom1:str|None=None,
                 atom2:str|None=None):

        super().__init__(color=attributes.color)

        self.bond_type=bond_type
        self.start=start
        self.end=end
        if isinstance(start,AtomicCluster):
            self.start=start.atom_pos  # 键端点取原子锚点，不受 text_offset 影响
        if isinstance(end,AtomicCluster):
            self.end=end.atom_pos
        self.start_edge=start_edge
        self.end_edge=end_edge
        self.side=side
        self.start_side_edge=start_side_edge
        self.end_side_edge=end_side_edge
        self.atom1=atom1
        self.atom2=atom2
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


class BondLookup:
    """键查找器：查询 StructuralFormula 中原子之间的化学键。

    绑定到一个 StructuralFormula，所有查询都以其中的
    ``atomic_clusters[name][Bond]`` 键列表为唯一事实来源，
    键对象按身份比较。通常无需直接构造，可通过
    ``StructuralFormula.bond_lookup`` 属性访问。

    Parameters
    ----------
    sf : StructuralFormula
        被查询的结构式对象。
    """

    def __init__(self, sf: 'StructuralFormula'):
        self.sf = sf

    def _bonds_of(self, name: str) -> list[Bond]:
        if name not in self.sf.atomic_clusters:
            raise ValueError(f"原子 '{name}' 不存在于结构中。")
        return self.sf.atomic_clusters[name][Bond]

    def between(self, start: str, end: str) -> Bond:
        """返回两原子之间的键；若不存在则抛出 ValueError。"""
        bond = self.between_or_none(start, end)
        if bond is None:
            raise ValueError(f"原子 '{start}' 与 '{end}' 之间不存在键。")
        return bond

    def between_or_none(self, start: str, end: str) -> Bond | None:
        """返回两原子之间的键；若不存在则返回 None。"""
        if start == end:
            return None
        start_bonds = self._bonds_of(start)
        end_bonds = self._bonds_of(end)
        for bond in start_bonds:
            if bond in end_bonds:
                return bond
        return None

    def is_bonded(self, start: str, end: str) -> bool:
        """判断两原子之间是否存在键。"""
        return self.between_or_none(start, end) is not None

    def type_between(self, start: str, end: str) -> BondType:
        """返回两原子之间的键类型；若不存在则抛出 ValueError。"""
        return self.between(start, end).bond_type

    def bonds(self, name: str) -> list[Bond]:
        """返回某原子的全部键（副本列表）。"""
        return list(self._bonds_of(name))

    def of_type(self, name: str, bond_type: BondType) -> list[Bond]:
        """返回某原子指定类型的全部键。"""
        return [bond for bond in self._bonds_of(name) if bond.bond_type == bond_type]

    def find(self,
             start: str | None = None,
             end: str | None = None,
             bond_type: BondType | None = None) -> Bond | None:
        """按条件查找第一个匹配的键；找不到返回 None。

        start 与 end 至少提供其一（提供后分别要求键与该原子相连），
        bond_type 为可选的键类型过滤。
        """
        if start is None and end is None:
            raise ValueError("find 至少需要提供 start 或 end。")
        if start is not None:
            start_bonds = self._bonds_of(start)
        else:
            start_bonds = None
        if end is not None:
            end_bonds = self._bonds_of(end)
        else:
            end_bonds = None

        candidates = start_bonds if start_bonds is not None else end_bonds
        for bond in candidates:
            if start_bonds is not None and bond not in start_bonds:
                continue
            if end_bonds is not None and bond not in end_bonds:
                continue
            if bond_type is not None and bond.bond_type != bond_type:
                continue
            return bond
        return None

    def all_bonds(self) -> list[Bond]:
        """返回整个结构中去重后的全部键（按首次出现的顺序）。"""
        seen = set()
        result = []
        for data in self.sf.atomic_clusters.values():
            for bond in data[Bond]:
                if id(bond) not in seen:
                    seen.add(id(bond))
                    result.append(bond)
        return result
