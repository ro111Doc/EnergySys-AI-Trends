import pandas as pd
import numpy as np
from pathlib import Path

# =========================
# 1. 从 WOS 格式提取引用关系
# =========================
def load_edges_from_wos(csv_path):
    # 自动尝试编码
    encodings = ["utf-8-sig", "utf-8", "gbk", "latin1"]
    df = None
    for enc in encodings:
        try:
            df = pd.read_csv(csv_path, encoding=enc)
            print(f"读取成功，编码: {enc}")
            break
        except Exception:
            continue

    if df is None:
        raise ValueError("CSV 读取失败。")

    # 识别 WOS 列名: TI (Title), CR (Cited References)
    ti_col = 'TI' if 'TI' in df.columns else ('title' if 'title' in df.columns else df.columns[0])
    cr_col = 'CR' if 'CR' in df.columns else ('cited_references' if 'cited_references' in df.columns else None)
    
    if not cr_col:
        print("警告：未找到 CR 列，请确认文件包含参考文献信息")
        return pd.DataFrame(columns=["citing_paper", "cited_paper"])

    rows = []
    for _, row in df.iterrows():
        citing = str(row[ti_col]).strip()
        # WOS 的参考文献通常以分号隔开
        raw_cr = str(row[cr_col])
        if raw_cr == "nan" or not raw_cr:
            continue
            
        cited_list = raw_cr.split(';')
        for cited in cited_list:
            cited = cited.strip()
            if cited:
                rows.append([citing, cited])

    edges = pd.DataFrame(rows, columns=["citing_paper", "cited_paper"])
    edges = edges.drop_duplicates()
    print(f"提取到原始引用关系数: {len(edges)}")
    return edges


# =========================
# 2. 构建引用矩阵 R (过滤高频被引文献以防内存溢出)
# =========================
def build_citation_matrix(edges, top_k=800):
    if edges.empty:
        return pd.DataFrame()
        
    # 为了保证计算效率，只选取被引频次最高的前 K 个文献
    top_cited = edges['cited_paper'].value_counts().head(top_k).index
    edges_filtered = edges[edges['cited_paper'].isin(top_cited)]
    
    r = (
        edges_filtered.assign(value=1)
        .pivot_table(
            index="citing_paper",
            columns="cited_paper",
            values="value",
            aggfunc="max",
            fill_value=0
        )
        .astype(int)
    )
    return r


# =========================
# 3. 构建共被引矩阵 C
# =========================
def build_co_citation_matrix(r):
    # C = R^T * R
    r_arr = r.to_numpy()
    c_arr = r_arr.T @ r_arr
    c = pd.DataFrame(c_arr, index=r.columns, columns=r.columns)
    np.fill_diagonal(c.values, 0)
    return c


# =========================
# 4. 计算 Cosine 相似度
# =========================
def calculate_cosine(matrix):
    x = matrix.to_numpy(dtype=float)
    norms = np.linalg.norm(x, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    sim = (x @ x.T) / (norms @ norms.T)
    sim = np.nan_to_num(sim, nan=0.0)
    sim_df = pd.DataFrame(sim, index=matrix.index, columns=matrix.index)
    np.fill_diagonal(sim_df.values, 0)
    return sim_df


# =========================
# 5. 生成网络边表 (Top-N 过滤)
# =========================
def generate_edge_list(sim_matrix, n=10):
    nodes = list(sim_matrix.index)
    arr = sim_matrix.to_numpy()
    rows = []
    
    for i in range(len(nodes)):
        row_vals = arr[i]
        n_keep = min(n, len(row_vals) - 1)
        if n_keep <= 0: continue
        
        # 获取最相似的索引
        top_indices = np.argpartition(row_vals, -n_keep)[-n_keep:]
        for j in top_indices:
            if arr[i, j] > 0:
                # 排序以去重单向边
                pair = sorted([nodes[i], nodes[j]])
                rows.append([pair[0], pair[1], arr[i, j]])
    
    return pd.DataFrame(rows, columns=["source", "target", "weight"]).drop_duplicates()


# =========================
# 主流程
# =========================
def run(csv_path, output_dir):
    print(f"正在分析文件: {csv_path.name}")
    edges = load_edges_from_wos(csv_path)
    
    if edges.empty:
        print("无有效数据，程序终止。")
        return

    print("构建引用矩阵...")
    r = build_citation_matrix(edges)
    
    print("构建共被引矩阵...")
    c = build_co_citation_matrix(r)
    
    print("计算相似度...")
    sim = calculate_cosine(c)
    
    print("生成边表...")
    edge_list = generate_edge_list(sim, n=10)
    
    # 自动创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存结果
    r.to_csv(output_dir / "citation_matrix_R.csv", encoding="utf-8-sig")
    c.to_csv(output_dir / "cocitation_matrix_C.csv", encoding="utf-8-sig")
    edge_list.to_csv(output_dir / "cocitation_network_edges.csv", index=False, encoding="utf-8-sig")
    
    print("-" * 30)
    print(f"分析完成！共提取 {len(edge_list)} 条共被引关系。")
    print(f"输出目录: {output_dir}")


if __name__ == "__main__":
    # 路径自动处理
    current_path = Path(__file__).resolve()
    # 假设你的项目结构是 bibliometric_analysis/src/...
    project_root = current_path.parents[2] 
    
    # 输入文件指向你新提供的文件
    input_csv = project_root / "data" / "included_final.csv"
    output_path = project_root / "data" / "co_citation_results"

    if input_csv.exists():
        run(input_csv, output_path)
    else:
        print(f"错误: 找不到文件 {input_csv}")
