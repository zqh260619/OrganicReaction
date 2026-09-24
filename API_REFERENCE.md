# OrganicReactionTools API 详解

本文档逐条说明 `OrganicReactionTools` 包对外暴露的全部功能。所有条目均以源码为准，
函数/方法签名按源码中的关键字参数（`*` 之后为仅关键字参数）抄录。

包的入口是 `from OrganicReactionTools import *`（见 [__init__.py](OrganicReactionTools/__init__.py)）。
该入口做了三件事：

1. 先 `from manim import *` 与 `from manim.typing import Vector3D`，把 manim 命名空间透出，
   因此 `Scene`、`Create`、`Write`、`DEGREES`、`UR`、`VGroup`、`Mobject`、`RED` 等可直接用；
2. 依次 `from .子模块 import *`，把下面 11 个子模块的公开名称重新导出；
3. 完整公开名称实测为 **684 个**（含 manim 全部公开名），其中本库自定义的类与函数共 **61 个**
   （模块分布：parameters 1、attributes 2、atoms 2、bonds 9、charges 12、decorations 6、
   electron_clouds 16、animations 5、structures 2、texts 3、functions 3）。

依赖版本：manim **0.21.0**（文档字符串按 0.20.1 渲染，见 `media/images`），Python **3.12**。

---

# ⚠️ 重要使用约定（务必先读）

本库有两处**必须遵守的调用约定**。它们不是缺陷，而是"电荷定位"与"轨道几何"两套机制的固有前提；
**违反约定的调用会在运行时直接抛异常**（`TypeError` / `ValueError`）。使用本库前请先确认这两条。

## 约定一：电荷类型必须与"原子是否有文本标签"匹配

> **无文本标签的原子 → 必须用 `*ByCoordinate`（带 `_COORDINATE` 后缀）版本；**
> **有文本标签的原子 → 必须用非坐标（不带后缀）版本。**

`ChargeType` 的 10 个取值按此分为**两组**，两组与原子状态**严格交叉配对、不可混用**：

| 电荷类型组 | 枚举取值 | 适用原子 | 用错的后果 |
|---|---|---|---|
| **非坐标版**（文本锚定） | `POSITIVE`、`NEGATIVE`、`SINGLE`、`PAIR`、`PARTIAL` | **有**文本标签的原子（`add_atom(text=...)` / `register_atom(mobject=...)` / `StructuralFormula(text=...)`） | 用在无文本原子上 → `TypeError: ... unexpected keyword argument 'position'` |
| **坐标版**（`*ByCoordinate`） | `POSITIVE_COORDINATE`、`NEGATIVE_COORDINATE`、`SINGLE_COORDINATE`、`PAIR_COORDINATE`、`PARTIAL_COORDINATE` | **无**文本标签的原子（`text=None` 的骨架碳节点等） | 用在有文本原子上 → `TypeError: ... unexpected keyword argument 'text'` |

> 上表中唯一的**双向可用例外是 `PARTIAL`**（不属于坐标版组，详见下方实测矩阵）。

**为什么必须这样配对**：非坐标版的图形类签名是 `(*, text, pos, attributes)` —— 它们需要**读原子文本的
包围盒角点**（`text.get_corner(pos)`）来定位电荷，`text` 必须是 `AtomicCluster`；
坐标版的签名是 `(*, position, attributes)` —— 它们只需要一个**绝对坐标**，天然适配没有文本的原子。
`Charge` 包装器则按 `text` 的实际类型分流，因此传入类型与原子状态不匹配时必然构造成员函数签名不符。

**正确写法示例**：

```python
# ✅ 有文本标签的原子（如 O、N、CH3）—— 用非坐标版
sf = StructuralFormula(name="C1", pos=[0,0,0], text=None)
sf.add_atom(name="O1", direction=90*DEGREES, text="O",
            bond_type=BondType.NORMAL_BOND, adjacency="C1")
sf.add_charge(text="O1", pos=UR, charge_type=ChargeType.NEGATIVE)          # ← 非坐标版

# ✅ 无文本标签的原子（骨架碳）—— 用坐标版
sf.add_atom(name="C2", direction=0, text=None,
            bond_type=BondType.NORMAL_BOND, adjacency="C1")
sf.add_charge(text="C2", pos=UR, charge_type=ChargeType.NEGATIVE_COORDINATE)  # ← 坐标版

# ❌ 以下两种都会在运行时抛 TypeError
sf.add_charge(text="C2", pos=UR, charge_type=ChargeType.NEGATIVE)             # 无文本原子 × 非坐标版
sf.add_charge(text="O1", pos=UR, charge_type=ChargeType.NEGATIVE_COORDINATE)  # 有文本原子 × 坐标版
```

> **仅 `PARTIAL` 一个取值是双向可用的例外**（实测）：`PartialCharge` 的签名同时接受
> `text`+`pos` 与 `position`，因此 `ChargeType.PARTIAL` 在**有文本**和**无文本**的原子上
> 都能正常工作。但请注意 **`PARTIAL_COORDINATE` 不属于例外** —— 它和其他 4 个坐标版一样，
> 用在有文本的原子上一律抛 `TypeError`。实测矩阵：

| 取值 | 有文本标签的原子 | 无文本标签的原子（`text=None`） |
|---|---|---|
| `POSITIVE`、`NEGATIVE`、`SINGLE`、`PAIR` | ✅ | ❌ `TypeError: ... 'position'` |
| **`PARTIAL`** | ✅ | ✅（**唯一双向可用**） |
| `PARTIAL_COORDINATE`、`POSITIVE_COORDINATE`、`NEGATIVE_COORDINATE`、`SINGLE_COORDINATE`、`PAIR_COORDINATE` | ❌ `TypeError: ... 'text'` | ✅ |

> 为保持可读性与一致性，**仍建议按上表配对使用**（有文本 → 非坐标版，无文本 → 坐标版），
> 把 `PARTIAL` 的双向能力当作兼容性冗余而非推荐用法。
>
> 若要挂电荷的原子恰好没有文本、又确实想用非坐标版，最省事的做法是**给该原子补一个文本标签**
> （如 `add_atom(..., text=r"\mathrm{C}")` 或 `register_atom(name=..., mobject=MathTex(r"\ "))`），
> 之后即可统一使用非坐标版 —— 非坐标版的 `anchor_mode="border"` 定位效果也是最好的。

## 约定二：分子轨道（成键/反键）必须传入两个**真实存在**的文本标签

> **`ElectronCloud` 构造分子轨道时，`texts` 必须是两个真实的 mobject，
> 不能包含 `None`（即不能用无文本标签的原子当标签）。**

- 涉及的类型：`ElectronCloudType.SIGMA_BOND_SS`、`SIGMA_ANTIBOND_SS`、`SIGMA_BOND_PP`、
  `SIGMA_BOND_SP`、`PI_BOND_PP`、`PI_ANTIBOND_PP`（即全部 6 种分子轨道）。
- 违反时抛：`ValueError("成键轨道与反键轨道必须同时提供 text1 和 text2 两个文本标签。")`。

```python
sf = StructuralFormula(name="C1", pos=[0,0,0], text=None)     # C1 无文本标签
sf.add_atom(name="O1", direction=90*DEGREES, text="O", bond_type=BondType.NORMAL_BOND, adjacency="C1")

# ❌ 错误：C1 是 text=None 的骨架原子，取出的 Mobject 为 None
ElectronCloud(cloud_type=ElectronCloudType.PI_BOND_PP,
              texts=[sf.atomic_clusters["C1"][Mobject],   # ← None
                     sf.atomic_clusters["O1"][Mobject]])
# ValueError: 成键轨道与反键轨道必须同时提供 text1 和 text2 两个文本标签。

# ✅ 正确：给两个参与成键的原子都补上真实文本标签
sf2 = StructuralFormula(name="C1", pos=[0,0,0], text=r"\mathrm{C}")
sf2.add_atom(name="O1", direction=90*DEGREES, text="O", bond_type=BondType.NORMAL_BOND, adjacency="C1")
ElectronCloud(cloud_type=ElectronCloudType.PI_BOND_PP,
              texts=[sf2.atomic_clusters["C1"][Mobject],
                     sf2.atomic_clusters["O1"][Mobject]])   # ✅ 正常
```

**为什么必须这样**：所有 6 种分子轨道的**尺寸、中心、方向、以及"让开标签"的偏置**
全部由两个文本标签的包围盒推导（内部函数 `_two_text_frame` 会取两标签四角在键方向与法向上的投影，
据此求出中缝、外侧锚点与缩放比例）。没有标签就无解，因此**这是刻意的强校验**，
而不是可以绕过的限制。

> **本约定不需要也不应当修改代码来"修复"**：它是几何可解性的前提，代码行为（抛异常并给出明确
> 中文提示）已经是正确的处理方式。使用者只需按约定提供两个真实标签即可。

**若确实需要在无文本节点上画分子轨道**，有两条合规途径：

1. 给该原子补一个**占位文本**（哪怕是空内容 mobject，如 `MathTex(r"\ ")`），
   让它成为合法的标签来源；
2. **不走包装器**，直接用几何参数手动构造图形类 —— `SigmaBondSS`、`SigmaAntiBondSS`、
   `SigmaBondPP`、`SigmaBondSP`、`PiBondPP`、`PiAntiBondPP` 在 `text1 = text2 = None` 时
   都有 `center` / `direction` / `length` / `width` 的回退路径，可自行指定几何。

---

## 目录

| 模块 | 功能域 | 条目 |
|---|---|---|
| `parameters.py` | 全局参数、默认文本基类 | 1 + 16 个常量 |
| `attributes.py` | 样式属性容器 | 2 |
| `atoms.py` | 原子文本、定位器 | 2 |
| `bonds.py` | 键几何、键包装器、键查询 | 9 |
| `charges.py` | 电荷图形、电荷包装器 | 12 |
| `decorations.py` | 括号、箭头、反应箭头 | 6 |
| `electron_clouds.py` | 轨道电子云、包装器 | 16 |
| `animations.py` | 迁移步骤、四类动画 | 5 |
| `structures.py` | 结构式总控类、苯环 | 2 |
| `texts.py` | 标题/副标题/描述 | 3 |
| `functions.py` | 时间线、布朗运动 | 3 |
| **合计** | | **61** |

---

## 1. `parameters.py`：全局参数与默认文本基类

所有数值都是**模块级可变全局变量**，导入后重新赋值即可全局改变默认外观。源码见
[parameters.py](OrganicReactionTools/parameters.py)。

### 1.1 `MathTex` — 本包默认的数学文本基类

```python
class MathTex(_ManimMathTex):
    def __init__(self, *tex_strings, tex_environment="gather*", **kwargs)
```

- **用途**：与 manim 的 `MathTex` 完全兼容，唯一区别是把默认 TeX 环境从 `align*`（各行**右**对齐）
  改为 `gather*`（各行**居中**）。本库所有文本类（`AtomicCluster`、`Title`、`Subtitle`、`Description`、
  电荷的 δ 文本、`ReactionArrow` 的字符串条件）都基于它。
- **关键参数**：显式传入 `tex_environment="align*"` 即恢复 manim 默认对齐行为。
- **附带全局量**：同模块定义 `mytemplate = TexTemplate()`，预置了 `\usepackage{ctex}`
  与 `\setlength{\jot}{-5pt}`，因此**可以直接写中文**（如 `Title(text=r"\text{示例一：…}")`）
  且多行行距更紧凑。该模板被所有文本类默认使用。
- **随机数**：`RNG = np.random.default_rng(seed=3)`，供 `brownian_motion` 使用，种子固定 ⇒ 动画可复现。

### 1.2 全局参数常量

