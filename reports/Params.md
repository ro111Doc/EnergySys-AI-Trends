# 项目参数总览 (Project Parameters & Traceability)

> **版本说明**：本文件为项目唯一参数追踪文档，取代所有历史版本。

## 一、 项目背景与范式
### 1.1 项目名称
- 中文：基于 LSTM 的电力负荷预测研究热点与发展趋势——文献计量分析（2015–2025）
- 英文：Research hotspots and development trends of LSTM in electric load forecasting: a bibliometric analysis (2015–2025)

### 1.2 项目类型
- 类型：文献计量学课程项目
- 研究范式：项目制、可复现研究流程

### 1.3 当前研究时间范围
- 起始年份：2015
- 终止年份：2025

### 1.4 当前实际数据库
- 已实际检索：
  - 中国知网（CNKI）
  - Web of Science（WoS）

### 1.5 计划可扩展数据库
- Scopus
- IEEE Xplore
- WanFang
- VIP

---

## 二、 工具栈与选型矩阵
[cite_start]本组根据“工具-任务匹配”原则，构建了以下四层工具栈 [cite: 8, 16]：

| 工具名 | 所在层级 | 要解决的问题 | 预期输出 | 风险点及应对 | 方案状态 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CiteSpace (v6.x)** | GUI层 | [cite_start]共被引聚类、突现检测、关键节点识别 [cite: 10] | 聚类图谱、Burst列表 | [cite_start]参数记录依赖人工；通过本文件落盘 [cite: 11] | **主方案** |
| **VOSviewer** | GUI层 | [cite_start]合作网络可视化、密度分布、主题演化 [cite: 11] | 合作图谱、Overlay图 | [cite_start]图美观但解释性需人工加强 [cite: 11] | **备选方案** |
| **PyAlex / pandas** | 数据/开源层 | [cite_start]自动取数、字段映射、数据清洗与去重 [cite: 12] | 清洗后的数据集 | [cite_start]API速率限制；建立缓存机制 [cite: 12] | **主方案** |
| **GPT Researcher** | Agent层 | [cite_start]领域术语扩展、背景调研、证据表初稿 [cite: 14] | 术语列表、综述大纲 | [cite_start]存在幻觉风险；必须人工核查证据 [cite: 15] | **备选方案** |

---

## 三、 当前执行口径 (基于 v2.1)

## 0. 文件元信息

| 项目 | 内容 |
|---|---|
| 文件名称 | `Params.md` |
| 当前版本 | v2.1 |
| 最近更新日期 | 2026-05-08 |
| 维护成员 | A |
| 当前阶段 | Lesson6 指标体系与基础可视化阶段 |
| 当前主题 | 能源系统中的时序预测方法 |
| 当前数据口径 | 最终筛选后的 WoS 格式数据 |
| 当前主要输入文件 | `screened_final.csv` |
| 当前建议存放路径 | `文档/Params.md` |
| 当前主要输出目录 | `输出/metrics/` |
| 当前对应脚本 | `src/metrics_visualization.py` |

---

## 1. 文件说明

本文件用于集中记录本项目在以下环节中的关键参数设置：

1. 研究主题与研究范围；
2. 检索词体系；
3. 数据源与字段映射；
4. 数据清洗与质量控制；
5. 指标体系；
6. 基础可视化；
7. 后续共被引、耦合、合作网络、突现分析与时间线分析；
8. 版本更新与执行日志。

本文件的作用包括：

1. 统一项目执行口径；
2. 明确每一步操作依据；
3. 保证后续结果可解释、可追溯、可复现；
4. 为 `query.yaml`、`metrics_spec.md`、`clean_rules.md`、`field_dictionary.md`、`screening_rule.md`、`data_quality.md`、`metrics_visualization.py` 提供参数层面的汇总说明。

本文件不是原始检索式全文，也不是最终论文方法部分，而是整个项目的**参数总表**。

---

## 2. 当前项目基础参数

### 2.1 当前项目名称

- 中文题目：从 LSTM 到 Transformer：能源系统时序预测方法的文献计量与演化分析
- 英文题目：From LSTM to Transformer: A Bibliometric and Evolutionary Analysis of Time-Series Forecasting Methods in Energy Systems

### 2.2 项目类型

| 参数 | 配置 |
|---|---|
| 课程类型 | 文献计量学与前沿趋势追踪课程项目 |
| 研究范式 | 项目制、可复现研究流程 |
| 分析类型 | 文献计量分析 + 方法演化分析 + 趋势识别 |
| 当前任务角色 | A：指标体系、指标可视化、参数日志更新 |
| 当前成果类型 | Markdown 文档、PNG 图表、CSV 指标表 |

