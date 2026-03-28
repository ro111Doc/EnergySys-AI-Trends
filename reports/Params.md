# Params.md

## 文件说明
本文件用于集中记录本项目在**检索、字段映射、数据清洗、去重、筛选、合并与后续分析**过程中的关键参数设置。  
其作用包括：

1. 统一项目执行口径；
2. 明确每一步操作依据；
3. 保证后续结果可解释、可追溯、可复现；
4. 为 `query.yaml`、`clean_rules.md`、`field_dictionary.md`、`screening_rule.md`、`data_quality.md` 提供参数层面的汇总说明。

本文件不是原始检索式全文，也不是最终论文方法部分，而是整个项目的**参数总表**。

---

## 一、项目基础参数

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

### 1.6 文件放置位置
- 推荐路径：`reports/Params.md`

说明：当前参数文件只对**已实际检索数据库**做正式记录；其他数据库仅保留扩展位，不视为当前正式数据来源。

---

## 二、检索参数（Search Parameters）

### 2.1 总体检索逻辑
当前统一检索逻辑为：

**方法词 AND 任务词 AND 场景词 NOT 排除词**

四层含义如下：
- 方法词：限定 LSTM 及其代表性改进模型；
- 任务词：限定电力负荷预测任务；
- 场景词：限定电力系统相关应用场景；
- 排除词：剔除明显跨领域干扰项。

---

### 2.2 方法词参数（Method Terms）

#### 中文方法词
- LSTM
- 长短期记忆网络
- 长短时记忆网络
- 双向长短期记忆网络
- BiLSTM
- 注意力机制LSTM

#### 英文方法词
- LSTM
- long short-term memory
- long short term memory
- BiLSTM
- bidirectional LSTM
- attention LSTM

#### 方法词参数说明
- 当前策略以“经典 LSTM + 常见变体”为主；
- 暂不无限扩展到所有混合模型写法，避免噪声过多；
- 若后续正式分析发现漏检明显，可增加：
  - hybrid LSTM
  - CNN-LSTM
  - GRU-LSTM
  - encoder-decoder LSTM

---

### 2.3 任务词参数（Task Terms）

#### 中文任务词
- 电力负荷预测
- 负荷预测
- 短期负荷预测
- 电力需求预测

#### 英文任务词
- load forecasting
- load prediction
- electric load forecasting
- power load forecasting
- electricity demand forecasting
- short-term load forecasting
- STLF

#### 任务词参数说明
- 当前任务词偏向“负荷预测”主任务；
- 暂不主动把“功率预测”“能耗预测”“电价预测”纳入主任务；
- 若某文献为“综合能源系统”但其中负荷预测只是附带模块，则倾向排除。

---

### 2.4 场景词参数（Context Terms）

#### 中文场景词
- 电力系统
- 智能电网
- 电网
- 配电网

#### 英文场景词
- power system
- power systems
- smart grid
- power grid
- distribution network

#### 场景词参数说明
- 当前场景词用于提高精确率；
- 场景词不应扩展得过于宽泛，否则会混入建筑能耗、医院能源系统、家庭能源管理等边缘主题；
- 若检索结果明显过少，可适度放宽场景限制。

---

### 2.5 排除词参数（Exclusion Terms）

#### 中文排除词
- 交通流预测
- 网络流量预测
- 服务器负载预测
- CPU负载预测
- 桥梁荷载预测

#### 英文排除词
- traffic flow forecasting
- network traffic forecasting
- server workload prediction
- CPU load prediction
- bridge load prediction

#### 排除词参数说明
- 当前排除词只用于排除明显跨领域文献；
- 不对“微电网”“综合能源系统”“建筑负荷”等边界主题直接使用排除词，而是放到筛选阶段处理；
- 原则：**排除词要少而准**。

---

### 2.6 时间参数
- 年份范围：2015–2025
- CNKI 执行方式：年份筛选 / 专业检索时间字段
- WoS 执行方式：`PY=(2015-2025)` 或等价年份过滤

