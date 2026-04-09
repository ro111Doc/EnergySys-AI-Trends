import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

INPUT_PATH = DATA_DIR / "merged_with_citations.csv"
OUTPUT_PATH = DATA_DIR / "screened_stage1.csv"


lstm_keywords = [
    "lstm", "long short-term memory", "bi-lstm", "attention", "gru", "rnn"
]
dl_keywords = [
    "deep learning", "neural network", "cnn", "transformer"
]

task_keywords = [
    "load forecasting", "load prediction", "electric load",
    "short-term load forecasting", "power load forecasting",
    "负荷预测", "电力负荷", "短期负荷预测"
]
domain_keywords = [
    "power system", "electric", "smart grid", "microgrid",
    "电力系统", "电网", "配电网", "微电网"
]

exclude_keywords = [
    "stock", "price forecasting", "traffic", "股票", "交通"
]


def read_csv_auto(csv_path: Path) -> pd.DataFrame:
    encodings = ["utf-8-sig", "utf-8", "gbk", "latin1"]
    last_error = None
    for enc in encodings:
        try:
            df = pd.read_csv(csv_path, encoding=enc)
            print(f"读取成功: {csv_path.name} | 编码: {enc}")
            return df
        except Exception as e:
            last_error = e
    raise ValueError(f"CSV读取失败: {csv_path}\n最后错误: {last_error}")


def pick_column(df: pd.DataFrame, candidates, default=None):
    for c in candidates:
        if c in df.columns:
            return c
    return default


def normalize_text(x):
    if pd.isna(x):
        return ""
    return str(x).strip()


def deduplicate_records(df: pd.DataFrame) -> pd.DataFrame:
    """
    专门针对 merged_with_citations.csv：
    优先按 DOI 去重；没有 DOI 时按题名去重。
    """
    df = df.copy()

    doi_col = pick_column(df, ["DOI", "doi"])
    title_col = pick_column(df, ["题名", "title", "Title", "标题"])

    if doi_col:
        df[doi_col] = df[doi_col].astype(str).str.strip().str.lower()
        has_doi = df[doi_col].notna() & (df[doi_col] != "") & (df[doi_col] != "nan")

        df_with_doi = df[has_doi].drop_duplicates(subset=[doi_col], keep="first")
        df_without_doi = df[~has_doi]

        if title_col:
            df[title_col] = df[title_col].astype(str).str.strip()
            df_without_doi = df_without_doi.drop_duplicates(subset=[title_col], keep="first")

        result = pd.concat([df_with_doi, df_without_doi], ignore_index=True)
        return result

    if title_col:
        df[title_col] = df[title_col].astype(str).str.strip()
        return df.drop_duplicates(subset=[title_col], keep="first")

    return df.drop_duplicates()


def stage1_screen(row, title_col, abstract_col, year_col):
    title = normalize_text(row.get(title_col, "")) if title_col else ""
    abstract = normalize_text(row.get(abstract_col, "")) if abstract_col else ""
    text = f"{title} {abstract}".lower()

    reasons = []

    year = None
    if year_col:
        try:
            year = pd.to_numeric(row.get(year_col), errors="coerce")
        except Exception:
            year = None

    if pd.isna(year):
        reasons.append("E4 - 时间缺失 / Year missing")
    else:
        year = int(year)
        if year < 2015 or year > 2025:
            reasons.append("E4 - 时间不符 / Out of range")

    if not any(k in text for k in task_keywords):
        reasons.append("E1 - 非本主题 / Not relevant")

    if not any(k in text for k in domain_keywords):
        reasons.append("E1 - 非本主题 / Not relevant")

    if not (any(k in text for k in lstm_keywords) or any(k in text for k in dl_keywords)):
        reasons.append("E3 - 方法不符 / Method mismatch")

    if any(k in text for k in exclude_keywords):
        reasons.append("E1 - 非本主题 / Not relevant")

    reasons = sorted(set(reasons))

    if len(reasons) == 0:
        return "include", ""

    if ("E1 - 非本主题 / Not relevant" not in reasons) and ("E3 - 方法不符 / Method mismatch" not in reasons):
        return "uncertain", "; ".join(reasons)

    return "exclude", "; ".join(reasons)


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"找不到文件: {INPUT_PATH}")

    df = read_csv_auto(INPUT_PATH)

    print(f"原始记录数: {len(df)}")
    df = deduplicate_records(df)
    print(f"去重后记录数: {len(df)}")

    title_col = pick_column(df, ["title", "Title", "题名", "标题"])
    abstract_col = pick_column(df, ["abstract", "Abstract", "摘要", "Summary"])
    year_col = pick_column(df, ["year", "Year", "年份"])

    if year_col is None:
        pub_col = pick_column(df, ["发表时间", "publication_date", "date"])
        if pub_col:
            df["年份_自动提取"] = (
                df[pub_col].astype(str).str.extract(r"(\d{4})", expand=False)
            )
            year_col = "年份_自动提取"

    print("识别到的列名：")
    print("title_col =", title_col)
    print("abstract_col =", abstract_col)
    print("year_col =", year_col)

    if title_col is None and abstract_col is None:
        raise ValueError("找不到标题或摘要列，至少要有一个。")

    df[["stage1_status", "stage1_reason"]] = df.apply(
        lambda row: pd.Series(stage1_screen(row, title_col, abstract_col, year_col)),
        axis=1
    )

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"Stage1完成，输出文件：{OUTPUT_PATH}")


if __name__ == "__main__":
    main()