### 2.3 当前研究时间范围

| 类型 | 时间范围 | 说明 |
|---|---|---|
| 计划研究窗口 | 2015–2025 | 原始设定，用于覆盖深度学习预测方法发展阶段 |
| 当前最终数据实际范围 | 2017–2025 | 由最终筛选后的 WoS 数据 `PY` 字段决定 |
| 是否包含 2026 | 否 | 当前最终数据不再使用旧版 2024–2026 混合数据口径 |
| 年份字段 | `PY` | WoS 中的 Publication Year |

### 2.4 当前研究主题变更

原始主题为：

```text
基于 LSTM 的电力负荷预测研究热点与发展趋势
```

当前主题已扩展为：

```text
能源系统中的时序预测方法
```

主题扩展原因：

1. LSTM-only 主题过窄，不利于形成长期时间演化分析；
2. 旧数据集中年份过度集中，难以支撑 burst、timeline 和 milestone 分析；
3. 课程要求强调趋势检测、技术演化和知识图谱叙事；
4. 新主题能够覆盖从传统统计模型、机器学习模型、循环神经网络到 Transformer 的完整方法谱系；
5. 新主题更适合形成“从 LSTM 到 Transformer”的技术路线叙事。

---

## 3. 当前目录参数

当前仓库采用中文目录结构。A 阶段相关文件建议按以下路径放置：

| 文件或目录 | 推荐路径 | 用途 |
|---|---|---|
| 参数总表 | `文档/Params.md` | 记录项目参数和更新日志 |
| 指标规范 | `文档/metrics_spec.md` | 定义指标体系 |
| 可视化脚本 | `src/metrics_visualization.py` | 生成指标可视化图 |
| 最终筛选数据 | `数据/processed/screened_final.csv` | 当前主要输入数据 |
| 指标输出目录 | `输出/metrics/` | 存放 PNG 图与 CSV 表 |
| Lesson6 报告 | `报告/lesson6/` | 存放阶段性汇报材料 |
| 检索配置 | `配置/query.yaml` | 记录检索式结构 |
| 同义词配置 | `配置/synonyms.yaml` | 记录方法词与场景词扩展 |

---

## 4. 当前数据源参数

### 4.1 当前正式数据源

| 数据源 | 当前状态 | 当前用途 |
|---|---|---|
| Web of Science | 当前 A 阶段正式使用 | 指标可视化、被引统计、来源期刊、学科类别 |
| CNKI | 历史阶段使用，当前不作为 A 阶段可视化主输入 | 可作为中文补充数据源 |
| Scopus | 暂未使用 | 保留扩展位 |
| IEEE Xplore | 暂未使用 | 保留扩展位 |
| WanFang | 暂未使用 | 保留扩展位 |
| VIP | 暂未使用 | 保留扩展位 |

### 4.2 当前最终数据参数

| 参数项 | 当前值 |
|---|---|
| 输入文件名 | `screened_final.csv` |
| 数据格式 | CSV |
| 字段体系 | WoS 导出字段 |
| 当前记录数 | 443 |
| 当前字段数 | 37 |
| 当前年份范围 | 2017–2025 |
| 当前推荐存放路径 | `数据/processed/screened_final.csv` |
| 当前编码处理 | 自动尝试 `utf-8-sig`、`utf-8`、`gb18030`、`latin1` |
| 当前分析脚本 | `src/metrics_visualization.py` |
| 当前输出路径 | `输出/metrics/` |

---

## 5. 检索参数（Search Parameters）

### 5.1 当前总体检索逻辑

当前项目检索逻辑从旧版：

```text
LSTM 方法词 AND 电力负荷预测任务词 AND 电力系统场景词
```

扩展为新版：

```text
时序预测任务词 AND 能源系统场景词 AND 预测方法词
```

当前检索逻辑包含三层：

1. 任务层：time-series forecasting / load forecasting / energy forecasting；
2. 场景层：energy systems / power systems / smart grid / microgrid / renewable energy；
3. 方法层：ARIMA / SVR / LSTM / GRU / Transformer / hybrid forecasting。

### 5.2 任务词参数

