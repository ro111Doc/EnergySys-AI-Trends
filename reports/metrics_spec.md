# metrics_spec.md

> 当前版本说明：本文件已更新至 **v2.1**，适用于项目新选题“能源系统中的时序预测方法”与 Lesson6 指标体系、基础可视化阶段。旧版 LSTM-only 指标体系仅作为历史记录保留，不再作为当前主分析口径。

---

## 0. 文件元信息

| 项目 | 内容 |
|---|---|
| 文件名称 | `metrics_spec.md` |
| 当前版本 | v2.1 |
| 最近更新日期 | 2026-05-08 |
| 维护成员 | A |
| 当前阶段 | Lesson6 指标体系与基础可视化阶段 |
| 当前主题 | 能源系统中的时序预测方法 |
| 当前数据口径 | 最终筛选后的 WoS 格式数据 |
| 当前主要输入文件 | `screened_final.csv` |
| 当前建议存放路径 | `文档/metrics_spec.md` |
| 当前主要输出目录 | `输出/metrics/` |
| 对应参数文件 | `文档/Params.md` |
| 对应脚本 | `src/metrics_visualization.py` |

---

## 1. 文件目的

本文件用于定义项目中的指标体系，包括：

1. 描述性统计指标；
2. 文献计量基础指标；
3. 方法演化指标；
4. 应用场景指标；
5. 数据质量指标；
6. 可视化输出指标；
7. 后续共被引、突现、时间线和 milestone 分析的接口指标。

本文件的作用包括：

1. 明确每个指标的计算字段；
2. 明确每个指标的计算公式；
3. 明确每个指标对应的输出文件；
4. 明确每个指标在研究问题中的作用；
5. 保证指标计算过程可复现；
6. 避免图表生成与研究主题脱节；
7. 为后续 3 图 1 表、M2 汇报和最终 mini review 提供统一指标口径。

---

## 2. 当前研究问题与指标对应关系

当前项目研究主题为：

```text
能源系统中的时序预测方法
```

核心研究问题如下：

| 编号 | 研究问题 | 对应指标类型 | 对应图表 |
|---|---|---|---|
| RQ1 | 该领域在 2017–2025 年的研究规模如何变化？ | 年发文趋势指标 | 年发文趋势图 |
| RQ2 | 当前语料由哪些文献类型和来源期刊构成？ | 文献结构指标 | 文献类型分布图、来源期刊 Top15 图 |
| RQ3 | 哪些文献具有较高引用影响力？ | 引用影响指标 | 高被引文献 Top20 图 |
| RQ4 | 哪些预测方法在能源系统时序预测中最常见？ | 方法频次指标 | 方法频次分布图 |
| RQ5 | 哪些能源应用场景是当前研究热点？ | 应用场景指标 | 应用场景频次分布图 |
| RQ6 | 当前研究涉及哪些主要学科类别？ | 学科类别指标 | 学科类别 Top15 图 |
| RQ7 | 当前数据是否足以支撑后续知识图谱分析？ | 数据质量指标 | 指标汇总表 |
| RQ8 | 哪些文献可能成为 milestone 候选？ | 高被引 + 后续共被引指标 | 高被引文献表、后续 milestone 表 |

---

## 3. 当前数据口径

### 3.1 输入数据

| 参数 | 当前值 |
|---|---|
| 文件名 | `screened_final.csv` |
| 推荐路径 | `数据/processed/screened_final.csv` |
| 数据来源 | Web of Science |
| 数据格式 | CSV |
| 字段体系 | WoS 字段体系 |
| 当前记录数 | 443 |
| 当前字段数 | 37 |
| 当前年份范围 | 2017–2025 |
| 当前编码处理 | 自动尝试 `utf-8-sig`、`utf-8`、`gb18030`、`latin1` |

---

### 3.2 当前核心字段

