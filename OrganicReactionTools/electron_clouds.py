"""电子云图形类、ElectronCloud 包装器与 ElectronCloudType 枚举。"""

from manim import VGroup, Circle, Ellipse, ParametricFunction, WHITE, ORIGIN, PI, TAU, ManimColor
from manim.typing import Vector3D
import numpy as np
from enum import Enum

from .attributes import AttributeHolder, DEFAULT_ATTRIBUTES
from .parameters import (electron_cloud_length, electron_cloud_width,
                         electron_cloud_radius, electron_cloud_small_ratio)

def _resolve_color(*,attributes:'AttributeHolder'=None,color:ManimColor|None=None)->ManimColor:
    if color is not None:
        return color
    if attributes is not None:
        return attributes.color
    return WHITE

def _direction_frame(direction:float)->tuple[np.ndarray,np.ndarray]:
    direction_vector=np.array([np.cos(direction),np.sin(direction),0])
    normal_vector=np.array([-np.sin(direction),np.cos(direction),0])
    return direction_vector,normal_vector

def _build_ellipse(*,center:Vector3D,direction:float,length:float,width:float,
                   color:ManimColor,stroke_width:float,**kwargs)->Ellipse:
    ellipse=Ellipse(width=length,height=width,color=color,stroke_width=stroke_width,**kwargs)
    ellipse.rotate(direction)
    ellipse.move_to(center)
    return ellipse

#Mobject classes
class OvalLine(ParametricFunction):
    """卵形线：单瓣电子云轮廓。

    尖端（较窄的一端）位于 center，圆端沿 direction 方向延伸 length。
    width 为垂直于 direction 方向的最大宽度。sharpness 控制卵形的
    不对称程度：越接近 1，尖端越明显；越接近 0，形状越接近沿
    direction 方向平移的圆，但必须满足 0 < sharpness < 1。

    Parameters
    ----------
    center : Vector3D
        尖端所在位置（通常为原子核或轨道节点）。
    direction : float
        圆端相对尖端的方向角（弧度）。
    length : float
        尖端到圆端的长度。
    width : float
        垂直于 direction 方向的最大宽度。
    sharpness : float
        卵形线不对称程度，范围 (0, 1)，默认 0.6。
    color : ManimColor | None
        曲线颜色；默认取 attributes.color，其次为 WHITE。
    stroke_width : float
        曲线线宽，默认 2。
    attributes : AttributeHolder | None
        样式属性，仅用于缺省颜色。
    **kwargs
        传递给 ParametricFunction 的额外参数。
    """
    def __init__(self,*,
                 center:Vector3D=ORIGIN,
                 direction:float=0,
                 length:float=electron_cloud_length,
                 width:float=electron_cloud_width,
                 sharpness:float=0.6,
                 color:ManimColor|None=None,
                 stroke_width:float=2,
                 attributes:'AttributeHolder'=None,
                 use_smoothing:bool=False,
                 **kwargs):

        if length<=0:
            raise ValueError(f"length 必须大于 0，实际为 {length}。")
        if width<=0:
            raise ValueError(f"width 必须大于 0，实际为 {width}。")
        if not 0<sharpness<1:
            raise ValueError(f"sharpness 必须在 (0, 1) 内，实际为 {sharpness}。")

        center=np.array(center,dtype=float)
        color=_resolve_color(attributes=attributes,color=color)
        direction_vector,normal_vector=_direction_frame(direction)

        # 先构造 x 范围为 [0,1]、y 范围为 [-0.5,0.5] 的基准卵形线，
        # 再分别缩放到指定的 length 与 width，使两个尺寸参数互相独立。
        c=0.5
        a=c*sharpness
        cos_peak=(-c+np.sqrt(c*c+8*a*a))/(4*a)
        sin_peak=np.sqrt(max(0.,1-cos_peak*cos_peak))
        half_width=(c+a*cos_peak)*sin_peak

        def egg_curve(t):
            r=c+a*np.cos(t)
            x=(r*np.cos(t)+(c-a))*length
            y=r*np.sin(t)/(2*half_width)*width
            return center+x*direction_vector+y*normal_vector

        super().__init__(egg_curve,t_range=[0,TAU],color=color,stroke_width=stroke_width,
                         use_smoothing=use_smoothing,**kwargs)

        self.center_point=center
        self.direction=direction
        self.length=length
        self.lobe_width=width
        self.sharpness=sharpness

