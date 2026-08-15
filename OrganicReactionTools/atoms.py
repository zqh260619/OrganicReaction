"""原子文本 AtomicCluster 与原子定位器 Locator。"""

from manim import PI, DEGREES
from manim.typing import Vector3D
import numpy as np

from .parameters import mytemplate, MathTex

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
                 attributes:'AttributeHolder',
                 text_offset:Vector3D=np.array([0,0,0])):

        super().__init__(text,color=attributes.color,font_size=attributes.font_size,
                         tex_template=mytemplate)
        self.move_to(pos)
        if np.any(text_offset != 0):
            self.shift(text_offset)
