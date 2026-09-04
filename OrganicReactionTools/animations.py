"""动画类与电子迁移步骤描述。"""

from manim import (Animation, Mobject, VGroup, AnimationGroup,
                   ReplacementTransform, FadeIn, FadeOut, Transform,
                   smooth, linear)
from manim.typing import Vector3D
import numpy as np
from typing import Callable, Optional

from .decorations import BezierArrow
from .bonds import Bond, BondType
from .charges import Charge
from .attributes import DEFAULT_ATTRIBUTES

class ElectronMigrationStep:
    """电子迁移步骤的描述。

    Attributes
    ----------
    replace : list[tuple[Mobject, Mobject]]
        要执行的 ReplacementTransform 列表，每项为 (source, target)，按顺序播放每一项变换动画。
        多对一：将多个 source 用 VGroup 包装。
        一对多：将多个 target 用 VGroup 包装，或使用 Mobject.copy()。
    create : list[Mobject]
        要在本步骤中 FadeIn 的新 Mobject 列表。
    fadeout : list[Mobject]
        要在本步骤中 FadeOut 的 Mobject 列表。
    lag_ratio : float
        步骤内部子动画之间的延迟比率（0~1），类似 AnimationGroup.lag_ratio。
    """
    def __init__(self,*,
                 replace:list[tuple[Mobject,Mobject]]|None=None,
                 create:list[Mobject]|None=None,
                 fadeout:list[Mobject]|None=None,
                 lag_ratio:float=0.3):
        self.replace=replace or []
        self.create=create or []
        self.fadeout=fadeout or []
        self.lag_ratio=lag_ratio

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
            # 与 Bond 包装器的契约一致：虚键按两端点真实距离重建
            sp=start+dv*attrs.edge_global*se
            ep=start+dv*(float(np.linalg.norm(angle_vector))-attrs.edge_global*ee)
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
        步骤之间的延迟比率（0~1），默认为 0.3。
    run_time : float
        每个步骤内子动画的运行时间。
    sync : bool
        动画结束后是否自动同步元数据（默认 True）：
        源/淡出的键与电荷自动注销，带标签的目标/新建键与电荷自动登记，
        无法自动同步的对象打印警告并收集到 ``unsynced``。
    **kwargs
        传递给 AnimationGroup 的额外参数。
    """
    def __init__(self,*,
                 sf:'StructuralFormula',
                 steps:list[ElectronMigrationStep],
                 lag_ratio:float=0.3,
                 run_time:float=1.0,
                 sync:bool=True,
                 **kwargs):

        self.sf=sf
        self.steps=steps
        self.sync=sync
        self.unsynced:list[Mobject]=[]
        self._all_sources:list[Mobject]=[]
        self._all_targets:list[Mobject]=[]
        self._all_creates:list[Mobject]=[]
        self._all_fadeouts:list[Mobject]=[]

        for step in steps:
            for source,target in step.replace:
                self._all_sources.append(source)
                self._all_targets.append(target)
            for obj in step.create:
                self._all_creates.append(obj)
            for obj in step.fadeout:
                self._all_fadeouts.append(obj)

        step_anims=[]
        for step in steps:
            sub_anims=[]
            for source,target in step.replace:
                sub_anims.append(ReplacementTransform(source,target,run_time=run_time))
            for obj in step.create:
                sub_anims.append(FadeIn(obj,run_time=run_time))
            for obj in step.fadeout:
                sub_anims.append(FadeOut(obj,run_time=run_time))
            step_anims.append(AnimationGroup(*sub_anims,lag_ratio=step.lag_ratio))

        super().__init__(*step_anims,lag_ratio=lag_ratio,**kwargs)

    def begin(self):
        """动画开始：从 StructuralFormula 中移除 source 和 fadeout 对象（它们保留在 Scene 中）。"""
        for source in self._all_sources:
            if isinstance(source,VGroup) and not isinstance(source,(Bond,Charge)):
                for submob in source.submobjects:
                    self.sf.remove(submob)
            else:
                self.sf.remove(source)
        for obj in self._all_fadeouts:
            if isinstance(obj,VGroup) and not isinstance(obj,(Bond,Charge)):
                for submob in obj.submobjects:
                    self.sf.remove(submob)
            else:
                self.sf.remove(obj)
        super().begin()

    def finish(self):
        """动画结束：将 target 和新创建的对象加入 StructuralFormula，
        并在 sync=True 时自动同步元数据字典。"""
        super().finish()
        for target in self._all_targets:
            if isinstance(target,VGroup) and not isinstance(target,(Bond,Charge)):
                for submob in target.submobjects:
                    self.sf.add(submob)
            else:
                self.sf.add(target)
        for obj in self._all_creates:
            self.sf.add(obj)
        if self.sync:
            self.unsynced=self.sf.sync_migration(self.steps)