| 类型 | 关键词 |
|---|---|
| 英文任务词 | `time series forecasting` |
| 英文任务词 | `time-series forecasting` |
| 英文任务词 | `load forecasting` |
| 英文任务词 | `load prediction` |
| 英文任务词 | `electricity demand forecasting` |
| 英文任务词 | `energy forecasting` |
| 英文任务词 | `power forecasting` |
| 英文任务词 | `short-term load forecasting` |
| 英文任务词 | `ultra-short-term load forecasting` |
| 中文任务词 | 电力负荷预测 |
| 中文任务词 | 负荷预测 |
| 中文任务词 | 能源预测 |
| 中文任务词 | 电力需求预测 |
| 中文任务词 | 短期负荷预测 |
| 中文任务词 | 超短期负荷预测 |

### 5.3 场景词参数

| 类型 | 关键词 |
|---|---|
| 英文场景词 | `energy system` |
| 英文场景词 | `power system` |
| 英文场景词 | `smart grid` |
| 英文场景词 | `microgrid` |
| 英文场景词 | `renewable energy` |
| 英文场景词 | `wind power` |
| 英文场景词 | `solar power` |
| 英文场景词 | `photovoltaic` |
| 英文场景词 | `integrated energy system` |
| 英文场景词 | `multi-energy system` |
| 英文场景词 | `demand response` |
| 英文场景词 | `building energy` |
| 中文场景词 | 能源系统 |
| 中文场景词 | 电力系统 |
| 中文场景词 | 智能电网 |
| 中文场景词 | 微电网 |
| 中文场景词 | 新能源 |
| 中文场景词 | 风电 |
| 中文场景词 | 光伏 |
| 中文场景词 | 综合能源系统 |
| 中文场景词 | 需求响应 |
| 中文场景词 | 建筑能源 |

### 5.4 方法词参数

| 方法阶段 | 代表关键词 |
|---|---|
| 统计预测方法 | `ARIMA`、`SARIMA` |
| 机器学习方法 | `SVR`、`SVM`、`Random Forest`、`XGBoost` |
| 循环神经网络 | `RNN`、`LSTM`、`GRU`、`BiLSTM` |
| 混合模型 | `CNN-LSTM`、`Attention-LSTM`、`hybrid forecasting`、`decomposition-based forecasting` |
| Transformer 系列 | `Transformer`、`TFT`、`Temporal Fusion Transformer`、`Informer`、`Autoformer`、`PatchTST`、`iTransformer`、`xLSTM` |

### 5.5 排除词参数

排除词仅用于剔除明显跨领域主题，不用于排除能源系统内部的边界主题。

| 类型 | 排除词 |
|---|---|
| 英文 | `traffic flow forecasting` |
| 英文 | `network traffic forecasting` |
| 英文 | `server workload prediction` |
| 英文 | `CPU load prediction` |
| 英文 | `bridge load prediction` |
| 中文 | 交通流预测 |
| 中文 | 网络流量预测 |
| 中文 | 服务器负载预测 |
| 中文 | CPU 负载预测 |
| 中文 | 桥梁荷载预测 |

排除原则：

1. 排除词要少而准；
2. 不直接排除 `microgrid`、`building energy`、`integrated energy systems` 等能源系统边界主题；
3. 对边界主题优先交给筛选规则处理。

---

## 6. 字段映射参数（Field Mapping Parameters）

### 6.1 当前 WoS 字段映射

当前 A 阶段以 WoS 字段为主，不再使用旧版中文字段进行指标可视化。

| 分析用途 | WoS 字段 | 字段含义 | 当前用途 |
|---|---|---|---|
| 年份分析 | `PY` | Publication Year | 年发文趋势 |
| 标题分析 | `TI` | Title | 高被引文献标题、方法词匹配 |
| 来源分析 | `SO` | Source Title | 来源期刊分布 |
| 文献类型分析 | `DT` | Document Type | 文献类型分布 |
| 摘要分析 | `AB` | Abstract | 方法词、场景词匹配 |
| 作者缩写 | `AU` | Authors | 后续作者分析 |
| 作者全名 | `AF` | Author Full Name | 后续作者合作网络 |
| DOI | `DI` | DOI | DOI 完整率统计 |
| 被引次数 | `TC` | Times Cited | 高被引文献排序 |
| 学科类别 | `SC` | Subject Category | 学科类别分布 |
| 参考文献 | `CR` | Cited References | 后续共被引分析 |
| 唯一标识 | `UT` | Unique WOS ID | 去重与溯源 |
| 关键词 | `DE` / `ID` | Author Keywords / Keywords Plus | 方法频次和主题分析 |

### 6.2 中文旧字段与当前字段对应关系

