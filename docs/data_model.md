# 图数据模型文档（docs/data model.md）
## 文档说明
本文档基于 Lesson 5 图数据模型要求，定义适用于微电网优化调度与电力负荷预测领域的文献计量分析图模型，包含节点、边、属性及关系规则，所有定义均依托项目现有数据文件，确保模型可复现、可落地。

## 1. 数据基础说明
### 1.1 数据来源
- 核心数据文件：`data/merged_with_citations.csv`（整合 CNKI 与 WoS 文献及引文数据）
- 字段定义依据：`data/field_dictionary.md`（统一字段映射标准）
- 数据背景支撑：`data/README.md`（数据源、导出时间、检索主题说明）
- 检索范围约束：`config/query.yaml`（研究领域、时间窗、字段限定规则）

### 1.2 数据规模
- 文献记录总数：156 条（CNKI 128 条 + WoS 28 条）
- 引文关系总数：189 条（含文献间互引、自引关系）
- 核心实体类型：文献、作者、机构、关键词、学科类别、基金项目

## 2. 图模型核心组件定义
### 2.1 节点类型（Node Type）
| 节点类型       | 标识（Label） | 核心属性（基于 field_dictionary.md）                                                                 | 数据来源字段                | 示例值                                                                 |
|----------------|---------------|------------------------------------------------------------------------------------------------------|-----------------------------|------------------------------------------------------------------------|
| 文献           | Paper         | paper_id（唯一标识）、title（题名）、year（发表年份）、doi（数字对象标识）、document_type（文献类型）、database（来源库） | doi + database              | paper_id: "10.3390/SU172411158_CNKI"；title: "考虑共享储能与综合需求响应协同的多区域风光微电网优化调度研究" |
| 作者           | Author        | author_id（唯一标识）、name（作者名）、name_full（作者全名）                                           | authors + authors_full      | author_id: "Liu_HX"；name: "Liu, HX"；name_full: "Liu Hongxin"          |
| 机构           | Institution   | inst_id（唯一标识）、name（机构名称）、country（所属国家/地区）                                       | affiliations                | inst_id: "Hunan_Univ"；name: "Hunan University"；country: "China"       |
| 关键词         | Keyword       | keyword_id（唯一标识）、term（关键词术语）、source（关键词来源：受控词/自由词）                        | keywords                    | keyword_id: "Microgrid_Optimization"；term: "微电网优化调度"；source: "自由词" |
| 学科类别       | Subject       | subject_id（唯一标识）、category（学科类别名称）                                                       | subject_category            | subject_id: "Electrical_Engineering"；category: "电气工程"               |
| 基金项目       | Fund          | fund_id（唯一标识）、name（基金名称）、grant_number（基金编号）                                         | fund                        | fund_id: "SGSHPD00ZSJS2413049"；name: "国网上海市电力公司科技项目"；grant_number: "SGSHPD00ZSJS2413049" |

### 2.2 边类型（Relationship Type）
| 边类型               | 标识（Label）       | 起点节点 | 终点节点 | 核心属性                | 关系说明                                                                 |
|----------------------|---------------------|----------|----------|-------------------------|--------------------------------------------------------------------------|
| 作者-发表-文献       | PUBLISHED           | Author   | Paper    | publish_year（发表年份） | 记录作者与所发表文献的关联，含多位作者共同发表场景                        |
| 作者-隶属-机构       | AFFILIATED_WITH     | Author   | Institution | affiliation_type（隶属类型） | 记录作者与所属机构的关联，支持同一作者隶属多个机构                        |
| 文献-包含-关键词     | CONTAINS_KEYWORD    | Paper    | Keyword  | keyword_weight（权重）  | 记录文献的关键词关联，权重可基于关键词出现频次计算                        |
| 文献-属于-学科       | BELONGS_TO_SUBJECT  | Paper    | Subject  | relevance（相关度）     | 记录文献所属学科类别，WoS 数据直接映射，CNKI 数据基于关键词推导            |
| 文献-受资助-基金     | FUNDED_BY           | Paper    | Fund     | funding_role（资助角色） | 记录文献的基金资助关系，含多个基金联合资助场景                            |
| 文献-引用-文献       | CITES               | Paper    | Paper    | cite_year（引用年份）   | 记录文献间的引文关系，基于 merged_with_citations.csv 中的 citing_paper 与 cited_paper 字段 |
| 机构-合作-机构       | COOPERATED_WITH     | Institution | Institution |合作次数（coop_count） | 记录不同机构通过共同发表文献形成的合作关系，合作次数按联合发文量统计        |