class SOrbital(Circle):
    """s 轨道电子云：以 center 为圆心的圆。"""
    def __init__(self,*,
                 center:Vector3D=ORIGIN,
                 direction:float=0,
                 radius:float=electron_cloud_radius,
                 color:ManimColor|None=None,
                 stroke_width:float=2,
                 attributes:'AttributeHolder'=None,
                 **kwargs):

        center=np.array(center,dtype=float)
        color=_resolve_color(attributes=attributes,color=color)

        super().__init__(radius=radius,color=color,arc_center=center,stroke_width=stroke_width,**kwargs)

        self.center_point=center
        self.direction=direction  # 圆形各向同性，direction 仅为统一接口而保留
        self.radius=radius

class POrbital(VGroup):
    """p 轨道电子云：沿 direction 方向相反的两瓣等大卵形线。"""
    def __init__(self,*,
                 center:Vector3D=ORIGIN,
                 direction:float=0,
                 length:float=electron_cloud_length,
                 width:float=electron_cloud_width,
                 color:ManimColor|None=None,
                 stroke_width:float=2,
                 attributes:'AttributeHolder'=None,
                 **kwargs):

        center=np.array(center,dtype=float)
        color=_resolve_color(attributes=attributes,color=color)

        super().__init__(color=color)

        self.positive_lobe=OvalLine(center=center,direction=direction,length=length,width=width,
                                    color=color,stroke_width=stroke_width,attributes=attributes,**kwargs)
        self.negative_lobe=OvalLine(center=center,direction=direction+PI,length=length,width=width,
                                    color=color,stroke_width=stroke_width,attributes=attributes,**kwargs)
        self.add(self.positive_lobe,self.negative_lobe)

        self.center_point=center
        self.direction=direction
        self.length=length
        self.lobe_width=width

class DOrbitalLobe(OvalLine):
    """d 轨道的一瓣：尖端位于 center 的卵形线。"""

class HybridOrbital(VGroup):
    """sp 杂化轨道：沿 direction 的大瓣与反方向的小瓣两条卵形线。

    sp、sp2、sp3 杂化轨道的单瓣形状相同，差别主要体现在空间取向；
    本类只描述单个杂化轨道本身，小瓣尺寸为大瓣乘以 small_ratio。

    Parameters
    ----------
    center : Vector3D
        两瓣尖端所在位置（原子核）。
    direction : float
        大瓣圆端的方向角（弧度）。
    length : float
        大瓣长度。
    width : float
        大瓣宽度。
    small_ratio : float
        小瓣与大瓣的长度、宽度比例，默认 0.5。
    color : ManimColor | None
        曲线颜色；默认取 attributes.color，其次为 WHITE。
    stroke_width : float
        曲线线宽，默认 2。
    attributes : AttributeHolder | None
        样式属性，仅用于缺省颜色。
    **kwargs
        传递给两条 OvalLine 的额外参数。
    """
    def __init__(self,*,
                 center:Vector3D=ORIGIN,
                 direction:float=0,
                 length:float=electron_cloud_length,
                 width:float=electron_cloud_width,
                 small_ratio:float=electron_cloud_small_ratio,
                 color:ManimColor|None=None,
                 stroke_width:float=2,
                 attributes:'AttributeHolder'=None,
                 **kwargs):

        if small_ratio<=0:
            raise ValueError(f"small_ratio 必须大于 0，实际为 {small_ratio}。")

        center=np.array(center,dtype=float)
        color=_resolve_color(attributes=attributes,color=color)

        super().__init__(color=color)

        self.large_lobe=OvalLine(center=center,direction=direction,length=length,width=width,
                                 color=color,stroke_width=stroke_width,attributes=attributes,**kwargs)
        self.small_lobe=OvalLine(center=center,direction=direction+PI,
                                 length=length*small_ratio,width=width*small_ratio,
                                 color=color,stroke_width=stroke_width,attributes=attributes,**kwargs)
        self.add(self.large_lobe,self.small_lobe)

        self.center_point=center
        self.direction=direction
        self.length=length
        self.lobe_width=width
        self.small_ratio=small_ratio

