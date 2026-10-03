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

## 代码与文件约定

- 所有 Python 文件保持纯 CRLF（仓库 `.gitattributes` 已声明 `*.py text eol=crlf`）；改完用字节级检查确认「CRLF 数 == 总行数、裸 LF == 0」。
- 不要在工作区留下不必要的文件：临时探针脚本用完即删；审查结论写在对话里，不落盘生成报告；确需新建文件先问用户。
- 命名与文件既有风格一致：原子名用「元素 + 序号」（`C1`/`O1`/`X1`…）；变量用 `<原子>_<角色>`（`OH_mob`、`X4_negative`、`C2_X3_bond`）；步骤名用数字后缀（`step_oh_attack2`、`step_x_attack3`）。不要字母后缀、不要 camelCase。
- 讲解文字统一用 `Description(text=...)`；化学式写 `\mathrm{...}`，不要在 `\text{}` 里直接写 Unicode 希腊字母或 `^`。
- 多处讲解文字默认都落在同一坐标 `[0,-3,0]`，必须用 `ReplacementTransform` 顺次替换，不能同时 `Write`（会重叠）。
- `StructuralFormula` 的 submobject 顺序决定 `Transform` 的逐项配对：做结构展开/缩写前，先重整子对象顺序使两侧对应。
- `text_offset`（`AtomicCluster` / `add_atom` / `register_atom`）是**固定位移**：它只随锚点平移，不随键或分子旋转（与 `RotateAtoms` 中电荷偏移的处理一致）。要让标签跟着分子转，须在动画结束后自行重设偏移。
- **所有测试代码必须写在仓库根目录的 `test.py`**（不被 git 跟踪），按场景类分块；不新建单独的测试文件，也不把测试混进根目录的其它 `*.py` —— 根目录下除 `test.py` 外的 `*.py` 一律是非测试代码。

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

- 无进行中的任务；等用户给出新目标。
- `SubstitutionReaction3.py` **已完成**：整部「一些常见的取代反应机理」教学动画（加成-消除机理 → 羰基活泼 α-H 亲电取代 → 卤仿反应）全部做完，并经用户渲染确认，**无需继续开发**。

## 备注

- 两个反复踩到的「场景成员关系」坑：
  1. `electron_migration`（以及某些 `self.add(...)`）会把 `StructuralFormula` 从 `Scene.mobjects` 中**拆散**；此后往结构式里新增的对象必须显式 `self.add(...)` 才会渲染。注意 `FadeIn`/`Create`/`Write` 是 introducer，`Scene.add_mobjects_from_animations` 会跳过它们，只加 `FadeIn` 救不回来。
  2. `rotate_atoms` 的动画 `mobject` 就是结构式本身且不是 introducer，会把结构式**重新聚合回场景**；此后 `sf.add(x)` 会立刻渲染 x。所以「替换原子文本」这类改动要把原子表更新（`remove` / `atomic_clusters[...][Mobject]=` / `add`）放到 `self.play` **之后**，否则新标签会在形变前闪现。
- 渲染产物：`media/videos/SubstitutionReaction3/1080p60/test.mp4`（用户渲染后会显示为已修改）。