| 字段 | 含义 | 当前用途 |
|---|---|---|
| `PY` | Publication Year，发表年份 | 年发文趋势 |
| `TI` | Title，题名 | 高被引文献标题、方法词匹配 |
| `SO` | Source Title，来源期刊 | 来源期刊分布 |
| `DT` | Document Type，文献类型 | 文献类型分布 |
| `AB` | Abstract，摘要 | 方法词、场景词匹配 |
| `AU` | Authors，作者缩写 | 后续作者合作分析 |
| `AF` | Author Full Name，作者全名 | 后续作者合作分析 |
| `DI` | DOI | DOI 完整率 |
| `TC` | Times Cited，被引次数 | 高被引文献排序 |
| `SC` | Subject Category，学科类别 | 学科类别分布 |
| `CR` | Cited References，被引参考文献 | 后续共被引分析 |
| `UT` | WoS Unique ID | 去重与溯源 |
| `DE` | Author Keywords，作者关键词 | 方法词与场景词匹配 |
| `ID` | Keywords Plus | 方法词与场景词匹配 |

---

## 4. 指标设计原则

### 4.1 可复现原则

所有指标必须满足：

1. 有明确输入字段；
2. 有明确计算逻辑；
3. 有明确输出文件；
4. 有明确脚本位置；
5. 有明确版本记录；
6. 能够被其他成员复查。

---

### 4.2 研究问题驱动原则

指标不单独存在，必须服务于研究问题。

例如：

- 年发文量用于回答研究热度变化；
- 方法频次用于回答方法谱系结构；
- 场景频次用于回答应用热点；
- 高被引文献用于形成 milestone 候选池；
- 学科类别用于说明交叉学科属性。

---

### 4.3 图谱兼容原则

当前指标属于基础指标，不替代 CiteSpace / VOSviewer 图谱分析。

当前指标需要为后续分析提供基础，包括：

1. 共被引分析；
2. 关键词共现分析；
3. 突现检测；
4. 时间线分析；
5. 作者合作网络；
6. 机构合作网络；
7. milestone 文献识别。

---

### 4.4 解释边界原则

所有指标必须明确解释边界：

1. 高频不等于重要；
2. 高被引不等于 milestone；
3. 发文量增长不等于技术成熟；
4. 字符串匹配不等于语义分类；
5. 描述性统计不等于知识结构分析。

---

## 5. 数据规模指标

### 5.1 总记录数

| 项目 | 内容 |
|---|---|
| 指标名称 | `total_records` |
| 中文名称 | 总记录数 |
| 输入字段 | 全表 |
| 计算公式 | `len(df)` |
| 当前用途 | 描述最终语料规模 |
| 输出文件 | `metrics_summary.csv` |
| 解释边界 | 仅表示最终筛选后记录数量，不代表研究影响力 |

---

### 5.2 字段数量

| 项目 | 内容 |
|---|---|
| 指标名称 | `total_fields` |
| 中文名称 | 字段数量 |
| 输入字段 | 全部列名 |
| 计算公式 | `len(df.columns)` |
| 当前用途 | 描述数据元信息丰富程度 |
| 输出文件 | `metrics_summary.csv` |
| 解释边界 | 字段数量多不代表字段质量高，需要结合完整率判断 |

---

### 5.3 年份范围

| 项目 | 内容 |
|---|---|
| 指标名称 | `year_range` |
| 中文名称 | 年份范围 |
| 输入字段 | `PY` |
| 计算公式 | `min(PY)` 与 `max(PY)` |
| 当前结果口径 | 2017–2025 |
| 输出文件 | `metrics_summary.csv` |
| 当前用途 | 判断是否具备时间趋势分析基础 |
| 解释边界 | 年份范围可支撑基础趋势图，但更细的阶段划分仍需结合图谱结果 |

---

## 6. 时间趋势指标

### 6.1 年发文量

| 项目 | 内容 |
|---|---|
| 指标名称 | `annual_publication_count` |
| 中文名称 | 年发文量 |
| 输入字段 | `PY` |
| 计算公式 | 按 `PY` 分组计数 |
| Python 逻辑 | `df["PY"].value_counts().sort_index()` |
| 输出图 | `annual_publication_trend.png` |
| 输出表 | `annual_publication_trend.csv` |
| 图中文名 | 年发文趋势图 |
| 研究用途 | 判断该领域整体研究热度变化 |
| 报告用途 | 支撑“能源系统时序预测研究快速发展”的背景描述 |
| 解释边界 | 发文量增长只能说明研究活跃度增加，不能直接说明技术成熟 |

---

### 6.2 年发文趋势变化

