"""电子云图形类、ElectronCloud 包装器与 ElectronCloudType 枚举。"""

from manim import (VGroup, Circle, Ellipse, ParametricFunction, Mobject,
                   WHITE, ORIGIN, PI, TAU, ManimColor, UL, UR, DL, DR)
from manim.typing import Vector3D
import numpy as np
from enum import Enum

from .attributes import AttributeHolder, DEFAULT_ATTRIBUTES
from .parameters import (electron_cloud_length, electron_cloud_width,
                         electron_cloud_radius, electron_cloud_small_ratio)

_ATOMIC_TEXT_BUFF=0.06
_DEFAULT_TEXT_BUFF=0.15
_DEFAULT_CURVE_GAP=0.05

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

def _text_radius(text:Mobject|None,text_buff:float)->float:
    if text is None:
        return 0.
    return 0.5*np.hypot(float(text.width),float(text.height))+text_buff

def _resolve_center(center:Vector3D|None,text:Mobject|None)->np.ndarray:
    if center is not None:
        return np.array(center,dtype=float)
    if text is not None:
        return np.array(text.get_center(),dtype=float)
    return np.array(ORIGIN,dtype=float)

def _lift_text(text:Mobject|None)->None:
    if text is None:
        return
    try:
        text.set_z_index(2)
    except AttributeError:
        pass

def _clean_style_kwargs(kwargs:dict)->dict:
    kwargs=dict(kwargs)
    for key in ("fill_opacity","stroke_opacity","fill_color","stroke_color"):
        kwargs.pop(key,None)
    return kwargs

def _style_lobe(lobe:Mobject,color:ManimColor,opacity:float)->Mobject:
    lobe.set_stroke(color=color,opacity=opacity)
    lobe.set_fill(color=color,opacity=opacity)
    return lobe

def _resolve_lobe_styles(*,lobe_count:int,color:ManimColor|None,opacity:float,
                         lobe_colors:list[ManimColor|None]|None,
                         lobe_opacities:list[float|None]|None,
                         attributes:'AttributeHolder'=None)->tuple[list[ManimColor],list[float]]:

    if not 0<=opacity<=1:
        raise ValueError(f"opacity 必须在 [0, 1] 内，实际为 {opacity}。")

    base_color=_resolve_color(attributes=attributes,color=color)
    if lobe_colors is None:
        colors=[base_color]*lobe_count
    else:
        if len(lobe_colors)!=lobe_count:
            raise ValueError(f"lobe_colors 必须提供 {lobe_count} 个颜色，实际为 {len(lobe_colors)} 个。")
        colors=[base_color if item is None else item for item in lobe_colors]

    if lobe_opacities is None:
        opacities=[opacity]*lobe_count
    else:
        if len(lobe_opacities)!=lobe_count:
            raise ValueError(f"lobe_opacities 必须提供 {lobe_count} 个透明度，实际为 {len(lobe_opacities)} 个。")
        opacities=[opacity if item is None else item for item in lobe_opacities]
        for item in opacities:
            if not 0<=item<=1:
                raise ValueError(f"lobe_opacities 中的透明度必须在 [0, 1] 内，实际为 {item}。")

    return colors,opacities

def _lobe_defaults(*,text:Mobject|None,text_buff:float,base_length:float,base_width:float)->tuple[float,float]:
    radius=_text_radius(text,text_buff)
    return max(base_length,2*radius),max(base_width,1.5*radius)

def _ellipse_defaults(*,text:Mobject|None,text_buff:float,base_length:float,base_width:float)->tuple[float,float]:
    radius=_text_radius(text,text_buff)
    return max(base_length,2*radius),max(base_width,2*radius)

def _separation_default(*,text:Mobject|None,text_buff:float,base:float)->float:
    return max(base,2*_text_radius(text,text_buff))

def _axis_half_extent(text:Mobject|None,direction_vector:np.ndarray,text_buff:float)->float:
    if text is None:
        return 0.
    corners=np.array([
        text.get_corner(UL),text.get_corner(UR),
        text.get_corner(DL),text.get_corner(DR),
    ])
    values=corners@direction_vector
    return 0.5*(values.max()-values.min())+text_buff

def _normal_half_extent(text:Mobject|None,normal_vector:np.ndarray,text_buff:float)->float:
    if text is None:
        return 0.
    corners=np.array([
        text.get_corner(UL),text.get_corner(UR),
        text.get_corner(DL),text.get_corner(DR),
    ])
    values=corners@normal_vector
    return 0.5*(values.max()-values.min())+text_buff

def _two_text_frame(text1:Mobject|None,text2:Mobject|None,direction:float|None,text_buff:float):
    if text1 is None and text2 is None:
        return None
    if text1 is None or text2 is None:
        raise ValueError("成键轨道与反键轨道必须同时提供 text1 和 text2 两个文本标签。")

    center1=np.array(text1.get_center(),dtype=float)
    center2=np.array(text2.get_center(),dtype=float)
    center_point=(center1+center2)/2
    if direction is None:
        bond_vector=center2-center1
        bond_length=np.linalg.norm(bond_vector)
        if bond_length<1e-9:
            raise ValueError("text1 与 text2 的中心不能重合。")
        direction=np.arctan2(bond_vector[1],bond_vector[0])
    direction_vector,normal_vector=_direction_frame(direction)

    pos1=float(np.dot(center1-center_point,direction_vector))
    pos2=float(np.dot(center2-center_point,direction_vector))
    if pos1<=pos2:
        start_pos,start_text,end_pos,end_text=pos1,text1,pos2,text2
    else:
        start_pos,start_text,end_pos,end_text=pos2,text2,pos1,text1

    start_axis_half=_axis_half_extent(start_text,direction_vector,text_buff)
    end_axis_half=_axis_half_extent(end_text,direction_vector,text_buff)
    start_normal_half=_normal_half_extent(start_text,normal_vector,text_buff)
    end_normal_half=_normal_half_extent(end_text,normal_vector,text_buff)

    frame={
        "center_point":center_point,
        "direction":direction,
        "direction_vector":direction_vector,
        "normal_vector":normal_vector,
        "start_text":start_text,
        "end_text":end_text,
        "start_pos":start_pos,
        "end_pos":end_pos,
        "start_axis_half":start_axis_half,
        "end_axis_half":end_axis_half,
        "start_normal_half":start_normal_half,
        "end_normal_half":end_normal_half,
        "start_inner":start_pos+start_axis_half,
        "end_inner":end_pos-end_axis_half,
        "start_outer":start_pos-start_axis_half,
        "end_outer":end_pos+end_axis_half,
        "inner_gap":end_pos-end_axis_half-(start_pos+start_axis_half),
        "max_axis_half":max(start_axis_half,end_axis_half),
        "max_normal_half":max(start_normal_half,end_normal_half),
    }
    return frame

