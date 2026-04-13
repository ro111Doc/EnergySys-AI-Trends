# 基于 LSTM 的电力负荷预测研究热点与发展趋势 —— 文献计量分析（2015-2025）
## 项目说明
本项目聚焦于深度学习模型 LSTM（Long Short-Term Memory）在电力负荷预测领域的研究热点与发展趋势，基于文献计量分析方法，对 2015–2025 年间相关学术成果进行系统梳理与定量分析。  
在研究背景上，LSTM 作为时间序列建模中的经典模型，在电力负荷预测任务中被广泛应用，尤其在短期负荷预测与多变量建模场景中表现突出。随着深度学习方法的不断发展，基于 LSTM 的改进模型（如 Bi-LSTM、Attention-LSTM 等）逐渐成为研究热点，使该领域具备丰富且连续的文献积累，为开展计量分析提供了良好的数据基础。
在方法上，本项目采用“检索—筛选—数据提取—分析”的标准流程，从 Web of Science、Scopus、IEEE Xplore 等主流学术数据库中获取文献数据。通过构建同义词表与检索式进行系统检索，并结合标题摘要初筛与全文复筛的双阶段筛选机制，对文献进行规范化筛选。同时引入基于规则的代码辅助筛选与多标签排除原因记录（reason code），以提高筛选过程的一致性与可复现性。  
在分析内容上，项目围绕以下几个方面展开：一是发文趋势分析，刻画该领域的时间演化特征；二是作者、机构及合作网络分析，识别核心研究群体；三是关键词共现与演化分析，挖掘研究热点与前沿方向；四是方法层面的发展路径分析，重点关注 LSTM 及其改进模型在不同应用场景中的演进过程，包括短期负荷预测、多变量建模等典型任务。  
通过上述分析，本项目旨在系统呈现基于 LSTM 的电力负荷预测研究的发展脉络，识别当前研究热点与潜在发展方向，为相关领域的学术研究与工程实践提供结构化、可参考的分析结果。

## 检索式
TS=(LSTM OR "long short-term memory" OR "long short term memory" OR BiLSTM OR "bidirectional LSTM" OR "attention LSTM")
AND TS=("electric load forecasting" OR "power load forecasting" OR "load forecasting" OR "load prediction" OR "electricity demand forecasting" OR "short-term load forecasting" OR STLF)
AND TS=("power system" OR "power systems" OR "smart grid" OR "power grid" OR "distribution network")
AND PY=(2015-2025)
NOT TS=("traffic flow forecasting" OR "network traffic forecasting" OR "server workload prediction" OR "CPU load prediction" OR "bridge load prediction")

## 项目进度
本项目已完成从文献数据获取、多轮筛选、网络分析到查新报告支撑的完整流程。以下是重点输出：  
1. 数据检索与筛选  
采集并合并原始文献数据，生成 merged_with_citations.csv（筛选前全量数据）。  
初筛：生成 screened_stage1.csv，新增 stage1_status/stage1_reason 字段标记筛选结果。  
复筛：生成 screened_final.csv，新增 stage2_status/stage2_reason 字段。  
编写数据对比分析脚本，生成 literature_screening_comparison.csv，量化展示筛选前后数据规模、结构、质量的变化，支撑 novelty_search_v0.md 查新报告的「对比表」章节。  
2. 图数据建模与数据质量评估，指标规范与清洗消歧规则  
交付图数据模型文档data_model.md、数据质量报告data_quality.md、全局参数配置文档params.md。完成图数据模型的设计与文档化，明确项目数据结构；完成原始数据质量评估，输出量化质量报告与改进建议。  
交付指标规范文档metrics_spec.md、清洗/消歧规则文档cleaning_rules.md，参数配置文档params.md补充清洗阈值、消歧优先级等配置项。完成核心计量指标的规范定义，为后续网络分析提供计算标准；完成清洗 / 消歧规则的编写，支持作者与机构层面的数据标准化。  
3. 共被引网络建模  
编写共被引网络脚本src/networks/co_citation.py，实现共被引矩阵构建函数、支持矩阵乘法计算共被引强度、可输出共被引网络与基础中心性指标。  
参数配置文档params.md补充共被引网络构建的核心参数，保持与前序课程参数文件的兼容性。  
4. 文献耦合与合作网络实现   
编写 src/networks/coupling_or_collab.py，基于 screened_final.csv 实现文献耦合网络（Bibliographic Coupling）。  
引用矩阵构建：使用 pivot_table 将长格式引用数据转换为「施引文献 × 被引文献」的二元矩阵。  
耦合强度计算：通过矩阵乘法 A @ A.T 得到耦合矩阵，元素值代表两篇文献共同引用的参考文献数量。  
网络生成：将耦合矩阵转换为 networkx 图结构，映射回原始文献 ID。  
中心性计算：实现  度中心性（Degree Centrality） 计算，输出 Top 5 中心性最高的文献，反映其在耦合网络中的连接广度。  