| 常量 | 默认值 | 含义 |
|---|---|---|
| `bond_length` | `1` | 键长，同时作为 `length_global` 与电子云尺寸基准 |
| `edge` | `0.25` | 键两端相对原子文本的边距（避免线穿过文字） |
| `ratio_transition_state` | `1.2` | 过渡态虚键长度的放大比例 |
| `default_charge_edge` | `0.1` | 电荷相对原子文本的默认边距 |
| `reaction_arrow_buffer` | `1` | `ReactionArrow` 自适应长度相对上下方宽度的余量 |
| `reaction_arrow_gap` | `0.2` | 反应箭头与上下方文本边界的间距 |
| `reaction_arrow_font_size` | `25` | 反应箭头上下方文本默认字号 |
| `electron_cloud_length` | `bond_length` | 电子云单瓣卵形线长度 |
| `electron_cloud_width` | `0.55*bond_length` | 电子云单瓣卵形线宽度 |
| `electron_cloud_radius` | `0.5*bond_length` | s 轨道球半径 |
| `electron_cloud_small_ratio` | `0.5` | 杂化轨道小瓣/大瓣尺寸比 |
| `title_height` / `title_coordinate[3]` / `title_size` | `3` / `[0,3,0]` / `60` | 标题高度、坐标、字号 |
| `subtitle_height` / `subtitle_coordinate` / `subtitle_size` | `2.3` / `[0,2.3,0]` / `30` | 副标题同上 |
| `description_height` / `description_coordinate` | `-3` / `[0,-3,0]` | 描述文本位置 |
| `txt_size` | `35` | 原子文本默认字号 |
| `partial_charge_font_size` | `25` | δ 部分电荷字号 |

---

## 2. `attributes.py`：样式属性

源码见 [attributes.py](OrganicReactionTools/attributes.py)。

### 2.1 `AttributeHolder` — 样式属性的集中容器

```python
class AttributeHolder:
    def __init__(self, *, base_ratio_outbond, base_ratio_inbond, num_inbond,
                 dashed_length_dashedbond, dashed_ratio_dashedbond,
                 ratio_transition_state_dashedbond, length_global, color,
                 edge_global, font_size, font_size_partial,
                 radius_negative, ratio_negative, stroke_width_negative, edge_charge,
                 radius_positive, ratio_positive, stroke_width_positive,
                 radius_single, distance_pair, distance_double,
                 edge_ratio_double, distance_triple)
```

- **用途**：纯数据持有者（无方法），把"键、电荷、文字"全部几何与配色参数打包成一个对象，
  由 `StructuralFormula`、`Bond`、`Charge`、`ElectronCloud` 共享引用。改一个对象的字段即可
  影响该结构式下所有后续生成的图形。
- **23 个字段分组**：
  - 键：`base_ratio_outbond` / `base_ratio_inbond`（箭头形键、多线键的张开比例）、`num_inbond`（内键线数）、
    `dashed_length_dashedbond` / `dashed_ratio_dashedbond`（虚键的实线段长与占空比）、
    `ratio_transition_state_dashedbond`（过渡态虚键标称长度）、`length_global`（键长）、
    `edge_global`（键边距）、`distance_double` / `edge_ratio_double` / `distance_triple`（双键、三键线距）；
  - 电荷：`radius_negative` / `ratio_negative` / `stroke_width_negative`，`radius_positive` /
    `ratio_positive` / `stroke_width_positive`，`radius_single`、`distance_pair`（孤对电子两点间距）、
    `edge_charge`（电荷边距）、`font_size_partial`（δ 字号）；
  - 文本与颜色：`color`、`font_size`。
- **构造方式**：必须全量给出 23 个关键字参数，通常不直接用，而是通过 `StructuralFormula`
  的同名参数间接构造。

### 2.2 `DEFAULT_ATTRIBUTES` — 全局默认属性实例

- 一个模块级 `AttributeHolder` 实例，取值全部来自 `parameters.py` 的全局常量
  （如 `length_global=bond_length`、`color=WHITE`、`radius_negative=0.05`、`distance_pair=0.1`）。
- **用途**：在没有 `StructuralFormula` 上下文时（例如单独使用 `BondTypeTransform`、
  `PolarityArrow`、`ElectronCloud`）作为兜底属性；`ElectronCloud` 的 `attributes` 参数默认就是它。

---

## 3. `atoms.py`：原子与定位

源码见 [atoms.py](OrganicReactionTools/atoms.py)。

### 3.1 `Locator` — 原子定位器

```python
class Locator:
    def __init__(self, *, radians=None, degrees=None, coord=None)
    @classmethod up() / down() / left() / right() -> Locator
    def get_coord(self, sf: 'StructuralFormula', adjacency: str) -> Vector3D
```

- **用途**：描述"新原子相对邻接原子放在哪"，支持两种模式：
  **角度模式**（给 `radians` 或 `degrees`，沿该极角、按 `sf.attributes.length_global` 键长偏移）
  与**坐标模式**（给 `coord`，直接用绝对坐标）。优先级为 `coord` > `degrees` > `radians` > 默认 `0.0`。
- **工厂方法**：`Locator.up()` / `down()` / `left()` / `right()` 分别对应 π/2、-π/2、π、0 弧度。
- **`get_coord`**：坐标模式返回 `coord` 的副本；角度模式返回
  `length_global*[cosθ, sinθ, 0] + sf.atomic_clusters[adjacency]["pos"]`。
  引用不存在的邻接原子会抛 `KeyError`。
- **说明**：这是为了做几何抽象而保留的工具类；当前 `StructuralFormula.add_atom` 内部
  直接用 `direction` 做同样的三角运算，未走 `Locator`，两者公式一致。

### 3.2 `AtomicCluster` — 原子文本

```python
class AtomicCluster(MathTex):
    def __init__(self, *, text: str, pos: Vector3D,
                 attributes: 'AttributeHolder', text_offset: Vector3D = [0,0,0])
```

- **用途**：一个原子（或基团）的显示文本，是 `MathTex` 子类，默认套用 `mytemplate`
  （支持中文）与 `attributes.color`、`attributes.font_size`。
- **关键点 — 锚点与显示分离**：`self.atom_pos` 保存**键端点用的锚点** `pos`（初始等于传入 `pos`），
  而 `text_offset` 只产生显示位移。所有化学键的端点都取 `atom_pos`
  （`Bond.__init__` 中显式读取 `start.atom_pos`），因此文字微调不会带动键几何。取 `atom_pos`
  时用的是原始列表引用，非副本。
- **属性**：`atom_pos`（`np.ndarray`）、以及继承自 `MathTex` 的全部 mobject 能力。
- **用法**：一般不由用户直接构造，而是通过 `StructuralFormula(name=..., pos=..., text=...)`
  或 `add_atom(text=...)` 间接创建，再以 `sf.atomic_clusters[name][Mobject]` 取回。

---

## 4. `bonds.py`：化学键

源码见 [bonds.py](OrganicReactionTools/bonds.py)。分三层：**几何类**（画线）→ **`BondType` 枚举**（登记）
→ **`Bond` 包装器**（元数据 + 复用能力）→ **`BondLookup`**（查询）。

### 4.1 `OutBond` — 外向楔形键（实心三角）

```python
class OutBond(Polygon):
    def __init__(self, *, start: Vector3D, direction: float,
                 start_edge=False, end_edge=False, attributes: 'AttributeHolder')
```

- **用途**：立体化学中"朝向观察者"的键，画成从起点（细）到终点（宽）的实心三角形多边形。
- **几何**：起点 = `start + start_edge*edge_global*单位方向`；终点 = `start + (length_global - end_edge*edge_global)*单位方向`；
  终点处向法向两侧各张开 `base_ratio_outbond*(length_global-(start_edge+end_edge)*edge_global)/2`。
  填充不透明、无描边（`fill_opacity=1, stroke_width=0`）。
- **参数**：`start_edge` / `end_edge` 是布尔量，表示该端是否缩进一个 `edge_global`（通常有文本的一端要缩进）。

### 4.2 `InBond` — 内向楔形键（渐宽的多条横线）

```python
class InBond(VGroup):
    def __init__(self, *, start, direction, start_edge=False, end_edge=False, attributes)
```

- **用途**：立体化学中"远离观察者"的键。
- **几何**：在起点与"终点±`base_ratio_inbond*…/2` 法向偏移"之间按 `num_inbond`（默认 5）等分插值，
  画 `num_inbond` 条长度递增的 `Line`（`stroke_width=2`），形成从细到宽的梯形束。
- **返回**：`VGroup`，子对象顺序即从窄到宽。

### 4.3 `DashedBond` — 过渡态虚键

```python
class DashedBond(DashedLine):
    def __init__(self, *, start, direction, start_edge=False, end_edge=False,
                 attributes, length: float | None = None)
```

- **用途**：表示部分成键/超共轭等非标准长度的连接（反应过渡态）。
- **长度两种语义**：`length=None`（默认）时按旧约定画**标称长度**
  `length_global*ratio_transition_state_dashedbond`（比普通键稍长）；`length` 显式给定时按该长度**精确**绘制。
  经 `Bond` 包装器构造时**总是**自动传入 `start` 与 `end` 的真实距离，因此包装后的虚键一定画到指定端点。
- **实测长度**：独立构造时标称长度为 `1.2`（= `length_global × ratio_transition_state_dashedbond = 1 × 1.2`）；
  经 `Bond` 包装器（即 `add_atom(bond_type=DASHED_BOND)`）构造时，画到两端点真实距离 `1.0`。
- **样式**：`dash_length` / `dashed_ratio` 取自 `attributes`。

### 4.4 `NormalBond` — 普通单键

```python
class NormalBond(Line):
    def __init__(self, *, start, direction, start_edge=False, end_edge=False, attributes)
```

- **用途**：最基础的单键，两端按 `edge_global` 缩进的直线。使用 manim 默认线宽。

### 4.5 `DoubleBond` — 双键（支持不对称长短线）

```python
class DoubleBond(VGroup):
    def __init__(self, *, start, direction, start_edge=False, end_edge=False,
                 attributes, side: int, start_side_edge: bool, end_side_edge: bool)
```

- **用途**：双键。通过 `side` 控制"两条线等长"还是"一长一短"（画不对称双键，如共轭/芳香体系常用）。
- **方向约定（源码注释的手性规则）**：右手平行屏幕、掌心向屏幕内侧、食指从 `start` 指向 `end`，
  **大拇指所指的一侧就是较短那条线的位置**。
- **三种取值**：
  - `side=0`：两线左右对称（各偏移 `0.5*length_global*edge_ratio_double`），等长；
  - `side=1`：主线在法向 `-` 侧、短线在 `+` 侧，右手法；
  - `side=-1`：短线在 `-` 侧，左手法。
  短线端是否额外缩进由 `start_side_edge` / `end_side_edge` 控制（`edge_ratio_double`）。
- **返回**：`VGroup`，`submobjects[0]` 是主线、`[1]` 是第二条线；`RotateAtoms`/`BondTypeTransform`
  按此顺序原地重建几何。

### 4.6 `TripleBond` — 三键

```python
class TripleBond(VGroup):
    def __init__(self, *, start, direction, start_edge=False, end_edge=False, attributes)
```

- **用途**：三键；主线居中，另两条各向法向两侧偏移 `length_global*distance_triple`，三线等长。
- **返回**：`VGroup` 含 3 条 `Line`，顺序为「中、`-` 法向、`+` 法向」。

### 4.7 `BondType` — 键类型枚举

```python
class BondType(Enum):
    NORMAL_BOND = NormalBond      IN_BOND = InBond        OUT_BOND = OutBond
    DASHED_BOND = DashedBond      DOUBLE_BOND = DoubleBond TRIPLE_BOND = TripleBond
```

- **用途**：枚举值即**几何类本身**（不是字符串），因此 `Bond` 里可直接 `bond_type.value(...)` 实例化。
  这是全库统一的"枚举登记类"模式（电荷、电子云同构）。
- **典型取值**：`BondType.NORMAL_BOND`、`BondType.DOUBLE_BOND`、`BondType.DASHED_BOND` 等。

### 4.8 `Bond` — 化学键包装器

