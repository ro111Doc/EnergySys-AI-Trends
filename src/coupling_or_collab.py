# -*- coding: utf-8 -*-
"""
文献耦合与合作网络 - Lesson 8 作业
功能：从 screened_final.csv 构建文献耦合网络（Bibliographic Coupling）
满足最小验收要求：实现一类网络 + 可运行 + 输出结果
"""
import pandas as pd
import numpy as np
import networkx as nx

def build_coupling_network(input_csv="screened_final.csv"):
    """
    构建文献耦合网络 Bibliographic Coupling
    原理：两篇文献若引用相同参考文献 → 形成耦合关系
    耦合强度 = 共同引用的参考文献数量
    """
    # 1. 读取数据
    df = pd.read_csv(input_csv, encoding="utf-8")

    # 2. 构建引用矩阵（文献 × 参考文献）
    # citing_paper = 施引文献
    # cited_paper = 被引文献（参考文献）
    citation_matrix = df.pivot_table(
        index="citing_paper",
        columns="cited_paper",
        aggfunc="size",
        fill_value=0
    )

    # 3. 计算文献耦合矩阵 B = A @ A.T
    coupling_matrix = np.dot(citation_matrix.values, citation_matrix.values.T)
    np.fill_diagonal(coupling_matrix, 0)  # 对角线置0（不与自身耦合）

    # 4. 构建网络
    G = nx.from_numpy_array(
        coupling_matrix,
        create_using=nx.Graph()
    )

    # 5. 映射回文献ID（方便查看）
    paper_ids = citation_matrix.index.tolist()
    id_map = {i: paper_ids[i] for i in range(len(paper_ids))}
    G = nx.relabel_nodes(G, id_map)

    # 6. 计算度中心性（最简单的中心性指标）
    centrality = nx.degree_centrality(G)

    return G, coupling_matrix, centrality

def print_top_central_papers(centrality, top_n=5):
    """输出中心性最高的文献"""
    print("=" * 60)
    print(f"📊 文献耦合网络 - 度中心性 Top {top_n}")
    print("=" * 60)
    sorted_central = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    for i, (paper_id, score) in enumerate(sorted_central[:top_n], 1):
        print(f"{i:2d}. {paper_id[:50]:<50} | 中心性 = {score:.4f}")

# ====================== 直接运行 ======================
if __name__ == "__main__":
    G, coupling_matrix, centrality = build_coupling_network()
    print_top_central_papers(centrality)

    print("\n✅ 文献耦合网络构建完成！")
    print(f"📌 网络节点数（施引文献）: {G.number_of_nodes()}")
    print(f"🔗 网络边数（耦合关系）: {G.number_of_edges()}")