def _inner_ellipse_geometry(frame):
    """返回两个文本标签之间用于放置椭圆的中心位置与长轴长度。"""
    if frame is None:
        return None
    left=frame["start_inner"]+_DEFAULT_CURVE_GAP
    right=frame["end_inner"]-_DEFAULT_CURVE_GAP
    length=max(_DEFAULT_CURVE_GAP,right-left)
    pos=0.5*(left+right)
    return pos,length

def _build_ellipse(*,center:Vector3D,direction:float,length:float,width:float,
                   color:ManimColor,opacity:float,stroke_width:float,**kwargs)->Ellipse:
    kwargs=_clean_style_kwargs(kwargs)
    ellipse=Ellipse(width=length,height=width,color=color,stroke_width=stroke_width,
                    fill_opacity=opacity,stroke_opacity=opacity,**kwargs)
    ellipse.rotate(direction)
    ellipse.move_to(center)
    _style_lobe(ellipse,color,opacity)
    return ellipse

def _outward_oval_lobe(*,reference_center:Vector3D,tip:Vector3D,outward_direction:float,
                       length:float,width:float,color:ManimColor,opacity:float,
                       stroke_width:float,text_buff:float=0.,**kwargs)->'OvalLine':
    """创建尖端朝内、圆端朝外的卵形线，并在构造时校验方向。"""
    lobe=OvalLine(center=tip,direction=outward_direction,length=length,width=width,
                  color=color,opacity=opacity,stroke_width=stroke_width,
                  text=None,text_buff=text_buff,**kwargs)
    reference=np.array(reference_center,dtype=float)
    tip_distance=float(np.linalg.norm(lobe.tip_point-reference))
    round_end_distance=float(np.linalg.norm(lobe.round_end_point-reference))
    if round_end_distance<=tip_distance+1e-9:
        raise ValueError("卵形线必须尖端朝里、圆端朝外，请检查 outward_direction 参数。")
    return lobe

#Mobject classes
class OvalLine(ParametricFunction):
    """卵形线：单瓣电子云轮廓。

    尖端（较窄的一端）位于 center 或文本标签外侧，圆端沿 direction
    方向延伸。width 为垂直于 direction 方向的最大宽度。默认
    sharpness=0.4 保证整条曲线为凸曲线，圆端与尖端均无凹陷。

    Parameters
    ----------
    center : Vector3D | None
        尖端所在位置；缺省时取 text 中心。
    direction : float
        圆端相对尖端的方向角（弧度）。
    length : float | None
        尖端到圆端的长度；缺省时根据文本标签大小自动调整。
    width : float | None
        垂直于 direction 方向的最大宽度；缺省时根据文本标签大小自动调整。
    sharpness : float
        卵形线不对称程度，范围 (0, 1)，默认 0.4。
    tip_ratio : float
        尖端附近的宽度比例，默认 0.9；越小尖端越尖。
    round_ratio : float
        圆端附近的宽度比例，默认 1.1；越大圆端越粗。
    color : ManimColor | None
        统一的边界与填充颜色。
    opacity : float
        统一的边界与填充不透明度，范围 [0, 1]，默认 1。
    stroke_width : float
        曲线线宽，默认 2。
    attributes : AttributeHolder | None
        样式属性，仅用于缺省颜色。
    text : Mobject | None
        原子文本标签；提供后尖端会自动让开标签。
    text_buff : float
        图形与文本标签之间的最小间距，默认 0.15。
    use_smoothing : bool
        是否对采样点做平滑，默认 False。
    **kwargs
        传递给 ParametricFunction 的额外参数。
    """
    def __init__(self,*,
                 center:Vector3D|None=None,
                 direction:float=0,
                 length:float|None=None,
                 width:float|None=None,
                 sharpness:float=0.4,
                 tip_ratio:float=0.9,
                 round_ratio:float=1.1,
                 color:ManimColor|None=None,
                 opacity:float=1.0,
                 stroke_width:float=2,
                 attributes:'AttributeHolder'=None,
                 text:Mobject|None=None,
                 text_buff:float=_ATOMIC_TEXT_BUFF,
                 use_smoothing:bool=False,
                 **kwargs):

        if not 0<sharpness<1:
            raise ValueError(f"sharpness 必须在 (0, 1) 内，实际为 {sharpness}。")
        if tip_ratio<=0:
            raise ValueError(f"tip_ratio 必须大于 0，实际为 {tip_ratio}。")
        if round_ratio<=0:
            raise ValueError(f"round_ratio 必须大于 0，实际为 {round_ratio}。")
        if not 0<=opacity<=1:
            raise ValueError(f"opacity 必须在 [0, 1] 内，实际为 {opacity}。")

        center_point=_resolve_center(center,text)
        color=_resolve_color(attributes=attributes,color=color)
        direction_vector,normal_vector=_direction_frame(direction)
        text_radius=_text_radius(text,text_buff)

        if text is not None:
            center_point=center_point+direction_vector*text_radius

        if length is None:
            length=max(electron_cloud_length,2*text_radius)
        if width is None:
            width=max(electron_cloud_width,1.5*text_radius)
        if length<=0:
            raise ValueError(f"length 必须大于 0，实际为 {length}。")
        if width<=0:
            raise ValueError(f"width 必须大于 0，实际为 {width}。")

        _lift_text(text)
        kwargs=_clean_style_kwargs(kwargs)

        # 先构造 x 范围为 [0,1]、y 范围为 [-0.5,0.5] 的基准凸卵形线，
        # 再分别缩放到指定的 length 与 width，使两个尺寸参数互相独立。
        # tip_ratio 控制尖端附近宽窄，round_ratio 控制圆端附近粗细。
        c=0.5
        a=c*sharpness
        t_samples=np.linspace(0,TAU,2001)
        r_samples=c+a*np.cos(t_samples)
        base_x_samples=(r_samples*np.cos(t_samples)+(c-a))
        multiplier_samples=tip_ratio*base_x_samples+round_ratio*(1-base_x_samples)
        y_samples=r_samples*np.sin(t_samples)*multiplier_samples
        half_width=max(float(np.max(np.abs(y_samples))),1e-12)

        def egg_curve(t):
            r=c+a*np.cos(t)
            base_x=(r*np.cos(t)+(c-a))
            # base_x 在 t=0 处为 1、t=PI 处为 0；将 x 反向后，
            # 尖端落在 center_point，圆端沿 direction 向外。
            x=(1-base_x)*length
            multiplier=tip_ratio*base_x+round_ratio*(1-base_x)
            y=r*np.sin(t)*multiplier/(2*half_width)*width
            return center_point+x*direction_vector+y*normal_vector

        super().__init__(egg_curve,t_range=[0,TAU],color=color,stroke_width=stroke_width,
                         fill_opacity=opacity,stroke_opacity=opacity,
                         use_smoothing=use_smoothing,**kwargs)
        self.close_path()
        _style_lobe(self,color,opacity)

        self.center_point=center_point
        self.tip_point=center_point
        self.round_end_point=center_point+length*direction_vector
        self.direction=direction
        self.length=length
        self.lobe_width=width
        self.sharpness=sharpness
        self.tip_ratio=tip_ratio
        self.round_ratio=round_ratio
        self.lobe_color=color
        self.lobe_opacity=opacity
        self.text=text
        self.text_buff=text_buff
        self.lobes=[self]

