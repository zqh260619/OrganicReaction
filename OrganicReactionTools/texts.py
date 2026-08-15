"""标题文本类。"""

from manim import WHITE
from manim.typing import Vector3D

from .parameters import (MathTex, mytemplate, title_coordinate, title_size,
                         subtitle_coordinate, subtitle_size,
                         description_coordinate, txt_size)

#Text classes
class Title(MathTex):
    def __init__(self,*,text:str,pos:Vector3D=title_coordinate,color=WHITE,size=title_size):

        super().__init__(text,color=color,tex_template=mytemplate,font_size=size)

        self.move_to(pos)

class Subtitle(MathTex):
    def __init__(self,*,text:str,pos:Vector3D=subtitle_coordinate,color=WHITE,size=subtitle_size):

        super().__init__(text,color=color,tex_template=mytemplate,font_size=size)

        self.move_to(pos)

class Description(MathTex):
    def __init__(self,*,text:str,pos:Vector3D=description_coordinate,color=WHITE,size=txt_size):

        super().__init__(text,color=color,tex_template=mytemplate,font_size=size)

        self.move_to(pos)
