# Params.md (Baseline & Technical Stack)

## 一、项目基础信息
* **项目名称（中）**：基于 LSTM 的电力负荷预测研究热点与发展趋势——文献计量分析（2015–2025）
* **项目名称（英）**：Research hotspots and development trends of LSTM in electric load forecasting: a bibliometric analysis (2015–2025)
* **研究范式**：项目制、可复现研究流程
* **时间范围**：2015 – 2025

---

## 二、工具路线对照表 (Tool Selection Matrix)
[cite_start]本组根据“工具-任务匹配”原则，构建了以下四层工具栈 [cite: 8, 16]：

| 工具名 | 所在层级 | 要解决的问题 | 预期输出 | 风险点及应对 | 方案状态 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CiteSpace (v6.x)** | GUI层 | [cite_start]共被引聚类、突现检测、关键节点识别 [cite: 10] | 聚类图谱、Burst列表 | [cite_start]参数记录依赖人工；通过本文件落盘 [cite: 11] | **主方案** |
| **VOSviewer** | GUI层 | [cite_start]合作网络可视化、密度分布、主题演化 [cite: 11] | 合作图谱、Overlay图 | [cite_start]图美观但解释性需人工加强 [cite: 11] | **备选方案** |
| **PyAlex / pandas** | 数据/开源层 | [cite_start]自动取数、字段映射、数据清洗与去重 [cite: 12] | 清洗后的数据集 | [cite_start]API速率限制；建立缓存机制 [cite: 12] | **主方案** |
| **GPT Researcher** | Agent层 | [cite_start]领域术语扩展、背景调研、证据表初稿 [cite: 14] | 术语列表、综述大纲 | [cite_start]存在幻觉风险；必须人工核查证据 [cite: 15] | **备选方案** |

---

## 三、核心执行参数 (Core Execution Parameters)

### 3.1 检索与数据参数
* **数据源**：中国知网 (CNKI)、Web of Science (WoS)
* **检索逻辑**：`方法词 AND 任务词 AND 场景词 NOT 排除词`
* **字段字典**：记录在 `field_dictionary.md` 中，重点治理 `CR` (Cited References) 字段

### 3.2 CiteSpace 分析参数 (Baseline)
* [cite_start]**分析单元 (Node Type)**：Cited Reference (CR), Keyword (ID/DE) [cite: 10, 243]
* [cite_start]**时间切片 (Time Slicing)**：1 Year/Slice [cite: 226]
* **阈值过滤 (Top-K)**：保留被引频次前 800 的文献进入运算
* [cite_start]**剪裁算法 (Pruning)**：Pathfinder / Pruning sliced networks [cite: 234]

### 3.3 网络拓扑参数
* **相似度算法**：余弦相似度 (Cosine Similarity)
* **切边策略**：Top-10 邻居过滤（仅保留最相似的前 10 个邻居）

---

## 四、职责边界与风险控制
1.  [cite_start]**自动化底线**：GUI 工具（CiteSpace/VOSviewer）仅用于建立参数直觉和产出 baseline 图谱，不承担批量重跑任务 [cite: 11]。
2.  [cite_start]**人工核查**：所有 Agent 生成的术语扩展和文献推荐，必须经过人工复核并回到原始数据验证 [cite: 15]。
3.  [cite_start]**版本管理**：任何参数改动必须同步更新至本 `Params.md`，确保后续 Lessons 10-16 的脚本复现具有一致性 。

---
**提交位置**：`baseline/params.md`
[cite_start]**用途**：作为项目架构前置文件，支撑后续实操与开源二开 。