class SOrbital(Circle):
    """s 轨道电子云：以原子文本标签为中心、大小自适应标签的填充圆。"""
    def __init__(self,*,
                 center:Vector3D|None=None,
                 direction:float=0,
                 radius:float|None=None,
                 color:ManimColor|None=None,
                 opacity:float=1.0,
                 stroke_width:float=2,
                 attributes:'AttributeHolder'=None,
                 text:Mobject|None=None,
                 text_buff:float=_ATOMIC_TEXT_BUFF,
                 **kwargs):

        if not 0<=opacity<=1:
            raise ValueError(f"opacity 必须在 [0, 1] 内，实际为 {opacity}。")

        center_point=_resolve_center(center,text)
        color=_resolve_color(attributes=attributes,color=color)
        text_radius=_text_radius(text,text_buff)

        if radius is None:
            radius=max(electron_cloud_radius,text_radius)
        if radius<=0:
            raise ValueError(f"radius 必须大于 0，实际为 {radius}。")

        _lift_text(text)
        kwargs=_clean_style_kwargs(kwargs)

        super().__init__(radius=radius,color=color,arc_center=center_point,
                         stroke_width=stroke_width,fill_opacity=opacity,stroke_opacity=opacity,**kwargs)
        _style_lobe(self,color,opacity)

        self.center_point=center_point
        self.direction=direction  # 圆形各向同性，direction 仅为统一接口而保留
        self.radius=radius
        self.lobe_color=color
        self.lobe_opacity=opacity
        self.text=text
        self.text_buff=text_buff
        self.lobes=[self]

class POrbital(VGroup):
    """p 轨道电子云：沿 direction 方向相反的两瓣等大填充卵形线。

    两瓣尖端朝内（指向文本标签），圆端朝外；separation 控制两瓣
    尖端之间的距离，避免曲线重叠并让开文本标签。
    """
    def __init__(self,*,
                 center:Vector3D|None=None,
                 direction:float=0,
                 separation:float|None=None,
                 length:float|None=None,
                 width:float|None=None,
                 color:ManimColor|None=None,
                 opacity:float=1.0,
                 lobe_colors:list[ManimColor|None]|None=None,
                 lobe_opacities:list[float|None]|None=None,
                 stroke_width:float=2,
                 attributes:'AttributeHolder'=None,
                 text:Mobject|None=None,
                 text_buff:float=_ATOMIC_TEXT_BUFF,
                 **kwargs):

        center_point=_resolve_center(center,text)
        direction_vector,_=_direction_frame(direction)
        text_radius=_text_radius(text,text_buff)
        if separation is None:
            separation=_separation_default(text=text,text_buff=text_buff,base=_DEFAULT_CURVE_GAP)
        if length is None or width is None:
            default_length,default_width=_lobe_defaults(text=text,text_buff=text_buff,
                                                        base_length=electron_cloud_length,
                                                        base_width=electron_cloud_width)
        if length is None:
            length=default_length
        if width is None:
            width=default_width

        colors,opacities=_resolve_lobe_styles(lobe_count=2,color=color,opacity=opacity,
                                              lobe_colors=lobe_colors,lobe_opacities=lobe_opacities,
                                              attributes=attributes)

        super().__init__(color=colors[0])

        positive_center=center_point+direction_vector*separation/2
        negative_center=center_point-direction_vector*separation/2
        self.positive_lobe=_outward_oval_lobe(reference_center=center_point,tip=positive_center,
                                             outward_direction=direction,
                                             length=length,width=width,color=colors[0],opacity=opacities[0],
                                             stroke_width=stroke_width,text_buff=text_buff,**kwargs)
        self.negative_lobe=_outward_oval_lobe(reference_center=center_point,tip=negative_center,
                                             outward_direction=direction+PI,
                                             length=length,width=width,color=colors[1],opacity=opacities[1],
                                             stroke_width=stroke_width,text_buff=text_buff,**kwargs)
        self.add(self.positive_lobe,self.negative_lobe)

        _lift_text(text)
        self.center_point=center_point
        self.direction=direction
        self.separation=separation
        self.length=length
        self.lobe_width=width
        self.lobe_colors=colors
        self.lobe_opacities=opacities
        self.text=text
        self.text_buff=text_buff
        self.lobes=[self.positive_lobe,self.negative_lobe]