| 旧字段口径 | 当前字段口径 | 说明 |
|---|---|---|
| `年份` | `PY` | 当前数据采用 WoS 年份字段 |
| `题名` | `TI` | 当前数据采用 WoS 标题字段 |
| `文献来源` / `来源库` | `SO` | 当前用于来源期刊统计 |
| `文献类型` | `DT` | 当前用于文献类型统计 |
| `摘要` | `AB` | 当前用于文本匹配 |
| `DOI` | `DI` | 当前用于 DOI 完整率 |
| `被引次数` | `TC` | 当前用于高被引排序 |
| `学科类别` | `SC` | 当前用于学科类别分布 |

---

## 7. 数据清洗参数（Cleaning Parameters）

### 7.1 通用清洗参数

| 参数项 | 当前设置 |
|---|---|
| 删除首尾空格 | 是 |
| 删除字段名前后空格 | 是 |
| DOI 大小写统一 | 建议统一为小写 |
| 原始字段保留 | 是 |
| 缺失值处理 | 统计时使用 `fillna("Unknown")` 或跳过 |
| 年份处理 | `PY` 转为整数 |
| 文本字段合并 | `TI` + `AB` + `DE` + `ID` |
| 编码输出 | `utf-8-sig` |
| Excel 兼容 | 是 |

### 7.2 当前脚本字段识别逻辑

脚本优先识别以下字段：

| 用途 | 字段优先级 |
|---|---|
| 年份 | `PY` → `年份` → `Year` |
| 标题 | `TI` → `题名` → `Title` |
| 来源 | `SO` → `文献来源` → `Source Title` |
| 文献类型 | `DT` → `文献类型` → `Document Type` |
| DOI | `DI` → `DOI` |
| 摘要 | `AB` → `摘要` → `Abstract` |
| 作者 | `AU` → `AF` → `作者` |
| 学科类别 | `SC` → `WC` → `学科类别` |
| 被引次数 | `TC` → `被引频次` → `Citations` |

---

## 8. 筛选参数（Screening Parameters）

### 8.1 当前筛选状态

| 参数 | 当前值 |
|---|---|
| 当前阶段 | 已完成最终筛选 |
| 当前使用文件 | `screened_final.csv` |
| 当前可视化数据 | 最终筛选后的 WoS 格式数据 |
| 旧版筛选数据 | 不再作为 A 阶段可视化主输入 |
| 当前筛选目标 | 支撑能源系统时序预测方法演化分析 |

### 8.2 当前纳入原则

文献原则上需满足以下条件：

1. 研究对象属于能源系统、电力系统、智能电网、微电网、新能源、综合能源或相关场景；
2. 研究任务涉及预测，尤其是时序预测、负荷预测、需求预测、发电预测或能源预测；
3. 研究方法涉及统计模型、机器学习、深度学习、混合模型或 Transformer 系列方法；
4. 文献能够为方法演化、场景扩展或前沿趋势提供证据。

### 8.3 当前排除原则

优先排除以下文献：

1. 交通流预测、网络流量预测、服务器负载预测等非能源系统预测；
2. 仅讨论优化调度但不包含预测任务的文献；
3. 仅讨论控制、规划、市场交易但预测不是主要模块的文献；
4. 缺少基本文献信息且无法进入统计分析的文献；
5. 与能源系统时序预测无直接关系的交叉噪声文献。

---

## 9. 指标体系参数（Metric Parameters）

### 9.1 数据规模指标

| 指标 | 字段 | 用途 |
|---|---|---|
| 总记录数 | 全表行数 | 描述最终语料规模 |
| 字段数量 | 全表列数 | 描述元数据完整度 |
| 最早年份 | `PY` | 判断研究起点 |
| 最新年份 | `PY` | 判断前沿覆盖 |
| DOI 完整率 | `DI` | 判断唯一标识完整性 |
| 摘要完整率 | `AB` | 判断文本分析可用性 |
| 标题完整率 | `TI` | 判断基础信息完整性 |
| 作者完整率 | `AU` / `AF` | 判断合作分析可用性 |

### 9.2 时间趋势指标

| 指标 | 字段 | 输出 |
|---|---|---|
| 年发文量 | `PY` | `annual_publication_trend.png` |
| 年发文量数据 | `PY` | `annual_publication_trend.csv` |

### 9.3 文献结构指标

| 指标 | 字段 | 输出 |
|---|---|---|
| 文献类型分布 | `DT` | `document_type_distribution.png` |
| 来源期刊 Top15 | `SO` | `top_source_distribution.png` |
| 学科类别 Top15 | `SC` | `category_distribution.png` |

### 9.4 引用影响指标

