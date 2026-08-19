"""OrganicReactionTools 包。

由单文件 OrganicReactionTools.py 重构而来。为保持向后兼容，
本包在顶层重新导出全部公开 API（以及原模块通过 ``from manim import *``
透出的 manim 命名空间），因此 ``from OrganicReactionTools import *``
与原有的调用代码完全无需修改。

子模块划分：
    parameters   全局参数、常量与默认文本基类（MathTex 多行默认居中）
    attributes   样式属性持有者 AttributeHolder 与 DEFAULT_ATTRIBUTES
    atoms        原子文本 AtomicCluster 与原子定位器 Locator
    bonds        化学键类、Bond 包装器与 BondType 枚举
    charges      电荷类、Charge 包装器与 ChargeType 枚举
    decorations  括号、箭头等装饰图形
    animations   动画类与电子迁移步骤描述
    structures   结构式 StructuralFormula 与苯环 Benzene
    texts        标题文本类
    functions    工具函数
"""

from manim import *
from manim.typing import Vector3D
import numpy as np
from typing import Callable, Optional
from enum import Enum

from .parameters import *
from .attributes import *
from .atoms import *
from .bonds import *
from .charges import *
from .decorations import *
from .animations import *
from .structures import *
from .texts import *
from .functions import *