class HybridOrbital(VGroup):
    """sp 杂化轨道：大瓣沿 direction、小瓣沿反方向，两瓣尖端朝内。

    sp、sp2、sp3 杂化轨道的单瓣形状相同，差别主要体现在空间取向；
    本类只描述单个杂化轨道本身，小瓣尺寸为大瓣乘以 small_ratio。
    """
    def __init__(self,*,
                 center:Vector3D|None=None,
                 direction:float=0,
                 separation:float|None=None,
                 length:float|None=None,
                 width:float|None=None,
                 small_ratio:float=electron_cloud_small_ratio,
                 color:ManimColor|None=None,
                 opacity:float=1.0,
                 lobe_colors:list[ManimColor|None]|None=None,
                 lobe_opacities:list[float|None]|None=None,
                 stroke_width:float=2,
                 attributes:'AttributeHolder'=None,
                 text:Mobject|None=None,
                 text_buff:float=_ATOMIC_TEXT_BUFF,
                 **kwargs):

        if small_ratio<=0:
            raise ValueError(f"small_ratio 必须大于 0，实际为 {small_ratio}。")

        center_point=_resolve_center(center,text)
        direction_vector,_=_direction_frame(direction)
        text_radius=_text_radius(text,text_buff)
        if separation is None:
            separation=_separation_default(text=text,text_buff=text_buff,base=_DEFAULT_CURVE_GAP)
        if length is None or width is None:
            default_length,default_width=_lobe_defaults(text=text,text_buff=text_buff,
                                                        base_length=electron_cloud_length,
                                                        base_width=electron_cloud_width)
        if length is None:
            length=default_length
        if width is None:
            width=default_width

        colors,opacities=_resolve_lobe_styles(lobe_count=2,color=color,opacity=opacity,
                                              lobe_colors=lobe_colors,lobe_opacities=lobe_opacities,
                                              attributes=attributes)

        super().__init__(color=colors[0])

        large_center=center_point+direction_vector*separation/2
        small_center=center_point-direction_vector*separation/2
        self.large_lobe=_outward_oval_lobe(reference_center=center_point,tip=large_center,
                                           outward_direction=direction,
                                           length=length,width=width,color=colors[0],opacity=opacities[0],
                                           stroke_width=stroke_width,text_buff=text_buff,**kwargs)
        self.small_lobe=_outward_oval_lobe(reference_center=center_point,tip=small_center,
                                           outward_direction=direction+PI,
                                           length=length*small_ratio,width=width*small_ratio,
                                           color=colors[1],opacity=opacities[1],
                                           stroke_width=stroke_width,text_buff=text_buff,**kwargs)
        self.add(self.large_lobe,self.small_lobe)

        _lift_text(text)
        self.center_point=center_point
        self.direction=direction
        self.separation=separation
        self.length=length
        self.lobe_width=width
        self.small_ratio=small_ratio
        self.lobe_colors=colors
        self.lobe_opacities=opacities
        self.text=text
        self.text_buff=text_buff
        self.lobes=[self.large_lobe,self.small_lobe]

class SPOrbital(HybridOrbital):
    """sp 杂化轨道。"""

class SP2Orbital(HybridOrbital):
    """sp2 杂化轨道。"""

class SP3Orbital(HybridOrbital):
    """sp3 杂化轨道。"""

class SigmaBondSS(Ellipse):
    """s-s sigma 成键轨道：基于两个原子文本标签绘制的填充椭圆。

    椭圆自动放置在 text1 与 text2 之间，长轴沿 text1 -> text2 方向，
    并且把两个文本标签包在椭圆内部。未提供标签时回退到
    center/direction 绘制。
    """
    def __init__(self,*,
                 center:Vector3D|None=None,
                 direction:float|None=None,
                 length:float|None=None,
                 width:float|None=None,
                 color:ManimColor|None=None,
                 opacity:float=1.0,
                 stroke_width:float=2,
                 attributes:'AttributeHolder'=None,
                 text1:Mobject|None=None,
                 text2:Mobject|None=None,
                 text_buff:float=_DEFAULT_TEXT_BUFF,
                 **kwargs):

        if not 0<=opacity<=1:
            raise ValueError(f"opacity 必须在 [0, 1] 内，实际为 {opacity}。")

        color=_resolve_color(attributes=attributes,color=color)
        frame=_two_text_frame(text1,text2,direction,text_buff)

        if frame is None:
            center_point=_resolve_center(center,None)
            direction=0. if direction is None else direction
            pos=0.
            if length is None:
                length=electron_cloud_length*0.8
            if width is None:
                width=max(0.4,0.75*length)
        else:
            direction=frame["direction"]
            base_center=frame["center_point"] if center is None else np.array(center,dtype=float)
            direction_vector,normal_vector=_direction_frame(direction)
            if length is None:
                length=0.8*max(electron_cloud_length,
                               frame["end_outer"]-frame["start_outer"]+2*text_buff)
            if width is None:
                width=max(0.5,2*frame["max_normal_half"])
                width=max(width,0.75*length)
            center_point=base_center
            _lift_text(text1)
            _lift_text(text2)

        if length<=0:
            raise ValueError(f"length 必须大于 0，实际为 {length}。")
        if width<=0:
            raise ValueError(f"width 必须大于 0，实际为 {width}。")

        direction_vector,normal_vector=_direction_frame(direction)
        kwargs=_clean_style_kwargs(kwargs)

        super().__init__(width=length,height=width,color=color,stroke_width=stroke_width,
                         fill_opacity=opacity,stroke_opacity=opacity,**kwargs)
        self.rotate(direction)
        self.move_to(center_point)
        _style_lobe(self,color,opacity)

        self.center_point=center_point
        self.direction=direction
        self.length=length
        self.ellipse_width=width
        self.lobe_color=color
        self.lobe_opacity=opacity
        self.text1=text1
        self.text2=text2
        self.text_buff=text_buff
        self.lobes=[self]