```python
class Bond(VGroup):
    def __init__(self, *, bond_type: BondType, start, end, start_edge=False, end_edge=True,
                 attributes: AttributeHolder, side=None, start_side_edge=None,
                 end_side_edge=None, atom1: str | None = None, atom2: str | None = None)
```

- **用途**：几何类之上的包装器，供 `StructuralFormula` 与动画系统使用。`VGroup` 子类，
  内部只放一个几何体（`self.submobjects[0]`）。
- **端点解析**：`start` / `end` 可以是 `AtomicCluster` 或 `Vector3D`；若是 `AtomicCluster`
  则自动改用其 **`atom_pos` 锚点**（不受 `text_offset` 影响）。`end_edge` 默认 **`True`**
  （因为"终点原子通常有文本"）。
- **记录/暴露的元数据**：
  - `bond_type`（后续 `BondTypeTransform.finish()` 会更新）、
  - `start` / `end`（np 数组）、`direction = arctan2(Δy, Δx)`（弧度，几何类靠它定向）、
  - `start_edge` / `end_edge` / `side` / `start_side_edge` / `end_side_edge`，
  - `atom1` / `atom2`（两端原子名，`sync_migration` 自动登记键时依赖这两个标签）。
- **分支构造**：`DOUBLE_BOND` 额外传 `side`、`start_side_edge`、`end_side_edge`；
  `DASHED_BOND` 传真实距离当 `length`；其余用默认标称长度。

### 4.9 `BondLookup` — 键查询器

```python
class BondLookup:
    def __init__(self, sf: 'StructuralFormula')
    between(start, end) -> Bond                     # 找不到抛 ValueError
    between_or_none(start, end) -> Bond | None
    is_bonded(start, end) -> bool
    type_between(start, end) -> BondType
    bonds(name) -> list[Bond]
    of_type(name, bond_type: BondType) -> list[Bond]
    find(start=None, end=None, bond_type=None) -> Bond | None
    all_bonds() -> list[Bond]
```

- **用途**：以 `sf.atomic_clusters[name][Bond]` 键列表为**唯一事实来源**的只读查询器，
  键按**身份**（`in` / `id()`）比较，不做几何判断。
- **获取方式**：`sf.bond_lookup`（property，每次返回新的轻量实例，无需自己构造）。
- **各方法**：
  - `between` / `between_or_none`：取两原子共有的那条键，前者找不到抛
    `ValueError("原子 'X' 与 'Y' 之间不存在键。")`，后者返回 `None`（`start == end` 也返回 `None`）；
  - `is_bonded`：布尔便捷判断，等价于 `between_or_none(...) is not None`；
  - `type_between`：直接返回 `bond_type`，不存在则抛 `ValueError`；
  - `bonds(name)`：某原子的全部键的**副本列表**（改副本不影响结构）；
  - `of_type(name, bond_type)`：某原子上指定类型的键（如列出一个碳上所有双键）；
  - `find(start, end, bond_type)`：条件查找第一条匹配键，`start` / `end` **至少给一个**
    （都给则要求键同时连着两端），类型可选过滤；两个都不给抛 `ValueError`；找不到返回 `None`；
  - `all_bonds()`：全结构去重后的键列表，按首次出现顺序（内部按 `id` 去重，因一条键同时挂在两个原子上）。
- **错误**：原子名不存在时，`bonds` / `of_type` / `find` / `between` 均抛 `ValueError("原子 'X' 不存在于结构中。")`。

---

## 5. `charges.py`：电荷

源码见 [charges.py](OrganicReactionTools/charges.py)。同样是"图形类 → `ChargeType` → `Charge` 包装器"三层结构，
并且每类都提供**文本锚定版**与**坐标版（`...ByCoordinate`）**两套实现。

### 5.1 `NegativeCharge` — 负电荷 ⊖

```python
class NegativeCharge(VGroup):
    def __init__(self, *, text: MathTex, pos: Vector3D, attributes)
```

- **用途**：官能团负电荷符号。锚点 = `text.get_corner(pos) + pos*edge_charge`，
  先取文本在 `pos` 方向的角点，再沿 `pos` 方向外移一个 `edge_charge`（默认 0.1）。
- **组成**：一个半径 `radius_negative`、线宽 `stroke_width_negative` 的圆 + 一条水平横线
  （左端到右端 = `±radius_negative*ratio_negative`）。

### 5.2 `PositiveCharge` — 正电荷 ⊕

```python
class PositiveCharge(VGroup):
    def __init__(self, *, text: MathTex, pos: Vector3D, attributes)
```

- **用途**：正电荷符号，锚点算法同上（用 `radius_positive` / `stroke_width_positive`）。
- **组成**：圆 + 横线 + 竖线（两条线各 `±radius_positive*ratio_positive`）。

### 5.3 `SingleCharge` — 单电子 ·

```python
class SingleCharge(Circle):
    def __init__(self, *, text: MathTex, pos: Vector3D, attributes)
```

- **用途**：自由基的单电子（一个实心小圆点）。半径为 `radius_single`（默认 0.01），`fill_opacity=1`。

### 5.4 `PairCharge` — 孤对电子 ¨

```python
class PairCharge(VGroup):
    def __init__(self, *, text: MathTex, pos: Vector3D, attributes)
```

- **用途**：孤对电子（两个与 `SingleCharge` 同半径的圆点）。
- **关键几何约定**：两个圆点中心位于电荷锚点两侧、相距 `distance_pair`（默认 0.1），
  并且**两点连线始终垂直于"文本中心 → 两点中点"的连线**。实现上先求单位方向
  `direction = (锚点 - 文本中心)`，再取法向 `normal = (-dy, dx, 0)`，两点为
  `锚点 ± normal*distance_pair/2`。若文本中心与锚点重合（退化）则回退用 `pos`，再退化则用 `+x`。

### 5.5 `NegativeChargeByCoordinate` / `PositiveChargeByCoordinate` / `SingleChargeByCoordinate`

```python
class NegativeChargeByCoordinate(VGroup):
    def __init__(self, *, position: Vector3D, attributes)
# PositiveChargeByCoordinate、SingleChargeByCoordinate 同签名
```

- **用途**：坐标版电荷，直接以 `position` 作为电荷锚点（不再从文本角点推算），
  图形与对应文本版完全一致。
