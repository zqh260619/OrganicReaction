"""装饰图形：括号与箭头。"""

from manim import VGroup, Line, CubicBezier, ArrowTriangleFilledTip, Arrow, WHITE, PI, UP, UL, RIGHT, DOWN, YELLOW, DEFAULT_STROKE_WIDTH, Mobject
from manim.typing import Vector3D
import numpy as np

from .parameters import (MathTex, mytemplate, reaction_arrow_buffer,
                         reaction_arrow_gap, reaction_arrow_font_size)

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

class PolarityArrow(VGroup):
    """化学键极性箭头：从正电端（δ+）指向负电端（δ-）。

    几何规格：
    - 总长度默认为"两端均有边距"的 NormalBond 线段长度
      （length_global - 2*edge_global），可通过 length 参数指定；
    - 线宽为单键（manim 默认线宽）的一半；
    - 末端箭头三角形长度为 length*0.15；
    - 起始端十字尾部：与箭头垂直的小线段，中点位于起点沿箭头
      方向 tail_offset 处，长度为其两倍（2*tail_offset）。

    放置规则：显示在键侧边时，起点取
    键起点 + edge_global*键方向 + 垂直方向的侧边偏移，
    使箭头中点与键线段中点的连线垂直于键所在直线。

    Parameters
    ----------
    start : Vector3D
        箭头起点（正电端）坐标。
    direction : float
        箭头指向（弧度），从正电端指向负电端。
    attributes : AttributeHolder
        样式属性（取 length_global、edge_global、color）。
    length : float
        箭头总长度（起点到箭头尖）；默认 -1 表示自动取
        length_global - 2*edge_global（与"两端均有边距"的单键线段等长）。
    tail_offset : float
        尾部小线段中点到箭头起点的距离，默认 0.07。
    **kwargs
        传递给 Arrow 的额外参数。
    """

    def __init__(self,*,
                 start:Vector3D,
                 direction:float,
                 attributes:'AttributeHolder',
                 length:float=-1.0,
                 tail_offset:float=0.07,
                 **kwargs):

        start_point=np.array(start,dtype=float)
        direction_vector=np.array([np.cos(direction),np.sin(direction),0])
        normal_vector=np.array([-direction_vector[1],direction_vector[0],0])
        color=attributes.color
        if length==-1.0:
            length=attributes.length_global-2*attributes.edge_global
        stroke_width=DEFAULT_STROKE_WIDTH/2  # 单键默认线宽的一半

        end_point=start_point+length*direction_vector
        arrow=Arrow(start=start_point,end=end_point,buff=0,color=color,
                    stroke_width=stroke_width,tip_length=length*0.15,
                    max_tip_length_to_length_ratio=1,
                    max_stroke_width_to_length_ratio=1000,  # 禁用按长度收缩线宽
                    **kwargs)

        tail_mid=start_point+tail_offset*direction_vector
        tail_bar=Line(start=tail_mid-normal_vector*tail_offset,
                      end=tail_mid+normal_vector*tail_offset,
                      stroke_width=stroke_width,color=color)

        super().__init__(arrow,tail_bar)

        self.start=start_point
        self.end=end_point
        self.length=length
        self.direction=direction
        self.tail_offset=tail_offset
        self.arrow=arrow
        self.tail_bar=tail_bar