class SigmaAntiBondSSLobe(OvalLine):
    """s-s sigma 反键轨道的一瓣：尖端位于 center 或文本标签外侧的卵形线。"""

class SigmaAntiBondSS(VGroup):
    """s-s sigma 反键轨道：基于两个原子文本标签绘制的两瓣填充卵形线。

    两瓣分别包住 text1 与 text2，尖端朝向键中心，圆端朝外；
    两个文本标签位于各自一侧的卵形线内部。
    """
    def __init__(self,*,
                 center:Vector3D|None=None,
                 direction:float|None=None,
                 separation:float|None=None,
                 length:float|None=None,
                 width:float|None=None,
                 color:ManimColor|None=None,
                 opacity:float=1.0,
                 lobe_colors:list[ManimColor|None]|None=None,
                 lobe_opacities:list[float|None]|None=None,
                 stroke_width:float=2,
                 attributes:'AttributeHolder'=None,
                 text1:Mobject|None=None,
                 text2:Mobject|None=None,
                 text_buff:float=_DEFAULT_TEXT_BUFF,
                 **kwargs):

        frame=_two_text_frame(text1,text2,direction,text_buff)

        if frame is None:
            center_point=_resolve_center(center,None)
            direction=0. if direction is None else direction
            direction_vector,normal_vector=_direction_frame(direction)
            if separation is None:
                separation=0.3
            if length is None or width is None:
                default_length,default_width=_lobe_defaults(text=None,text_buff=text_buff,
                                                            base_length=electron_cloud_length,
                                                            base_width=electron_cloud_width)
            if length is None:
                length=default_length
            if width is None:
                width=default_width
        else:
            direction=frame["direction"]
            center_point=frame["center_point"] if center is None else np.array(center,dtype=float)
            direction_vector,normal_vector=_direction_frame(direction)
            use_explicit_tips=False
            if separation is None:
                left_tip_pos=frame["start_inner"]+_DEFAULT_CURVE_GAP
                right_tip_pos=frame["end_inner"]-_DEFAULT_CURVE_GAP
                separation=right_tip_pos-left_tip_pos
                use_explicit_tips=True
            if length is None:
                length=max(electron_cloud_length*1.2,2*frame["max_axis_half"])
            if width is None:
                width=max(electron_cloud_width*1.2,2*frame["max_normal_half"])
            _lift_text(text1)
            _lift_text(text2)

        colors,opacities=_resolve_lobe_styles(lobe_count=2,color=color,opacity=opacity,
                                              lobe_colors=lobe_colors,lobe_opacities=lobe_opacities,
                                              attributes=attributes)

        super().__init__(color=colors[0])

        if frame is not None and use_explicit_tips:
            right_center=center_point+direction_vector*right_tip_pos
            left_center=center_point+direction_vector*left_tip_pos
        else:
            right_center=center_point+direction_vector*separation/2
            left_center=center_point-direction_vector*separation/2
        self.right_lobe=_outward_oval_lobe(reference_center=center_point,tip=right_center,
                                           outward_direction=direction,
                                           length=length,width=width,color=colors[0],opacity=opacities[0],
                                           stroke_width=stroke_width,text_buff=text_buff,**kwargs)
        self.left_lobe=_outward_oval_lobe(reference_center=center_point,tip=left_center,
                                          outward_direction=direction+PI,
                                          length=length,width=width,color=colors[1],opacity=opacities[1],
                                          stroke_width=stroke_width,text_buff=text_buff,**kwargs)
        self.add(self.right_lobe,self.left_lobe)

        self.center_point=center_point
        self.direction=direction
        self.separation=separation
        self.length=length
        self.lobe_width=width
        self.lobe_colors=colors
        self.lobe_opacities=opacities
        self.text1=text1
        self.text2=text2
        self.text_buff=text_buff
        self.lobes=[self.right_lobe,self.left_lobe]

