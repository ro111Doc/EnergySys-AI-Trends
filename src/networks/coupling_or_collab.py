# -*- coding: utf-8 -*-
"""
coupling_or_collab.py
功能：基于screened_final.csv（67篇筛选后文献），实现【作者合作网络】+【文献耦合网络】分析
适配说明：针对中文字段（作者、文献来源、被引文献等）定制数据解析逻辑
修复：修正draw_networkx_edges参数名错误，兼容所有networkx版本
"""
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# -------------------------- 1. 基础配置与数据加载 --------------------------
# 中文字体设置（解决可视化乱码）
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 读取筛选后的数据（screened_final.csv）
df = pd.read_csv('screened_final.csv')
print(f"✅ 成功加载筛选后数据：{len(df)} 篇文献")
print(f"📊 数据字段：{df.columns.tolist()}")

# 数据预处理：处理缺失值，确保核心字段可用
df['作者'] = df['作者'].fillna('未知作者')
df['cited_paper'] = df['cited_paper'].fillna('')
df['题名'] = df['题名'].fillna('未知标题')

# -------------------------- 2. 核心工具函数（适配中文数据） --------------------------
def parse_chinese_authors(author_str):
    """
    解析中文作者字段（支持“张三,李四;王五”等分隔格式）
    返回清洗后的作者列表
    """
    if pd.isna(author_str) or author_str == '未知作者':
        return ['未知作者']
    
    # 处理多种分隔符（逗号、分号、空格）
    separators = [',', ';', '，', '；', ' ']
    for sep in separators:
        author_str = author_str.replace(sep, '|')
    
    # 分割并去重、去空
    authors = list(set([a.strip() for a in author_str.split('|') if a.strip()]))
    return authors if authors else ['未知作者']

def extract_cited_papers(cited_str):
    """
    解析被引文献字段（cited_paper），提取有效被引记录
    过滤过短记录，避免无效耦合
    """
    if pd.isna(cited_str) or cited_str.strip() == '':
        return []
    
    # 按分号分割被引文献（适配中文数据格式）
    cited_list = [c.strip() for c in cited_str.split(';') if c.strip()]
    # 过滤长度小于10的无效记录（如仅作者名，无年份/标题）
    valid_cited = [c for c in cited_list if len(c) >= 10]
    return valid_cited

# -------------------------- 3. 作者合作网络构建与分析 --------------------------
print("\n" + "="*50)
print("🔍 开始构建【作者合作网络】")
print("="*50)

# 1. 提取所有作者及合作关系
all_authors = []  # 存储所有作者
collab_edges = []  # 存储合作关系（边）

for idx, row in df.iterrows():
    # 解析当前文献的作者列表
    authors = parse_chinese_authors(row['作者'])
    all_authors.extend(authors)
    
    # 生成两两合作关系（仅保留2人及以上的文献）
    if len(authors) >= 2:
        for i in range(len(authors)):
            for j in range(i+1, len(authors)):
                # 按“作者A-作者B”排序，避免重复边（如A-B和B-A视为同一条边）
                edge = tuple(sorted([authors[i], authors[j]]))
                collab_edges.append(edge)

# 2. 统计高频作者（筛选发表≥2篇的核心作者，适配67篇文献的小规模数据）
author_count = Counter(all_authors)
core_authors = [author for author, count in author_count.items() if count >= 2]
print(f"📈 核心作者（发表≥2篇）：{len(core_authors)} 位")
for auth, cnt in [(a, author_count[a]) for a in core_authors]:
    print(f"  - {auth}: {cnt} 篇")

# 3. 构建合作网络（仅保留核心作者，避免网络过于稀疏）
G_collab = nx.Graph()
# 添加节点（核心作者）
G_collab.add_nodes_from(core_authors)
# 添加边（合作关系，仅保留核心作者之间的合作）
valid_edges = [edge for edge in collab_edges if edge[0] in core_authors and edge[1] in core_authors]
G_collab.add_edges_from(valid_edges)

# 4. 计算合作网络核心指标
collab_metrics = {
    "节点数（核心作者）": G_collab.number_of_nodes(),
    "边数（合作关系）": G_collab.number_of_edges(),
    "网络密度": round(nx.density(G_collab), 4),
    "平均度中心性": round(np.mean(list(dict(G_collab.degree()).values())), 2) if G_collab.number_of_nodes() > 0 else 0
}

print(f"\n📊 作者合作网络指标：")
for metric, value in collab_metrics.items():
    print(f"  - {metric}: {value}")

# -------------------------- 4. 文献耦合网络构建与分析 --------------------------
print("\n" + "="*50)
print("🔍 开始构建【文献耦合网络】")
print("="*50)