#### 时间参数说明
- 2015–2025 是当前正式研究窗口；
- 若出现 2025 年 Early Access 文献，可保留，但需在年份与正式发表状态上单独标记。

---

### 2.7 检索字段参数

#### CNKI
- 当前优先字段：`TKA`
- 含义：篇名 + 关键词 + 摘要（篇关摘）

#### WoS
- 当前优先字段：`TS`
- 含义：主题检索（标题、摘要、关键词等相关字段）

#### 检索字段参数说明
- CNKI 当前主策略为 `TKA`，兼顾召回与精确；
- WoS 当前主策略为 `TS`，适合形成英文主题检索集合；
- 当前不以题名限定为主，否则会漏掉大量相关文献。

---

### 2.8 当前检索版本参数
- 当前记录版本：V0.2
- 版本状态：已执行
- 已记录位置：
  - `config/query.yaml`
  - `reports/query_changelog.md`
  - `reports/query_rationale.md`

---

## 三、数据源参数（Database Parameters）

### 3.1 CNKI 参数
- 数据源名称：CNKI
- 当前记录类型：
  - 期刊
  - 硕士
  - 外文期刊
  - 会议（若后续出现）
- 当前导出字段：
  - `SrcDatabase-来源库`
  - `Title-题名`
  - `Author-作者`
  - `Organ-单位`
  - `Source-文献来源`
  - `Summary-摘要`
  - `PubTime-发表时间`
  - `Year-年`
  - `Fund-基金`（部分）
  - `DOI-DOI`（部分）

#### CNKI 参数说明
- 当前 CNKI 是中文检索主来源；
- 部分结果中混有“外文期刊”记录，但仍按 CNKI 数据源处理；
- 摘要字段已较前期版本更完整，适合进入初筛阶段。

---

### 3.2 WoS 参数
- 数据源名称：Web of Science
- 当前主要标签字段：
  - `PT`
  - `AU`
  - `AF`
  - `TI`
  - `SO`
  - `DT`
  - `AB`
  - `C1`
  - `C3`
  - `RP`
  - `EM`
  - `FU`
  - `FX`
  - `CR`
  - `TC`
  - `Z9`
  - `PY`
  - `DI`
  - `UT`
  - `DA`

#### WoS 参数说明
- WoS 当前是英文检索主来源；
- `UT` 为唯一标识，必须保留；
- `CR`、`TC`、`DI` 是 WoS 相对高价值字段；
- `AB` 和 `TI` 为初筛核心字段。

---

## 四、字段映射参数（Field Mapping Parameters）

### 4.1 统一字段体系
后续统一表建议映射为以下字段：

- `database`
- `source_type`
- `title`
- `authors`
- `authors_full`
- `affiliations`
- `source`
- `document_type`
- `abstract`
- `year`
- `pub_time`
- `fund`
- `doi`
- `references`
- `cited_times`
- `unique_id`
- `language`
- `source_file`
- `keep`
- `exclude_reason`
- `note`
- `screen_stage`

---

### 4.2 CNKI 映射参数
- `SrcDatabase-来源库` → `source_type`
- `Title-题名` → `title`
- `Author-作者` → `authors`
- `Organ-单位` → `affiliations`
- `Source-文献来源` → `source`
- `Summary-摘要` → `abstract`
- `PubTime-发表时间` → `pub_time`
- `Year-年` → `year`
- `Fund-基金` → `fund`
- `DOI-DOI` → `doi`

---

### 4.3 WoS 映射参数
- `AU` → `authors`
- `AF` → `authors_full`
- `TI` → `title`
- `SO` → `source`
- `DT` → `document_type`
- `AB` → `abstract`
- `C1` → `affiliations`
- `C3` → `organizations`
- `FU` → `fund`
- `CR` → `references`
- `TC` → `cited_times`
- `PY` → `year`
- `DI` → `doi`
- `UT` → `unique_id`

---

## 五、文本清洗参数（Cleaning Parameters）

