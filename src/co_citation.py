import pandas as pd
import numpy as np
from pathlib import Path


# =========================
# 1. 读取你的 merged_with_citations.csv
# =========================
def load_edges_from_merged(csv_path):
    # 自动尝试几种常见编码
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
        raise ValueError("CSV 读取失败，请检查文件编码。")

    required_cols = ["citing_paper", "cited_paper"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"缺少必要列: {missing}")

    edges = df[["citing_paper", "cited_paper"]].copy()
    edges = edges.dropna()

    edges["citing_paper"] = edges["citing_paper"].astype(str).str.strip()
    edges["cited_paper"] = edges["cited_paper"].astype(str).str.strip()

    edges = edges[
        (edges["citing_paper"] != "") &
        (edges["cited_paper"] != "")
    ]

    edges = edges.drop_duplicates()

    print(f"引用关系数: {len(edges)}")
    return edges


# =========================
# 2. 构建引用矩阵 R
# =========================
def build_citation_matrix(edges):
    r = (
        edges.assign(value=1)
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
    c = r.T @ r
    c = pd.DataFrame(c, index=r.columns, columns=r.columns)
    np.fill_diagonal(c.values, 0)
    return c


# =========================
# 4. cosine 相似度
# =========================
def cosine_similarity(matrix):
    x = matrix.to_numpy(dtype=float)
    norms = np.linalg.norm(x, axis=1, keepdims=True)
    norms[norms == 0] = 1.0

    sim = (x @ x.T) / (norms @ norms.T)
    sim = np.nan_to_num(sim, nan=0.0, posinf=0.0, neginf=0.0)

    sim_df = pd.DataFrame(sim, index=matrix.index, columns=matrix.index)
    np.fill_diagonal(sim_df.values, 0)
    return sim_df


# =========================
# 5. Top-N 过滤
# =========================
def top_n_filter(sim_matrix, n=10):
    arr = sim_matrix.to_numpy(dtype=float)
    filtered = np.zeros_like(arr)

    for i in range(arr.shape[0]):
        row = arr[i].copy()
        row[i] = -np.inf

        n_keep = min(n, arr.shape[0] - 1)
        if n_keep <= 0:
            continue

        idx = np.argpartition(row, -n_keep)[-n_keep:]
        filtered[i, idx] = arr[i, idx]

    filtered = np.maximum(filtered, filtered.T)

    result = pd.DataFrame(
        filtered,
        index=sim_matrix.index,
        columns=sim_matrix.columns
    )
    np.fill_diagonal(result.values, 0)
    return result


# =========================
# 6. 矩阵转边表
# =========================
def matrix_to_edges(matrix):
    nodes = list(matrix.index)
    arr = matrix.to_numpy(dtype=float)

    rows = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if arr[i, j] > 0:
                rows.append([nodes[i], nodes[j], arr[i, j]])

    return pd.DataFrame(rows, columns=["source", "target", "weight"])


# =========================
# 7. 主流程
# =========================
def run(csv_path, output_dir):
    print("读取数据...")
    edges = load_edges_from_merged(csv_path)

    print("构建引用矩阵 R...")
    r = build_citation_matrix(edges)
    print("R shape:", r.shape)

    print("构建共被引矩阵 C...")
    c = build_co_citation_matrix(r)
    print("C shape:", c.shape)

    print("计算 cosine 相似度...")
    sim = cosine_similarity(c)

    print("进行 Top-N 过滤...")
    filtered = top_n_filter(sim, n=10)

    print("生成网络边表...")
    edge_list = matrix_to_edges(filtered)
    print("边数:", len(edge_list))

    output_dir.mkdir(parents=True, exist_ok=True)

    r.to_csv(output_dir / "R_matrix.csv", encoding="utf-8-sig")
    c.to_csv(output_dir / "C_matrix.csv", encoding="utf-8-sig")
    sim.to_csv(output_dir / "similarity_matrix.csv", encoding="utf-8-sig")
    filtered.to_csv(output_dir / "filtered_matrix.csv", encoding="utf-8-sig")
    edge_list.to_csv(output_dir / "network_edges.csv", index=False, encoding="utf-8-sig")

    print("完成！")
    print("输出目录：", output_dir)


# =========================
# 8. 自动定位路径运行
# =========================
if __name__ == "__main__":
    current_file = Path(__file__).resolve()

    # 当前文件: bibliometric_analysis/src/networks/co_citation.py
    # 项目根目录: bibliometric_analysis
    project_root = current_file.parents[2]

    csv_path = project_root / "data" / "merged_with_citations.csv"
    output_dir = project_root / "data" / "co_citation_outputs"

    print("当前脚本路径：", current_file)
    print("项目根目录：", project_root)
    print("CSV路径：", csv_path)
    print("CSV是否存在：", csv_path.exists())

    if not csv_path.exists():
        raise FileNotFoundError(
            f"找不到文件: {csv_path}\n"
            f"请确认 merged_with_citations.csv 是否放在 bibliometric_analysis/data/ 下"
        )

    run(csv_path, output_dir)