| 指标 | 字段 | 输出 |
|---|---|---|
| 高被引文献 Top20 | `TI` + `TC` | `top_cited_papers.png` |
| 高被引文献数据表 | `TI` + `TC` | `top_cited_papers.csv` |

说明：高被引文献只是 milestone 候选池，不等于最终 milestone 文献。

### 9.5 方法演化指标

当前方法频次统计基于 `TI`、`AB`、`DE`、`ID` 字段的规则匹配。

| 方法类别 | 匹配词 |
|---|---|
| ARIMA | `ARIMA`、`SARIMA` |
| SVR / SVM | `SVR`、`SVM`、`support vector` |
| Random Forest | `random forest` |
| XGBoost | `XGBoost`、`extreme gradient` |
| RNN | `RNN`、`recurrent neural` |
| LSTM | `LSTM`、`long short-term memory`、`long short term memory` |
| GRU | `GRU`、`gated recurrent` |
| BiLSTM | `BiLSTM`、`bidirectional LSTM` |
| CNN-LSTM | `CNN-LSTM`、`CNN LSTM`、`convolutional LSTM` |
| Attention | `attention` |
| Transformer | `transformer`、`TFT`、`temporal fusion transformer`、`Informer`、`Autoformer`、`PatchTST`、`iTransformer` |
| Decomposition | `VMD`、`EMD`、`EEMD`、`CEEMDAN`、`decomposition` |

### 9.6 应用场景指标

当前应用场景频次统计基于 `TI`、`AB`、`DE`、`ID` 字段的规则匹配。

| 场景类别 | 匹配词 |
|---|---|
| Smart Grid | `smart grid` |
| Microgrid | `microgrid`、`micro-grid` |
| Renewable Energy | `renewable`、`wind power`、`solar`、`photovoltaic`、`PV` |
| Integrated Energy Systems | `integrated energy`、`multi-energy` |
| Demand Response | `demand response` |
| Electricity Load | `electricity load`、`load forecasting`、`power load` |
| Energy Demand | `energy demand`、`demand forecasting` |
| Building Energy | `building`、`building energy` |

---

## 10. 可视化参数（Visualization Parameters）

### 10.1 当前脚本参数

| 参数项 | 当前设置 |
|---|---|
| 脚本名称 | `metrics_visualization.py` |
| 推荐路径 | `src/metrics_visualization.py` |
| 数据处理库 | `pandas` |
| 绘图库 | `matplotlib` |
| 图像分辨率 | 300 dpi |
| 输出格式 | PNG + CSV |
| 输出目录 | `输出/metrics/` |
| 图形风格 | 白底学术风 |
| 坐标轴语言 | 英文为主 |
| 中文说明 | 在报告和 README 中补充 |
| 文件编码 | `utf-8-sig` |
| Top 来源数量 | 15 |
| Top 高被引文献数量 | 20 |

### 10.2 当前已生成图表

| 序号 | 英文文件名 | 中文名称 | 文件类型 | 用途 |
|---|---|---|---|---|
| 1 | `annual_publication_trend.png` | 年发文趋势图 | PNG | 展示 2017–2025 年发文变化 |
| 2 | `annual_publication_trend.csv` | 年发文趋势数据表 | CSV | 记录每年发文数量 |
| 3 | `document_type_distribution.png` | 文献类型分布图 | PNG | 展示 Article、Review 等类型结构 |
| 4 | `document_type_distribution.csv` | 文献类型分布数据表 | CSV | 记录不同文献类型数量 |
| 5 | `top_source_distribution.png` | 来源期刊 Top15 分布图 | PNG | 展示高产来源期刊 |
| 6 | `top_source_distribution.csv` | 来源期刊 Top15 数据表 | CSV | 记录来源期刊发文数量 |
| 7 | `top_cited_papers.png` | 高被引文献 Top20 分布图 | PNG | 展示高被引文献候选 |
| 8 | `top_cited_papers.csv` | 高被引文献 Top20 数据表 | CSV | 记录文献标题与被引次数 |
| 9 | `method_frequency_distribution.png` | 方法频次分布图 | PNG | 展示主要预测方法出现频次 |
| 10 | `method_frequency_distribution.csv` | 方法频次分布数据表 | CSV | 记录各方法文献数量 |
| 11 | `scenario_frequency_distribution.png` | 应用场景频次分布图 | PNG | 展示主要能源应用场景 |
| 12 | `scenario_frequency_distribution.csv` | 应用场景频次分布数据表 | CSV | 记录场景文献数量 |
| 13 | `category_distribution.png` | 学科类别 Top15 分布图 | PNG | 展示 WoS 学科类别分布 |
| 14 | `category_distribution.csv` | 学科类别 Top15 数据表 | CSV | 记录学科类别频次 |
| 15 | `metrics_summary.csv` | 指标汇总表 | CSV | 记录数据量、字段识别、完整率等 |
| 16 | `README_metrics_outputs.md` | 指标可视化结果说明文档 | Markdown | 说明输出文件与字段映射 |