# 1. 提取每篇文献的被引记录（构建文献-被引文献映射）
doc_cited_map = {}  # key: 文献标识（题名+年份）, value: 被引文献列表
doc_ids = []        # 存储所有文献标识

for idx, row in df.iterrows():
    # 用“题名+年份”作为唯一文献标识（适配无UT字段的情况）
    doc_id = f"{row['题名'][:20]}...({row['年份']})" if pd.notna(row['年份']) else f"{row['题名'][:25]}..."
    doc_ids.append(doc_id)
    
    # 提取当前文献的有效被引记录
    cited_papers = extract_cited_papers(row['cited_paper'])
    doc_cited_map[doc_id] = cited_papers

print(f"📄 有效被引文献统计：")
cited_count = [len(v) for v in doc_cited_map.values() if len(v) > 0]
print(f"  - 有被引记录的文献：{len(cited_count)} 篇")
print(f"  - 平均每篇文献被引记录数：{round(np.mean(cited_count), 1)} 条" if cited_count else "  - 无有效被引记录")

# 2. 计算文献耦合关系（两篇文献共享被引文献≥1条即视为耦合）
coupling_edges = []  # 存储耦合关系（边），格式：(doc1, doc2, 共享被引数)

for i in range(len(doc_ids)):
    doc1 = doc_ids[i]
    cited1 = set(doc_cited_map[doc1])
    
    for j in range(i+1, len(doc_ids)):
        doc2 = doc_ids[j]
        cited2 = set(doc_cited_map[doc2])
        
        # 计算共享被引文献数量
        shared_cited = len(cited1 & cited2)
        if shared_cited >= 1:  # 适配小规模数据，降低耦合阈值
            coupling_edges.append((doc1, doc2, {'weight': shared_cited}))

# 3. 构建耦合网络
G_coupling = nx.Graph()
# 添加边（耦合关系）
G_coupling.add_edges_from(coupling_edges)
# 提取有耦合关系的文献节点
coupled_docs = list(G_coupling.nodes())

# 4. 计算耦合网络核心指标
coupling_metrics = {
    "节点数（有耦合关系的文献）": G_coupling.number_of_nodes(),
    "边数（耦合关系）": G_coupling.number_of_edges(),
    "网络密度": round(nx.density(G_coupling), 4),
    "平均共享被引数": round(np.mean([d['weight'] for u, v, d in G_coupling.edges(data=True)]), 1) if G_coupling.number_of_edges() > 0 else 0
}

print(f"\n📊 文献耦合网络指标：")
for metric, value in coupling_metrics.items():
    print(f"  - {metric}: {value}")

# -------------------------- 5. 双网络可视化（适配小规模数据） --------------------------
print("\n🎨 正在绘制双网络可视化图...")

# 创建2个子图（左右布局）
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

# -------------------------- 5.1 作者合作网络可视化 --------------------------
if G_collab.number_of_nodes() > 0:
    # 弹簧布局（k值调大，避免节点重叠）
    pos1 = nx.spring_layout(G_collab, k=3, iterations=100)
    
    # 绘制节点（大小与发表论文数正相关）
    node_sizes = [author_count[auth] * 300 for auth in G_collab.nodes()]  # 节点大小：发表数×300
    nx.draw_networkx_nodes(
        G_collab, pos1, ax=ax1, 
        node_size=node_sizes,
        node_color='#FF6B6B',  # 红色节点
        alpha=0.8,
        edgecolors='#333'  # 节点边框
    )
    
    # 绘制边（合作关系）【修复：color → edge_color】
    nx.draw_networkx_edges(
        G_collab, pos1, ax=ax1,
        width=1.2,
        edge_color='#888888',  # 修正参数名
        alpha=0.6
    )
    
    # 绘制节点标签（作者名）
    nx.draw_networkx_labels(
        G_collab, pos1, ax=ax1,
        font_size=9,
        font_weight='bold'
    )
    
    ax1.set_title(
        f'作者合作网络\n（{len(core_authors)}位核心作者 | 密度={collab_metrics["网络密度"]}）',
        fontsize=12, fontweight='bold', pad=20
    )
else:
    ax1.text(0.5, 0.5, '暂无足够合作关系数据\n（需2位及以上作者发表≥2篇文献）', 
             ha='center', va='center', fontsize=11, transform=ax1.transAxes)
    ax1.set_title('作者合作网络', fontsize=12, fontweight='bold')

ax1.axis('off')  # 隐藏坐标轴

