"""全局参数与常量。"""

from manim import TexTemplate
import numpy as np

mytemplate = TexTemplate()
mytemplate.add_to_preamble(r"\usepackage{ctex}").add_to_preamble(r"\setlength{\jot}{-5pt}")

RNG=np.random.default_rng(seed=3)

#PARAMETERS
#structures
bond_length=1
"""键长"""
edge=0.25
"""键边距"""
ratio_transition_state=1.2
"""过渡态键长比例"""
default_charge_edge=0.07
"""默认电荷边距"""
#texts
title_height=3
"""标题高度"""
title_coordinate=[0,title_height,0]
"""标题坐标"""
title_size=60
"""标题大小"""
subtitle_height=2.3
"""副标题高度"""
subtitle_coordinate=[0,subtitle_height,0]
"""副标题坐标"""
subtitle_size=30
"""副标题大小"""
description_height=-3
"""描述性文本高度"""
description_coordinate=[0,description_height,0]
"""描述性文本坐标"""
txt_size=35
"""文字大小"""