| 项目 | 内容 |
|---|---|
| 指标名称 | `annual_trend_pattern` |
| 中文名称 | 年发文趋势变化 |
| 输入字段 | `PY` |
| 计算逻辑 | 对年发文量序列观察增长、波动或下降 |
| 输出文件 | `annual_publication_trend.png` |
| 当前用途 | 为 timeline 和 burst 分析提供背景 |
| 解释边界 | 如果近一年下降，需要考虑数据库收录延迟，不可直接判断领域衰退 |

---

## 7. 文献结构指标

### 7.1 文献类型分布

| 项目 | 内容 |
|---|---|
| 指标名称 | `document_type_distribution` |
| 中文名称 | 文献类型分布 |
| 输入字段 | `DT` |
| 计算公式 | 按 `DT` 分组计数 |
| Python 逻辑 | `df["DT"].fillna("Unknown").value_counts()` |
| 输出图 | `document_type_distribution.png` |
| 输出表 | `document_type_distribution.csv` |
| 图中文名 | 文献类型分布图 |
| 研究用途 | 判断语料是以 Article、Review 还是其他类型为主 |
| 解释边界 | Review 比例高可能增强综述性，但也可能造成高被引偏差 |

---

### 7.2 来源期刊分布

| 项目 | 内容 |
|---|---|
| 指标名称 | `top_source_distribution` |
| 中文名称 | 来源期刊 Top15 分布 |
| 输入字段 | `SO` |
| 计算公式 | 按 `SO` 分组计数，取 Top15 |
| Python 逻辑 | `df["SO"].value_counts().head(15)` |
| 输出图 | `top_source_distribution.png` |
| 输出表 | `top_source_distribution.csv` |
| 图中文名 | 来源期刊 Top15 分布图 |
| 研究用途 | 判断研究主要发表在哪些期刊或出版源 |
| 解释边界 | 高产期刊不等于高影响力期刊，需要结合 TC、JCR 或学科分区另行判断 |

---

### 7.3 学科类别分布

| 项目 | 内容 |
|---|---|
| 指标名称 | `category_distribution` |
| 中文名称 | 学科类别 Top15 分布 |
| 输入字段 | `SC` |
| 计算公式 | 分号拆分后计数，取 Top15 |
| Python 逻辑 | `df["SC"].str.split(";").explode().value_counts().head(15)` |
| 输出图 | `category_distribution.png` |
| 输出表 | `category_distribution.csv` |
| 图中文名 | 学科类别 Top15 分布图 |
| 研究用途 | 判断能源系统时序预测的交叉学科属性 |
| 解释边界 | WoS 学科类别由数据库赋值，不能完全等同于论文真实研究内容 |

---

## 8. 引用影响指标

### 8.1 高被引文献 Top20

| 项目 | 内容 |
|---|---|
| 指标名称 | `top_cited_papers` |
| 中文名称 | 高被引文献 Top20 |
| 输入字段 | `TI` + `TC` |
| 计算公式 | 按 `TC` 降序排列，取 Top20 |
| Python 逻辑 | `df.sort_values("TC", ascending=False).head(20)` |
| 输出图 | `top_cited_papers.png` |
| 输出表 | `top_cited_papers.csv` |
| 图中文名 | 高被引文献 Top20 分布图 |
| 研究用途 | 形成 milestone 候选文献池 |
| 解释边界 | 高被引文献不一定是 milestone，后续必须结合 burst、centrality、sigma 和技术贡献判断 |

---

### 8.2 被引次数

| 项目 | 内容 |
|---|---|
| 指标名称 | `times_cited` |
| 中文名称 | 被引次数 |
| 输入字段 | `TC` |
| 字段来源 | WoS Times Cited |
| 当前用途 | 高被引排序 |
| 后续用途 | milestone 初筛 |
| 解释边界 | `TC` 是 WoS 内部被引统计，可能低估跨库引用 |

---

## 9. 方法演化指标

### 9.1 方法频次分布

| 项目 | 内容 |
|---|---|
| 指标名称 | `method_frequency_distribution` |
| 中文名称 | 方法频次分布 |
| 输入字段 | `TI`、`AB`、`DE`、`ID` |
| 计算方法 | 对标题、摘要和关键词进行规则匹配 |
| 输出图 | `method_frequency_distribution.png` |
| 输出表 | `method_frequency_distribution.csv` |
| 图中文名 | 方法频次分布图 |
| 研究用途 | 判断能源系统时序预测中主要方法的出现频次 |
| 解释边界 | 规则匹配存在漏检、误检，不能完全替代人工方法分类 |