### 5.1 通用清洗参数
- 删除首尾空格：是
- 删除连续空格：是
- 保留原始大小写：是
- DOI 大小写统一：建议统一为小写
- 空值填充：不强制填充，保留空白
- 作者分隔符标准化：统一使用分号 `;`
- 原始字段保留：是

---

### 5.2 CNKI 清洗参数
- 来源库简写：
  - 外文期刊 → 英刊
  - 期刊 → 期刊
  - 硕士 → 硕论
  - 博士 → 博论
  - 会议 → 会议
- 年份来源优先级：
  1. `Year`
  2. `PubTime` 提取
- 单位字段处理：先整体保留，不拆分
- 题名清洗：仅做空格与符号规范，不改词义

---

### 5.3 WoS 清洗参数
- 必保留 `UT`：是
- 必保留 `CR`：是
- 作者优先字段：
  1. `AF`
  2. `AU`
- 机构优先字段：
  1. `C3`（若需机构标准化）
  2. `C1`
- 被引优先保留：
  - `TC`
  - `Z9`、
## 六、去重参数（Deduplication Parameters）

### 6.1 去重优先级
1. `doi` 完全一致
2. `title + year` 高一致
3. 标题仅有大小写、空格、标点差异
4. 相同 `UT`（WoS 内部）

### 6.2 重复保留规则
若同一文献在多个数据库重复出现：
1. 优先保留字段更完整版本；
2. 若 WoS 版本含 `UT`、`CR`、`TC`，通常优先保留 WoS；
3. 若 CNKI 摘要更完整，可将摘要补入统一表，但需保留来源记录；
4. 原始数据源字段不得删除。

### 6.3 不视为重复的情况
- 学位论文与后续期刊论文
- 会议版与正式发表版
- 同主题但 DOI、标题、作者不同的改进研究

---

## 七、筛选参数（Screening Parameters）

### 7.1 当前筛选阶段
- 当前阶段：初筛前 / 初筛准备阶段
- 当前判断依据：题名 + 摘要 + 来源字段

### 7.2 纳入参数
文献原则上需同时满足：
1. 主题核心为电力负荷预测或电力需求预测；
2. 方法核心明确涉及 LSTM 或其变体；
3. 场景属于电力系统、电网、智能电网、配电网等；
4. 可为后续热点分析或方法演化分析提供有效证据。

### 7.3 排除参数
初筛阶段优先排除：
1. 交通流、网络流量、服务器负载等跨领域文献；
2. 仅附带预测模块，但主体并非电力负荷预测的文献；
3. 以调度优化、需求响应、建筑能耗管理、医院能源管理、P2P 家庭能源交易为主，且负荷预测不是研究核心的文献；
4. 主题严重偏离电力系统语境的文献。

### 7.4 边界文献参数
对于边界样本：
- `keep = maybe`
- `exclude_reason = 边界文献`
- `note = 待二次人工判断`

### 7.5 建议新增筛选字段
- `keep`
- `exclude_reason`
- `note`
- `screen_stage`
- `database`
- `source_file`

---

## 八、数据合并参数（Merge Parameters）

### 8.1 合并前提
只有在满足以下条件时，才允许合并 CNKI 与 WoS：
1. 两库已分别完成基础清洗；
2. 已完成字段映射；
3. 已完成初步去重；
4. 已增加 `database` 与 `source_file` 字段。

### 8.2 合并策略
- 合并方式：纵向拼接
- 合并主键：优先使用 `doi`
- 辅助比对键：
  - `title`
  - `year`
  - `authors`

### 8.3 合并后要求
- 保留来源标识：必须
- 保留原始数据源信息：必须
- 不得覆盖原始字段：必须

### 8.4 合并后检查项
- 记录总数
- DOI 重复数
- 标题重复数
- 缺失摘要数
- 缺失 DOI 数
- 来源库分布

---

## 九、输出参数（Output Parameters）

### 9.1 原始数据目录
- `data/raw/`

### 9.2 中间清洗数据目录
- `data/interim/`