class SigmaBondPP(VGroup):
    """p-p sigma 成键轨道：基于两个原子文本标签绘制的填充椭圆与两瓣卵形线。

    中部椭圆位于两个文本标签之间，两个外侧卵形线分别位于两个标签
    的外侧，尖端朝内、圆端朝外，所有图形互不重叠且不覆盖标签。
    """
    def __init__(self,*,
                 center:Vector3D|None=None,
                 direction:float|None=None,
                 middle_length:float|None=None,
                 middle_width:float|None=None,
                 lobe_length:float|None=None,
                 lobe_width:float|None=None,
                 color:ManimColor|None=None,
                 opacity:float=1.0,
                 lobe_colors:list[ManimColor|None]|None=None,
                 lobe_opacities:list[float|None]|None=None,
                 stroke_width:float=2,
                 attributes:'AttributeHolder'=None,
                 text1:Mobject|None=None,
                 text2:Mobject|None=None,
                 text_buff:float=_DEFAULT_TEXT_BUFF,
                 **kwargs):

        frame=_two_text_frame(text1,text2,direction,text_buff)

        if frame is None:
            center_point=_resolve_center(center,None)
            direction=0. if direction is None else direction
            direction_vector,normal_vector=_direction_frame(direction)
            middle_center=center_point
            if middle_length is None:
                middle_length=electron_cloud_length*0.8
            if middle_width is None:
                middle_width=0.32
            if lobe_length is None:
                lobe_length=0.3
            if lobe_width is None:
                lobe_width=0.24
            left_tip=center_point-direction_vector*(middle_length/2+_DEFAULT_CURVE_GAP)
            right_tip=center_point+direction_vector*(middle_length/2+_DEFAULT_CURVE_GAP)
        else:
            direction=frame["direction"]
            center_point=frame["center_point"] if center is None else np.array(center,dtype=float)
            direction_vector,normal_vector=_direction_frame(direction)
            middle_pos,inner_middle_length=_inner_ellipse_geometry(frame)
            middle_center=center_point+direction_vector*middle_pos
            if middle_width is None:
                middle_width=0.8*max(0.5,2.4*frame["max_normal_half"])
            if middle_length is None:
                # 长轴必须沿键轴，因此键轴方向长度要大于垂直方向宽度；
                # 同时整体缩小为原来的 0.8 倍，避免与文本标签重合。
                middle_length=0.8*max(inner_middle_length,1.3*middle_width)
            if lobe_length is None:
                lobe_length=0.6*max(0.4,1.5*frame["max_axis_half"])
            if lobe_width is None:
                lobe_width=0.6*max(0.3,1.1*frame["max_normal_half"])
            left_tip=center_point+direction_vector*(frame["start_outer"]-_DEFAULT_CURVE_GAP)
            right_tip=center_point+direction_vector*(frame["end_outer"]+_DEFAULT_CURVE_GAP)
            _lift_text(text1)
            _lift_text(text2)

        colors,opacities=_resolve_lobe_styles(lobe_count=3,color=color,opacity=opacity,
                                              lobe_colors=lobe_colors,lobe_opacities=lobe_opacities,
                                              attributes=attributes)

        super().__init__(color=colors[0])

        self.middle=_build_ellipse(center=middle_center,direction=direction,
                                   length=middle_length,width=middle_width,
                                   color=colors[0],opacity=opacities[0],
                                   stroke_width=stroke_width,**kwargs)
        self.left_lobe=_outward_oval_lobe(reference_center=center_point,tip=left_tip,
                                          outward_direction=direction+PI,
                                          length=lobe_length,width=lobe_width,color=colors[1],opacity=opacities[1],
                                          stroke_width=stroke_width,text_buff=text_buff,**kwargs)
        self.right_lobe=_outward_oval_lobe(reference_center=center_point,tip=right_tip,
                                           outward_direction=direction,
                                           length=lobe_length,width=lobe_width,color=colors[2],opacity=opacities[2],
                                           stroke_width=stroke_width,text_buff=text_buff,**kwargs)
        self.add(self.middle,self.left_lobe,self.right_lobe)

        self.center_point=center_point
        self.direction=direction
        self.middle_length=middle_length
        self.middle_width=middle_width
        self.lobe_length=lobe_length
        self.lobe_width=lobe_width
        self.lobe_colors=colors
        self.lobe_opacities=opacities
        self.text1=text1
        self.text2=text2
        self.text_buff=text_buff
        self.lobes=[self.middle,self.left_lobe,self.right_lobe]

class SigmaBondSP(VGroup):
    """s-p sigma 成键轨道：基于两个原子文本标签绘制的大小两瓣填充卵形线。

    大瓣位于 direction 负侧，并把该侧文本标签包在内部；小瓣位于
    direction 正侧文本标签外侧。未提供标签时退化为围绕 center 的
    大小两瓣。
    """
    def __init__(self,*,
                 center:Vector3D|None=None,
                 direction:float|None=None,
                 separation:float|None=None,
                 length:float|None=None,
                 width:float|None=None,
                 small_ratio:float=electron_cloud_small_ratio*0.7,
                 color:ManimColor|None=None,
                 opacity:float=1.0,
                 lobe_colors:list[ManimColor|None]|None=None,
                 lobe_opacities:list[float|None]|None=None,
                 stroke_width:float=2,
                 attributes:'AttributeHolder'=None,
                 text1:Mobject|None=None,
                 text2:Mobject|None=None,
                 text_buff:float=_DEFAULT_TEXT_BUFF,
                 **kwargs):

        if small_ratio<=0:
            raise ValueError(f"small_ratio 必须大于 0，实际为 {small_ratio}。")

        frame=_two_text_frame(text1,text2,direction,text_buff)

        if frame is None:
            center_point=_resolve_center(center,None)
            direction=0. if direction is None else direction
            direction_vector,normal_vector=_direction_frame(direction)
            if separation is None:
                separation=_separation_default(text=None,text_buff=text_buff,base=_DEFAULT_CURVE_GAP)
            if length is None or width is None:
                default_length,default_width=_lobe_defaults(text=None,text_buff=text_buff,
                                                            base_length=electron_cloud_length,
                                                            base_width=electron_cloud_width)
            if length is None:
                length=default_length
            if width is None:
                width=default_width
        else:
            direction=frame["direction"]
            center_point=frame["center_point"] if center is None else np.array(center,dtype=float)
            direction_vector,normal_vector=_direction_frame(direction)
            use_explicit_tips=False
            if separation is None:
                # 大瓣尖端向另一侧靠近，使大瓣整体更贴近键中心
                large_tip_pos=frame["start_inner"]+_DEFAULT_CURVE_GAP+0.15
                small_tip_pos=frame["end_outer"]+_DEFAULT_CURVE_GAP
                separation=small_tip_pos-large_tip_pos
                use_explicit_tips=True
            if length is None:
                length=max(electron_cloud_length*1.5,2*frame["max_axis_half"])
            if width is None:
                width=max(electron_cloud_width*1.5,2*frame["max_normal_half"])
            _lift_text(text1)
            _lift_text(text2)

        colors,opacities=_resolve_lobe_styles(lobe_count=2,color=color,opacity=opacity,
                                              lobe_colors=lobe_colors,lobe_opacities=lobe_opacities,
                                              attributes=attributes)

        super().__init__(color=colors[0])

        if frame is not None and use_explicit_tips:
            large_center=center_point+direction_vector*large_tip_pos
            small_center=center_point+direction_vector*small_tip_pos
        else:
            large_center=center_point-direction_vector*separation/2
            small_center=center_point+direction_vector*separation/2
        self.large_lobe=_outward_oval_lobe(reference_center=center_point,tip=large_center,
                                           outward_direction=direction+PI,
                                           length=length,width=width,color=colors[0],opacity=opacities[0],
                                           stroke_width=stroke_width,text_buff=text_buff,**kwargs)
        self.small_lobe=_outward_oval_lobe(reference_center=center_point,tip=small_center,
                                           outward_direction=direction,
                                           length=length*small_ratio,width=width*small_ratio,
                                           color=colors[1],opacity=opacities[1],
                                           stroke_width=stroke_width,text_buff=text_buff,**kwargs)
        self.add(self.large_lobe,self.small_lobe)

        self.center_point=center_point
        self.direction=direction
        self.separation=separation
        self.length=length
        self.lobe_width=width
        self.small_ratio=small_ratio
        self.lobe_colors=colors
        self.lobe_opacities=opacities
        self.text1=text1
        self.text2=text2
        self.text_buff=text_buff
        self.lobes=[self.large_lobe,self.small_lobe]