## 成员及其分工
组长：刘泽熙
组员：郭逸清，龚乐瑶，兰宏智

分工：
1. 兰宏智：检索策略与数据整合
负责文献检索方案设计与数据获取，是检索阶段的主要执行者。与龚乐瑶共同讨论并确定同义词表、限定条件及排除条件，在此基础上独立完成V0检索式与query.yaml配置文件的编写。阶段二中负责在数据库中执行实际检索，导出 txt 格式文献数据，形成field_dictionary.md，同时记录processed信息。在检索过程中根据实际效果对检索策略进行优化，并协助更新query_changelog.md。此外，负责撰写数据说明README.md（与项目说明文档区分），确保数据来源与结构清晰可复现。

2. 龚乐瑶：检索设计文档与数据质量控制
负责检索策略的文档化与数据质量分析工作。与兰宏智共同制定同义词表与检索规则后，撰写query_rationale.md，对检索式设计思路进行系统说明，并完成query_changelog.md的初版记录。阶段二中参与数据整合过程，并基于整理后的数据撰写data_quality.md，对缺失率、重复率及数据一致性进行分析与评估，保障数据质量。同时在检索过程中持续维护检索变更日志，确保策略调整具有可追溯性。

3. 郭逸清：筛选规则设计与扩展任务
负责文献筛选方法的设计与部分前期扩展工作。与刘泽熙共同讨论并制定筛选策略，包括纳入标准、排除标准及筛选流程，并独立撰写screening_rule.md，明确筛选逻辑与执行规范。针对兰宏智导出的 txt 数据，针对性搜索并提供适配的格式转换代码模板，并负责初步的文献检索内容格式转换与整合工作，保障后续数据处理可用。阶段二中利用空档时间完成《方向与开源项目候选表》的整理，并提交相关环境配置截图，为项目后续拓展提供参考。在阶段三中参与文献实际筛选工作，并基于筛选结果参与novelty_search_v0.md的撰写，重点负责研究内容梳理与信息整理。

4. 刘泽熙：流程设计与项目工程支持
负责筛选流程可视化设计与项目工程化支持工作。与郭逸清共同制定筛选流程后，绘制PRISMA流程草图，明确文献筛选各阶段的结构与数量关系。基于郭逸清提供的代码模板，将兰宏智导出的 txt 文献数据转换为可直接被筛选代码读取的标准化文档，并负责初步的文献检索内容格式转换与整合，保证筛选环节数据可用。阶段二中完成项目说明README.md（区别于数据说明文档）以及Requirements.txt的编写，确保项目环境配置清晰可复现。在阶段三中参与文献筛选与结果整理，协助完成novelty_search_v0.md，重点支持流程结构整理与结果呈现。

总体说明：  
本项目采用分阶段、小组协作的方式推进。兰宏智、龚乐瑶组侧重于检索与数据处理，郭逸清、刘泽熙组侧重于筛选与分析设计。在阶段划分上，各组任务相对独立且可并行推进，同时在关键节点进行协同配合。通过合理分工与过程记录，保证项目在方法规范性、数据质量与结果可复现性方面达到课程要求。

## 核心目标
基于 Web of Science、Scopus、IEEE Xplore 等数据库中与电力负荷预测相关的文献数据，围绕 LSTM（Long Short-Term Memory）及其在能源领域的应用，开展系统性的文献计量分析，回答以下核心问题：
2015–2025 年间，基于 LSTM 的电力负荷预测研究的发文趋势及其阶段性发展特征；
该领域的核心研究机构、高产出作者及其合作关系网络；
关键词共现与演化分析，识别研究热点（如短期负荷预测、多变量建模、Attention-LSTM 等）及其变化趋势；
代表性高被引文献与关键研究成果，梳理技术发展路径与方法演进过程（如从传统 LSTM 到改进模型）；
当前研究中存在的主要问题与不足，并基于证据链分析总结未来可能的发展方向。

## 项目结构
项目采用模块化结构设计，将数据、代码与文档分离，提升可维护性与可复现性：  
data/：存放原始数据及筛选结果（CSV）  
src/：存放筛选与数据处理脚本（如 stage1、stage2）  
reports/：存放方法文档与分析报告  
outputs/：存放图像结果（如 PRISMA 流程图）  
config/：配置文件（如 query.yaml）  
README.md：项目整体说明  