---

## 11. 质量控制参数（Quality Control Parameters）

### 11.1 当前基础质量检查项

| 检查项 | 字段 | 当前处理方式 |
|---|---|---|
| 题名是否缺失 | `TI` | 计算完整率 |
| 作者是否缺失 | `AU` / `AF` | 计算完整率 |
| 摘要是否缺失 | `AB` | 计算完整率 |
| DOI 是否缺失 | `DI` | 计算完整率 |
| 年份是否缺失 | `PY` | 缺失则不参与年趋势统计 |
| 被引次数是否缺失 | `TC` | 缺失按 0 或跳过处理 |
| 来源期刊是否缺失 | `SO` | 缺失填为 `Unknown` |
| 文献类型是否缺失 | `DT` | 缺失填为 `Unknown` |
| 学科类别是否缺失 | `SC` | 缺失则跳过类别统计 |

### 11.2 当前验证结果

| 验证项 | 结果 | 说明 |
|---|---|---|
| CSV 读取 | 通过 | 文件可被 pandas 正常读取 |
| 字段识别 | 通过 | 成功识别 `PY`、`TI`、`SO`、`DT`、`AB`、`TC`、`SC` |
| 年份范围 | 通过 | 覆盖 2017–2025 |
| PNG 输出 | 通过 | 已生成 7 张 PNG 图 |
| CSV 输出 | 通过 | 每张图均有对应 CSV 表 |
| 汇总表输出 | 通过 | 已生成 `metrics_summary.csv` |
| 说明文档输出 | 通过 | 已生成 `README_metrics_outputs.md` |
| 主题一致性 | 通过 | 已由 LSTM-only 更新为能源系统时序预测方法 |

---

## 12. 后续分析参数（Analysis Parameters）

### 12.1 共被引分析参数

当前状态：待基于新 WoS 最终数据重跑。

| 参数 | 当前建议 |
|---|---|
| 分析单元 | Cited Reference |
| 依赖字段 | `CR` |
| 推荐工具 | CiteSpace / Python |
| 推荐时间切片 | 1 年 |
| 时间范围 | 2017–2025 |
| 节点类型 | Reference |
| 重点输出 | 共被引网络图、聚类标签、Modularity Q、Silhouette |
| 用途 | 识别知识基础与 milestone 候选文献 |

说明：旧版基于 `citing_paper` → `cited_paper` 的共被引参数保留为历史记录，但当前正式分析应优先使用 WoS `CR` 字段。

### 12.2 突现分析参数

当前状态：待执行。

| 参数 | 当前建议 |
|---|---|
| 分析对象 | Keywords / References |
| 依赖字段 | `DE`、`ID`、`CR` |
| 推荐工具 | CiteSpace |
| 时间范围 | 2017–2025 |
| 输出指标 | burst strength、begin year、end year |
| 用途 | 识别快速升温的方法与主题 |

### 12.3 时间线分析参数

当前状态：待执行。

| 参数 | 当前建议 |
|---|---|
| 分析对象 | Keywords / References |
| 推荐工具 | CiteSpace Timeline View |
| 时间切片 | 1 年 |
| 时间范围 | 2017–2025 |
| 用途 | 解释方法从 LSTM、混合模型到 Transformer 的演化过程 |

### 12.4 作者合作网络参数

当前状态：待基于新 WoS 数据重跑。

| 参数 | 当前建议 |
|---|---|
| 依赖字段 | `AU` / `AF` |
| 分析单元 | Author |
| 推荐工具 | VOSviewer / CiteSpace / Python |
| 节点筛选 | 可设置发文量 ≥ 2 |
| 用途 | 识别核心作者与合作团队 |

### 12.5 机构合作网络参数

当前状态：待基于新 WoS 数据重跑。

| 参数 | 当前建议 |
|---|---|
| 依赖字段 | `C1` / `C3` |
| 分析单元 | Institution |
| 推荐工具 | VOSviewer / CiteSpace |
| 用途 | 识别核心机构和区域合作格局 |

---

## 13. 当前风险与注意事项