---

### 9.2 方法词表

| 方法类别 | 匹配词 | 说明 |
|---|---|---|
| ARIMA | `ARIMA`、`SARIMA` | 统计预测方法 |
| SVR / SVM | `SVR`、`SVM`、`support vector` | 传统机器学习方法 |
| Random Forest | `random forest` | 集成学习方法 |
| XGBoost | `XGBoost`、`extreme gradient` | 梯度提升方法 |
| RNN | `RNN`、`recurrent neural` | 循环神经网络基础方法 |
| LSTM | `LSTM`、`long short-term memory`、`long short term memory` | 深度时序预测核心方法 |
| GRU | `GRU`、`gated recurrent` | 轻量循环神经网络方法 |
| BiLSTM | `BiLSTM`、`bidirectional LSTM` | 双向时序建模方法 |
| CNN-LSTM | `CNN-LSTM`、`CNN LSTM`、`convolutional LSTM` | 混合深度学习方法 |
| Attention | `attention` | 注意力机制 |
| Transformer | `transformer`、`TFT`、`temporal fusion transformer`、`Informer`、`Autoformer`、`PatchTST`、`iTransformer` | Transformer 系列方法 |
| Decomposition | `VMD`、`EMD`、`EEMD`、`CEEMDAN`、`decomposition` | 信号分解与混合预测方法 |

---

### 9.3 方法演化解释框架

当前项目采用以下方法演化路径作为解释框架：

| 阶段 | 方法特征 | 代表方法 |
|---|---|---|
| 第一阶段 | 统计预测 | ARIMA、SARIMA |
| 第二阶段 | 机器学习预测 | SVR、Random Forest、XGBoost |
| 第三阶段 | 循环神经网络预测 | RNN、LSTM、GRU、BiLSTM |
| 第四阶段 | 混合深度学习预测 | CNN-LSTM、Attention-LSTM、Decomposition-LSTM |
| 第五阶段 | Transformer 预测 | TFT、Informer、PatchTST、iTransformer |

该框架仅作为解释模型，最终阶段划分仍需结合年发文趋势、关键词时间线、突现词和共被引聚类共同验证。

---

## 10. 应用场景指标

### 10.1 应用场景频次分布

| 项目 | 内容 |
|---|---|
| 指标名称 | `scenario_frequency_distribution` |
| 中文名称 | 应用场景频次分布 |
| 输入字段 | `TI`、`AB`、`DE`、`ID` |
| 计算方法 | 对标题、摘要和关键词进行规则匹配 |
| 输出图 | `scenario_frequency_distribution.png` |
| 输出表 | `scenario_frequency_distribution.csv` |
| 图中文名 | 应用场景频次分布图 |
| 研究用途 | 判断能源系统时序预测的主要应用场景 |
| 解释边界 | 场景词匹配不能完全代表论文应用对象，后续需要人工复核典型文献 |

---

### 10.2 应用场景词表

| 场景类别 | 匹配词 | 说明 |
|---|---|---|
| Smart Grid | `smart grid` | 智能电网场景 |
| Microgrid | `microgrid`、`micro-grid` | 微电网场景 |
| Renewable Energy | `renewable`、`wind power`、`solar`、`photovoltaic`、`PV` | 新能源预测场景 |
| Integrated Energy Systems | `integrated energy`、`multi-energy` | 综合能源系统 |
| Demand Response | `demand response` | 需求响应场景 |
| Electricity Load | `electricity load`、`load forecasting`、`power load` | 电力负荷预测 |
| Energy Demand | `energy demand`、`demand forecasting` | 能源需求预测 |
| Building Energy | `building`、`building energy` | 建筑能源场景 |

---

## 11. 数据质量指标

### 11.1 元数据完整率

