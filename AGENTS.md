# 工作区记忆（AGENTS.md）

本文件由 AI 助手按需维护，记录用户对该工作区助手的长期要求；每个工作区一份。

## 通用要求

- 用中文回复、用中文写注释。
- 先读后改：动手前先读相关代码段（尤其文件末尾、以及被引用的定义）；文件被用户改动过（工具提示 stale/changed）就先重读再改，不要凭记忆改。
- 一次只做用户明确要求的事，不顺手重构无关代码。
- 每次改完必须做静态校验并如实汇报：语法 `python -c "import ast,io;ast.parse(io.open('SubstitutionReaction3.py',encoding='utf-8').read())"` + 行尾字节检查。
- 渲染职责按内容划分：
  - **API（`OrganicReactionTools/`）有修改时，必须由我用真实渲染的测试代码验证 API 功能是否符合预期**，不能只做静态检查、也不能只跑断言。做法：改 `test.py` 里对应的测试场景（含断言 + 可视化），跑 `manim -qh --disable_caching test.py <场景>`，并抽帧核对关键帧，确认"效果确实出现在画面里且位置正确"。抽帧用 PyAV（`av`，详见「工具与环境」）。
  - **动画代码（`SubstitutionReaction*.py` 等用户作品）的渲染由用户自己执行**，我不代替用户出片。判定标准：**项目根目录下的 `*.py`，只要不是 `test.py`，一律认定为非测试代码（用户作品）**，我不渲染、也不出片。
  - 渲染失败时先定位原因（环境 vs 代码）再决定怎么办，并如实说明未验证项及原因，不因报错就跳过验证。
- 封面等静态配图：纯黑底、白色 LaTeX（ctex）文本与白色线框为主体；允许非居中排版（标题左对齐 + 图示居右下）与少量彩色点缀（整套封面只用一两个彩色色相，不限定用在哪些对象上）；**视频画面本身仍保持纯白、居中**。

## 代码与文件约定

- 所有 Python 文件保持纯 CRLF（仓库 `.gitattributes` 已声明 `*.py text eol=crlf`）；改完用字节级检查确认「CRLF 数 == 总行数、裸 LF == 0」。
- 不要在工作区留下不必要的文件：临时探针脚本用完即删；审查结论写在对话里，不落盘生成报告；确需新建文件先问用户。
- 命名与文件既有风格一致：原子名用「元素 + 序号」（`C1`/`O1`/`X1`…）；变量用 `<原子>_<角色>`（`OH_mob`、`X4_negative`、`C2_X3_bond`）；步骤名用数字后缀（`step_oh_attack2`、`step_x_attack3`）。不要字母后缀、不要 camelCase。
- 讲解文字统一用 `Description(text=...)`；化学式写 `\mathrm{...}`，不要在 `\text{}` 里直接写 Unicode 希腊字母或 `^`。
- 多处讲解文字默认都落在同一坐标 `[0,-3,0]`，必须用 `ReplacementTransform` 顺次替换，不能同时 `Write`（会重叠）。
- `StructuralFormula` 的 submobject 顺序决定 `Transform` 的逐项配对：做结构展开/缩写前，先重整子对象顺序使两侧对应。
- `text_offset`（`AtomicCluster` / `add_atom` / `register_atom`）是**固定位移**：它只随锚点平移，不随键或分子旋转（与 `RotateAtoms` 中电荷偏移的处理一致）。要让标签跟着分子转，须在动画结束后自行重设偏移。
- **所有测试代码必须写在仓库根目录的 `test.py`**（不被 git 跟踪），按场景类分块；不新建单独的测试文件，也不把测试混进根目录的其它 `*.py` —— 根目录下除 `test.py` 外的 `*.py` 一律是非测试代码。
- 根目录 `VideoCover.py` 专门生成 B 站封面：**一个封面一个独立场景类，场景名即封面名（不要都叫 `test`）**；模块内直接把分辨率固定为 1920×1080；封面图用 `manim VideoCover.py <场景名> -s` 保存末帧，产物在 `media/images/VideoCover/<场景名>_*.png`。

### 代码风格（实测约定）

以下风格由现有代码实测得出，新代码一律照此写。

**作品文件**（根目录除 `test.py` 外的 `*.py`）：

