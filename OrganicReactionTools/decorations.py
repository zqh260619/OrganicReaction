"""装饰图形：括号与箭头。"""

from manim import VGroup, Line, CubicBezier, ArrowTriangleFilledTip, Arrow, WHITE, PI, UP, UL, YELLOW
from manim.typing import Vector3D
import numpy as np

from .parameters import MathTex

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
    - 箭头总长度与"两端均有边距"的 NormalBond 线段长度相同，
      即 length_global - 2*edge_global；
    - 线段粗细为单键（manim 默认线宽）的一半；
    - 起始端有一个与箭头垂直的短线段（十字形尾部）：其长度是
      小线段中点到箭头起点的两倍——小线段中点位于箭头起点
      沿箭头方向 tail_offset 处，因此小线段长度为 2*tail_offset。

    Parameters
    ----------
    start : Vector3D
        箭头起点（正电端）坐标。
    direction : float
        箭头指向（弧度），从正电端指向负电端。
    attributes : AttributeHolder
        样式属性（取 length_global、edge_global、color）。
    tail_offset : float
        尾部小线段中点到箭头起点的距离，默认 0.1。
    **kwargs
        传递给 Arrow 的额外参数。
    """

    def __init__(self,*,
                 start:Vector3D,
                 direction:float,
                 attributes:'AttributeHolder',
                 tail_offset:float=0.1,
                 **kwargs):

        start_point=np.array(start,dtype=float)
        direction_vector=np.array([np.cos(direction),np.sin(direction),0])
        normal_vector=np.array([-np.sin(direction),np.cos(direction),0])

        length=attributes.length_global-2*attributes.edge_global
        stroke_width=Line().stroke_width/2  # 单键默认线宽的一半

        end_point=start_point+length*direction_vector

        arrow=Arrow(start=start_point,end=end_point,buff=0,
                    stroke_width=stroke_width,color=attributes.color,
                    tip_length=length*0.3,max_tip_length_to_length_ratio=1,
                    max_stroke_width_to_length_ratio=1000,  # 禁用按长度收缩线宽，保证恰为单键一半
                    **kwargs)

        tail_mid=start_point+tail_offset*direction_vector
        tail_bar=Line(start=tail_mid-normal_vector*tail_offset,
                      end=tail_mid+normal_vector*tail_offset,
                      stroke_width=stroke_width,color=attributes.color)

        super().__init__(arrow,tail_bar)

        self.start=start_point
        self.end=end_point
        self.length=length
        self.direction=direction
        self.tail_offset=tail_offset
        self.arrow=arrow
        self.tail_bar=tail_bar