### 9.3 最终处理数据目录
- `data/processed/`

### 9.4 文档目录
以下文件统一放入 `reports/`：
- `query_changelog.md`
- `query_rationale.md`
- `clean_rules.md`
- `Params.md`
- `data_quality.md`
- `screening_rule.md`

### 9.5 主说明文件
- `README.md` 放仓库根目录

---

## 十、质量控制参数（Quality Control Parameters）

### 10.1 基础质量检查项
- 题名是否缺失
- 作者是否缺失
- 摘要是否缺失
- DOI 是否缺失
- 年份是否缺失
- 是否存在明显重复记录

### 10.2 当前建议阈值
- 题名缺失率：应为 0
- 年份缺失率：应尽量接近 0
- 摘要缺失率：允许存在，但需单独记录
- DOI 缺失率：允许存在，不作为强制剔除条件
- 重复记录：正式分析前应尽量清零

### 10.3 异常记录处理方式
- 不直接删除；
- 先标注 `note`；
- 再进入人工复核；
- 复核结论写入 `processed` 或筛选记录表。

---

## 十一、后续分析参数（Analysis Parameters）

### 11.1 当前状态说明
正式文献计量分析参数尚未最终锁定，因此以下内容为**预设分析参数**，仅作项目规划依据。

### 11.2 发文趋势分析参数
- 统计字段：`year`
- 统计单位：篇
- 输出形式：年度折线图 / 柱状图

### 11.3 作者分析参数
- 统计字段：`authors`
- 处理方式：作者拆分后计数
- 输出形式：高产作者表、合作网络图

### 11.4 机构分析参数
- 统计字段：`affiliations`
- 输出形式：高产机构表、机构合作图

### 11.5 关键词与主题分析参数
前提条件：
- 必须补齐或稳定获得关键词字段，或从摘要中提取辅助词

当前状态：
- CNKI / WoS 当前摘要字段较可用
- 关键词字段仍需后续补充

### 11.6 引文分析参数
适用数据源：
- 优先 WoS

依赖字段：
- `CR`
- `TC`
- `DI`
- `UT`

---

## 十二、版本管理参数（Versioning Parameters）

### 12.1 当前版本
- 参数文件版本：v0.1
- 状态：当前生效

### 12.2 参数更新触发条件
以下情况必须更新 `Params.md`：
1. 检索式结构发生改变；
2. 新增数据库；
3. 字段体系改变；
4. 去重规则改变；
5. 筛选规则改变；
6. 分析工具或分析口径改变。

### 12.3 联动更新文件
参数更新后，原则上同步检查以下文件：
- `README.md`
- `query.yaml`
- `query_changelog.md`
- `field_dictionary.md`
- `clean_rules.md`
- `screening_rule.md`
- `data_quality.md`

---

## 十三、参数使用说明

### 13.1 使用顺序
建议按以下顺序使用本文件中的参数：
1. 先读项目基础参数与检索参数；
2. 再读数据源参数与字段映射参数；
3. 然后按清洗参数处理原始数据；
4. 再按去重参数、筛选参数完成中间表整理；
5. 最后依据质量控制参数和分析参数进入正式分析阶段。

### 13.2 使用边界
- 本文件用于规范项目过程；
- 不直接替代 `query.yaml`；
- 不直接替代 `field_dictionary.md`；
- 不直接替代 `clean_rules.md`；
- 但上述文件中的关键设置，应与本文件保持一致。

### 13.3 当前适用范围
- 适用于当前阶段的 CNKI 与 WoS 双数据源处理；
- 适用于检索、清洗、去重、筛选、合并的全过程；
- 后续如新增数据库，必须扩展本文件对应部分。

---

## 十四、版本记录

### v0.1
- 建立项目参数总表；
- 覆盖检索、字段映射、清洗、去重、筛选、合并、输出、质量控制与分析预设参数；
- 与当前 `README.md`、`field_dictionary.md`、`clean_rules.md` 保持一致。