class SPOrbital(HybridOrbital):
    """sp 杂化轨道。"""

class SP2Orbital(HybridOrbital):
    """sp2 杂化轨道。"""

class SP3Orbital(HybridOrbital):
    """sp3 杂化轨道。"""

class SigmaBondSS(Ellipse):
    """s-s sigma 成键轨道：以 center 为中心的椭圆。

    椭圆长轴沿 direction，长度为 length；短轴垂直于 direction，
    长度为 width。
    """
    def __init__(self,*,
                 center:Vector3D=ORIGIN,
                 direction:float=0,
                 length:float=electron_cloud_length,
                 width:float=0.4,
                 color:ManimColor|None=None,
                 stroke_width:float=2,
                 attributes:'AttributeHolder'=None,
                 **kwargs):

        center=np.array(center,dtype=float)
        color=_resolve_color(attributes=attributes,color=color)

        super().__init__(width=length,height=width,color=color,stroke_width=stroke_width,**kwargs)

        self.rotate(direction)
        self.move_to(center)

        self.center_point=center
        self.direction=direction
        self.length=length
        self.ellipse_width=width

class SigmaAntiBondSSLobe(OvalLine):
    """s-s sigma 反键轨道的一瓣：尖端位于 center 的卵形线。"""

class SigmaAntiBondSS(SigmaAntiBondSSLobe):
    """s-s sigma 反键轨道（按需求仅绘制其中一瓣）。"""

class SigmaBondPP(VGroup):
    """p-p sigma 成键轨道：中部椭圆与外侧两瓣卵形线。

    中部椭圆长轴沿 direction，外侧两瓣的尖端分别接在椭圆两端，
    圆端继续沿 direction 向外延伸。
    """
    def __init__(self,*,
                 center:Vector3D=ORIGIN,
                 direction:float=0,
                 middle_length:float=electron_cloud_length,
                 middle_width:float=0.4,
                 lobe_length:float=0.5,
                 lobe_width:float=0.4,
                 color:ManimColor|None=None,
                 stroke_width:float=2,
                 attributes:'AttributeHolder'=None,
                 **kwargs):

        center=np.array(center,dtype=float)
        color=_resolve_color(attributes=attributes,color=color)
        direction_vector,_=_direction_frame(direction)

        super().__init__(color=color)

        self.middle=_build_ellipse(center=center,direction=direction,length=middle_length,width=middle_width,
                                   color=color,stroke_width=stroke_width,**kwargs)
        left_center=center-direction_vector*middle_length/2
        right_center=center+direction_vector*middle_length/2
        self.left_lobe=OvalLine(center=left_center,direction=direction+PI,length=lobe_length,width=lobe_width,
                                color=color,stroke_width=stroke_width,attributes=attributes,**kwargs)
        self.right_lobe=OvalLine(center=right_center,direction=direction,length=lobe_length,width=lobe_width,
                                 color=color,stroke_width=stroke_width,attributes=attributes,**kwargs)
        self.add(self.middle,self.left_lobe,self.right_lobe)

        self.center_point=center
        self.direction=direction
        self.middle_length=middle_length
        self.middle_width=middle_width
        self.lobe_length=lobe_length
        self.lobe_width=lobe_width

class SigmaBondSP(HybridOrbital):
    """s-p sigma 成键轨道：大瓣沿 direction、小瓣沿反方向的两条卵形线。"""

class PiBondPP(VGroup):
    """p-p pi 成键轨道：沿 direction 上下对称的两个扁椭圆。"""
    def __init__(self,*,
                 center:Vector3D=ORIGIN,
                 direction:float=0,
                 length:float=electron_cloud_length,
                 width:float=0.25,
                 offset:float=0.35,
                 color:ManimColor|None=None,
                 stroke_width:float=2,
                 attributes:'AttributeHolder'=None,
                 **kwargs):

        center=np.array(center,dtype=float)
        color=_resolve_color(attributes=attributes,color=color)
        direction_vector,normal_vector=_direction_frame(direction)

        super().__init__(color=color)

        self.upper_ellipse=_build_ellipse(center=center+normal_vector*offset,direction=direction,
                                          length=length,width=width,color=color,stroke_width=stroke_width,**kwargs)
        self.lower_ellipse=_build_ellipse(center=center-normal_vector*offset,direction=direction,
                                          length=length,width=width,color=color,stroke_width=stroke_width,**kwargs)
        self.add(self.upper_ellipse,self.lower_ellipse)

        self.center_point=center
        self.direction=direction
        self.length=length
        self.ellipse_width=width
        self.offset=offset