### 2.3 节点唯一标识规则
| 节点类型       | 唯一标识生成规则                                                                 | 说明                                                                 |
|----------------|----------------------------------------------------------------------------------|----------------------------------------------------------------------|
| Paper          | 采用「DOI + 来源库」组合（如 "10.3390/SU172411158_CNKI"）；无 DOI 文献用「标题+作者」哈希 | 确保跨库文献唯一区分，避免 DOI 缺失导致的重复节点                        |
| Author         | 采用「姓名标准化缩写」（姓全拼+名首字母，如 "Liu_HX"）                            | 统一 CNKI 与 WoS 作者名格式，减少同名作者重复节点                        |
| Institution    | 采用「机构标准化名称」哈希（如 "Hunan_University" 对应 "Hunan_Univ"）              | 处理机构名称不同写法（如“湖南大学”与“Hunan University”）的消歧问题        |
| Keyword        | 采用「关键词术语」哈希（如 "微电网优化调度" 对应 "Microgrid_Optimization"）        | 统一中英文关键词表述，避免同义关键词重复节点                            |
| Subject        | 采用「学科类别名称」哈希（如“电气工程”对应 "Electrical_Engineering"）               | 基于 WoS 学科分类标准统一命名，确保学科节点一致性                        |
| Fund           | 采用「基金编号+基金名称」组合哈希（如 "SGSHPD00ZSJS2413049_国网上海电力科技项目"） | 确保不同基金项目唯一区分，支持无编号基金的唯一标识                        |

## 3. 数据映射与处理规则
### 3.1 字段映射关系（关联 field_dictionary.md）
| 图模型组件       | 对应统一字段名       | 原始数据字段（CNKI/WoS）                          | 处理规则                                                                 |
|------------------|----------------------|---------------------------------------------------|--------------------------------------------------------------------------|
| Paper.title      | title                | CNKI.Title / WoS.TI                               | 保留原始标题，去除特殊字符，统一编码为 UTF-8                              |
| Paper.year       | year                 | CNKI.Year / WoS.PY                                | 统一为 4 位整数格式，过滤异常年份值                                      |
| Author.name      | authors              | CNKI.Author（分号分隔）/ WoS.AU（逗号分隔）        | 拆分多作者，标准化姓名格式（姓全拼+名首字母）                            |
| Institution.name | affiliations         | CNKI.Organ / WoS.C1/C3                            | 拆分多机构，标准化机构名称（统一中英文、去除冗余后缀）                    |
| Keyword.term     | keywords             | CNKI.Keywords / WoS.Keywords                      | 拆分多关键词，统一中英文表述，去除同义重复                                |
| Paper.cites      | references           | WoS.CR / CNKI.参考文献（无）                       | 仅基于 WoS 参考文献字段构建引文关系，CNKI 文献引文关系标注为“无”          |

### 3.2 数据清洗适配规则
1. 缺失值处理：
   - 核心属性缺失（如 Paper.title、Author.name）的记录直接排除；
   - 非核心属性缺失（如 Fund.grant_number）标注为 "N/A"，保留节点关联；
   - CNKI 无 references 字段，对应 Paper 节点的 CITES 边标注为“无可用数据”。

2. 重复数据处理：
   - 完全重复节点（标识规则一致）直接合并，保留属性最完整的记录；
   - 疑似重复节点（如名称相似的机构）添加“疑似重复”标签，保留原始数据供人工核查。

3. 格式标准化：
   - 日期格式：统一为“YYYY”（年份）、“YYYY-MM-DD”（发表时间）；
   - 文本格式：去除换行符、特殊符号，统一大小写（英文关键词首字母大写）。