- 缩进 4 空格、禁用 Tab；续行用圆括号分组并把内容对齐到括号后一列；算术续行把运算符写在行首；不使用反斜杠续行。
- `=` 两侧不加空格（赋值与关键字参数一律 `name=value`）；逗号后不加空格（`self.play(FadeIn(a),FadeIn(b))`）。
- 运算符紧贴书写：`a+b`、`i*length_global`、`x==y`，不写 `a + b`（历史遗留仅 3 处带空格，新代码不要跟）。
- 字符串一律双引号，不用单引号、不用 f-string。
- import 只写一行 `from OrganicReactionTools import *`（manim 命名空间由包透出），不额外 import。
- 注释 `#` 紧接中文不带空格（`#水分子和氢氧根离子消失`）；节与节之间用横幅注释 `#-----------------------Haloform reaction-----------------------`。
- 空行：同一逻辑块内不空行，块与块之间 1 行，节与节之间最多 2 行。
- 行长不强制换行（实测 p95=102、最长 226）；过长表达式用括号分组，不要为压行宽写难读的代码。
- 命名：原子名「元素 + 序号」；变量 `<原子>_<角色>`；步骤 `step_<动作>` + 数字后缀；讲解文本 `text<序号>` 从 1 连续编号；变量不用 camelCase（历史遗留的原子名 `HplusR` 不回改）。
- 重复的动画流程**显式展开**，不抽成函数（不要 `perform_halogenation` 那种封装）。
- 节奏默认值：主要步骤 `run_time=1.5` 后跟 `self.wait(1.5)`；短过渡 0.8 / 0.5；倒放用 0.3（5 倍速）。
- 结构式操作固定套路：`bond_lookup.between` 取键、`atomic_clusters[name][Mobject]` 取文本；替换动画一律 `ReplacementTransform`；**对原子表的非动画修改放到 `self.play` 之后**（原因见「备注」的闪现坑）。

**测试文件**（仅 `test.py`，风格与作品文件不同，不要互相混用）：

- 用常规写法：注释写 `# 文字`（带空格），逗号后带空格。
- 一个场景一个 `class`；断言与可视化并重（现有 226 处 `assert`、41 处 `np.allclose` 坐标校验）。
- 测试代码只写在 `test.py`，不新建其它测试文件。

**包**（`OrganicReactionTools/`）：

- 与作品文件同样的紧凑写法（`=` / 逗号不加空格、4 空格缩进、双引号）。
- 函数写中文 docstring（用途、几何规格、参数含义与校验）；参数带类型注解，常用 `*` 限定关键字参数；校验失败一律 `raise ValueError("中文提示")`。

## 工具与环境

- 包 `OrganicReactionTools` 的权威说明是 `API_REFERENCE.md`（含文首「务必先读」的两条约定）；写代码前先查该文档与包源码，不靠猜。
  - 约定一：电荷类型必须与「原子有无文本标签」匹配 —— 无文本标签的原子只能用 `*_COORDINATE` 版。
  - 约定二：`ElectronCloud` 的 6 种分子轨道必须传两个真实存在的文本标签。
- Windows + PowerShell（`pwsh -Command`）：不支持 heredoc，多行脚本用 `@'...'@ | python -` 管道；`Get-Content` 控制台可能显示乱码，核对中文请用 read 工具。
- manim 0.21.0 / Python 3.12（解释器 `D:\pythion312\python.exe`）；manim 用 PyAV（`av 17.1.0`，自带完整 libav*）合成视频，**不需要外部 ffmpeg**。
- 抽帧核对用 PyAV：`av.open(...)` → `container.seek(int(t / stream.time_base))` → `frame.to_image()`（Pillow 已装），无外部依赖、也不受 PATH 影响。
- 备选：B 站客户端自带的 `%APPDATA%\bilibili\ffmpeg\ffmpeg.exe`（正版 FFmpeg 3.0.1，2016 年构建，带上海哔哩哔哩数字签名、未改动）可用 `-ss <t> -i <mp4> -frames:v 1` 抽帧；但该二进制随客户端升级/卸载会变动或消失，且版本过旧，故只作后备，优先用 PyAV。
- 渲染偶发 MiKTeX/dvisvgm 日志权限失败，可用管理员权限 + 外部 `--media_dir` 绕过。

## 当前目标

- 合集「有机化学机理动画」不再限定取代反应主题，后续视频的主题由用户另行指定。
- 封面生成见 `VideoCover.py`（当前合集总封面场景名 `CollectionCover`）。
- `SubstitutionReaction3.py` **已完成**：整部「一些常见的取代反应机理」教学动画（加成-消除机理 → 羰基活泼 α-H 亲电取代 → 卤仿反应）全部做完，并经用户渲染确认，**无需继续开发**。

## 备注

- 两个反复踩到的「场景成员关系」坑：
  1. `electron_migration`（以及某些 `self.add(...)`）会把 `StructuralFormula` 从 `Scene.mobjects` 中**拆散**；此后往结构式里新增的对象必须显式 `self.add(...)` 才会渲染。注意 `FadeIn`/`Create`/`Write` 是 introducer，`Scene.add_mobjects_from_animations` 会跳过它们，只加 `FadeIn` 救不回来。
  2. `rotate_atoms` 的动画 `mobject` 就是结构式本身且不是 introducer，会把结构式**重新聚合回场景**；此后 `sf.add(x)` 会立刻渲染 x。所以「替换原子文本」这类改动要把原子表更新（`remove` / `atomic_clusters[...][Mobject]=` / `add`）放到 `self.play` **之后**，否则新标签会在形变前闪现。
- 渲染产物：`media/videos/SubstitutionReaction3/1080p60/test.mp4`（用户渲染后会显示为已修改）。