- **⭐ 唯一适用场景**：**原子没有文本标签（`text=None`）时只能用它**
  —— 见 [约定一](#约定一电荷类型必须与原子是否有文本标签匹配)。有文本标签的原子**不要**用这一组。

### 5.6 `PairChargeByCoordinate` — 坐标版孤对电子

```python
class PairChargeByCoordinate(VGroup):
    def __init__(self, *, position: Vector3D, attributes)
```

- **用途**：`PairCharge` 的坐标版；`position` 是两圆点中点。
- **两种行为**：**直接构造**时两圆点水平排列在 `position` 两侧；
  通过 `Charge` 包装器（`add_charge` / `build_charge`）构造时，包装器会自动把它旋转到
  与"原子 `pos` → 两圆点中点"方向**垂直**（`rotate(arctan2(pos.y, pos.x) + π/2)`）。

### 5.7 `PartialCharge` — 部分电荷 δ…δ⁺/⁻

```python
class PartialCharge(VGroup):
    def __init__(self, *, text: MathTex | None = None, pos: Vector3D | None = None,
                 position: Vector3D | None = None, attributes,
                 delta_count: int = 1, sign: str = "+", anchor_mode: str = "border")
```

- **用途**：极性键上的部分电荷 δ⁺ / δ⁻，支持多 δ（如 δδ⁺）。TeX 串由
  `r"\delta"*delta_count + "^{" + sign + "}"` 生成；字号取 `attributes.font_size_partial`。
- **定位模式 `anchor_mode`（两种，语义差别很重要）**：
  - `"border"`（默认）：电荷文本**边框上与 `pos` 反向的那个点**，与原子文本在 `pos` 方向的
    角点**重合**。例如 `pos=UR` 时，`δδ+` 的左下角贴住原子文本的右上角。
    该模式**忽略 `edge_charge`**，且必须提供非零 `pos`。
  - `"center"`：电荷文本**中心**位于"原子文本角点 + `pos*edge_charge`"，即保持传统中心对齐。
- **位置来源**：给 `position` 就直接用该坐标；否则必须**同时**给 `text` 与 `pos`。
- **校验（全部抛 `ValueError`）**：`delta_count` 必须是 ≥1 的 **int**；`sign` 只能是 `"+"` / `"-"`；
  `anchor_mode` 只能是 `"border"` / `"center"`；`border` 模式缺 `pos`、或位置信息不足、或 `pos` 为零向量。
- **暴露属性**：`delta_count`、`sign`、`anchor_mode`、`position`（最终对齐点）、`font_size`、`charge_text`。

### 5.8 `PartialChargeByCoordinate` — 坐标版部分电荷

```python
class PartialChargeByCoordinate(PartialCharge):
    def __init__(self, *, position: Vector3D, attributes, delta_count=1, sign="+",
                 anchor_mode="border", pos: Vector3D | None = None)
```

- **用途**：`PartialCharge` 的坐标版本；`position` 直接指定电荷位置。
  在 `anchor_mode="border"` 时仍需 `pos` 指定方向，用于决定与 `position` 对齐的边框点。

### 5.9 `ChargeType` — 电荷类型枚举

```python
class ChargeType(Enum):
    POSITIVE = PositiveCharge                 NEGATIVE = NegativeCharge
    SINGLE = SingleCharge                     PAIR = PairCharge
    PARTIAL = PartialCharge                   PARTIAL_COORDINATE = PartialChargeByCoordinate
    POSITIVE_COORDINATE = PositiveChargeByCoordinate
    NEGATIVE_COORDINATE = NegativeChargeByCoordinate
    SINGLE_COORDINATE = SingleChargeByCoordinate
    PAIR_COORDINATE = PairChargeByCoordinate
```

- **用途**：10 个取值，前 5 个为文本锚定版、后 5 个为坐标版。`StructuralFormula.add_charge`
  与 `build_charge` 只接受这些枚举值。
- **⭐⭐ 选型规则（强制，见 [约定一](#约定一电荷类型必须与原子是否有文本标签匹配)）**：

  | 目标原子 | 必须使用的取值 |
  |---|---|
  | **有**文本标签（`text=` / `mobject=` 非空） | `POSITIVE`、`NEGATIVE`、`SINGLE`、`PAIR`、`PARTIAL`（**不带** `_COORDINATE` 后缀的 5 个） |
  | **无**文本标签（`text=None`） | `POSITIVE_COORDINATE`、`NEGATIVE_COORDINATE`、`SINGLE_COORDINATE`、`PAIR_COORDINATE`、`PARTIAL_COORDINATE`（**带**后缀的 5 个） |

  **两组不可互换**：选错会在运行时抛 `TypeError`。**唯一例外是 `PARTIAL`**（有/无文本原子都可用）；
  `PARTIAL_COORDINATE` 不属例外，仍只适用于无文本原子。完整对照表与原因见文首
  [约定一](#约定一电荷类型必须与原子是否有文本标签匹配)。

### 5.10 `Charge` — 电荷包装器

```python
class Charge(VGroup):
    def __init__(self, *, charge_type: ChargeType, text: AtomicCluster | Vector3D,
                 pos: Vector3D, attributes, atom_name: str | None = None,
                 delta_count: int = 1, sign: str = "+", anchor_mode: str = "border")
```

- **用途**：统一入口。根据 `text` 的类型分流：`AtomicCluster` 走文本锚定版，
  `Vector3D` 走坐标版（位置 = `pos*edge_charge + text`，但 `border` 模式的部分电荷例外：
  `position` 直接取 `text` 作为对齐点、忽略 `edge_charge`）。
- **`PAIR_COORDINATE` 特例**：构造后自动旋转到与 `pos` 垂直（见 5.6）。
- **元数据**：`charge_type`、`text`、`atom_name`（`sync_migration` 登记电荷时依赖此标签）。
- **`delta_count` / `sign` / `anchor_mode`**：仅对 `PARTIAL` 与 `PARTIAL_COORDINATE` 生效，
  其它类型传入会被忽略（不会报错）。
- **⭐⭐ 选型规则（本包装器最重要的使用约束，违反即抛 `TypeError`）**：
  必须让 `charge_type` 与"原子是否有文本标签"匹配 ——
  **无文本标签的原子只用 `*_COORDINATE` 版本，有文本标签的原子只用非坐标版本**。
  完整对照表、报错原文与正确/错误写法示例见文首
  [约定一](#约定一电荷类型必须与原子是否有文本标签匹配)；下面的实测记录是它的依据。

  | `charge_type` 组 | 原子**有**文本标签 | 原子**无**文本标签（`text=None`） |
  |---|---|---|
  | **非坐标版**：`POSITIVE`、`NEGATIVE`、`SINGLE`、`PAIR`、`PARTIAL` | ✅ 全部正常 | ❌ 前 4 个抛 `TypeError: ... unexpected keyword argument 'position'`；**`PARTIAL` 例外：✅ 正常** |
  | **坐标版**：`*_COORDINATE` 五种 | ❌ 抛 `TypeError: ... unexpected keyword argument 'text'`（**含 `PARTIAL_COORDINATE`**） | ✅ 全部正常 |

  > 上表已实测确认：双向可用的只有 `PARTIAL` **一个**取值；`PARTIAL_COORDINATE` 与其余 4 个
  > 坐标版一样，属于"仅无文本原子可用"。

  两条报错的成因（对应上面表格的两行）：

  - **无文本原子 × 非坐标版**：此时 `add_charge` 的 `self.atomic_clusters[text][Mobject] or ...["pos"]`
    求值结果退化成一个**坐标**（`Vector3D`），`Charge` 于是走
    `charge_type.value(position=..., ...)` 坐标分支；而非坐标版的签名是
    `(*, text, pos, attributes)`，**没有 `position` 形参**，故抛
    `TypeError: ... unexpected keyword argument 'position'`。
  - **有文本原子 × 坐标版**：只要原子有文本，传入 `Charge` 的就一定是 `AtomicCluster`，
    `Charge` 于是走文本分支并调用 `charge_type.value(text=..., pos=..., ...)`；
    而坐标版的签名是 `(*, position, attributes, ...)`，**没有 `text` 形参**，故抛
    `TypeError: ... unexpected keyword argument 'text'`（实测例：
    `sf.add_charge(text='A', pos=UR, charge_type=ChargeType.NEGATIVE_COORDINATE)` →
    `NegativeChargeByCoordinate.__init__() got an unexpected keyword argument 'text'`）。

  **两条合规出路**：① 按原子状态选对应的一组类型（推荐，也是本库的设计意图）；
  ② 给所有需要挂电荷的原子统一补上文本标签，然后统一用非坐标版
  （其 `anchor_mode="border"` 定位效果也最好）。

---

## 6. `decorations.py`：装饰图形

源码见 [decorations.py](OrganicReactionTools/decorations.py)。

### 6.1 `BracketBetweenPoints` — 括号

```python
class BracketBetweenPoints(VGroup):
    def __init__(self, *, start: Vector3D, end: Vector3D, ratio_edge=0.1, **kwargs)
```

- **用途**：在两点之间画一个"左括号"形状（直线 + 两端同向短线），常用于标注一段结构（如共振式的一侧）。
- **约定（源码注释）**：按左括号理解，**上端是 `start`、下端是 `end`**。
- **几何**：`main` 为主线；两端各加一条沿法向 `(-dy, dx, 0)`、长度 `ratio_edge` 的短线。
- **参数**：`ratio_edge` 是短相对主线的比例；`**kwargs` 透传给三条 `Line`（可设 `color`、`stroke_width`）。
- **返回**：`VGroup(edge_start, main, edge_end)`。

### 6.2 `BezierArrow` — 三次贝塞尔曲线箭头

```python
class BezierArrow(VGroup):
    def __init__(self, *, start_anchor, start_handle, end_anchor, end_handle,
                 color=WHITE, stroke_width=2, arrow_size=-1.0, opacity=1.0, **kwargs)
```

- **用途**：画弯曲的电子转移箭头（弯箭头）。给定三次贝塞尔的起点/起点控制柄/终点/终点控制柄。
- **默认箭头大小**：`arrow_size=-1` 时自动取起终点距离的 15%。
- **组成的两个可寻址部件**：`self.bezier`（`CubicBezier` 曲线）与 `self.tip`（`ArrowTriangleFilledTip`）。
  箭头三角会被旋转到底点切线方向并按魔法系数回缩，使箭头与曲线不重叠且中心对齐
  （源码注明这些魔数"建议不要随意修改"）。
- **`opacity`**：同时作用于曲线描边与箭头填充（`OpacityEffect` 动画专门识别这两个部件）。

### 6.3 `LightArrow` — 光照/光箭头

```python
class LightArrow(VGroup):
    def __init__(self, *, end: Vector3D, length: float = 1.5, pos: Vector3D = UL,
                 color=YELLOW, mark: bool = True, width=1, end_edge: float = 0, **kwargs)
```

- **用途**：从 `end` 点向 `pos` 方向（默认 `UL` 左上）伸出的光照箭头，用于表示光子照射（如自由基引发步骤）。
- **几何**：起点 = `end + pos*length`；终点 = `end + pos*end_edge`（`end_edge=0` 即正好指到 `end`）。
- **`mark=True`（默认）**：在箭头中点附近额外显示 `MathTex(r"h\nu")`（黄色、字号 15），
  即"光子"标注；设 `False` 则只画箭头。
- **属性**：`length`、`start`、`end`。

### 6.4 `PolarityArrow` — 键极性箭头（δ⁺→δ⁻）

```python
class PolarityArrow(VGroup):
    def __init__(self, *, start: Vector3D, direction: float, attributes,
                 length: float = -1.0, tail_offset: float = 0.07, **kwargs)
```

- **用途**：化学键极性的标准箭头，从正电端（δ⁺）指向负电端（δ⁻），尾部带一个十字小横杠。
- **几何规格**：
  - 总长度默认（`length=-1`）为 `length_global - 2*edge_global`，即**与"两端都有边距"的单键线段等长**；
  - 线宽为 manim 单键默认线宽的一半（`DEFAULT_STROKE_WIDTH/2`），并显式禁用按长度收缩线宽
    （`max_stroke_width_to_length_ratio=1000`）；
  - 末端箭头三角长度为 `length*0.15`（`max_tip_length_to_length_ratio=1` 允许长尖）；
  - 尾部十字：中点位于起点沿箭头方向 `tail_offset` 处，长度 `2*tail_offset`，与箭头垂直。
- **属性**：`start`、`end`、`length`、`direction`、`tail_offset`、`arrow`、`tail_bar`。

### 6.5 `BondPolarityArrow` — 键旁极性箭头

```python
class BondPolarityArrow(PolarityArrow):
    def __init__(self, *, start: Vector3D, end: Vector3D, attributes, side: int,
                 tail_offset: float = 0.07, offset: float = -1.0, length: float = -1.0, **kwargs)
```

- **用途**：给定键的两端坐标，自动算好位置与指向的极性箭头。
- **侧向约定 `side`**：与 `DoubleBond` 的 `side≠0` 完全一致的手性约定（右手/左手定则）：
  `side=1` 右手侧（`+` 法向）、`side=-1` 左手侧（`-` 法向）；**`side=0` 会抛 `ValueError`**。
- **默认值**：`offset=-1` ⇒ 箭头与键的距离 = 尾部小线段长度 `2*tail_offset`；
  `length=-1` ⇒ 键长 − `2*edge_global`。
- **核心几何不变式**：由"箭头中点与键线段中点的连线垂直于键所在直线"反推箭头起点
  `arrow_start = 键起点 + (键长-length)/2*键方向 + side*offset*法向`，
  因此**对任意 `length` 该垂直性质都成立**（长度变化时箭头起点自动平移）。
- **额外属性**：`bond_start` / `bond_end`（键的两端）、`side`、`offset`。
  注意 `self.start` / `self.end` 是**箭头自身**的起终点，不是键的端点。
- **校验**：键起终点重合时抛 `ValueError("键的起点与终点不能重合。")`。

### 6.6 `ReactionArrow` — 反应箭头

```python
class ReactionArrow(VGroup):
    def __init__(self, *, start: Vector3D, above=None, below=None, length: float = -1.0,
                 buffer: float = reaction_arrow_buffer, gap: float = reaction_arrow_gap,
                 color=WHITE, font_size: float = reaction_arrow_font_size, **kwargs)
    def rebuild(self) -> None
```

- **用途**：标准的水平右向反应箭头，箭头**上方**放反应条件、**下方**放试剂/催化剂等。
- **输入形式极灵活**：`above` / `below` 各自可以是**单个 Mobject**、**Mobject 列表**或 **TeX 字符串**。
  - 字符串：用本包 `MathTex` + `mytemplate` 按 `font_size` 渲染 ⇒ **可写中文**、可用 `\mathrm{}`；
  - 列表：`VGroup(...).arrange(DOWN, buff=0.2)` 竖直堆叠成一栏，宽度取整栏边界宽度；
  - `above` 与 `below` **不能同时为空**（否则抛 `ValueError`）。
- **几何规格**：
  - 箭头强制水平、指向右侧，由 `start`（尾端）与 `length`（尾端到箭尖总长）确定；
  - 上下方对象**水平居中于箭头中点**（`start.x + length/2`）；
  - 上下方对象的**外沿**（下沿/上沿）与箭头直线距离为 `gap`（负值被夹取为 `0`）；
  - `length=-1` 时**自适应**：`max(上方整体宽度, 下方整体宽度) + buffer`。
- **样式与层级**：默认线宽 `DEFAULT_STROKE_WIDTH/2`、默认尖端长度 `length*0.075`
  （都是 `PolarityArrow` 所用值的一半），可用 `stroke_width` / `tip_length` 覆盖并会被 `rebuild` 保持；
  上下方内容统一 `set_color(color)`，且 `z_index` 至少提升到 2 ⇒ **文本压在箭头之上，不会被压住**。
- **`rebuild()`**：在**文本内容或字号改变后**调用，按当前尺寸重新自适应长度与间距并重排。
  它以箭头当前实际位置为新起点，因此 `move_to` / `shift` 之后再 `rebuild` 仍满足几何契约。
- **校验**：`length` 显式给定但 `≤0`、`buffer<0`、`font_size≤0` 均抛 `ValueError`。

---

## 7. `electron_clouds.py`：电子云

源码见 [electron_clouds.py](OrganicReactionTools/electron_clouds.py)。
文件内部先有一批**私有**几何辅助函数（`_two_text_frame`、`_outward_oval_lobe`、`_resolve_lobe_styles` 等）
负责"自动让开文本标签 + 校验方向 + 分瓣配色"，随后是 14 个图形类。所有图形类共享同一套参数语义：

- `center` / `text`（原子轨道）或 `text1` / `text2`（成键、反键轨道）：**给了文本标签就自动按标签推算中心与尺寸**，
  否则回退用 `center` / `direction`；
- `color` / `opacity` / `stroke_width` / `lobe_colors` / `lobe_opacities`：统一或逐瓣配色；
  逐瓣列表长度不匹配、`opacity` 不在 `[0,1]` 等都会抛 `ValueError`；
- `attributes`：仅用于缺省颜色（缺省时用 `WHITE`）；
- `text_buff`：图形与文本标签之间的最小间距；
- 每个实例都暴露 `lobes` 列表（各瓣可寻址）、`center_point`、`direction` 等元数据。

### 7.1 `OvalLine` — 卵形线（单瓣电子云轮廓）

```python
class OvalLine(ParametricFunction):
    def __init__(self, *, center=None, direction: float = 0, length=None, width=None,
                 sharpness: float = 0.4, tip_ratio: float = 0.9, round_ratio: float = 1.1,
                 color=None, opacity: float = 1.0, stroke_width: float = 2, attributes=None,
                 text=None, text_buff=0.06, use_smoothing: bool = False, **kwargs)
```

- **用途**：一切"瓣"的基础形状 —— 一条**尖端朝内、圆端朝外**的闭合凸曲线（类蛋形），
  由参数方程采样 2001 个点生成并 `close_path()`。
- **形状控制**：
  - `sharpness` ∈ (0,1)，默认 0.4 —— 不对称程度，此默认值保证整条曲线**凸、无凹陷**；
  - `tip_ratio`（默认 0.9，越小尖端越尖）控制尖端附近宽窄；`round_ratio`（默认 1.1，越大圆端越粗）控制圆端；
  - `length` 为尖端到圆端长度，`width` 为垂直方向最大宽度，**两参数互相独立**（实现上是先构造
    归一化基准曲线再分别缩放 x/y，并用 `half_width` 归一化）。
- **自动避让文本**：给定 `text` 时，尖端起点整体沿 `direction` 外移 `0.5*hypot(text.width, text.height)+text_buff`，
  同时缺省 `length` / `width` 也按标签尺寸放大（`max(基准值, 2*r)` / `max(基准值, 1.5*r)`），
  最后把文本 `z_index` 提到 2。
- **暴露属性**：`center_point`、`tip_point`、`round_end_point`、`direction`、`length`、`lobe_width`、
  `sharpness`、`tip_ratio`、`round_ratio`、`lobe_color`、`lobe_opacity`、`text`、`text_buff`、`lobes=[self]`。
- **校验**：`sharpness` 不在 (0,1)、`tip_ratio≤0`、`round_ratio≤0`、`opacity` 越界、`length≤0`、`width≤0` 均抛 `ValueError`。
- **`use_smoothing`**：是否对采样点做 manim 平滑，默认 `False`。

### 7.2 `SOrbital` — s 轨道（球）

```python
class SOrbital(Circle):
    def __init__(self, *, center=None, direction: float = 0, radius=None, color=None,
                 opacity: float = 1.0, stroke_width: float = 2, attributes=None,
                 text=None, text_buff=0.06, **kwargs)
```

- **用途**：s 轨道的球形电子云，一个填充圆，中心默认取 `text` 中心。
- **缺省半径**：`max(electron_cloud_radius, 标签半径)` ⇒ 自动包住原子标签。
- **`direction`**：圆各向同性，保留该参数只为与其它图形类接口统一。

### 7.3 `POrbital` — p 轨道（哑铃）

```python
class POrbital(VGroup):
    def __init__(self, *, center=None, direction: float = 0, separation=None, length=None,
                 width=None, color=None, opacity=1.0, lobe_colors=None, lobe_opacities=None,
                 stroke_width: float = 2, attributes=None, text=None, text_buff=0.06, **kwargs)
```

- **用途**：p 轨道两个**等大**的瓣，沿 `direction` 正反两个方向。
- **几何**：两瓣尖端朝内（指向文本标签）、圆端朝外；`separation` 控制两尖端间距，
  缺省为 `max(0.05, 2*标签半径)` ⇒ 既避免曲线重叠又让开标签。
- **可寻址部件**：`self.positive_lobe`（`+direction` 侧）、`self.negative_lobe`（`-direction` 侧），
  以及 `self.lobes = [positive, negative]`。两瓣可分别配色（`lobe_colors` 长度须为 2）。
- **校验**：内部的 `_outward_oval_lobe` 会检查"圆端必须比尖端离参考中心更远"，
  否则抛 `ValueError("卵形线必须尖端朝里、圆端朝外，请检查 outward_direction 参数。")`。

### 7.4 `HybridOrbital` — 杂化轨道（大瓣 + 小瓣）

```python
class HybridOrbital(VGroup):
    def __init__(self, *, center=None, direction: float = 0, separation=None, length=None,
                 width=None, small_ratio: float = electron_cloud_small_ratio, color=None,
                 opacity=1.0, lobe_colors=None, lobe_opacities=None, stroke_width: float = 2,
                 attributes=None, text=None, text_buff=0.06, **kwargs)
```

- **用途**：sp / sp² / sp³ 杂化轨道的单个轨道：**大瓣沿 `direction`、小瓣沿反方向**，两瓣尖端朝内。
- **尺寸**：小瓣 = 大瓣的 `length` / `width` **同乘 `small_ratio`**（默认 0.5），即形状相似、等比例缩小。
- **说明**：三种杂化轨道的单瓣形状相同，差别只在空间取向，因此本类只描述**单个**杂化轨道；
  用户按几何需要自行摆放多个实例（例如 sp³ 的四个方向）。
- **可寻址部件**：`large_lobe`、`small_lobe`、`lobes`；属性含 `small_ratio`。
- **校验**：`small_ratio≤0` 抛 `ValueError`。

### 7.5 `SPOrbital` / `SP2Orbital` / `SP3Orbital` — 杂化轨道别名

```python
class SPOrbital(HybridOrbital): ...   # sp
class SP2Orbital(HybridOrbital): ...  # sp2
class SP3Orbital(HybridOrbital): ...  # sp3
```

- **用途**：三个**零改写**子类，纯粹为语义命名与 `ElectronCloudType` 枚举提供三个独立类型，
  参数、行为与 `HybridOrbital` 完全相同。

### 7.6 `SigmaBondSS` — s-s σ 成键轨道

```python
class SigmaBondSS(Ellipse):
    def __init__(self, *, center=None, direction=None, length=None, width=None, color=None,
                 opacity=1.0, stroke_width=2, attributes=None,
                 text1=None, text2=None, text_buff=0.15, **kwargs)
```

- **用途**：两个 s 轨道头碰头形成的 σ 成键轨道 —— 一个把两个原子标签**都包在内部**的填充椭圆。
- **几何（有标签时）**：长轴沿 `text1 → text2` 方向，`length = 0.8*max(electron_cloud_length, 两标签外沿总跨度+2*text_buff)`，
  `width = max(0.5, 2*max_normal_half, 0.75*length)`。
- **无标签时**：退化为按 `center` / `direction` 摆放，`length = 0.8*electron_cloud_length`、`width = max(0.4, 0.75*length)`。
- **属性**：`center_point`、`direction`、`length`、`ellipse_width`、`text1`、`text2`、`lobes=[self]`。

### 7.7 `SigmaAntiBondSSLobe` — s-s σ 反键单瓣

```python
class SigmaAntiBondSSLobe(OvalLine):
    ...
```

- **用途**：`SigmaAntiBondSS` 的一瓣（尖端位于 `center` 或标签外侧的卵形线），
  以独立类名暴露以便单独引用/继承；参数与 `OvalLine` 完全一致。

### 7.8 `SigmaAntiBondSS` — s-s σ 反键轨道

```python
class SigmaAntiBondSS(VGroup):
    def __init__(self, *, center=None, direction=None, separation=None, length=None, width=None,
                 color=None, opacity=1.0, lobe_colors=None, lobe_opacities=None,
                 stroke_width=2, attributes=None, text1=None, text2=None, text_buff=0.15, **kwargs)
```

- **用途**：两个 s 轨道反相组合的 σ* 反键轨道 —— **两瓣卵形线**，各自包住 `text1` / `text2`，
  尖端朝向键中心、圆端朝外，两瓣间留出节面空隙。
- **几何（有标签时）**：`separation` 缺省时按"两标签内沿 ± 曲线间隙"精确取尖端位置；
  `length = max(1.2*electron_cloud_length, 2*max_axis_half)`、`width = max(1.2*electron_cloud_width, 2*max_normal_half)`。
- **可寻址部件**：`right_lobe`、`left_lobe`、`lobes`；无标签时 `separation` 缺省 0.3。

### 7.9 `SigmaBondPP` — p-p σ 成键轨道（三件套）

```python
class SigmaBondPP(VGroup):
    def __init__(self, *, center=None, direction=None, middle_length=None, middle_width=None,
                 lobe_length=None, lobe_width=None, color=None, opacity=1.0,
                 lobe_colors=None, lobe_opacities=None, stroke_width=2, attributes=None,
                 text1=None, text2=None, text_buff=0.15, **kwargs)
```

- **用途**：两个 p 轨道头碰头成键的 σ 轨道 —— **3 个部件**：中部椭圆（位于两标签之间）+ 左右两个外侧卵形线
  （分别位于两标签外侧，尖端朝内、圆端朝外）。所有图形互不重叠且不覆盖标签。
- **可寻址部件**：`middle`、`left_lobe`、`right_lobe`、`lobes`（长度 3，可三段分别配色）。
- **缺省尺寸（有标签时）**：中部短轴在 0.8 倍基础上再缩 0.8 倍（`middle_width`），
  中部长度基于**缩短前**的短轴计算（避免短轴调整牵连长轴）；两侧瓣长/宽各取
  `0.6*max(0.4, 1.5*max_axis_half)` / `0.6*max(0.3, 1.1*max_normal_half)`；
  尖端位置由两个标签的四角在键方向上的投影外沿决定（±0.02 余量）。

### 7.10 `SigmaBondSP` — s-p σ 成键轨道（大小瓣）

```python
class SigmaBondSP(VGroup):
    def __init__(self, *, center=None, direction=None, separation=None, length=None, width=None,
                 small_ratio: float = electron_cloud_small_ratio*0.7, color=None, opacity=1.0,
                 lobe_colors=None, lobe_opacities=None, stroke_width=2, attributes=None,
                 text1=None, text2=None, text_buff=0.15, **kwargs)
```

- **用途**：s 轨道与 p 轨道成键的 σ 轨道 —— **一大一小两瓣**，大瓣把该侧标签包在内部，
  小瓣位于另一侧标签外侧。缺省 `small_ratio = 0.5*0.7 = 0.35`（比杂化轨道的 0.5 更小）。
- **整体缩放**：有标签时的默认几何以**右侧原子中心为位似中心**把整体缩小为 3/4
  （`scale_factor=0.75`），并同步修正各瓣的 `center_point` / `tip_point` / `round_end_point` /
  `length` / `lobe_width` 以及自身的 `separation` / `length` / `lobe_width`，
  保证元数据与显示一致。无标签时 `scale_factor=1.0`。
- **可寻址部件**：`large_lobe`、`small_lobe`、`lobes`；属性含 `scale_factor`、`scale_center`。
- **校验**：`small_ratio≤0` 抛 `ValueError`。

### 7.11 `PiBondPP` — p-p π 成键轨道

```python
class PiBondPP(VGroup):
    def __init__(self, *, center=None, direction=None, length=None, width=None, offset=None,
                 color=None, opacity=1.0, lobe_colors=None, lobe_opacities=None,
                 stroke_width=2, attributes=None, text1=None, text2=None, text_buff=0.15, **kwargs)
```

- **用途**：两个 p 轨道肩并肩成键的 π 轨道 —— 键上下各一个**扁平填充椭圆**，不覆盖原子标签。
- **几何（有标签时）**：`length = 1.2*max(electron_cloud_length, 两标签中心距+0.1)`；
  `width = 1.2*max(0.25, 0.5*max_normal_half)`；`offset`（法向偏移）缺省
  `max(0.35, 标签法向半径 + width/2 + 0.05)` ⇒ 自动让开标签。
- **可寻址部件**：`upper_ellipse`、`lower_ellipse`、`lobes`。

### 7.12 `PiAntiBondPP` — p-p π 反键轨道

```python
class PiAntiBondPP(VGroup):
    def __init__(self, *, center=None, direction=None, separation=None, lobe_length=None,
                 lobe_width=None, tilt_angle: float = np.pi*75/180, color=None, opacity=1.0,
                 lobe_colors=None, lobe_opacities=None, stroke_width=2, attributes=None,
                 text1=None, text2=None, text_buff=0.15, **kwargs)
```

- **用途**：π 反键轨道 π* —— **4 个倾斜的卵形线**：左右两标签外侧各有一对上下倾斜的瓣，
  尖端均指向两个标签、圆端朝外。
- **`tilt_angle`**：倾斜角，默认 `75°`；四瓣方向固定为 `[π−θ, π+θ, θ, −θ]`。
- **几何（有标签时）**：通过 `anchor_on_ray` 沿各瓣方向把锚点推到标签四角投影之外（+0.02 余量），
  再沿该方向外移 `tip_offset = max(2*0.05, 0.25*lobe_width)`；
  `lobe_length = 1.2*max(0.7, 1.5*max_axis_half)`；`lobe_width = 1.2*max(0.35, 1.0*max_normal_half)`。
- **可寻址部件与锚点属性**：`lobes`（长度 4，可四瓣配色）、`left_anchor`、`right_anchor`、
  `upper_left_anchor`、`lower_left_anchor`、`upper_right_anchor`、`lower_right_anchor`、`separation`、`tilt_angle`。

### 7.13 `ElectronCloudType` — 电子云类型枚举

```python
class ElectronCloudType(Enum):
    S_ORBITAL = SOrbital                     P_ORBITAL = POrbital
    HYBRID_ORBITAL = HybridOrbital           SP_ORBITAL = SPOrbital
    SP2_ORBITAL = SP2Orbital                 SP3_ORBITAL = SP3Orbital
    SIGMA_BOND_SS = SigmaBondSS              SIGMA_ANTIBOND_SS = SigmaAntiBondSS
    SIGMA_BOND_PP = SigmaBondPP              SIGMA_BOND_SP = SigmaBondSP
    PI_BOND_PP = PiBondPP                    PI_ANTIBOND_PP = PiAntiBondPP
```

- **用途**：12 个取值，值即图形类。内部分为两组：
  - **原子轨道/杂化轨道**（`S_ORBITAL`、`P_ORBITAL`、`HYBRID_ORBITAL`、`SP_*`）：需要**一个**文本标签；
  - **分子轨道**（`SIGMA_*`、`PI_*`，共 6 个）：需要**两个**文本标签；
    其中 `SIGMA_ANTIBOND_SS` 与 `PI_ANTIBOND_PP` 属**反键轨道**，默认隐藏边界。
- **⭐ 分子轨道组额外受 [约定二](#约定二分子轨道成键反键必须传入两个真实存在的文本标签) 约束**：
  这 6 个取值传入的标签**必须真实存在**，不能用 `text=None` 的骨架原子（其 `Mobject` 为 `None`），
  否则抛 `ValueError`。原子轨道/杂化轨道组无此限制。

### 7.14 `ElectronCloud` — 电子云包装器

```python
class ElectronCloud(VGroup):
    def __init__(self, *, cloud_type: ElectronCloudType, center=None, direction=None,
                 attributes=DEFAULT_ATTRIBUTES, texts=None, text=None, text1=None, text2=None,
                 text_buff: float | None = None, show_border: bool | None = None, **kwargs)
```

- **用途**：电子云图形的统一入口，与 `Bond` / `Charge` 的包装方式一致：枚举保存图形类，
  包装器负责记录 `center` / `direction` 元数据并把生成的图形加入自身。
- **标签传参（推荐 `texts`）**：统一用 `texts` —— 原子轨道/杂化轨道传**一个**，
  成键/反键轨道传**两个**；数量不对会抛 `ValueError`（提示该传 1 个还是 2 个）。
  `text` / `text1` / `text2` 仍保留用于**向后兼容**。
- **`show_border`**：`None`（默认）时**原子轨道与成键轨道显示边界、反键轨道隐藏边界**；
  显式传 `True` / `False` 可覆盖。隐藏的实现是把 `cloud.lobes` 中每瓣 `set_stroke(width=0)`。
- **`color` 优先级**：`kwargs` 中的 `color` > `attributes.color` > `WHITE`（由 `_resolve_color` 决定）。
- **暴露属性**：`cloud_type`、`center_point`、`direction`、`texts`、`text`、`text1`、`text2`、
  `text_buff`、`show_border`、`cloud`（内部真实图形，可访问 `lobes` 等）。
- **⭐⭐ 强制约定：分子轨道必须传入两个"真实存在"的文本标签（实用中最容易踩的坑）**：
  `texts` **绝不能包含 `None`**。`sf.atomic_clusters[name][Mobject]` 对 `text=None` 的骨架原子
  返回 `None`，把它当标签传给 6 种分子轨道（`SIGMA_BOND_SS`、`SIGMA_ANTIBOND_SS`、`SIGMA_BOND_PP`、
  `SIGMA_BOND_SP`、`PI_BOND_PP`、`PI_ANTIBOND_PP`）会抛
  `ValueError("成键轨道与反键轨道必须同时提供 text1 和 text2 两个文本标签。")`。
  也就是说 `ElectronCloud(cloud_type=ElectronCloudType.PI_BOND_PP, texts=[None, some_text])` **不可用**。
  完整说明、正确/错误写法与两条合规替代途径见文首
  [约定二](#约定二分子轨道成键反键必须传入两个真实存在的文本标签)。

  ```python
  # ❌ 错误：C1 是 text=None 的骨架原子 → 取出的 Mobject 为 None
  ElectronCloud(cloud_type=ElectronCloudType.PI_BOND_PP,
                texts=[sf.atomic_clusters["C1"][Mobject], sf.atomic_clusters["O1"][Mobject]])

  # ✅ 正确：两个参与成键的原子都要有真实文本标签
  ElectronCloud(cloud_type=ElectronCloudType.PI_BOND_PP,
                texts=[sf.atomic_clusters["C1_text"][Mobject], sf.atomic_clusters["O1"][Mobject]])
  ```

  **原因（刻意设计，非缺陷）**：全部 6 种分子轨道的尺寸、中心、方向，以及"让开标签"的偏置，
  都由两个文本标签的**包围盒**推导（内部 `_two_text_frame` 取两标签四角在键方向与法向上的投影，
  据此求出中缝、外侧锚点与缩放比例）。没有标签就无解，所以这里必须强校验。
  **合规出路**：① 给该原子补一个占位文本（如 `MathTex(r"\ ")`）使其成为合法标签来源；
  ② 不走包装器，直接用 `center` / `direction` / `length` / `width` 手动构造 7.6–7.12 的图形类
  （这些类在 `text1=text2=None` 时都有 `center` 回退路径）。
- **对照**：原子轨道/杂化轨道（`S_ORBITAL`、`P_ORBITAL`、`HYBRID_ORBITAL`、`SP_*`）**没有**这条限制
  —— 它们允许 `texts=None` 或 `None` 元素，靠 `center` / `radius` / `length` 参数定位。

---

## 8. `animations.py`：动画

源码见 [animations.py](OrganicReactionTools/animations.py)。

### 8.1 `ElectronMigrationStep` — 电子迁移步骤描述

```python
class ElectronMigrationStep:
    def __init__(self, *, replace=None, create=None, fadeout=None, lag_ratio: float = 0.3)
```

- **用途**：**纯数据**描述"一步电子迁移要做哪些变换"，本身不是动画。
- **三个列表字段**：
  - `replace: list[tuple[Mobject, Mobject]]` —— 每项 `(source, target)`，按顺序播放 `ReplacementTransform`。
    多对一：把多个 source 用 `VGroup` 包起来；一对多：把多个 target 用 `VGroup` 包起来，或对 target 用 `Mobject.copy()`。
  - `create: list[Mobject]` —— 本步要 `FadeIn` 的新对象；
  - `fadeout: list[Mobject]` —— 本步要 `FadeOut` 的对象。
- **`lag_ratio`**：步内各子动画之间的延迟比率（0~1），语义同 `AnimationGroup.lag_ratio`。
- **典型写法**（见 [test.py](test.py#L53-L58)）：把"旧电荷 + 旧单键"合成一个 `VGroup` 一起变换成新双键。

### 8.2 `OpacityEffect` — 仅改透明度的通用动画

```python
class OpacityEffect(Animation):
    def __init__(self, *, mobject: Mobject, initial_opacity: float, final_opacity: float,
                 run_time: float, func: Callable[[float], float] = linear, **kwargs)
```

- **用途**：从 `initial_opacity` 平滑过渡到 `final_opacity`，且可自定义速率曲线 `func`
  （默认 `linear`；传 `smooth` 等即可缓入缓出）。相比 manim 的 `FadeIn/FadeOut`，它**不改变位置**，
  适合做"电子云淡淡浮现/消退"这类效果。
- **`BezierArrow` 特例**：若目标是 `BezierArrow`，会分别设置 `tip` 的填充透明度与 `bezier` 的描边透明度
  （因为弯箭头由曲线+箭头两个部件组成，直接 `set_opacity` 效果不理想）；其它 mobject 走 `set_opacity`。
- **插值**：`opacity = func(α)*(final-initial) + initial`。

### 8.3 `RotateAtoms` — 原子旋转 + 键跟随伸缩

```python
class RotateAtoms(Animation):
    def __init__(self, *, structural_formula: 'StructuralFormula', atom_names: str | list[str],
                 center: str | Vector3D, angle: float, about_edge: bool = True,
                 run_time: float = 1.0, rate_func: Callable = smooth, **kwargs)
```

- **用途**：绕指定中心旋转一个或多个原子，**相连化学键实时伸缩**跟随，电荷随原子平移。
  比"整体 rotate mobject"更正确 —— 键的几何是按原子锚点重算的，不会被拉变形。
- **`center`**：可以是原子名字符串或坐标；为名字时 `about_edge=True`（默认）以该原子的
  **键端点坐标 `pos`** 为旋转中心，`False` 则以**原子文本的视觉中心**为中心
  （文本为 `None` 时回退到 `pos`）。
- **准备阶段（构造时快照）**：记录各待旋原子的初始 `pos`；建立"键 → 所连两原子名"映射
  （只覆盖与待旋原子相连的键）；记录每个原子电荷中心相对原子 `pos` 的偏移量 ⇒ 旋转时电荷保持相对位置。
- **每帧**：按 `angle*rate_func(α)` 旋转原子 → 更新 `atomic_clusters[name]["pos"]` 与 mobject 位置
  → 调 `_rebuild_bond` **原地**重置各键几何（不删不建，避免残留）→ 平移电荷。
- **`_rebuild_bond` 覆盖全部键型**：单键/虚键用 `put_start_and_end_on`；外向楔形用 `set_points_as_corners`；
  内向楔形逐条重建；三键与双键按 `side` 分支重算 —— 与构造期的几何公式一一对应。
- **矩阵式需求**：从 `StructuralFormula.rotate_atoms(...)` 获取实例更省事（会先做参数校验）。

### 8.4 `BondTypeTransform` — 键型变换 + 旋转（单动画）

```python
class BondTypeTransform(Transform):
    def __init__(self, *, bond: Bond, target_type: BondType, angle: float,
                 about_point: Vector3D | None = None, sf: 'StructuralFormula' | None = None, **kwargs)
```

- **用途**：用 `Transform` 的底层点插值，**同时**完成两件事：
  ① 键类型形状变换（如 `NormalBond → DoubleBond`）；② 键绕指定点旋转。两者同时开始、同时结束。
- **`about_point`**：旋转中心，默认键的起点（即绕起点原子转动另一端）。
- **`sf`（可选）**：传入所属结构式后，动画**每帧**同步旋转两端原子的 mobject 与它们的电荷
  （电荷保持相对原子 `pos` 的初始偏移）。
- **构造时**：以相同起止点建一条目标类型的键（双键的 `side` / `*_side_edge` 缺省时自动取 0 / `False`），
  再把目标键 `rotate(angle, about_point)` ⇒ 目标点位直接体现终态；属性取自 `sf.attributes`，无 `sf` 时用 `DEFAULT_ATTRIBUTES`。
- **`finish()`（动画结束时）**：更新 `bond.bond_type`、用旋转公式重算 `bond.start` / `bond.end` / `bond.direction`，
  并在有 `sf` 时把两端原子在 `atomic_clusters` 中的 `"pos"` 数据同步为新坐标（mobject 位置已在 `interpolate` 中处理）。
- **`interpolate_mobject(α)`**：先 `super()` 做键几何插值，再旋转原子 mobject。

### 8.5 `ElectronMigration` — 电子迁移动画组

```python
class ElectronMigration(AnimationGroup):
    def __init__(self, *, sf: 'StructuralFormula', steps: list[ElectronMigrationStep],
                 lag_ratio: float = 0.3, run_time: float = 1.0, sync: bool = True, **kwargs)
```

- **用途**：把若干 `ElectronMigrationStep` 组装成一个 `AnimationGroup`，是"画反应机理"的主力动画。
  每步内部由 `replace → ReplacementTransform`、`create → FadeIn`、`fadeout → FadeOut`
  组成一个 `AnimationGroup(lag_ratio=step.lag_ratio)`；步与步之间由外层 `lag_ratio` 控制
  （0 = 全部同时开始，1 = 依次执行）。
- **`run_time`**：每个**子动画**的运行时间。
- **构造时收集**四份清单（`_all_sources` / `_all_targets` / `_all_creates` / `_all_fadeouts`）供首尾钩子使用。
- **`begin()`**：把 source 与被淡出的对象从 `sf` 中移除（**它们仍留在 Scene 里**，动画期间可见）。
  若某对象是 `VGroup` 且不是 `Bond`/`Charge`（即用户为"多对一"自组的组），则逐个移除其子对象。
- **`finish()`**：把 target 与新建对象加入 `sf`（同样对自组 `VGroup` 展开子对象），
  然后在 `sync=True` 时调用 `sf.sync_migration(steps)` 自动同步元数据，把无法同步的对象收进 **`self.unsynced`**。
- **`sync`**：默认 `True`；设为 `False` 可完全手工管理登记。

---

## 9. `structures.py`：结构式

源码见 [structures.py](OrganicReactionTools/structures.py)。这是全库的**总控类**，
把原子、键、电荷、动画、装饰的入口都收拢在一处。

### 9.1 `StructuralFormula` — 结构式（`VGroup` 子类）

```python
class StructuralFormula(VGroup):
    def __init__(self, *, base_ratio_outbond=0.2, base_ratio_inbond=0.2, num_inbond=5,
                 dashed_length_dashedbond=0.1, dashed_ratio_dashedbond=0.5,
                 ratio_transition_state_dashedbond=bond_length*ratio_transition_state,
                 length_global=bond_length, color=WHITE, edge_global=edge, font_size=txt_size,
                 font_size_partial=partial_charge_font_size, radius_negative=0.05,
                 ratio_negative=0.6, stroke_width_negative=1.2, edge_charge=default_charge_edge,
                 radius_positive=0.05, ratio_positive=0.6, stroke_width_positive=1.2,
                 radius_single=0.01, distance_pair=0.1, distance_double=0.12,
                 edge_ratio_double=0.08, distance_triple=0.12,
                 name=None, pos=None, text=None, text_offset=[0,0,0])
```

**构造参数** = `AttributeHolder` 的全部 23 个样式参数（可以直接在这里整体改样式）
+ 可选的首个原子：`name`（原子名）、`pos`（坐标）、`text`（TeX 文本，`None` 表示"无文本的碳节点"）、
`text_offset`（只影响显示、不影响键端点）。

**内部数据结构（用户经常直接用）**：

| 成员 | 类型 | 含义 |
|---|---|---|
| `attributes` | `AttributeHolder` | 本结构式的样式属性 |
| `atomic_clusters` | `dict[str, dict]` | 原子表，值是 `{Mobject: 文本或None, "pos": 坐标, "adj": [邻接名], Bond: [键]}` |
| `charges` | `dict[str, Charge]` | 原子名 → 电荷包装器 |
| `bond_lookup` | property → `BondLookup` | 键查询器（见 4.9） |

> 访问原子与键的惯用法（见 [test.py](test.py#L42-L44)）：
> `sf.atomic_clusters["O1"][Mobject]` 取文本、`sf.atomic_clusters["O1"][Bond][0]` 取第一条键、
> `sf.charges["O1"]` 取电荷。

**方法清单（1 个 property + 17 个方法，共 18 项）**：

#### （1）建结构

- **`add_atom(*, name, direction=None, text=None, bond_type=None, adjacency=None, pos=None, side=None, start_side_edge=None, end_side_edge=None, text_offset=[0,0,0])`**
  向结构式添加一个原子，并按 `bond_type` 与 `adjacency` 自动连一条键。
  **空结构式**：只接受 `pos`（必须给）；**非空结构式**：`adjacency`、`direction`、`bond_type` **三者都必填**。
  新原子坐标 = `length_global*[cos(direction), sin(direction), 0] + 邻接原子 pos`。
  键的 `start_edge` / `end_edge` 自动按两端"是否有文本"决定。重复的 `name` 抛 `ValueError`。
- **`register_atom(*, name, mobject, adjacency=None, bond_type=None, side=None, start_side_edge=None, end_side_edge=None)`**
  把**外部已创建**的 mobject 注册为原子（如把独立画好的亲电试剂 E⁺ 并入结构式，以便参与电子迁移）。
  坐标取 `AtomicCluster.atom_pos`（若传入的是 `AtomicCluster`）或 `mobject.get_center()`；
  给 `adjacency` 时建一条键（`bond_type` 缺省 `NORMAL_BOND`），不给则为**无键独立原子**。
  `add_atom` 是"内部创建"，本方法是"外部接纳"。
- **`add_bond(*, start, end, bond_type, side=None, start_side_edge=None, end_side_edge=None)`**
  在两个**已存在**原子之间新建键并登记到双方的 `[Bond]` 与 `adj`。
  校验：两端原子必须存在、`start != end`、两端之间**尚无键**，违者抛 `ValueError`。
  双键分支会额外透传 `side` / `*_side_edge`。
- **`build_bond(...) -> Bond`** — 与 `add_bond` **参数完全一致**，但**只创建不添加**：
  返回键对象而不挂进结构式。用途是先在场景外准备好"目标键"，再交给 `ElectronMigrationStep`
  做 `ReplacementTransform` 的 target。
- **`add_charge(*, text, pos, charge_type, delta_count=1, sign="+", anchor_mode="border")`**
  给指定原子挂电荷。`text` 是**原子名**（不是电荷文本），`pos` 是方向向量（如 `UR`、`DOWN`）。
  校验：原子必须存在、该原子**不能已有电荷**。自动创建 `Charge` 并放进 `self.charges[name]` 与场景。
  - **⭐⭐ `charge_type` 必须与目标原子"是否有文本标签"匹配（选错即抛 `TypeError`）**：
    **有文本标签的原子用非坐标版**（`ChargeType.NEGATIVE` 等），
    **无文本标签的原子（`text=None`）用坐标版**（`ChargeType.NEGATIVE_COORDINATE` 等）。
    完整对照表与示例见文首 [约定一](#约定一电荷类型必须与原子是否有文本标签匹配)。
- **`build_charge(...) -> Charge`** — 同样**只创建不添加**，返回电荷包装器（供动画 target 用）。
  **`charge_type` 遵守与 `add_charge` 完全相同的配对规则**（见上）。

#### （2）改结构 / 删结构

- **`delete_atom(*, names: str | list[str], anim: type[Animation] = FadeOut) -> Animation`**
  删除一个或多个原子，**返回一个可直接 `self.play(...)` 的动画**（不自己播放）。
  连带删除：该原子的文本、所有挂在它上面的键（并从邻接原子的 `[Bond]` / `adj` 中**双向**清理）、
  该原子的电荷（从 `charges` 弹出）。原子不存在抛 `ValueError`。
- **`delete_bond(*, start, end, anim=FadeOut) -> Animation`**
  删除两原子之间的键，双向清理 `[Bond]` 与 `adj`，返回淡出动画。
  内部用 `assert` 做一致性自检（键必须在两端列表中、邻接关系必须对称）；不存在键抛 `ValueError`。
- **`delete_charge(*, text, anim=FadeOut) -> Animation`**
  从场景与 `charges` 中移除某原子的电荷，返回动画。原子不存在或该原子无电荷均抛 `ValueError`。
- **`register_bond(*, start, end, bond: Bond) -> None`** — 把**外部创建**的键登记进两端原子的
  `[Bond]` 与 `adj`（**幂等**：已存在则不重复添加）。配合 `build_bond` 或 `ElectronMigration.sync=False` 手工同步使用。
- **`register_charge(*, name, charge: Charge) -> None`** — 把外部创建的电荷登记进 `charges[name]`。
- **`unregister_bond(bond: Bond) -> None`** — 按**身份**从所有原子的 `[Bond]` 移除该键，
  并在恰好找到两个端点时同步清理 `adj`（幂等）。
- **`unregister_charge(charge: Charge) -> str | None`** — 从 `charges` 中按身份移除，**返回其所属原子名**（无则 `None`）。
- **`sync_migration(steps: list[ElectronMigrationStep]) -> list`** — 按步骤列表同步元数据：
  **先注销**（`replace` 的 source 与 `fadeout`）**后登记**（`replace` 的 target 与 `create`）。
  只自动登记**带标签**的对象（`Bond.atom1` / `atom2`、`Charge.atom_name`）；
  标签缺失或原子不存在时**打印警告**并把对象收集进返回列表，供手工登记。
  内部 `_sync_unregister` / `_sync_register` 对 `VGroup` 会**递归展开**子对象，因此 `VGroup(Bond, Charge)` 这种组合也能被正确同步。

#### （3）动画工厂

- **`rotate_atoms(*, atom_names, center, angle, about_edge=True, run_time=1.0, rate_func=smooth, **kwargs) -> Animation`**
  参数校验后返回 `RotateAtoms` 实例（见 8.3）。校验：待旋原子与中心原子必须存在，否则抛 `ValueError`。
  `atom_names` 可传单个字符串或列表。
- **`electron_migration(*, steps, lag_ratio=0.3, run_time=1.0, sync=True, **kwargs) -> ElectronMigration`**
  参数校验后返回 `ElectronMigration` 实例（见 8.5）。这是画机理动画最常用的入口。

#### （4）装饰

- **`polarity_arrow(*, start, end, side, **kwargs) -> BondPolarityArrow`**
  在 `start`–`end` 键旁边生成**键极性箭头**（**装饰对象，不加入结构式**，可直接 `self.play(Create(...))`）。
  自动取两原子的 `pos` 作为键端点、`self.attributes` 作为样式；
  `side=1` 右手侧、`side=-1` 左手侧（`side=0` 在 `BondPolarityArrow` 内抛 `ValueError`）；
  其余参数（`tail_offset`、`offset`、`length`）原样透传。原子不存在抛 `ValueError`。

### 9.2 `Benzene` — 苯环

```python
class Benzene(StructuralFormula):
    def __init__(self, *, center: Vector3D, first_c_angle: float = 90*DEGREES,
                 c_names: list[str] | None = None, **kwargs)
```

- **用途**：一步生成标准苯环 —— 六个**无文本**碳原子组成的规则六边形，单双键交替。
  继承 `StructuralFormula`，因此 `add_atom` / `add_charge` / `electron_migration` 等全部可用。
- **参数**：
  - `center`：环中心坐标（**必填**）；
  - `first_c_angle`：第一个碳 `c_names[0]` 相对环中心的角度（弧度，与 `add_atom` 的 `direction` 同语义），
    默认 90°（C1 在正上方）；
  - `c_names`：六个碳名，默认 `["C1"…"C6"]`，必须是**六个互不相同**的名字（否则 `ValueError`）；
  - `**kwargs`：`StructuralFormula` 的全部样式参数透传（例如 `length_global` 会在内部被用作环半径）。
- **几何**：C1 位于 `center + radius*[cos, sin, 0]`，半径 = `length_global`（缺省 `bond_length`=1）；
  之后**顺时针**依次添加 C2…C6，相邻键方向每次减 60°；
  C1–C2 之间为双键，其余单双键交替（`bond_types = [DOUBLE, NORMAL, DOUBLE, NORMAL, DOUBLE]`），
  最后闭合 C6–C1 单键。所有双键取 **`side=-1` 且两端 `*_side_edge=True`**（即不对称长短线朝统一一侧，形成标准芳香环观感）。
- **禁止参数**：`name` / `pos` / `text` / `text_offset` 会被拒绝（位置由 `center` 与 `first_c_angle` 自动计算），
  传入抛 `ValueError`。
- **取代基**：**不在初始化时添加**，创建后用 `add_atom` / `add_charge` / `add_bond` 等方法挂接（与直接操作 `StructuralFormula` 相同）；
  [test.py](test.py#L505) 的 `TestBenzeneMigration` 演示了用它做亲电进攻生成 Wheland 中间体。

---

## 10. `texts.py`：标题文本

源码见 [texts.py](OrganicReactionTools/texts.py)。

### 10.1 `Title` — 标题

```python
class Title(MathTex):
    def __init__(self, *, text: str, pos: Vector3D = title_coordinate,
                 color=WHITE, size=title_size)
```

- **用途**：顶部大标题。默认坐标 `[0, 3, 0]`、默认字号 60、默认白色，套用 `mytemplate`（可写中文）。
- **典型用法**：`Title(text=r"\text{示例一：丙酮水合物负离子的电子迁移}")`。

### 10.2 `Subtitle` — 副标题

```python
class Subtitle(MathTex):
    def __init__(self, *, text: str, pos: Vector3D = subtitle_coordinate,
                 color=WHITE, size=subtitle_size)
```

- **用途**：次级标题/小标签。默认坐标 `[0, 2.3, 0]`、默认字号 30。
  测试代码中常用 `size=25` 并手动 `move_to` 到画面某侧做分区标签。

### 10.3 `Description` — 描述文本

```python
class Description(MathTex):
    def __init__(self, *, text: str, pos: Vector3D = description_coordinate,
                 color=WHITE, size=txt_size)
```

- **用途**：底部说明文字。默认坐标 `[0, -3, 0]`、默认字号 = `txt_size`（35）。
- **三者关系**：都是 `MathTex` 的极薄子类，唯一差别就是默认坐标与默认字号；
  三个默认值全部来自 `parameters.py`，改全局常量即可整体挪位。

---

## 11. `functions.py`：工具函数

源码见 [functions.py](OrganicReactionTools/functions.py)。

### 11.1 `play_timeline(scene: Scene, timeline: dict[float, Animation])` — 按时间轴播放

- **用途**：把"时间点 → 动画（或动画列表）"的字典一次性播放完，省去手写一长串
  `self.play` / `self.wait`。灵感来自 `github.com/abul4fia/manim-play-timeline`（源码注释已注明）。
- **行为**：对按键排序后的每个 `(time, animation)`：先 `scene.wait(time - 上个时间点)` 补足间隔，
  再对动画列表里每个动画调用 `turn_animation_into_updater(anim)` + `scene.add(anim.mobject)`
  ⇒ **多个动画在同一时间点并发**；同时记录 `run_time + time` 的最大值作为结束时间，
  循环结束后若还有剩余则 `scene.wait(ending - pretime)` 收尾。
- **注意**：函数内部在 `if ending > time` 中引用了循环变量 `time`，依赖"字典非空"这一前提。

### 11.2 `merging_timeline(timeline1, timeline2)` — 合并两条时间轴

- **用途**：把两条时间轴拼成一条；**同一时间点冲突时自动合并为列表**（先转 list 再 `extend`），
  非冲突时间点直接沿用原值。
- **返回**：新的字典（内部先 `timeline1.copy()`，不会修改入参的键集合）。
- **典型用法**：`merging_timeline(brownian_motion(objA, ...), brownian_motion(objB, ...))`。

### 11.3 `brownian_motion(items: Mobject | list, num: int, time: float = 1.0)` — 布朗运动

- **用途**：生成"随机抖动"的时间轴，表现分子/离子的热运动。
- **递归设计**：**传列表**时对每个元素递归调用并逐层 `merging_timeline` 合并 ⇒ 返回值永远是时间轴字典，
  可直接交给 `play_timeline`；两种入参的返回类型因此保持一致。
- **单个对象的实现**：用固定种子随机数 `RNG` 在 `[0, time]` 内生成 `num` 个排序节点（末尾补 `time`），
  每个节点产生一个 `ApplyMethod(items.shift, dx, run_time=节点间隔, rate_func=smooth)`；
  位移 `dx = [U(-0.5,0.5), U(-0.5,0.5), 0]`，累加到 `destination` 上，
  若越界（`|x|>5` 或 `|y|>3`）则按 `x/7*6`、`y/4*3` 折回画面内 ⇒ 抖动被约束在可见区域。
- **`num`**：抖动段数；`time`：总时长。返回值为 `dict[float, list[ApplyMethod]]`。

---

## 12. 使用示例与配套资料

- **`test.py`**（1857 行，21 个 `Scene`）：覆盖电子迁移、`PairCharge` 垂直线性质断言、
  `Benzene` 三种场景、极性箭头 `side`/`offset`/`length` 组合、`BondTypeTransform` 独立与联动、
  12 种电子云类型、`PartialCharge` 定位模式等 —— 是最好的**用法字典**。
- **`SubstitutionReaction1/2/3.py`**：三个完整教学动画（亲核取代反应），演示多步机理编排。
- **渲染产物**：`media/videos/**` 与 `media/images/SubstitutionReaction1/test_ManimCE_v0.20.1.png`。
- **渲染命令**（文件头注释给出）：`manim test.py test -pqh`（p=预览、q=高质量、h=1080p60）。

---

## 13. 附录：本次梳理的运行时校验结果

文首 [约定一](#约定一电荷类型必须与原子是否有文本标签匹配) 与
[约定二](#约定二分子轨道成键反键必须传入两个真实存在的文本标签) 是对代码在
`manim 0.21.0` / Python 3.12.2 下**实际执行**得到的，不是静态推断。
两条约定**属设计意图，不属于缺陷，因此不在本次改动范围内修复**，仅在文档中予以强调。
其余实测**正常**的行为如下（可作为回归基线）：

| 校验项 | 结果 |
|---|---|
| `StructuralFormula(name, pos, text)` + `add_atom(..., direction, text, bond_type, adjacency)` | ✅ 原子表、邻接、键同时建好 |
| `bond_lookup.is_bonded` / `type_between` / `all_bonds` | ✅ 与 `atomic_clusters` 一致 |
| `build_bond` / `build_charge` **不**改动结构式 | ✅ 键数、电荷数不变（可直接当动画 target） |
| `register_bond` → `unregister_bond`（幂等登记 / 按身份注销） | ✅ 键数 2 → 3 → 2，`is_bonded` 同步翻转 |
| `delete_atom` / `delete_bond` / `delete_charge` | ✅ 都返回 `FadeOut` 实例，且内部表同步清理干净 |
| `Benzene(center, first_c_angle)` | ✅ 6 个无文本碳、6 条环键、单双键交替（`DOUBLE, NORMAL, DOUBLE, NORMAL, DOUBLE, NORMAL`） |
| `Locator(degrees=90).get_coord(sf, 'C1')` | ✅ 返回 `[0, 1, 0]`，等于 `length_global` 沿 +y |
| `polarity_arrow(side=±1)` | ✅ 长度 0.5 = `length_global - 2*edge_global`；起点位移与键方向的点积为 0 ⇒ 垂直性成立 |
| `ReactionArrow(above=[两个字符串], below=字符串)` | ✅ 自适应长度、上下居中、`z_index ≥ 2`（文本压在箭头上） |
| `ReactionArrow(start=...)` 无 above/below、`length=0` | ✅ 均按文档抛 `ValueError` |
| `PartialCharge(anchor_mode='border')` | ✅ 电荷文本角点与原子文本角点重合；`delta_count=0` / `sign='x'` / `anchor_mode='q'` 均抛 `ValueError` |
| `ElectronCloud(texts=...)` 数量校验 | ✅ 给分子轨道 1 个、给原子轨道 3 个标签，均抛 `ValueError` 且提示明确 |
| 反键/成键轨道的 `show_border` 默认值 | ✅ 仅 `SIGMA_ANTIBOND_SS`（2 瓣）与 `PI_ANTIBOND_PP`（4 瓣）默认隐藏边界（`stroke_width=0`），其余 10 种保留边界 |
| 12 种 `ElectronCloudType` 全部可构造（原子轨道给 1 个标签、分子轨道给 2 个标签） | ✅ 12/12 成功，`lobes` 数依次为 1, 2, 2, 2, 2, 2, 1, 2, 3, 2, 2, 4 |
| `DashedBond` 长度语义 | ✅ 独立构造标称 1.2；经 `Bond` 包装器画到真实端点距离 1.0 |
| `merging_timeline` 同时间点合并 | ✅ 冲突时间点自动并为列表（`{0: [FadeIn, FadeOut], 1: [FadeIn]}`） |
| `brownian_motion` 单对象与列表两种入参 | ✅ 返回类型统一为时间轴字典，可直接交 `play_timeline` |
| **约定一** 配对规则（有文本 → 非坐标版，无文本 → 坐标版） | ✅ 正确配对全部成功；两种错配均按预期抛 `TypeError` |
| **约定一** `PARTIAL` 双向可用、`PARTIAL_COORDINATE` 仅限无文本原子 | ✅ 实测确认（`PARTIAL_COORDINATE` + 有文本原子会抛 `TypeError`） |
| **约定二** 分子轨道必须两个真实标签 | ✅ 含 `None` 抛 `ValueError`；两个真实标签时 6 种分子轨道 **6/6** 全部成功 |
| **约定二** 两条合规替代途径 | ✅ 占位文本（`MathTex(r"\ ")`）可用；6 个图形类在 `text1=text2=None` 下均可构造（`lobes` 依次 1/2/3/2/2/4） |
| **对照** 原子轨道/杂化轨道允许无标签构造 | ✅ `S_ORBITAL` / `P_ORBITAL` / `HYBRID_ORBITAL` 接受 `center=...` 或 `texts=[None]` |

**两条约定边界的复现脚本**（如需回归，两条都应报错 —— 这是预期行为，不是待修复项）：

```python
from OrganicReactionTools import *
from manim import UR
# 约定一 · 反例 A：坐标版用在"有文本"的原子上（应报错）
s = StructuralFormula(name='A', pos=[0,0,0], text='A')
s.add_charge(text='A', pos=UR, charge_type=ChargeType.NEGATIVE_COORDINATE)
# TypeError: NegativeChargeByCoordinate.__init__() got an unexpected keyword argument 'text'
# ✅ 改成 s.add_charge(text='A', pos=UR, charge_type=ChargeType.NEGATIVE) 即正常

# 约定一 · 反例 B：非坐标版用在"无文本"的原子上（应报错，PARTIAL 除外）
sf = StructuralFormula(name='C1', pos=[0,0,0], text=None)
sf.add_atom(name='C2', direction=0, text=None, bond_type=BondType.NORMAL_BOND, adjacency='C1')
sf.add_charge(text='C2', pos=UR, charge_type=ChargeType.NEGATIVE)
# TypeError: NegativeCharge.__init__() got an unexpected keyword argument 'position'
# ✅ 改成 charge_type=ChargeType.NEGATIVE_COORDINATE 即正常

# 约定二：分子轨道以无文本原子（Mobject 为 None）为标签（应报错）
sf.add_atom(name='O1', direction=90*DEGREES, text='O', bond_type=BondType.NORMAL_BOND, adjacency='C1')
ElectronCloud(cloud_type=ElectronCloudType.PI_BOND_PP,
              texts=[sf.atomic_clusters['C1'][Mobject], sf.atomic_clusters['O1'][Mobject]])
# ValueError: 成键轨道与反键轨道必须同时提供 text1 和 text2 两个文本标签。
# ✅ 给 C1 补一个真实文本标签（或改用 center/direction/length/width 手动构造图形类）即正常
```