1. 当前指标图属于描述性统计，不能替代正式知识图谱。
2. 方法频次和场景频次基于字符串匹配，存在漏检和误检风险。
3. 高被引文献 Top20 只是 milestone 候选，不等于最终 milestone。
4. 共被引、突现、时间线、合作网络仍需基于新数据重跑。
5. 如果后续将英文输出文件名改为中文，需要同步修改脚本和 README。
6. 旧版 LSTM-only 参数仅作为历史记录保留，不应再作为主分析依据。
7. 如果后续合并 CNKI 数据，需要重新检查字段映射和去重策略。
8. 如果新增数据库，必须更新本文件的数据源参数、字段映射和筛选口径。

---

## 14. 版本管理参数（Versioning Parameters）

### 14.1 当前版本

| 项目 | 内容 |
|---|---|
| 当前版本 | v2.1 |
| 状态 | 当前生效 |
| 维护成员 | A |
| 更新日期 | 2026-05-08 |
| 当前任务 | Lesson6 指标可视化与参数日志更新 |

### 14.2 更新触发条件

以下情况必须更新本文件：

1. 研究主题发生变化；
2. 检索式结构发生变化；
3. 数据源发生变化；
4. 最终筛选数据发生变化；
5. 字段名或字段映射发生变化；
6. 输入路径发生变化；
7. 输出路径发生变化；
8. 新增或删除指标；
9. 新增图表输出；
10. CiteSpace / VOSviewer / Python 分析参数发生变化；
11. 共被引、突现、时间线、合作网络等核心图谱重跑；
12. 组内成员完成新的阶段性结果。

### 14.3 联动更新文件

| 文件 | 是否必须检查 | 检查内容 |
|---|---|---|
| `README.md` | 是 | 项目主题、目录结构、运行命令是否同步 |
| `配置/query.yaml` | 是 | 检索式是否与当前主题一致 |
| `文档/metrics_spec.md` | 是 | 指标定义是否与参数文件一致 |
| `文档/screening_rule.md` | 是 | 纳入/排除标准是否跟随新选题变化 |
| `文档/field_dictionary.md` | 是 | 字段映射是否匹配 WoS 字段 |
| `文档/data_quality.md` | 是 | 数据质量统计是否基于最新数据 |
| `src/metrics_visualization.py` | 是 | 输入路径、字段名、输出目录是否正确 |
| `输出/metrics/` | 是 | 图表和 CSV 是否已经生成 |
| `报告/lesson6/` | 建议 | 阶段性报告是否引用最新图表 |

---

## 15. 版本记录与执行日志（Version Log）

### v0.1：项目参数总表初建

- 更新时间：早期项目阶段
- 更新成员：项目组
- 主题口径：基于 LSTM 的电力负荷预测
- 主要内容：
  1. 建立项目参数总表；
  2. 记录 CNKI 与 WoS 的基础检索参数；
  3. 记录字段映射、清洗、去重、筛选、合并等参数；
  4. 建立初步数据质量控制阈值；
  5. 预留共被引、作者合作、机构分析等后续分析入口。

- 局限：
  1. 版本记录过于简略；
  2. 未记录实际输入文件；
  3. 未记录脚本路径；
  4. 未记录输出文件；
  5. 未反映后续选题扩展；
  6. 与当前最终筛选数据字段不完全匹配。

### v1.0：LSTM 电力负荷预测阶段参数版本

- 更新时间：LSTM-only 选题阶段
- 主题口径：

```text
基于 LSTM 的电力负荷预测研究热点与发展趋势
```

- 时间窗口：

```text
2015–2025
```

- 方法词重点：
  - LSTM
  - BiLSTM
  - Attention-LSTM
  - CNN-LSTM

- 任务词重点：
  - 电力负荷预测
  - load forecasting
  - short-term load forecasting
  - electricity demand forecasting

- 场景词重点：
  - power system
  - smart grid
  - distribution network

- 主要贡献：
  1. 明确了初始研究方向；
  2. 建立了方法词、任务词、场景词、排除词四层检索逻辑；
  3. 为初步筛选和数据质量检查提供了参数基础。

- 发现的问题：
  1. 数据时间跨度不足；
  2. 方法范围过窄；
  3. 检索结果容易集中于近年 LSTM 变体；
  4. 不利于形成清晰的 timeline 演化分析；
  5. 不利于识别从传统模型到深度模型再到 Transformer 的技术路线。

### v2.0：研究主题扩展版本

- 更新时间：选题重构阶段
- 触发原因：

原始 LSTM-only 选题无法充分支撑课程要求中的：

