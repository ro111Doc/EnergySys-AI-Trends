import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

INPUT_PATH = DATA_DIR / "screened_stage1.csv"
OUTPUT_PATH = DATA_DIR / "screened_final.csv"


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

        return pd.concat([df_with_doi, df_without_doi], ignore_index=True)

    if title_col:
        df[title_col] = df[title_col].astype(str).str.strip()
        return df.drop_duplicates(subset=[title_col], keep="first")

    return df.drop_duplicates()


def stage2_screen(row, fulltext_col, language_col):
    reasons = []

    status = normalize_text(row.get("stage1_status", "")).lower()
    if status == "exclude":
        return "exclude", normalize_text(row.get("stage1_reason", ""))

    fulltext = normalize_text(row.get(fulltext_col, "")) if fulltext_col else ""
    language = normalize_text(row.get(language_col, "")) if language_col else ""
    fulltext_lower = fulltext.lower()
    language_lower = language.lower()

    if language_col:
        allowed = {"english", "chinese", "英文", "中文", "en", "zh"}
        if language_lower and language_lower not in allowed:
            reasons.append("E5 - 语言不符 / Language mismatch")

    if fulltext.strip() == "":
        reasons.append("E2 - 无全文 / No full text")

    if fulltext.strip() != "":
        method_hits = ["lstm", "long short-term memory", "gru", "rnn", "transformer"]
        if not any(k in fulltext_lower for k in method_hits):
            reasons.append("E3 - 方法不符 / Method mismatch")

        quality_hits = ["experiment", "result", "validation", "实验", "结果", "验证"]
        if not any(k in fulltext_lower for k in quality_hits):
            reasons.append("E6 - 质量不符 / Low quality")

    reasons = sorted(set(reasons))

    if reasons:
        return "exclude", "; ".join(reasons)

    return "include", ""


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"找不到文件: {INPUT_PATH}，请先运行 stage1_screen.py")

    df = read_csv_auto(INPUT_PATH)
    print(f"Stage2输入记录数: {len(df)}")

    df = deduplicate_records(df)
    print(f"Stage2去重后记录数: {len(df)}")

    fulltext_col = pick_column(df, ["fulltext", "全文", "FullText", "正文"])
    language_col = pick_column(df, ["language", "Language", "语言"])

    print("识别到的列名：")
    print("fulltext_col =", fulltext_col)
    print("language_col =", language_col)

    df[["stage2_status", "stage2_reason"]] = df.apply(
        lambda row: pd.Series(stage2_screen(row, fulltext_col, language_col)),
        axis=1
    )

    df = deduplicate_records(df)
    print(f"Stage2输出前去重后记录数: {len(df)}")

    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"Stage2完成，输出文件：{OUTPUT_PATH}")


if __name__ == "__main__":
    main()