class PiBondPP(VGroup):
    """p-p pi 成键轨道：基于两个原子文本标签绘制的上下两个填充扁椭圆。"""
    def __init__(self,*,
                 center:Vector3D|None=None,
                 direction:float|None=None,
                 length:float|None=None,
                 width:float|None=None,
                 offset:float|None=None,
                 color:ManimColor|None=None,
                 opacity:float=1.0,
                 lobe_colors:list[ManimColor|None]|None=None,
                 lobe_opacities:list[float|None]|None=None,
                 stroke_width:float=2,
                 attributes:'AttributeHolder'=None,
                 text1:Mobject|None=None,
                 text2:Mobject|None=None,
                 text_buff:float=_DEFAULT_TEXT_BUFF,
                 **kwargs):

        frame=_two_text_frame(text1,text2,direction,text_buff)

        if frame is None:
            center_point=_resolve_center(center,None)
            direction=0. if direction is None else direction
            direction_vector,normal_vector=_direction_frame(direction)
            ellipse_center=center_point
            if length is None:
                length=electron_cloud_length*1.2
            if width is None:
                width=0.3
            if offset is None:
                offset=0.35
        else:
            direction=frame["direction"]
            center_point=frame["center_point"] if center is None else np.array(center,dtype=float)
            direction_vector,normal_vector=_direction_frame(direction)
            ellipse_center=center_point
            if length is None:
                length=1.2*max(electron_cloud_length,
                               frame["end_pos"]-frame["start_pos"]+0.1)
            if width is None:
                width=1.2*max(0.25,0.5*frame["max_normal_half"])
            if offset is None:
                offset=max(0.35,frame["max_normal_half"]+width/2+_DEFAULT_CURVE_GAP)
            _lift_text(text1)
            _lift_text(text2)

        colors,opacities=_resolve_lobe_styles(lobe_count=2,color=color,opacity=opacity,
                                              lobe_colors=lobe_colors,lobe_opacities=lobe_opacities,
                                              attributes=attributes)

        super().__init__(color=colors[0])

        self.upper_ellipse=_build_ellipse(center=ellipse_center+normal_vector*offset,direction=direction,
                                          length=length,width=width,color=colors[0],opacity=opacities[0],
                                          stroke_width=stroke_width,**kwargs)
        self.lower_ellipse=_build_ellipse(center=ellipse_center-normal_vector*offset,direction=direction,
                                          length=length,width=width,color=colors[1],opacity=opacities[1],
                                          stroke_width=stroke_width,**kwargs)
        self.add(self.upper_ellipse,self.lower_ellipse)

        self.center_point=center_point
        self.direction=direction
        self.length=length
        self.ellipse_width=width
        self.offset=offset
        self.lobe_colors=colors
        self.lobe_opacities=opacities
        self.text1=text1
        self.text2=text2
        self.text_buff=text_buff
        self.lobes=[self.upper_ellipse,self.lower_ellipse]