1. 趋势检测；
2. 主题演化；
3. milestone 文献识别；
4. 方法谱系分析；
5. 从图谱到技术叙事的转换。

- 主题由：

```text
基于 LSTM 的电力负荷预测
```

扩展为：

```text
能源系统中的时序预测方法
```

- 方法范围扩展为：

| 方法阶段 | 代表方法 |
|---|---|
| 统计预测方法 | ARIMA、SARIMA |
| 机器学习方法 | SVR、Random Forest、XGBoost |
| 循环神经网络方法 | RNN、LSTM、GRU、BiLSTM |
| 混合深度学习方法 | CNN-LSTM、Attention-LSTM、decomposition-based models |
| Transformer 系列方法 | TFT、Informer、Autoformer、PatchTST、iTransformer、xLSTM |

- 本次更新结果：
  1. 研究主题具备更长时间跨度；
  2. 方法演化路径更完整；
  3. 后续可形成“从 LSTM 到 Transformer”的技术叙事；
  4. 与课程对趋势分析、突现分析和知识图谱叙事的要求更匹配。

### v2.1：Lesson6 指标可视化参数更新版本

- 更新时间：2026-05-08
- 更新成员：A
- 当前任务：生成指标可视化图，并更新参数日志
- 当前数据：最终筛选后的 WoS 格式数据
- 当前数据规模：443 条记录
- 当前字段数量：37 个字段
- 当前实际年份范围：2017–2025
- 当前字段体系：WoS 字段体系

#### v2.1.1 输入数据记录

| 项目 | 内容 |
|---|---|
| 输入文件 | `screened_final.csv` |
| 推荐路径 | `数据/processed/screened_final.csv` |
| 记录数 | 443 |
| 字段数 | 37 |
| 年份字段 | `PY` |
| 题名字段 | `TI` |
| 来源字段 | `SO` |
| 文献类型字段 | `DT` |
| 摘要字段 | `AB` |
| 被引次数字段 | `TC` |
| 学科类别字段 | `SC` |

#### v2.1.2 本次实际产出

本次已生成：

1. 年发文趋势图；
2. 文献类型分布图；
3. 来源期刊 Top15 分布图；
4. 高被引文献 Top20 分布图；
5. 方法频次分布图；
6. 应用场景频次分布图；
7. 学科类别 Top15 分布图；
8. 指标汇总表；
9. 指标可视化结果说明文档。

#### v2.1.3 本次更新的验证记录

| 验证项 | 验证结果 | 说明 |
|---|---|---|
| CSV 可读取 | 通过 | 文件可被 pandas 正常读取 |
| 字段识别 | 通过 | 成功识别 `PY`、`TI`、`SO`、`DT`、`AB`、`TC`、`SC` 等字段 |
| 年份范围 | 通过 | 实际覆盖 2017–2025 |
| 图表输出 | 通过 | 已生成 7 张 PNG 图 |
| CSV 输出 | 通过 | 每张图均配套 CSV 数据表 |
| 指标汇总 | 通过 | 已生成 `metrics_summary.csv` |
| 结果说明 | 通过 | 已生成 `README_metrics_outputs.md` |
| 与当前主题一致性 | 通过 | 指标已从 LSTM-only 扩展为时序预测方法谱系 |

---

## 16. 后续更新计划

### 16.1 C / D 成员完成图谱分析后需要补充

后续如果 C / D 成员完成以下任务，需要继续更新本文件：

1. CiteSpace 共被引网络；
2. CiteSpace 关键词聚类；
3. CiteSpace burst detection；
4. CiteSpace timeline view；
5. VOSviewer 合作网络；
6. milestone 文献候选表；
7. 结构变异分析；
8. 最终 3 图 1 表解释文字。

### 16.2 下一版建议版本号

| 触发事件 | 建议版本号 |
|---|---|
| 新增 CiteSpace 共被引和关键词聚类参数 | v2.2 |
| 新增 burst 和 timeline 参数 | v2.3 |
| 新增 milestone 表参数 | v2.4 |
| 形成 M2 提交版 3 图 1 表 | v3.0 |

---

## 17. 使用说明

使用本文件时，建议按以下顺序阅读：

1. 先看第 2–4 节，确认项目主题、目录和数据源；
2. 再看第 5–8 节，确认检索、字段、清洗和筛选口径；
3. 然后看第 9–11 节，确认指标、图表和质量控制参数；
4. 最后看第 14–16 节，确认版本记录和后续更新计划。

本文件中的当前主口径为 v2.1。旧版 LSTM-only 内容仅作为历史记录，不作为当前正式分析依据。