| 指标名称 | 中文名称 | 输入字段 | 计算公式 | 输出文件 |
|---|---|---|---|---|
| `title_complete_rate` | 题名完整率 | `TI` | 非空 `TI` 数 / 总记录数 × 100% | `metrics_summary.csv` |
| `author_complete_rate` | 作者完整率 | `AU` / `AF` | 非空作者字段数 / 总记录数 × 100% | `metrics_summary.csv` |
| `doi_complete_rate` | DOI 完整率 | `DI` | 非空 `DI` 数 / 总记录数 × 100% | `metrics_summary.csv` |
| `abstract_complete_rate` | 摘要完整率 | `AB` | 非空 `AB` 数 / 总记录数 × 100% | `metrics_summary.csv` |
| `year_complete_rate` | 年份完整率 | `PY` | 非空 `PY` 数 / 总记录数 × 100% | `metrics_summary.csv` |

---

### 11.2 数据质量解释规则

1. 题名和年份是最低必要字段；
2. 摘要完整率影响方法频次和场景频次统计；
3. DOI 完整率影响去重和外部链接匹配；
4. 作者完整率影响后续合作网络分析；
5. `CR` 字段完整性影响后续共被引分析，但当前指标可视化阶段暂不直接计算。

---

## 12. 当前输出文件清单

| 序号 | 文件名 | 中文名称 | 类型 | 对应指标 |
|---|---|---|---|---|
| 1 | `annual_publication_trend.png` | 年发文趋势图 | PNG | 年发文量 |
| 2 | `annual_publication_trend.csv` | 年发文趋势数据表 | CSV | 年发文量 |
| 3 | `document_type_distribution.png` | 文献类型分布图 | PNG | 文献类型分布 |
| 4 | `document_type_distribution.csv` | 文献类型分布数据表 | CSV | 文献类型分布 |
| 5 | `top_source_distribution.png` | 来源期刊 Top15 分布图 | PNG | 来源期刊分布 |
| 6 | `top_source_distribution.csv` | 来源期刊 Top15 数据表 | CSV | 来源期刊分布 |
| 7 | `top_cited_papers.png` | 高被引文献 Top20 分布图 | PNG | 高被引文献 |
| 8 | `top_cited_papers.csv` | 高被引文献 Top20 数据表 | CSV | 高被引文献 |
| 9 | `method_frequency_distribution.png` | 方法频次分布图 | PNG | 方法频次 |
| 10 | `method_frequency_distribution.csv` | 方法频次分布数据表 | CSV | 方法频次 |
| 11 | `scenario_frequency_distribution.png` | 应用场景频次分布图 | PNG | 应用场景频次 |
| 12 | `scenario_frequency_distribution.csv` | 应用场景频次分布数据表 | CSV | 应用场景频次 |
| 13 | `category_distribution.png` | 学科类别 Top15 分布图 | PNG | 学科类别 |
| 14 | `category_distribution.csv` | 学科类别 Top15 数据表 | CSV | 学科类别 |
| 15 | `metrics_summary.csv` | 指标汇总表 | CSV | 数据规模与完整率 |
| 16 | `README_metrics_outputs.md` | 指标可视化结果说明文档 | Markdown | 输出说明 |

---

## 13. 与后续知识图谱分析的接口

### 13.1 共被引分析接口

| 当前指标 | 后续用途 |
|---|---|
| 高被引文献 Top20 | milestone 候选池 |
| `CR` 字段 | 构建共被引网络 |
| 年份范围 2017–2025 | 时间切片设置 |
| 学科类别分布 | 解释跨学科知识基础 |

---

### 13.2 突现分析接口

| 当前指标 | 后续用途 |
|---|---|
| 方法频次分布 | 识别潜在突现方法 |
| 应用场景频次分布 | 识别潜在突现场景 |
| 年发文趋势 | 判断突现年份是否处于研究扩张期 |

---

### 13.3 时间线分析接口

| 当前指标 | 后续用途 |
|---|---|
| 年发文趋势 | 提供背景时间轴 |
| 方法频次分布 | 支撑方法演化路线 |
| 学科类别分布 | 解释学科扩展过程 |

---

### 13.4 milestone 分析接口

最终 milestone 文献不只依据高被引排序，而应综合：

1. WoS 被引次数 `TC`；
2. CiteSpace burst strength；
3. betweenness centrality；
4. sigma；
5. 共被引聚类位置；
6. 文献的实际技术贡献。

---

## 14. 当前指标体系局限