class BondPolarityArrow(PolarityArrow):
    """在化学键旁边生成极性键箭头。

    给定键的起点 start 与终点 end，自动计算箭头位置与指向：
    - 箭头与键平行，从 start 指向 end；
    - 箭头在键的哪一侧由 side 决定，约定与 DoubleBond 的 side≠0
      较短线相同（手平行于屏幕平面，手掌心向屏幕内侧，食指从
      start 指向 end，大拇指的方向为箭头所在侧）：
      side=1 用右手，side=-1 用左手；side 不能为 0；
    - 箭头与键之间的距离默认等于尾部小线段的长度（2*tail_offset），
      可通过 offset 参数指定；
    - 默认长度与"两端均有边距"的单键线段相同
      （键长 - 2*edge_global），可通过 length 参数指定（-1 表示自动）；
    - 箭头中点与键线段中点的连线垂直于键所在直线，且该性质对
      任意 length 都成立（length 变化时箭头起点会相应移动）。

    本类继承 PolarityArrow：self.start / self.end 为箭头自身的起终点，
    键的起终点存于 self.bond_start / self.bond_end。

    Parameters
    ----------
    start : Vector3D
        键的起点（正电端一侧的原子坐标）。
    end : Vector3D
        键的终点（负电端一侧的原子坐标）。
    attributes : AttributeHolder
        样式属性（取 edge_global、color 等）。
    side : int
        箭头所在侧：1（右手，+法向）或 -1（左手，-法向），不能为 0。
    tail_offset : float
        尾部十字参考尺寸，默认 0.07。
    offset : float
        箭头与键之间的距离，默认 -1 表示取尾部小线段长度（2*tail_offset）。
    length : float
        箭头总长度，默认 -1 表示取 键长 - 2*edge_global。
    **kwargs
        传递给 PolarityArrow（Arrow）的额外参数。
    """

    def __init__(self,*,
                 start:Vector3D,
                 end:Vector3D,
                 attributes:'AttributeHolder',
                 side:int,
                 tail_offset:float=0.07,
                 offset:float=-1.0,
                 length:float=-1.0,
                 **kwargs):

        if side not in (1,-1):
            raise ValueError(f"side 只能取 1（右手）或 -1（左手），不能为 0，实际为 {side}。")

        start_point=np.array(start,dtype=float)
        end_point=np.array(end,dtype=float)
        bond_vector=end_point-start_point
        bond_length=np.linalg.norm(bond_vector)
        if bond_length==0:
            raise ValueError("键的起点与终点不能重合。")
        direction=np.arctan2(bond_vector[1],bond_vector[0])
        direction_vector=bond_vector/bond_length
        normal_vector=np.array([-direction_vector[1],direction_vector[0],0])

        if offset==-1.0:
            offset=2*tail_offset  # 默认间距 = 尾部小线段长度
        if length==-1.0:
            length=bond_length-2*attributes.edge_global

        # 由"箭头中点与键线段中点连线垂直"反推箭头起点：
        # 键线段中点 = 键起点 + 键长/2*键方向，
        # 故箭头起点 = 键起点 + (键长-length)/2*键方向 + side*offset*法向。
        arrow_start=start_point+(bond_length-length)/2*direction_vector+side*offset*normal_vector

        super().__init__(start=arrow_start,direction=direction,attributes=attributes,
                         length=length,tail_offset=tail_offset,**kwargs)

        self.bond_start=start_point
        self.bond_end=end_point
        self.side=side
        self.offset=offset