## 4. 图模型应用场景
| 应用场景                | 所需节点-边组合                                                                 | 数据限制说明                                                                 |
|-------------------------|--------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| 作者合作网络分析        | Author + PUBLISHED + Paper + AFFILIATED_WITH + Institution + COOPERATED_WITH    | 需先标准化作者名和机构名称，避免同名/同机构不同写法导致的分析偏差            |
| 关键词共现分析          | Paper + CONTAINS_KEYWORD + Keyword                                              | 基于文献关键词关联推导共现关系，权重按共同出现频次计算                      |
| 引文网络分析            | Paper + CITES + Paper                                                          | 仅支持 WoS 文献间的共被引/引文耦合分析，CNKI 文献无参考文献数据无法参与      |
| 机构合作趋势分析        | Institution + COOPERATED_WITH + Institution + Paper + PUBLISHED + Author        | 合作次数按联合发文量统计，时间趋势基于 Paper.publish_year 字段                |
| 基金资助分布分析        | Fund + FUNDED_BY + Paper + Author + Institution                                | 支持统计不同基金的资助发文量、资助机构分布等维度                            |

## 5. 模型版本与依赖说明
### 5.1 模型版本
- 版本号：v1.0
- 生成时间：2026-03-28
- 适配课程：文献计量学 Lesson 5 图数据模型要求

### 5.2 依赖文件清单
| 依赖文件路径                | 用途                                  | 必选程度 |
|-----------------------------|---------------------------------------|----------|
| data/merged_with_citations.csv | 提供节点、边的原始数据支撑            | 必选     |
| data/field_dictionary.md     | 定义字段映射规则，确保属性一致性      | 必选     |
| data/README.md               | 补充数据背景，支撑模型可复现性        | 必选     |
| config/query.yaml            | 明确检索范围，限定模型应用边界        | 必选     |
| reports/data_quality.md      | 参考数据质量问题，调整模型适配策略    | 可选     |
| reports/query_rationale.md   | 关联检索式设计逻辑，解释模型合理性    | 可选     |

### 5.3 后续优化方向
1. 补充 CNKI 文献的参考文献数据，完善引文网络的完整性；
2. 引入作者消歧算法（如基于机构、研究方向的联合消歧），提升 Author 节点准确性；
3. 增加关键词权重计算模型（如 TF-IDF），优化 CONTAINS_KEYWORD 边的属性维度。


# 更新：
## 1. 数据来源与范围
- 数据源：Web of Science 核心合集
- 主题：**LSTM 在电力负荷预测中的应用（2015–2025）**
- 筛选版本：D 复筛最终纳入文献
- 文件：`included_final.csv`

## 2. 实体节点（Node）
1. **Paper（论文）**
   - 字段：DOI、标题(TI)、摘要(AB)、作者(AU)、年份(PY)、期刊(SO)、文献类型(DT)、关键词(KW)、WOS编号(UT)
2. **Author（作者）**
   - 字段：作者全称、通讯作者标识、机构、国家/地区
3. **Institution（机构）**
   - 字段：机构名称、国家、发文量
4. **Keyword（关键词）**
   - 字段：关键词文本、出现频次、年份分布
5. **Journal（期刊）**
   - 字段：期刊名、学科分类、发表年份区间
6. **Model（模型）**
   - 字段：LSTM、BiLSTM、CNN-LSTM、Attention-LSTM、PSO-LSTM、GA-LSTM 等变体
7. **Method（方法）**
   - 字段：负荷预测、短期负荷预测(STLF)、超短期预测、特征选择、分解算法、优化算法
8. **Scenario（应用场景）**
   - 字段：智能电网、配电网、综合能源系统、工业园区、居民负荷

## 3. 关系边（Edge）
1. **Write（作者-论文）**
   - 作者 → 论文
2. **Affiliate（作者-机构）**
   - 作者 → 机构
3. **Cite（论文-参考文献）**
   - 论文 → 引用文献
4. **Co-author（作者-作者）**
   - 合作关系
5. **Co-occur（关键词-关键词）**
   - 共现关系
6. **Use（论文-模型/方法）**
   - 论文使用的模型与方法
7. **Publish（论文-期刊）**
   - 发表关系

## 4. 权重定义
- 合作权重：共同发文数
- 共现权重：关键词共现频次
- 引用权重：被引次数
- 模型关联权重：模型在论文中被使用次数

## 5. 与原选题匹配说明
- 研究对象：**LSTM 及其变体在电力负荷预测中的应用**
- 时间约束：2015–2025
- 主题约束：排除交通流、网络流量、服务器负载等非电力领域
- 分析目标：研究热点、主题演化、发展趋势
