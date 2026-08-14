"""结构式 StructuralFormula。"""

from manim import VGroup, Mobject, Animation, FadeOut, WHITE, smooth
from manim.typing import Vector3D
import numpy as np
from typing import Callable

from .parameters import bond_length, ratio_transition_state, edge, txt_size, default_charge_edge
from .attributes import AttributeHolder
from .atoms import AtomicCluster
from .bonds import Bond, BondType
from .charges import Charge, ChargeType
from .animations import RotateAtoms, ElectronMigration, ElectronMigrationStep

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
                 distance_pair=0.1,
                 distance_double=0.12,
                 edge_ratio_double=0.08,
                 distance_triple=0.12,
                 name:str|None=None,
                 pos:Vector3D|None=None,
                 text:str|None=None,
                 text_offset:Vector3D=np.array([0,0,0]),
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
                                        distance_pair=distance_pair,
                                        distance_double=distance_double,
                                        edge_ratio_double=edge_ratio_double,
                                        distance_triple=distance_triple)

        super().__init__(color=self.attributes.color)

        self.atomic_clusters={}

        if name is not None:
            if text!=None:
                self.atomic_clusters[name]={Mobject:AtomicCluster(text=text,pos=pos,attributes=self.attributes,
                                                                  text_offset=text_offset),
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
                 end_side_edge:bool|None=None,
                 text_offset:Vector3D=np.array([0,0,0])):

        if name in self.atomic_clusters:
            raise ValueError(f"原子 '{name}' 已经存在于结构中，不能重复添加。")

        if not self.atomic_clusters:
            if pos is None:
                raise ValueError("向空结构式添加第一个原子时必须提供 pos 参数。")
            if text is not None:
                self.atomic_clusters[name]={Mobject:AtomicCluster(text=text,pos=pos,attributes=self.attributes,
                                                                  text_offset=text_offset),
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
            self.atomic_clusters[name]={Mobject:AtomicCluster(text=text,pos=pos,attributes=self.attributes,
                                                              text_offset=text_offset),
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

    def register_atom(self,*,
                      name:str,
                      mobject:Mobject,
                      adjacency:str|None=None,
                      bond_type:BondType|None=None,
                      side:int|None=None,
                      start_side_edge:bool|None=None,
                      end_side_edge:bool|None=None):
        """将已存在的 Mobject 注册为结构式的原子。

        与 add_atom 不同，此方法接受外部已创建的 Mobject 作为原子对象，
        而不是内部创建新的 AtomicCluster。适用于将独立创建的结构部件
        （如亲电试剂 E⁺）整合到结构式中，以便参与电子迁移动画。

        Parameters
        ----------
        name : str
            新原子的名称，需唯一。
        mobject : Mobject
            已存在的 Mobject 对象，作为原子的显示文本。
        adjacency : str | None
            邻接原子的名称。若为 None，则不创建键（独立原子）。
        bond_type : BondType | None
            与邻接原子之间的键类型。仅在提供 adjacency 时有效，
            默认为 BondType.NORMAL_BOND。
        side : int | None
            双键的左右不对称参数（仅对 DOUBLE_BOND 有效）。
        start_side_edge : bool | None
            起始端是否使用 side 边距。
        end_side_edge : bool | None
            终止端是否使用 side 边距。
        """
        if name in self.atomic_clusters:
            raise ValueError(f"原子 '{name}' 已经存在于结构中，不能重复添加。")

        pos=np.array(mobject.get_center(),dtype=float)

        self.atomic_clusters[name]={
            Mobject:mobject,
            "pos":pos,
            "adj":[],
            Bond:[]
        }

        if adjacency is not None:
            if adjacency not in self.atomic_clusters:
                raise ValueError(f"邻接原子 '{adjacency}' 不存在于结构中。")
            if bond_type is None:
                bond_type=BondType.NORMAL_BOND

            bond=Bond(bond_type=bond_type,
                      start=self.atomic_clusters[adjacency][Mobject] or self.atomic_clusters[adjacency]["pos"],
                      end=mobject,
                      start_edge=(self.atomic_clusters[adjacency][Mobject]!=None),
                      end_edge=True,
                      attributes=self.attributes,
                      side=side,
                      start_side_edge=start_side_edge,
                      end_side_edge=end_side_edge)

            self.atomic_clusters[name][Bond].append(bond)
            self.atomic_clusters[name]["adj"].append(adjacency)
            self.atomic_clusters[adjacency][Bond].append(bond)
            self.atomic_clusters[adjacency]["adj"].append(name)
            self.add(bond)

        self.add(mobject)

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

    def delete_charge(self,*,
                      text:str,
                      anim:type[Animation]=FadeOut)->Animation:

        if text not in self.atomic_clusters:
            raise ValueError(f"原子 '{text}' 不存在于结构中。")
        if text not in self.charges:
            raise ValueError(f"原子 '{text}' 上不存在电荷。")

        charge=self.charges[text]
        self.remove(charge)
        self.charges.pop(text)

        return anim(charge)

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
                           lag_ratio:float=0.3,
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