# -------------------------- 5.2 文献耦合网络可视化 --------------------------
if G_coupling.number_of_nodes() > 0:
    # 弹簧布局（k值调大，适配文献标识较长的情况）
    pos2 = nx.spring_layout(G_coupling, k=4, iterations=100)
    
    # 绘制节点（大小固定，避免混乱）
    nx.draw_networkx_nodes(
        G_coupling, pos2, ax=ax2,
        node_size=500,
        node_color='#4ECDC4',  # 青色节点
        alpha=0.8,
        edgecolors='#333'
    )
    
    # 绘制边（耦合关系，线宽与共享被引数正相关）【修复：color → edge_color】
    edge_weights = [d['weight'] for u, v, d in G_coupling.edges(data=True)]
    nx.draw_networkx_edges(
        G_coupling, pos2, ax=ax2,
        width=[w*0.8 for w in edge_weights],  # 线宽：共享被引数×0.8
        edge_color='#555555',  # 修正参数名
        alpha=0.7
    )
    
    # 绘制边标签（共享被引数）
    edge_labels = {(u, v): d['weight'] for u, v, d in G_coupling.edges(data=True)}
    nx.draw_networkx_edge_labels(
        G_coupling, pos2, ax=ax2,
        edge_labels=edge_labels,
        font_size=8,
        font_color='#FF3333'
    )
    
    ax2.set_title(
        f'文献耦合网络\n（{len(coupled_docs)}篇耦合文献 | 平均共享被引数={coupling_metrics["平均共享被引数"]}）',
        fontsize=12, fontweight='bold', pad=20
    )
else:
    ax2.text(0.5, 0.5, '暂无足够耦合关系数据\n（需文献共享≥1条被引记录）', 
             ha='center', va='center', fontsize=11, transform=ax2.transAxes)
    ax2.set_title('文献耦合网络', fontsize=12, fontweight='bold')

ax2.axis('off')  # 隐藏坐标轴

# 调整子图间距，保存图片
plt.tight_layout()
plt.savefig('collab_coupling_network_screened.png', dpi=300, bbox_inches='tight')
plt.close()

# -------------------------- 6. 结果保存（量化指标表格） --------------------------
print("\n💾 正在保存分析结果...")

# 6.1 作者合作网络指标表
if core_authors:
    # 计算每位核心作者的度中心性（合作广度）
    author_degree = dict(G_collab.degree())
    collab_result = pd.DataFrame({
        '作者': core_authors,
        '发表文献数': [author_count[auth] for auth in core_authors],
        '合作作者数（度中心性）': [author_degree.get(auth, 0) for auth in core_authors]
    }).sort_values('发表文献数', ascending=False)
    
    collab_result.to_csv('作者合作网络指标_screened.csv', index=False, encoding='utf-8-sig')
    print(f"  ✅ 作者合作指标表已保存：作者合作网络指标_screened.csv")

# 6.2 文献耦合网络指标表
if coupling_edges:
    # 提取耦合关系详情
    coupling_result = pd.DataFrame({
        '文献1': [edge[0] for edge in coupling_edges],
        '文献2': [edge[1] for edge in coupling_edges],
        '共享被引文献数': [edge[2]['weight'] for edge in coupling_edges]
    }).sort_values('共享被引文献数', ascending=False)
    
    coupling_result.to_csv('文献耦合网络指标_screened.csv', index=False, encoding='utf-8-sig')
    print(f"  ✅ 文献耦合指标表已保存：文献耦合网络指标_screened.csv")

# 6.3 网络整体指标汇总
overall_metrics = pd.DataFrame({
    '指标类别': ['作者合作网络', '作者合作网络', '作者合作网络', '作者合作网络',
               '文献耦合网络', '文献耦合网络', '文献耦合网络', '文献耦合网络'],
    '指标名称': ['核心作者数', '合作关系数', '网络密度', '平均度中心性',
               '耦合文献数', '耦合关系数', '网络密度', '平均共享被引数'],
    '指标值': [collab_metrics['节点数（核心作者）'], collab_metrics['边数（合作关系）'],
             collab_metrics['网络密度'], collab_metrics['平均度中心性'],
             coupling_metrics['节点数（有耦合关系的文献）'], coupling_metrics['边数（耦合关系）'],
             coupling_metrics['网络密度'], coupling_metrics['平均共享被引数']]
})

overall_metrics.to_csv('双网络整体指标汇总_screened.csv', index=False, encoding='utf-8-sig')
print(f"  ✅ 整体指标汇总表已保存：双网络整体指标汇总_screened.csv")

print("\n🎉 所有分析完成！")
print("📁 输出文件清单：")
print("  1. collab_coupling_network_screened.png → 双网络可视化图")
print("  2. 作者合作网络指标_screened.csv → 核心作者量化指标")
print("  3. 文献耦合网络指标_screened.csv → 文献耦合详情")
print("  4. 双网络整体指标汇总_screened.csv → 整体统计指标")