class PiAntiBondPP(VGroup):
    """p-p pi 反键轨道：基于两个原子文本标签绘制的四个倾斜填充卵形线。

    左右两个文本标签外侧各有一对上下倾斜的卵形线，四个瓣稍大且
    分别远离文本标签；尖端均指向两个文本标签，圆端朝外。
    """
    def __init__(self,*,
                 center:Vector3D|None=None,
                 direction:float|None=None,
                 separation:float|None=None,
                 lobe_length:float|None=None,
                 lobe_width:float|None=None,
                 tilt_angle:float=np.pi/3,
                 color:ManimColor|None=None,
                 opacity:float=1.0,
                 lobe_colors:list[ManimColor|None]|None=None,
                 lobe_opacities:list[float|None]|None=None,
                 stroke_width:float=2,
                 attributes:'AttributeHolder'=None,
                 text1:Mobject|None=None,
                 text2:Mobject|None=None,
                 text_buff:float=_DEFAULT_TEXT_BUFF,
                 **kwargs):

        frame=_two_text_frame(text1,text2,direction,text_buff)

        if frame is None:
            center_point=_resolve_center(center,None)
            direction=0. if direction is None else direction
            direction_vector,normal_vector=_direction_frame(direction)
            if separation is None:
                separation=electron_cloud_length
            if lobe_length is None:
                lobe_length=0.6
            if lobe_width is None:
                lobe_width=0.4
            left_anchor=center_point-direction_vector*separation/2
            right_anchor=center_point+direction_vector*separation/2
            anchors=[left_anchor,left_anchor,right_anchor,right_anchor]
            lobe_directions=[
                PI-tilt_angle,
                PI+tilt_angle,
                tilt_angle,
                -tilt_angle,
            ]
        else:
            direction=frame["direction"]
            center_point=frame["center_point"] if center is None else np.array(center,dtype=float)
            direction_vector,normal_vector=_direction_frame(direction)
            start_text=frame["start_text"]
            end_text=frame["end_text"]
            anchors=[
                start_text.get_corner(UL),
                start_text.get_corner(DL),
                end_text.get_corner(UR),
                end_text.get_corner(DR),
            ]
            lobe_directions=[
                PI-tilt_angle,
                PI+tilt_angle,
                tilt_angle,
                -tilt_angle,
            ]
            if lobe_length is None:
                lobe_length=max(0.7,1.5*frame["max_axis_half"])
            if lobe_width is None:
                lobe_width=max(0.35,1.0*frame["max_normal_half"])
            _lift_text(text1)
            _lift_text(text2)

        colors,opacities=_resolve_lobe_styles(lobe_count=4,color=color,opacity=opacity,
                                              lobe_colors=lobe_colors,lobe_opacities=lobe_opacities,
                                              attributes=attributes)

        super().__init__(color=colors[0])

        tip_offset=max(2*_DEFAULT_CURVE_GAP,0.25*lobe_width)
        self.lobes=[]
        lobe_index=0
        for anchor,lobe_direction in zip(anchors,lobe_directions):
            lobe_direction_vector=np.array([np.cos(lobe_direction),np.sin(lobe_direction),0])
            lobe_center=anchor+lobe_direction_vector*tip_offset
            lobe=_outward_oval_lobe(reference_center=center_point,tip=lobe_center,
                                     outward_direction=lobe_direction,
                                     length=lobe_length,width=lobe_width,
                                     color=colors[lobe_index],opacity=opacities[lobe_index],
                                     stroke_width=stroke_width,text_buff=text_buff,**kwargs)
            self.lobes.append(lobe)
            self.add(lobe)
            lobe_index+=1

        self.center_point=center_point
        self.direction=direction
        self.left_anchor=anchors[0]
        self.right_anchor=anchors[2]
        self.upper_left_anchor=anchors[0]
        self.lower_left_anchor=anchors[1]
        self.upper_right_anchor=anchors[2]
        self.lower_right_anchor=anchors[3]
        self.separation=float(np.linalg.norm(anchors[2]-anchors[0]))
        self.lobe_length=lobe_length
        self.lobe_width=lobe_width
        self.tilt_angle=tilt_angle
        self.lobe_colors=colors
        self.lobe_opacities=opacities
        self.text1=text1
        self.text2=text2
        self.text_buff=text_buff

class ElectronCloudType(Enum):
    S_ORBITAL=SOrbital
    P_ORBITAL=POrbital
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

_MOLECULAR_CLOUD_TYPES={
    ElectronCloudType.SIGMA_BOND_SS,
    ElectronCloudType.SIGMA_ANTIBOND_SS,
    ElectronCloudType.SIGMA_BOND_PP,
    ElectronCloudType.SIGMA_BOND_SP,
    ElectronCloudType.PI_BOND_PP,
    ElectronCloudType.PI_ANTIBOND_PP,
}

class ElectronCloud(VGroup):
    """电子云图形包装器。

    与 Bond、Charge 的包装方式一致：ElectronCloudType 枚举保存具体
    图形类，包装器负责记录 center、direction 等元数据并把生成的
    图形加入自身。

    原子轨道与杂化轨道通过 text 传入一个原子文本标签；所有成键
    轨道与反键轨道通过 text1、text2 传入两个原子文本标签，中心与
    方向会根据标签自动确定，图形尺寸也会自动调整以避免覆盖标签。
    """
    def __init__(self,*,
                 cloud_type:ElectronCloudType,
                 center:Vector3D|None=None,
                 direction:float|None=None,
                 attributes:'AttributeHolder'=DEFAULT_ATTRIBUTES,
                 text:Mobject|None=None,
                 text1:Mobject|None=None,
                 text2:Mobject|None=None,
                 text_buff:float|None=None,
                 **kwargs):

        color=kwargs.pop("color",None)
        color=_resolve_color(attributes=attributes,color=color)

        super().__init__(color=color)

        cloud_kwargs=dict(kwargs)
        if text_buff is not None:
            cloud_kwargs["text_buff"]=text_buff

        is_molecular=cloud_type in _MOLECULAR_CLOUD_TYPES
        if is_molecular:
            if text is not None:
                raise ValueError("成键轨道与反键轨道请使用 text1、text2 传入两个原子文本标签。")
            cloud_kwargs.update(text1=text1,text2=text2)
            cloud=cloud_type.value(center=center,direction=direction,
                                   color=color,attributes=attributes,
                                   **cloud_kwargs)
        else:
            cloud_direction=0. if direction is None else direction
            cloud=cloud_type.value(center=center,direction=cloud_direction,
                                   color=color,attributes=attributes,
                                   text=text,**cloud_kwargs)

        self.cloud_type=cloud_type
        self.center_point=cloud.center_point
        self.direction=cloud.direction
        self.text=text
        self.text1=text1
        self.text2=text2
        self.text_buff=cloud.text_buff
        self.cloud=cloud
        self.add(cloud)