class PiAntiBondPP(VGroup):
    """p-p pi 反键轨道：四个倾斜的卵形线。

    四个卵形线的尖端分别位于 direction 轴线上距 center ±separation/2
    处，并按 tilt_angle 向轴两侧倾斜，形成上下两对反相瓣。
    """
    def __init__(self,*,
                 center:Vector3D=ORIGIN,
                 direction:float=0,
                 separation:float=electron_cloud_length,
                 lobe_length:float=0.6,
                 lobe_width:float=0.4,
                 tilt_angle:float=np.pi/4,
                 color:ManimColor|None=None,
                 stroke_width:float=2,
                 attributes:'AttributeHolder'=None,
                 **kwargs):

        center=np.array(center,dtype=float)
        color=_resolve_color(attributes=attributes,color=color)
        direction_vector,_=_direction_frame(direction)

        super().__init__(color=color)

        self.lobes=[]
        for side in (1,-1):
            lobe_center=center+side*direction_vector*separation/2
            base_direction=0 if side==1 else PI
            for sign in (1,-1):
                lobe=OvalLine(center=lobe_center,direction=base_direction+sign*tilt_angle,
                              length=lobe_length,width=lobe_width,
                              color=color,stroke_width=stroke_width,attributes=attributes,**kwargs)
                self.lobes.append(lobe)
                self.add(lobe)

        self.center_point=center
        self.direction=direction
        self.separation=separation
        self.lobe_length=lobe_length
        self.lobe_width=lobe_width
        self.tilt_angle=tilt_angle

class ElectronCloudType(Enum):
    S_ORBITAL=SOrbital
    P_ORBITAL=POrbital
    D_ORBITAL_LOBE=DOrbitalLobe
    HYBRID_ORBITAL=HybridOrbital
    SP_ORBITAL=SPOrbital
    SP2_ORBITAL=SP2Orbital
    SP3_ORBITAL=SP3Orbital
    SIGMA_BOND_SS=SigmaBondSS
    SIGMA_ANTIBOND_SS=SigmaAntiBondSS
    SIGMA_BOND_PP=SigmaBondPP
    SIGMA_BOND_SP=SigmaBondSP
    PI_BOND_PP=PiBondPP
    PI_ANTIBOND_PP=PiAntiBondPP

class ElectronCloud(VGroup):
    """电子云图形包装器。

    与 Bond、Charge 的包装方式一致：ElectronCloudType 枚举保存具体
    图形类，包装器负责记录 center、direction 等元数据并把生成的
    图形加入自身。中心与方向是全部电子云图形的公共参数，其余几何
    参数（radius、length、width 等）通过 **kwargs 传给具体图形类。

    Parameters
    ----------
    cloud_type : ElectronCloudType
        电子云类型。
    center : Vector3D
        轨道中心（对单瓣图形为尖端位置，对椭圆为椭圆中心）。
    direction : float
        轨道主轴方向角（弧度）。
    attributes : AttributeHolder
        样式属性（取 color）。
    **kwargs
        传递给 cloud_type 对应图形类的额外几何或样式参数。
    """
    def __init__(self,*,
                 cloud_type:ElectronCloudType,
                 center:Vector3D=ORIGIN,
                 direction:float=0,
                 attributes:'AttributeHolder'=DEFAULT_ATTRIBUTES,
                 **kwargs):

        color=kwargs.pop("color",None)
        color=_resolve_color(attributes=attributes,color=color)

        super().__init__(color=color)

        self.cloud_type=cloud_type
        self.center_point=np.array(center,dtype=float)
        self.direction=direction
        self.cloud=cloud_type.value(center=self.center_point,direction=self.direction,
                                    color=color,attributes=attributes,**kwargs)
        self.add(self.cloud)