1. 当前方法频次统计依赖字符串匹配，不能完全覆盖同义词和缩写变体；
2. 场景频次统计也依赖规则匹配，无法完全替代人工分类；
3. 高被引排序基于 WoS `TC` 字段，可能低估其他数据库中的引用；
4. 当前指标图属于基础统计，不等同于知识图谱；
5. 当前指标体系尚未包含 CiteSpace 的 modularity、silhouette、burst、centrality 和 sigma；
6. 后续如果合并 CNKI 数据，需要重新定义中英文字段统一规则；
7. 当前输出文件名保留英文，中文名称通过文档映射说明。

---

## 15. 版本记录与执行日志

### v1.0：LSTM-only 指标体系版本

| 项目 | 内容 |
|---|---|
| 主题 | 基于 LSTM 的电力负荷预测 |
| 主要指标 | 数据规模、数据质量、筛选保留率、引用网络密度 |
| 局限 | 方法范围过窄，难以支撑长期演化分析 |
| 状态 | 已弃用，仅作历史记录 |

---

### v2.0：能源系统时序预测指标体系版本

| 项目 | 内容 |
|---|---|
| 更新时间 | 选题重构阶段 |
| 主题变化 | 从 LSTM 电力负荷预测扩展为能源系统时序预测方法 |
| 新增指标 | 方法演化指标、场景频次指标、Transformer 相关指标 |
| 目的 | 支撑“从 LSTM 到 Transformer”的方法演化叙事 |
| 状态 | 已被 v2.1 细化 |

---

### v2.1：Lesson6 指标可视化版本

| 项目 | 内容 |
|---|---|
| 更新时间 | 2026-05-08 |
| 更新成员 | A |
| 输入数据 | `screened_final.csv` |
| 数据规模 | 443 条记录 |
| 字段数量 | 37 个字段 |
| 实际年份范围 | 2017–2025 |
| 字段体系 | WoS 字段体系 |
| 输出目录 | `输出/metrics/` |
| 核心产出 | 7 张 PNG 图 + 8 个 CSV 表 + 指标汇总表 + README 说明文件 |
| 当前状态 | 当前生效 |

#### v2.1 具体更新内容

1. 将字段口径从中文字段切换为 WoS 字段；
2. 将年份字段设定为 `PY`；
3. 将标题字段设定为 `TI`；
4. 将来源期刊字段设定为 `SO`；
5. 将文献类型字段设定为 `DT`；
6. 将摘要字段设定为 `AB`；
7. 将被引次数字段设定为 `TC`；
8. 将学科类别字段设定为 `SC`；
9. 新增年发文趋势指标；
10. 新增来源期刊 Top15 指标；
11. 新增文献类型分布指标；
12. 新增高被引文献 Top20 指标；
13. 新增方法频次分布指标；
14. 新增应用场景频次分布指标；
15. 新增学科类别 Top15 指标；
16. 新增指标汇总表；
17. 明确所有输出文件的中文名称；
18. 明确所有指标的解释边界；
19. 明确与后续共被引、突现、时间线和 milestone 分析的接口。

---

## 16. 后续更新计划

| 触发事件 | 建议版本号 | 更新内容 |
|---|---|---|
| 新增 CiteSpace 共被引网络指标 | v2.2 | 增加 modularity Q、silhouette、聚类标签、代表文献 |
| 新增 burst detection 结果 | v2.3 | 增加 burst strength、begin、end、ongoing 状态 |
| 新增 timeline view 结果 | v2.4 | 增加主题演化阶段与聚类平均年份 |
| 新增 milestone 候选表 | v2.5 | 增加 TC、burst、centrality、sigma、技术贡献 |
| 形成 M2 版 3 图 1 表 | v3.0 | 整合基础指标和知识图谱指标 |

---

## 17. 使用说明

使用本文件时，建议按以下顺序阅读：

1. 先看第 2–3 节，确认研究问题与数据口径；
2. 再看第 5–11 节，确认每类指标定义、字段和输出文件；
3. 然后看第 12–13 节，确认当前输出和后续图谱接口；
4. 最后看第 15–16 节，确认版本日志和后续更新计划。

当前正式指标口径为 **v2.1**。旧版 LSTM-only 指标体系仅作历史记录，不作为当前正式分析依据。