class ReactionArrow(VGroup):
    """反应箭头：水平指向右侧，上下方显示反应条件和试剂等信息。

    几何规格：
    - 箭头强制水平且指向右侧，由 start（起点/尾端坐标）与 length
      （尾端到箭尖的总长度）确定；
    - 上下方对象水平居中于箭头中点（即 start 沿 +x 方向偏移 length/2）；
    - 上方对象整体的外沿（下沿）与箭头所在直线的距离为 gap，下方同理；
    - length 缺省时自适应：长度 = max(上方整体宽度, 下方整体宽度) + buffer。

    每一侧可以传单个对象、对象列表或 TeX 字符串：字符串会用本包默认的
    MathTex（ctex 模板，可写中文与 \\mathrm{}）按 font_size 渲染；
    列表会用 VGroup(...).arrange(DOWN, buff=0.2) 竖直堆叠成一栏，
    宽度取整栏的矩形边界宽度。文本会置于箭头之上（z_index 提升），
    不会被箭头压住。

    文本内容或字号改变后，调用 rebuild() 可让长度与间距重新按新尺寸自适应。

    Parameters
    ----------
    start : Vector3D
        箭头起点（尾端）坐标。
    above : Mobject | list | str | None
        箭头上方显示的对象，默认 None（不显示）。
    below : Mobject | list | str | None
        箭头下方显示的对象，默认 None（不显示）。
        above 与 below 不能同时为空。
    length : float
        箭头总长度；默认 -1 表示按上下方宽度自适应，
        即 max(上方宽度, 下方宽度) + buffer。
    buffer : float
        自适应时长度相对上下方宽度较大值的余量，默认 1。
    gap : float
        上下方对象外沿与箭头直线的距离，默认 0.2；负值会被夹取为 0。
    color : ManimColor
        箭头与文本颜色，默认 WHITE。
    font_size : float
        字符串内容渲染成 MathTex 时的字号，默认 25。
    **kwargs
        传递给内部 Arrow 的额外参数（如 stroke_width、tip_length 等）。
    """

    def __init__(self,*,
                 start:Vector3D,
                 above:Mobject|list|str|None=None,
                 below:Mobject|list|str|None=None,
                 length:float=-1.0,
                 buffer:float=reaction_arrow_buffer,
                 gap:float=reaction_arrow_gap,
                 color=WHITE,
                 font_size:float=reaction_arrow_font_size,
                 **kwargs):

        if length!=-1.0 and length<=0:
            raise ValueError(f"length 必须为正数，或用 -1 表示自适应，实际为 {length}。")
        if buffer<0:
            raise ValueError(f"buffer 不能为负数，实际为 {buffer}。")
        if font_size<=0:
            raise ValueError(f"font_size 必须大于 0，实际为 {font_size}。")

        super().__init__(color=color)

        self.above=self._build_side(items=above,color=color,font_size=font_size)
        self.below=self._build_side(items=below,color=color,font_size=font_size)

        if self.above is None and self.below is None:
            raise ValueError("ReactionArrow 的 above 与 below 不能同时为空。")

        self.start_point=np.array(start,dtype=float)
        self.buffer=buffer
        self.gap=max(gap,0)  # 负间距会让文本压住箭头，夹取为 0
        self.color=color
        self.font_size=font_size
        self.arrow_kwargs=dict(kwargs)

        if length==-1.0:
            self._apply_auto_length()  # 自适应：max(上方宽度, 下方宽度) + buffer
        else:
            self.length=float(length)  # 显式给定长度时不参与自适应
        self.arrow=self._new_arrow()
        self.add(self.arrow)
        self._layout()

    def _build_side(self,*,items,color,font_size)->VGroup|None:
        """把一侧的输入统一整理成竖直堆叠的 VGroup；无内容时返回 None。"""
        if items is None:
            return None
        if isinstance(items,(str,Mobject)):
            items=[items]
        else:
            items=list(items)
        if len(items)==0:
            return None

        mobjects=[]
        for item in items:
            if isinstance(item,str):
                mobjects.append(MathTex(item,color=color,font_size=font_size,
                                        tex_template=mytemplate))
            else:
                mobjects.append(item)

        if len(mobjects)==1:
            group=VGroup(mobjects[0])
        else:
            group=VGroup(*mobjects).arrange(DOWN,buff=0.2)
        for mobject in group:
            mobject.set_z_index(max(float(mobject.z_index),2.))  # 文本压在箭头之上
        return group

    @staticmethod
    def _side_width(group:VGroup|None)->float:
        return 0. if group is None else float(group.width)

    def _apply_auto_length(self)->None:
        """按上下方对象的当前宽度重新计算自适应长度。"""
        self.length=max(self._side_width(self.above),self._side_width(self.below))+self.buffer

    def _new_arrow(self)->Arrow:
        """按当前起点与长度新建内部箭头（复用构造时传入的 Arrow 参数）。"""
        return Arrow(start=self.start_point,end=self.start_point+RIGHT*self.length,
                     buff=0,color=self.color,**self.arrow_kwargs)

    def _layout(self)->None:
        """按当前长度与两侧尺寸重新摆放箭头与上下方对象。"""
        start_point=np.array(self.arrow.get_start(),dtype=float)
        mid=start_point+np.array([self.length/2,0,0])
        if self.above is not None:
            self.above.move_to([mid[0],start_point[1]+self.gap+self.above.height/2,0])
        if self.below is not None:
            self.below.move_to([mid[0],start_point[1]-self.gap-self.below.height/2,0])

    def rebuild(self)->None:
        """按上下方对象的当前尺寸重新自适应长度并重排（内容或字号改变后调用）。

        起点以箭头当前的实际位置为准，因此 move_to/shift 之后再调用
        rebuild 仍保持几何契约。
        """
        self.remove(self.arrow)
        if self.above is not None:
            self.remove(self.above)
        if self.below is not None:
            self.remove(self.below)

        self.start_point=np.array(self.arrow.get_start(),dtype=float)
        self._apply_auto_length()
        self.arrow=self._new_arrow()

        self.add(self.arrow)
        if self.above is not None:
            self.add(self.above)
        if self.below is not None:
            self.add(self.below)
        self._layout()
